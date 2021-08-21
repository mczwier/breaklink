#!/usr/bin/env python3

import sys, os, argparse, shutil
from pathlib import Path


parser = argparse.ArgumentParser(description='''\
Replace symbolic links with copies of the referenced file(s). Non-symlinks
issue a warning (unless -q/--quiet is specified) but this is not an error,
so that shell globs can catch symlinks (which are dereferenced) among
non-symlinks (which are not).
''')

parser.add_argument('filename', nargs='+',
                    help='Link(s) to replace with a copy of the referenced file(s).')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Report what is being done')
parser.add_argument('-q', '--quiet', action='store_true',
                    help='Be quiet (do not complain about non-links)')
parser.add_argument('-n', '--dry-run', action='store_true',
                    help='Report what would be done without taking any action.')

args = parser.parse_args()

VERBOSE = args.verbose or False
QUIET = args.quiet or False
DRYRUN = False
if args.dry_run:
    QUIET = False
    VERBOSE = True
    DRYRUN = True
    
def vprint(*args, **kwargs):
    global VERBOSE

    if VERBOSE:
        print(*args, **kwargs)

def nqprint(*args, **kwargs):
    global VERBOSE, QUIET

    if not QUIET or VERBOSE:
        print(*args, **kwargs)


for filename in args.filename:
    p = Path(filename)

    if p.is_symlink():
        orig = p.resolve(strict=True)
        vprint('replace {} with {}'.format(p, orig))
        if not DRYRUN:
            p.unlink()
            shutil.copy2(orig, p)
    else:
        nqprint('{} is not a symlink'.format(p), file=sys.stderr)

