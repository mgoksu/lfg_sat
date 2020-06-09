from collections import defaultdict
from math import log
# from IPython import embed
import sys


dic = defaultdict(list)

grammar_path = 'grammar.pcfg.bin'
with open(grammar_path, 'r') as f:
    for line in f.readlines():
        if '->' in line:
            k, v = line.split('->')
            y, p = v.split('#')
            dic[y.strip()].append((k.strip(), log(float(p))))


def unary(dic, K, _dp, _bt, i, j):
    q = [(_k, _p, K) for _k, _p in dic[K] if ' ' not in _k]

    while len(q) > 0:
        _k, _p, k = q[0]
        q = q[1:]
        if ' ' not in _k:
            p = _dp[k]
            if _k not in _dp:
                _dp[_k] = p+_p
                _bt[_k] = ((i, j, k))
                q += [(__k, __p, _k) for __k, __p in dic[_k] if ' ' not in __k]
            elif p+_p > _dp[_k]:
                _dp[_k] = p+_p
                _bt[_k] = ((i, j, k))
                q += [(__k, __p, _k) for __k, __p in dic[_k] if ' ' not in __k]
    return _dp, _bt


def backtrace(bt, i, j, t):
    a = bt[i][j][t]
    if len(a) == 3:
        _i, _j, _t = a
        if _t == t and i == _i and j == _j:
            return t
        if t.endswith("'"):
            return backtrace(bt, _i, _j, _t)
        else:
            return '(%s %s)' % (t, backtrace(bt, _i, _j, _t))
    else:
        (i0, j0, k0), (i1, j1 ,k1) = a
        if t.endswith("'"):
            return '%s %s' % (backtrace(bt, i0, j0, k0), backtrace(bt, i1, j1, k1))
        else:
            return '(%s %s %s)' % (t, backtrace(bt, i0, j0, k0), backtrace(bt, i1, j1, k1))


def initialize(sent, dic, unk):
    dp = defaultdict(lambda: defaultdict(dict))
    bt = defaultdict(lambda: defaultdict(dict))

    for i, w in enumerate(sent):
        if unk and (w not in dic or len(dic[w]) == 0):
            w = '<unk>'
        for k, p in dic[w]:
            dp[i][i][k] = p
            bt[i][i][k] = ((i, i, w))
            bt[i][i][w] = ((i, i, w))
            dp[i][i], bt[i][i] = unary(dic, k, dp[i][i], bt[i][i], i, i)
    return dp, bt


def cky(dp, bt, dic, sent):
    for j in range(1, len(sent)):
        for i in range(len(sent)):
            _j = i+j
            if _j+1 > len(sent):
                continue
            for k in range(i, _j):
                if len(dp[i][k]) == 0 or len(dp[k+1][_j]) == 0:
                    continue
                left = dp[i][k]
                right = dp[k+1][_j]
                for t0, p0 in left.items():
                    for t1, p1 in right.items():
                        if '%s %s'%(t0, t1) not in dic:
                            continue
                        for t, p in dic['%s %s' % (t0, t1)]:
                            _p = p0 + p1 + p
                            if len(dp[i][_j]) == 0 or t not in dp[i][_j]:
                                dp[i][_j][t] = _p
                                bt[i][_j][t] = ((i, k, t0), (k+1, _j, t1))
                            else:
                                if _p > dp[i][_j][t]:
                                    dp[i][_j][t] = _p
                                    bt[i][_j][t] = ((i, k, t0), (k+1, _j, t1))
            ts = list(dp[i][_j].keys())
            for t in ts:
                dp[i][_j], bt[i][_j] = unary(dic, t, dp[i][_j], bt[i][_j], i, _j)
    return dp, bt


def cky_kbest(dp, bt, dic, sent):
    other_bt_count = 0
    for j in range(1, len(sent)):
        for i in range(len(sent)):
            _j = i+j
            if _j+1 > len(sent):
                continue
            for k in range(i, _j):
                if len(dp[i][k]) == 0 or len(dp[k+1][_j]) == 0:
                    continue
                left = dp[i][k]
                right = dp[k+1][_j]
                for t0, p0 in left.items():
                    for t1, p1 in right.items():
                        if '%s %s'%(t0, t1) not in dic:
                            continue
                        for t, p in dic['%s %s' % (t0, t1)]:
                            _p = p0 + p1 + p
                            if len(dp[i][_j]) == 0 or t not in dp[i][_j]:
                                dp[i][_j][t] = _p
                                bt[i][_j][t] = ((i, k, t0), (k+1, _j, t1))
                            else:
                                if _p > dp[i][_j][t]:
                                    dp[i][_j][t] = _p
                                    bt[i][_j][t] = ((i, k, t0), (k+1, _j, t1))
            ts = list(dp[i][_j].keys())
            for t in ts:
                dp[i][_j], bt[i][_j] = unary(dic, t, dp[i][_j], bt[i][_j], i, _j)
    return dp, bt


def get_cky(sent, unk):
    sent = sent.strip().split()

    dp, bt = initialize(sent, dic, unk)
    # dp, bt = cky(dp, bt, dic, sent)
    dp, bt = cky_kbest(dp, bt, dic, sent)

    if 'TOP' in bt[0][len(sent) - 1]:
        return backtrace(bt, 0, len(sent) - 1, 'TOP').strip()
    else:
        return 'NONE'


if __name__ == '__main__':
    dic = defaultdict(list)

    grammar_path = sys.argv[1]
    with open(grammar_path, 'r') as f:
        for line in f.readlines():
            if '->' in line:
                k, v = line.split('->')
                y, p = v.split('#')
                dic[y.strip()].append((k.strip(), log(float(p))))

    dp = defaultdict(lambda: defaultdict(dict))

    unk = False
    if len(sys.argv) > 2:
        unk = True

    for sent in sys.stdin:
        sent = sent.strip().split()

        dp, bt = initialize(sent, dic, unk)
        dp, bt = cky(dp, bt, dic, sent)

        if 'TOP' in bt[0][len(sent)-1]:
            print(backtrace(bt, 0, len(sent)-1, 'TOP').strip())
        else:
            print('NONE')
