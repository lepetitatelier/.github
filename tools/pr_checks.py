#!/usr/bin/env python3
"""Checks for a pull request in any lepetitatelier repo. Run from the repo root.

usage: pr_checks.py <base-ref> [--all]

1. Big files go through Git LFS: a file the repo's .gitattributes sends to LFS must be committed as an LFS pointer,
   and any other new file over 5 MB must be added to LFS.
2. Relative links in Markdown point to files that exist in the repo (links starting with / are website paths).

Only files changed since <base-ref> are checked (--all checks every tracked file). Problems are printed as GitHub
annotations; the exit code is 1 if there are any.
"""
import os, re, subprocess, sys
from urllib.parse import unquote

MAX_PLAIN = 5 * 1024 * 1024


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def changed(base, everything):
    if everything:
        out = git("ls-files", "-z")
    else:
        out = git("diff", "-z", "--name-only", "--diff-filter=AMR", f"{base}...HEAD")
    return [p for p in out.split("\0") if p]


errors = 0


def error(path, msg, line=None):
    global errors
    errors += 1
    loc = f"file={path}" + (f",line={line}" if line else "")
    print(f"::error {loc}::{msg}")


def check_lfs(paths):
    attrs = {}
    if paths:
        out = subprocess.run(["git", "check-attr", "-z", "filter", "--stdin"], input="\0".join(paths) + "\0",
                             capture_output=True, text=True, check=True).stdout.split("\0")
        for i in range(0, len(out) - 2, 3):
            attrs[out[i]] = out[i + 2]
    for p in paths:
        try:
            size = int(git("cat-file", "-s", f"HEAD:{p}").strip())
        except subprocess.CalledProcessError:
            continue  # submodule or not in HEAD
        head = subprocess.run(["git", "cat-file", "-p", f"HEAD:{p}"], capture_output=True).stdout[:120]
        pointer = head.startswith(b"version https://git-lfs.github.com/spec/v1")
        if attrs.get(p) == "lfs" and not pointer:
            error(p, "This file type goes through Git LFS here but was committed as a normal file. "
                     "Fix: `git lfs install`, then `git rm --cached <file> && git add <file>` and commit again.")
        elif not pointer and size > MAX_PLAIN:
            error(p, f"{size / 1e6:.1f} MB committed without Git LFS. Add its type to .gitattributes "
                     "(`git lfs track '*.ext'`), then `git rm --cached <file> && git add <file>`.")


LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
TRACKED = None


def exists(path):
    global TRACKED
    if TRACKED is None:
        TRACKED = set()
        for f in git("ls-files", "-z").split("\0"):
            if not f:
                continue
            TRACKED.add(f)
            parts = f.split("/")
            for i in range(1, len(parts)):
                TRACKED.add("/".join(parts[:i]))
    return path.rstrip("/") in TRACKED or path in ("", ".")


def check_links(paths):
    for p in paths:
        if not p.lower().endswith(".md") or "/upstream/" in f"/{p}" or not os.path.isfile(p):
            continue
        fence = False
        for n, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            if line.lstrip().startswith(("```", "~~~")):
                fence = not fence
            if fence:
                continue
            for target in LINK.findall(re.sub(r"`[^`]*`", "", line)):
                # skip URLs, anchors, and site paths like /projects/x/ (cards are also website pages)
                if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith(("#", "/")):
                    continue
                t = unquote(target.split("#")[0].split("?")[0])
                if not t:
                    continue
                full = os.path.normpath(os.path.join(os.path.dirname(p), t))
                if full.startswith(".."):
                    error(p, f"Link leaves the repo: {target}. Link to another repo with its full GitHub URL.", n)
                elif not exists(full):
                    error(p, f"Broken link: {target} (no {full} in this repo).", n)


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
    files = changed(base, "--all" in sys.argv)
    print(f"Checking {len(files)} file(s).")
    check_lfs(files)
    check_links(files)
    if errors:
        print(f"{errors} problem(s). Each one is shown on the file in the pull request.")
        sys.exit(1)
    print("All good.")
