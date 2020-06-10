import sys
import math 
from collections import defaultdict
from tree import Tree


def unary(i, j, sentence, dp, back):
    for r1 in runa:
        for r2 in runa[r1]:
            score = runa[r1][r2] + dp[i][j][r2[0]]
            if score < dp[i][j][r1]:
                if r2[0] == sentence[i]:
                    dp[i][j][r1] = score
                    back[i][j][r1] = ('Terminal', r2)
                else:
                    dp[i][j][r1] = score
                    back[i][j][r1] = ('NonTerminal', r2)

def cky(sentence):
    dp = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 9999999.)))
    back = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
    n = len(sentence)

    for i in xrange(n):
        dp[i][i+1][sentence[i]] = 0.0

    for diff in xrange(1,n+1):
        for i in xrange(n - diff + 1):
            j = i + diff
            for k in xrange(i+1, j):
                for r1 in rbin:
                    for r2 in rbin[r1]:
                        score = rbin[r1][r2] + dp[i][k][r2[0]] + dp[k][j][r2[1]]
                        if score < dp[i][j][r1]:
                            dp[i][j][r1] = score
                            back[i][j][r1] = (k, r2)
            for itr in xrange(10):
                unary(i, j, sentence, dp, back)
    for i in xrange(10):
        unary(0, len(sentence), sentence, dp, back)
    return dp, back

def backtrack(i, j, r1, sentence_origin, back):
    def rev(i, j, r1, sentence_origin):
        if back[i][j][r1] == None:
            return ''
        (k, r2) = back[i][j][r1]
        if k == 'Terminal':
            return '(' + r1 + ' ' + sentence_origin[i] + ')'
        elif k == 'NonTerminal':
            return '(' + r1 + ' ' + rev(i,j,r2[0],sentence_origin) + ')'
        else:
            return '(' + r1 + ' ' + rev(i,k,r2[0],sentence_origin) + ' ' + rev(k,j,r2[1],sentence_origin) + ')'
    return rev(i, j, r1, sentence_origin)

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
            runa[k1][k2] = -math.log(float(p[-1]))
        else:
            k2 = (p[2],p[3])
            rbin[k1][k2] = -math.log(float(p[-1]))


    for line in sys.stdin:
        sentence_origin = line.strip().split()
        sentence = []
        for x in sentence_origin:
            if len(sys.argv) > 2 and x not in lexicon:
                x = '<unk>'
            sentence.append(x)
        dp, back = cky(sentence)

        print(math.exp(-dp[0][len(sentence)]['TOP']))
        res = backtrack(0, len(sentence),'TOP', sentence_origin, back)
        if len(res) != 0:
            print debinarize(Tree.parse(res))
        else:
            print 'NONE'
