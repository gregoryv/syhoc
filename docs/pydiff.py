#!/usr/bin/env python3
"""
Usage examples:
  # Compare a file between two git refs
  python git_html_diff.py v0.2 HEAD myfile -o diff.html

  # Compare two arbitrary files directly
  python git_html_diff.py -file-a old.txt -file-b new.txt -o diff.html
"""

import subprocess
import sys
import argparse
from difflib import HtmlDiff
from pathlib import Path

def git_show(ref, path):
    """Return file contents at given git ref."""
    p = subprocess.run(['git', 'show', f'{ref}:{path}'], capture_output=True, text=True)
    if p.returncode != 0:
        return ""
    return p.stdout

def read_file(path):
    """Return file contents from local file."""
    try:
        return Path(path).read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {path}: {e}", file=sys.stderr)
        return ""

def main():
    ap = argparse.ArgumentParser(description="Generate a side-by-side HTML diff (Git refs or local files).")

    # Two modes: git or file
    ap.add_argument('ref_a', nargs='?', help="Git ref A (e.g. v0.2)")
    ap.add_argument('ref_b', nargs='?', help="Git ref B (e.g. HEAD)")
    ap.add_argument('path', nargs='?', help="File path in repo")

    ap.add_argument('-file-a', dest='file_a', help="Path to first local file")
    ap.add_argument('-file-b', dest='file_b', help="Path to second local file")
    ap.add_argument('-o', '--output', default='diff.html', help="Output HTML file")

    args = ap.parse_args()

    # Determine mode
    if args.file_a and args.file_b:
        # Local file diff mode
        a_text = read_file(args.file_a).splitlines()
        b_text = read_file(args.file_b).splitlines()
        fromdesc = args.file_a
        todesc = args.file_b
    elif args.ref_a and args.ref_b and args.path:
        # Git mode
        a_text = git_show(args.ref_a, args.path).splitlines()
        b_text = git_show(args.ref_b, args.path).splitlines()
        fromdesc = f'{args.ref_a}:{args.path}'
        todesc = f'{args.ref_b}:{args.path}'
    else:
        ap.error("Must specify either (ref_a ref_b path) or (-file-a FILEA -file-b FILEB)")

    # Generate HTML diff
    hd = HtmlDiff(tabsize=4, wrapcolumn=80)
    html = hd.make_file(a_text, b_text, fromdesc=fromdesc, todesc=todesc)

    Path(args.output).write_text(html, encoding='utf-8')
    print(f"Wrote {args.output}")

if __name__ == '__main__':
    main()
