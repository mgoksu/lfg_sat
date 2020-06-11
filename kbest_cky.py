import sys
from collections import defaultdict
from tree import Tree

class Parser(object):
    def __init__(self, vocab_file='./train.dict', grammar_file='grammar.pcfg.bin'):
        self.rbin = defaultdict(lambda: defaultdict(float))
        self.runa = defaultdict(lambda: defaultdict(float))
        self.lexicon = set()

        with open(vocab_file, 'r') as f:
            for word in f:
                self.lexicon.add(word.strip().split()[0])

        # read in grammers
        with open(grammar_file, 'r') as f:
            rules = f.readlines()
        for rule in rules[1:]:
            p = rule.split()
            k1 = p[0]
            if len(p) == 5:
                k2 = (p[2],)
                self.runa[k1][k2] = float(p[-1])
            else:
                k2 = (p[2],p[3])
                self.rbin[k1][k2] = float(p[-1])
        

    def unary(self, i, j, sentence, dp, kbest):
        for r1 in self.runa:
            tmp = []
            for r2 in self.runa[r1]:
                # if i == 2 and j == 6 and r1 == 'VP_VBP':
                #     print 'fuck'
                #     print dp[i][j][r1]
                for idx, statu in enumerate(dp[i][j][r2[0]]):
                    if r2[0] == sentence[i]:
                        tmp.append([self.runa[r1][r2] * statu[0],
                                    ('Terminal', r2, idx, 0)])
                    else:
                        tmp.append([self.runa[r1][r2] * statu[0],
                                    ('NonTerminal', r2, idx, 0)])
            for t in dp[i][j][r1]:
                if t not in tmp:
                    tmp.append(t)
            dp[i][j][r1] = sorted(tmp, key=lambda x: x[0])[:-kbest-1:-1]

    def cky(self, sentence, kbest):
        dp = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        back = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
        n = len(sentence)

        for i in range(n):
            dp[i][i+1][sentence[i]] = [[1.0, ()]]

        for diff in range(1,n+1):
            for i in range(n - diff + 1):
                j = i + diff
                for k in range(i+1, j):
                    for r1 in self.rbin:
                        tmp = []
                        for r2 in self.rbin[r1]:
                            # if r2[0] in dp[i][k] and r2[1] in dp[k][j]:
                            for left_idx, left in enumerate(dp[i][k][r2[0]]):
                                for right_idx, right in enumerate((dp[k][j][r2[1]])):
                                    tmp.append([self.rbin[r1][r2] * left[0] * right[0],
                                                (k, r2, left_idx, right_idx)])
                                        # print(r1, r2, left_idx, right_idx, i, j, k)
                        for t in dp[i][j][r1]:
                            if t not in tmp:
                                tmp.append(t)
                        dp[i][j][r1] = sorted(tmp, key=lambda x: x[0])[:-kbest-1:-1]

                for itr in range(10):
                    self.unary(i, j, sentence, dp, kbest)

        for i in range(10):
            self.unary(0, len(sentence), sentence, dp, kbest)
        return dp

    def backtrack(self, i, j, r1, sentence_origin, dp):
        result = []
        def rev(i, j, r1, sentence_origin, idx):
            if dp[i][j][r1] == None:
                return ''
            try:
                (k, r2, left_idx, right_idx) = dp[i][j][r1][idx][1]
            except Exception:
                print(dp[i][j][r1])
                # dafasdfasd
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

    def debinarize(self, t):
        if t.is_terminal():
            return t.dostr()
        res = ''
        if t.label[-1] != '\'':
            res += '(' + t.label + ' '
            for i,x in enumerate(t.subs):
                if i < len(t.subs) - 1:
                    res += self.debinarize(x) + ' '
                else:
                    res += self.debinarize(x)
            res += ')'
        else:
            for i,x in enumerate(t.subs):
                if i < len(t.subs) - 1:
                    res += self.debinarize(x) + ' '
                else:
                    res += self.debinarize(x)
        return res
    
    def parse(self, sentence_origin, kbest):
        sentence = []
        for x in sentence_origin:
            if len(sys.argv) > 2 and x not in self.lexicon:
                x = '<unk>'
            sentence.append(x)
        dp = self.cky(sentence, kbest)
        result = self.backtrack(0, len(sentence),'TOP', sentence_origin, dp)
        return result


if __name__ == "__main__":
    parser = Parser()
    kbest = 5
    for line in sys.stdin:
        sentence_origin = line.strip().split()

        result = parser.parse(sentence_origin, kbest)
        print(result)
        for score, res in result:
            print(score)
            if len(res) != 0:
                print(parser.debinarize(Tree.parse(res)))
            else:
                print('NONE')


