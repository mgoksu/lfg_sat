import sys
from tree import Tree
from collections import defaultdict

def get_words(t):
    a=[]
    if t.is_terminal():
        a += [t.word]
    else:
        for sub in t.subs:
            a += get_words(sub)

    return a

def tree_to_str(t, h):
    if t.is_terminal():
        return "(%s %s)" % (t.label, t.word if h[t.word]>1 else '<unk>')
    else:
        tmp=[]
        for sub in t.subs:
            tmp.append(tree_to_str(sub, h))
        return "(%s %s)" % (t.label, ' '.join(tmp))


h = defaultdict(lambda: 0)

lines = list(sys.stdin)

for i, line in enumerate(lines):
    t = Tree.parse(line.strip(), trunc=False)

    words = get_words(t)

    for w in words:
        h[w] += 1

#print(h)

f = open('train.trees.unk', 'w')
# f = open('02-21.10way.clean.unk', 'w')
for i, line in enumerate(lines):
    t = Tree.parse(line.strip(), trunc=False)

    #print(t)
    #print(print_tree(t, h))
    f.write(tree_to_str(t, h))
    f.write("\n")

f.close()

f = open('train.dict', 'w')
# f = open('02-21.10way.clean.dict', 'w')
for k in h:
    if h[k]>1:
        f.write(k)
        f.write("\n")

f.close()
