import hashlib
import os
import pathlib
import re
import stat
import typing as tp
import zlib

from pyvcs.refs import update_ref
from pyvcs.repo import repo_find


def hash_object(data: bytes, fmt: str, write: bool = False) -> str:
    header = f"{fmt} {len(data)}\0"
    store = header.encode() + data
    result = hashlib.sha1(store).hexdigest()
    if write:
        gitdir = repo_find(os.getcwd())
        os.makedirs(gitdir / "objects" / result[0:2], exist_ok=True)
        pathlib.Path(gitdir / "objects" / result[0:2] / result[2:]).touch()
        cur_file = open(gitdir / "objects" / result[0:2] / result[2:], "wb")
        level = -1
        if fmt == "tree":
            level = 1
        cur_file.write(zlib.compress(store, level))
        cur_file.close()
    return result


def resolve_object(obj_name: str, gitdir: pathlib.Path) -> tp.List[str]:
    if len(obj_name) not in range(4, 41):
        raise AssertionError(f"Not a valid object name {obj_name}")
    obj_dir = gitdir / "objects"
    if not os.path.isdir(obj_dir / obj_name[0:2]):
        raise AssertionError(f"Not a valid object name {obj_name}")
    curr_dir = obj_dir / obj_name[0:2]
    ending = obj_name[2:]
    n = len(ending)
    result = []
    for f in os.listdir(curr_dir):
        if os.path.isfile(curr_dir / f) and f == ending or f[0:n] == ending:
            result.append(obj_name[0:2] + f)
    if len(result) == 0:
        raise AssertionError(f"Not a valid object name {obj_name}")
    return result


def find_object(obj_name: str, gitdir: pathlib.Path) -> str:
    return resolve_object(obj_name, gitdir)[0]


def read_object(sha: str, gitdir: pathlib.Path) -> tp.Tuple[str, bytes]:
    obj_path = find_object(sha, gitdir)
    cur_file = open(gitdir / "objects" / obj_path[0:2] / obj_path[2:], "rb")
    obj_data = zlib.decompress(cur_file.read())
    right, left = obj_data.find(b" "), obj_data.find(b"\x00")
    length = int(obj_data[right:left].decode("ascii"))
    content = obj_data[left + 1 :]
    fmt = obj_data[:right].decode()
    cur_file.close()
    return fmt, content


def read_tree(data: bytes) -> tp.List[tp.Tuple[int, str, str]]:
    result = []
    while len(data) > 0:
        fmt = data[:6].decode()
        data = data[6:]
        if fmt == "100644":
            data = data[1:]
            sep_ind = data.find(b"\x00")
            # print("Name ---", data[:sep_ind].decode())
            # print("Hash ---", data[sep_ind + 1 : sep_ind + 21].hex())
            result.append((100644, data[:sep_ind].decode(), data[sep_ind + 1 : sep_ind + 21].hex()))
            data = data[sep_ind + 21 :]
        else:
            sep_ind = data.find(b"\x00")
            # print("Name ---", data[:sep_ind].decode())
            # print("Hash ---", data[sep_ind + 1 : sep_ind + 21].hex())
            result.append((40000, data[:sep_ind].decode(), data[sep_ind + 1 : sep_ind + 21].hex()))
            data = data[sep_ind + 21 :]
    return result


def cat_file(obj_name: str, pretty: bool = True) -> None:
    if "GIT_DIR" not in os.environ:
        gitname = pathlib.Path(".git")
    else:
        gitname = pathlib.Path(os.environ["GIT_DIR"])
    fmt, data = read_object(obj_name, gitname)
    if fmt == "blob":
        if pretty:
            print(data.decode())
        else:
            print(data)
        return
    elif fmt == "tree":
        content = read_tree(data)
        if pretty:
            for entry in content:
                if entry[0] == 40000:
                    print("040000", "tree", entry[2] + "\t" + entry[1])
                else:
                    print("100644", "blob", entry[2] + "\t" + entry[1])
        else:
            for entry in content:
                print(entry[2])
    else:
        print(data.decode())


def find_tree_files(tree_sha: str, gitdir: pathlib.Path) -> tp.List[tp.Tuple[str, str]]:
    # print("CURRENT TREE: " + tree_sha)
    fmt, content = read_object(tree_sha, gitdir)
    objects = read_tree(content)
    result = []
    for obj in objects:
        if obj[0] == 100644 or obj[0] == 100755:
            result.append((obj[1], obj[2]))
        else:
            # print("SUB_TREE: ", obj[1])
            sub_objects = find_tree_files(obj[2], gitdir)
            for sub_obj in sub_objects:
                result.append((obj[1] + "/" + sub_obj[0], sub_obj[1]))
    return result


def commit_parse(raw: bytes, start: int = 0, dct=None):
    # PUT YOUR CODE HERE
    ...
