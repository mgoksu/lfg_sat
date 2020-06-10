import sys
from collections import defaultdict
from tree import Tree

def unary(i, j, sentence, dp, kbest):
    for r1 in runa:
        tmp = []
        for r2 in runa[r1]:
            # if i == 2 and j == 6 and r1 == 'VP_VBP':
            #     print 'fuck'
            #     print dp[i][j][r1]
            for idx, statu in enumerate(dp[i][j][r2[0]]):
                if r2[0] == sentence[i]:
                    tmp.append([runa[r1][r2] * statu[0],
                                ('Terminal', r2, idx, 0)])
                else:
                    tmp.append([runa[r1][r2] * statu[0],
                                ('NonTerminal', r2, idx, 0)])
        for t in dp[i][j][r1]:
            if t not in tmp:
                tmp.append(t)
        dp[i][j][r1] = sorted(tmp, key=lambda x: x[0])[:-kbest-1:-1]

def cky(sentence, kbest):
    dp = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    back = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
    n = len(sentence)

    for i in xrange(n):
        dp[i][i+1][sentence[i]] = [[1.0, ()]]

    for diff in xrange(1,n+1):
        for i in xrange(n - diff + 1):
            j = i + diff
            for k in xrange(i+1, j):
                for r1 in rbin:
                    tmp = []
                    for r2 in rbin[r1]:
                        # if r2[0] in dp[i][k] and r2[1] in dp[k][j]:
                        for left_idx, left in enumerate(dp[i][k][r2[0]]):
                            for right_idx, right in enumerate((dp[k][j][r2[1]])):
                                tmp.append([rbin[r1][r2] * left[0] * right[0],
                                            (k, r2, left_idx, right_idx)])
                                    # print(r1, r2, left_idx, right_idx, i, j, k)
                    for t in dp[i][j][r1]:
                        if t not in tmp:
                            tmp.append(t)
                    dp[i][j][r1] = sorted(tmp, key=lambda x: x[0])[:-kbest-1:-1]

            for itr in xrange(10):
                unary(i, j, sentence, dp, kbest)

    for i in xrange(10):
        unary(0, len(sentence), sentence, dp, kbest)
    return dp

def backtrack(i, j, r1, sentence_origin, dp):
    result = []
    def rev(i, j, r1, sentence_origin, idx):
        if dp[i][j][r1] == None:
            return ''
        try:
            (k, r2, left_idx, right_idx) = dp[i][j][r1][idx][1]
        except Exception:
            print dp[i][j][r1]
            dafasdfasd
        if k == 'Terminal':
            return '(' + r1 + ' ' + sentence_origin[i] + ')'
        elif k == 'NonTerminal':
            return '(' + r1 + ' ' + rev(i,j,r2[0],sentence_origin, left_idx) + ')'
        else:
            return '(' + r1 + ' ' + rev(i,k,r2[0],sentence_origin, left_idx) + ' ' + rev(k,j,r2[1],sentence_origin, right_idx) + ')'
    
    for idx in range(len(dp[i][j][r1])):
        result.append([dp[i][j][r1][idx][0], rev(i, j, r1, sentence_origin, idx)])
        # print i, j, r1, sentence_origin, idx
    return result

def debinarize(t):
    if t.is_terminal():
        return t.dostr()
    res = ''
    if t.label[-1] != '\'':
        res += '(' + t.label + ' '
        for i,x in enumerate(t.subs):
            if i < len(t.subs) - 1:
                res += debinarize(x) + ' '
            else:
                res += debinarize(x)
        res += ')'
    else:
        for i,x in enumerate(t.subs):
            if i < len(t.subs) - 1:
                res += debinarize(x) + ' '
            else:
                res += debinarize(x)
    return res

# main

if __name__ == "__main__":
    # dp = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    # back = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
    rbin = defaultdict(lambda: defaultdict(float))
    runa = defaultdict(lambda: defaultdict(float))
    lexicon = set()

    if len(sys.argv) > 2:
        with open(sys.argv[2], 'r') as f:
            for word in f:
                lexicon.add(word.strip().split()[0])

    # read in grammers
    with open(sys.argv[1], 'r') as f:
        rules = f.readlines()
    for rule in rules[1:]:
        p = rule.split()
        k1 = p[0]
        if len(p) == 5:
            k2 = (p[2],)
            runa[k1][k2] = float(p[-1])
        else:
            k2 = (p[2],p[3])
            rbin[k1][k2] = float(p[-1])

    kbest = 5
    for line in sys.stdin:
        sentence_origin = line.strip().split()
        sentence = []
        for x in sentence_origin:
            if len(sys.argv) > 2 and x not in lexicon:
                x = '<unk>'
            sentence.append(x)
        dp = cky(sentence, kbest)
        # print(dp)
        result = backtrack(0, len(sentence),'TOP', sentence_origin, dp)
        for score, res in result:
            print score
            if len(res) != 0:
                print debinarize(Tree.parse(res))
            else:
                print 'NONE'


