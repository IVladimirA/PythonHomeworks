import os
import pathlib
import typing as tp

from pyvcs.index import read_index, update_index
from pyvcs.objects import commit_parse, find_object, find_tree_files, read_object
from pyvcs.refs import get_ref, is_detached, resolve_head, update_ref
from pyvcs.tree import commit_tree, write_tree


def add(gitdir: pathlib.Path, paths: tp.List[pathlib.Path]) -> None:
    update_index(gitdir, paths)


def commit(gitdir: pathlib.Path, message: str, author: tp.Optional[str] = None) -> str:
    commit_sha = commit_tree(gitdir, write_tree(gitdir, read_index(gitdir)), message, author=author)
    if is_detached(gitdir):
        ref = gitdir / "HEAD"
    else:
        ref = pathlib.Path(get_ref(gitdir))
    # print(f"REF: {ref}")
    f = open(gitdir / ref, "w")
    f.write(commit_sha)
    f.close()
    return commit_sha


def checkout(gitdir: pathlib.Path, obj_name: str) -> None:
    fmt, old_content = read_object(obj_name, gitdir)
    old_content_s = old_content.decode()
    objects = find_tree_files(old_content_s[5:25], gitdir)
    """print(f"CONTENTS of {obj_name}:")
    for obj in objects:
        print(obj[0], obj[1])
    print("")"""
    project_dir = gitdir.absolute().parent
    print("PROJECT DIR", project_dir)
    old_dirs = []
    for obj in objects:
        if os.path.isfile(project_dir / obj[0]):
            os.remove(project_dir / obj[0])
        elif os.path.isdir(project_dir / obj[0]):
            if len(os.listdir(project_dir / obj[0])) == 0:
                os.rmdir(project_dir / obj[0])
            else:
                old_dirs.append(project_dir / obj[0])
    cur_dir_i, cnt = 0, 0
    removed = [False] * len(old_dirs)
    while cnt < len(old_dirs):
        if not removed[cur_dir_i] and len(os.listdir(old_dirs[cur_dir_i])) == 0:
            os.rmdir(old_dirs[cur_dir_i])
            removed[cur_dir_i] = True
            cnt += 1
        cur_dir_i += 1
        if cur_dir_i >= len(old_dirs):
            cur_dir_i = 0
    print("CONTENT OF GITDIR: ")
    print(os.listdir(project_dir))
    print("")
