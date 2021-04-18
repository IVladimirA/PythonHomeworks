import os
import pathlib
import stat
import time
import typing as tp

from pyvcs.index import GitIndexEntry, read_index
from pyvcs.objects import hash_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref


def write_tree(gitdir: pathlib.Path, index: tp.List[GitIndexEntry], dirname: str = "") -> str:
    data = []
    i = 0
    while i < len(index):
        entry = index[i]
        par_dir = entry.name.find(dirname)
        if dirname != "" and par_dir != 0:
            i += 1
            continue
        name = entry.name
        if dirname != "":
            name = entry.name[len(dirname) + 1 :]
        mode = 10755
        if entry.mode == 33188:
            mode = 100644
        parent_cnt = len(pathlib.Path(name).parents)
        if parent_cnt > 1:
            mode = 40000
            cur_dir = pathlib.Path(name).parents[parent_cnt - 2].as_posix()
            if dirname != "":
                cur_dir = dirname + "/" + cur_dir
            data.append(
                b"".join(
                    [
                        (f"{mode} {pathlib.Path(name).parents[parent_cnt- 2].as_posix()}").encode(),
                        b"\x00",
                        bytes.fromhex(write_tree(gitdir, index, cur_dir)),
                    ]
                )
            )
            k = i
            for j in range(k, len(index)):
                sub_entry = index[j]
                sub_dir_p = sub_entry.name.find(dirname)
                if dirname != "" and sub_dir_p != 0:
                    continue
                sub_name = entry.name
                if dirname != "":
                    sub_name = sub_entry.name[len(dirname) + 1 :]
                sub_parent_cnt = len(pathlib.Path(sub_name).parents)
                if (
                    sub_parent_cnt > 1
                    and pathlib.Path(sub_name).parents[sub_parent_cnt - 2].as_posix() == name
                ):
                    i = j
        else:
            data.append(
                b"".join(
                    [
                        (f"{mode} {pathlib.Path(entry.name).name}").encode(),
                        b"\x00",
                        entry.sha1,
                    ]
                )
            )
        i += 1
        # p = len(pathlib.Path(entry.name).parents)
        # print(pathlib.Path(entry.name).as_posix(), pathlib.Path(entry.name).parents[p - 1])
        # print()
    content = b"".join(data)
    return hash_object(content, "tree", True)


def commit_tree(
    gitdir: pathlib.Path,
    tree: str,
    message: str,
    parent: tp.Optional[str] = None,
    author: tp.Optional[str] = None,
) -> str:
    if author is None and "GIT_AUTHOR_NAME" in os.environ and "GIT_AUTHOR_EMAIL" in os.environ:
        author = os.environ["GIT_AUTHOR_NAME"] + " " + os.environ["GIT_AUTHOR_EMAIL"]
    if author is None:
        author = "Vladimir Ivanov example@example.com"
    comm_time = (
        str(int(time.mktime(time.localtime()))) + " " + str(time.strftime("%z", time.gmtime()))
    )
    content = (
        "tree "
        + tree
        + "\nauthor "
        + author
        + " "
        + comm_time
        + "\ncommitter "
        + author
        + " "
        + comm_time
        + "\n\n"
        + message
        + "\n"
    )
    return hash_object(content.encode(), "commit", True)
