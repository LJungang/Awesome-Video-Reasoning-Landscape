#!/usr/bin/env python3
"""Compatibility entry point; the live catalog now uses scripts/catalog.py."""
import argparse
import sys
from catalog import main

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    sys.argv = [sys.argv[0], 'check' if args.check else 'render']
    main()
