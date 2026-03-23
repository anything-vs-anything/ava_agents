#!/usr/bin/env python3
"""
Scan all .py files in the repo for import statements and flag any that are not
part of the Python standard library.  Exit 0 if clean, 1 if third-party
packages are detected.

Usage:
    python3 scripts/check_deps.py
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STDLIB_MODULES: set[str] = {
    "__future__",
    "abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio",
    "asyncore", "atexit", "audioop", "base64", "bdb", "binascii",
    "binhex", "bisect", "builtins", "bz2", "calendar", "cgi", "cgitb",
    "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections",
    "colorsys", "compileall", "concurrent", "configparser", "contextlib",
    "contextvars", "copy", "copyreg", "cProfile", "crypt", "csv",
    "ctypes", "curses", "dataclasses", "datetime", "dbm", "decimal",
    "difflib", "dis", "distutils", "doctest", "email", "encodings",
    "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput",
    "fnmatch", "fractions", "ftplib", "functools", "gc", "getopt",
    "getpass", "gettext", "glob", "graphlib", "grp", "gzip", "hashlib",
    "heapq", "hmac", "html", "http", "idlelib", "imaplib", "imghdr",
    "imp", "importlib", "inspect", "io", "ipaddress", "itertools",
    "json", "keyword", "lib2to3", "linecache", "locale", "logging",
    "lzma", "mailbox", "mailcap", "marshal", "math", "mimetypes",
    "mmap", "modulefinder", "multiprocessing", "netrc", "nis", "nntplib",
    "numbers", "operator", "optparse", "os", "ossaudiodev", "pathlib",
    "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform",
    "plistlib", "poplib", "posix", "posixpath", "pprint", "profile",
    "pstats", "pty", "pwd", "py_compile", "pyclbr", "pydoc",
    "queue", "quopri", "random", "re", "readline", "reprlib",
    "resource", "rlcompleter", "runpy", "sched", "secrets", "select",
    "selectors", "shelve", "shlex", "shutil", "signal", "site",
    "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "spwd",
    "sqlite3", "sre_compile", "sre_constants", "sre_parse", "ssl",
    "stat", "statistics", "string", "stringprep", "struct", "subprocess",
    "sunau", "symtable", "sys", "sysconfig", "syslog", "tabnanny",
    "tarfile", "telnetlib", "tempfile", "termios", "test", "textwrap",
    "threading", "time", "timeit", "tkinter", "token", "tokenize",
    "tomllib", "trace", "traceback", "tracemalloc", "tty", "turtle",
    "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib",
    "uu", "uuid", "venv", "warnings", "wave", "weakref", "webbrowser",
    "winreg", "winsound", "wsgiref", "xdrlib", "xml", "xmlrpc",
    "zipapp", "zipfile", "zipimport", "zlib", "zoneinfo",
    "_thread", "_io", "_collections_abc",
}


def top_level(module_name: str) -> str:
    return module_name.split(".")[0]


def scan_file(path: Path) -> list[str]:
    """Return list of non-stdlib top-level module names imported by *path*."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        print(f"  WARN: syntax error in {path}: {exc}", file=sys.stderr)
        return []

    third_party: list[str] = []
    for node in ast.walk(tree):
        names: list[str] = []
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names = [node.module]
        for name in names:
            tl = top_level(name)
            if tl not in STDLIB_MODULES:
                third_party.append(tl)
    return third_party


def main() -> int:
    py_files = sorted(ROOT.rglob("*.py"))
    if not py_files:
        print("No .py files found.")
        return 0

    issues: list[tuple[Path, list[str]]] = []
    for path in py_files:
        if ".venv" in path.parts or "node_modules" in path.parts:
            continue
        third = scan_file(path)
        if third:
            issues.append((path, third))

    print(f"Scanned {len(py_files)} Python file(s).")
    if not issues:
        print("All imports are standard-library. No third-party dependencies detected.")
        return 0

    print(f"\nThird-party imports found in {len(issues)} file(s):")
    for path, modules in issues:
        rel = path.relative_to(ROOT)
        unique = sorted(set(modules))
        print(f"  {rel}: {', '.join(unique)}")
    print("\nIf intentional, add these to a requirements.txt or pyproject.toml.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
