#!/usr/bin/env python
"""
A few suggestions:
    1. Don't make mistakes, mistakes are more expensive
    2. Avoid bugs and code that works in 80% cases
    3. Keep track of things that needs to be tied up
    4. Leverage consistency, reuse instead of creating again
"""

from collections import UserDict
from functools import wraps
import re
import json
import argparse
source_pattern = '({\s*%\s+((source)\s+([-./\w]+)|((\w+\.)*\w+))})'


class HybridDataSource(UserDict):
    def __init__(self, data={}):
        self.data = data

    def hybrid_wrap(func):
        @wraps(func)
        def auto_type_function(*args):
            res = func(*args)
            if isinstance(res, (dict, list)):
                return HybridDataSource(res)
            return res
        return auto_type_function

    @hybrid_wrap
    def __getitem__(self, key):
        if isinstance(self.data, dict):
            return self.data[key]
        return self.data[int(key)]


data_source = HybridDataSource()


def load_data_source(fn):
    source = json.load(open(fn))
    data_source.update(source)


def interp_line(line):
    # classify into 3 types:
    # 1. load data source
    # 2. data injection
    # 3. as is
    res = re.findall(source_pattern, line)

    if not res:
        return line
    for r in res:
        if r[2]:
            # source pattern, replace with empty line
            fn = r[3]
            load_data_source(fn)
            line = line.replace(r[0], f'# data source: {fn}')
        elif r[4]:
            d = data_source
            for k in r[4].split('.'):
                d = d[k]
            line = line.replace(r[0], str(d))
    return line


def populate_file(in_f, out_f):
    out_f.writelines([interp_line(l) for l in in_f.readlines()])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file', type=argparse.FileType('r'))
    parser.add_argument('out_file', type=argparse.FileType('w'))
    args = parser.parse_args()
    populate_file(args.in_file, args.out_file)
