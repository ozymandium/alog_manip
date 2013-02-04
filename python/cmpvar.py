#! /usr/bin/env python
"""
Robert Cofield, 2013/02/03
find all recorded variables in 2 alog files and compare the lists
"""
import sys, os
from pprint import pprint as pp

fn = ['', '']
f = [None, None]
v = [[], []]


if __name__ == '__main__':
    for n in 0,1:
        fn[n] = sys.argv[n+1]
        f[n] = file(fn[n], 'rU')
        for l in f[n]:
            if '%' in l or l == '':
                continue
            var = l.split()[1]
            if var not in v[n]:
                v[n].append(var)

    _0_not_1 = [var for var in v[0] if var not in v[1]]
    _1_not_0 = [var for var in v[1] if var not in v[0]]

    print('\n\n---------- Compare *.alog Variables ----------')
    print('\n== In file %s:' % fn[0])
    pp(v[0])
    print('== unique to this file:')
    pp(_0_not_1)
    print('\n== In file %s:' % fn[1])
    pp(v[1])
    print('==  unique to this file:')
    pp(_1_not_0)
