import hashlib
import operator
import os
import pathlib
import struct
import typing as tp

from pyvcs.objects import hash_object


class GitIndexEntry(tp.NamedTuple):
    # @see: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    ctime_s: int
    ctime_n: int
    mtime_s: int
    mtime_n: int
    dev: int
    ino: int
    mode: int
    uid: int
    gid: int
    size: int
    sha1: bytes
    flags: int
    name: str

    def pack(self) -> bytes:
        s = str.encode(self.name, "utf-8")
        return struct.pack(
            f">10i20sh{len(s) + 3}s",
            self.ctime_s,
            self.ctime_n,
            self.mtime_s,
            self.mtime_n,
            self.dev,
            self.ino,
            self.mode,
            self.uid,
            self.gid,
            self.size,
            self.sha1,
            self.flags,
            s,
        )

    @staticmethod
    def unpack(data: bytes) -> "GitIndexEntry":
        (
            ctime_s,
            ctime_n,
            mtime_s,
            mtime_n,
            dev,
            ino,
            mode,
            uid,
            gid,
            size,
            sha1,
            flags,
        ) = struct.unpack(">10i20sh", data[:62])
        data = data[62:]
        last_byte = data.find(b"\x00\x00\x00")
        name = data[:last_byte].decode()
        return GitIndexEntry(
            ctime_s, ctime_n, mtime_s, mtime_n, dev, ino, mode, uid, gid, size, sha1, flags, name
        )


def read_index(gitdir: pathlib.Path) -> tp.List[GitIndexEntry]:
    index_f = pathlib.Path(gitdir / "index")
    result: tp.List[GitIndexEntry] = []
    if not os.path.isfile(index_f):
        return result
    content = open(index_f, "rb")
    data = content.read()
    dirc, version, cnt = struct.unpack(">4s2i", data[:12])
    data = data[12:]
    for i in range(cnt):
        result.append(GitIndexEntry.unpack(data))
        data = data[62:]
        next_byte = data.find(b"\x00\x00\x00")
        data = data[next_byte + 3 :]
    content.close()
    return result


def write_index(gitdir: pathlib.Path, entries: tp.List[GitIndexEntry]) -> None:
    result = []
    result.append(b"DIRC")
    result.append(struct.pack(">2i", 2, len(entries)))
    for entry in entries:
        result.append(entry.pack())
    index_path = str(gitdir / "index")
    data = b"".join(result)
    result.append(struct.pack(">20s", hashlib.sha1(data).digest()))
    pathlib.Path(index_path).touch()
    f = open(index_path, "wb")
    f.write(b"".join(result))
    f.close()


def ls_files(gitdir: pathlib.Path, details: bool = False) -> None:
    files = read_index(gitdir)
    result = []
    if details:
        for f in files:
            mode = 100755
            if f.mode == 33188:
                mode = 100644
            result.append(" ".join([str(mode), str(f.sha1.hex()), "0"]) + "\t" + f.name)
        print("\n".join(result))
    else:
        for f in files:
            result.append(f.name)
        print("\n".join(result))


def update_index(gitdir: pathlib.Path, paths: tp.List[pathlib.Path], write: bool = True) -> None:
    indexdir = gitdir / "index"
    entries = []
    if os.path.isfile(indexdir):
        entries = read_index(gitdir)
    else:
        pathlib.Path(indexdir).touch()
    for path in paths:
        fileinfo = os.stat(path)
        f = open(path, "r")
        data = f.read()
        f.close()
        sha = hashlib.sha1((f"blob {len(data)}\0" + data).encode())
        new_entry = GitIndexEntry(
            int(fileinfo.st_ctime),
            0,
            int(fileinfo.st_mtime),
            0,
            fileinfo.st_dev,
            fileinfo.st_ino,
            fileinfo.st_mode,
            fileinfo.st_uid,
            fileinfo.st_gid,
            fileinfo.st_size,
            sha.digest(),
            0,
            str(path.as_posix()),
        )
        if new_entry in entries:
            continue
        hash_object(data.encode(), "blob", True)
        k = 0
        while k < len(entries):
            if entries[k].name == new_entry.name:
                entries[k] = new_entry
                break
            k += 1
        if k == len(entries):
            entries.append(new_entry)
    entries.sort(key=lambda x: x.name)
    write_index(gitdir, entries)
