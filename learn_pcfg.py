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

def tree_to_str(t):
    if t.is_terminal():
        return "(%s %s)" % (t.label, t.word)
    else:
        tmp=[]
        for sub in t.subs:
            tmp.append(tree_to_str(sub))
        return "(%s %s)" % (t.label, ' '.join(tmp))

def print_subs(t):
    if not t.is_terminal():
        print(t.label)
        print(len(t.subs))
        for sub in t.subs:
            print_subs(sub)

def binarize(t):
    if not t.is_terminal():
        if len(t.subs)>2:
            new_node=Tree(t.label+'_'+t.subs[0].label, (t.subs[0].span[1], t.subs[-1].span[1]), subs=[ss for ss in t.subs[1:]])
            t.subs=[t.subs[0], new_node]
            # recursive
            binarize(t.subs[0])
            binarize(new_node)
        else:
            # recursive
            for sub in t.subs:
                binarize(sub)

def count(t, h):
    if t.is_terminal():
        h[t.label][t.word] += 1
    else:
        tmp = ' '.join([s.label for s in t.subs])
        h[t.label][tmp] += 1
        for sub in t.subs:
            count(sub, h)
            #tmp.append(tree_to_str(sub))
        #return "(%s %s)" % (t.label, ' '.join(tmp))
    


############################
lines = list(sys.stdin)

h = defaultdict(lambda: defaultdict(lambda: 0))

for i, line in enumerate(lines):
    t = Tree.parse(line.strip(), trunc=False)

    count(t, h)

    #t.pp()
    #print(print_tree(t))
    #print_subs(t)

    #binarize(t)
    #t.pp()
    #print(tree_to_str(t))
    #print_subs(t)
print('TOP')
for k in h:
    s = sum(h[k].values())
    for j in h[k]:
        print('{} -> {} # {:.4f}'.format(k, j, float(h[k][j])/s))
