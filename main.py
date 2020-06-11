
from pysmt.shortcuts import Symbol, And, GE, LT, Plus, Equals, Int, get_model
from pysmt.typing import INT

from const import PL, DT_SG_WORDS, DT_PL_WORDS
from tree import Tree
from read_config import read_features
from kbest_cky import Parser
from old_cky import get_cky


CONF = 'feature_grammar.fcfg'

ex_sent = '(TOP (S (NP (DT these) (NNS flights)) (VP (VBP are) (ADJP (JJ next)))))'


def tree_to_str(t):
    if t.is_terminal():
        return "(%s %s)" % (t.label, t.word)
    else:
        tmp=[]
        for sub in t.subs:
            tmp.append(tree_to_str(sub))
        return "(%s %s)" % (t.label, ' '.join(tmp))


def get_label(node_str):
    if '[' in node_str:
        return node_str[:node_str.index('[')]
    else:
        return node_str


def get_feat(node_str):
    if '[' in node_str:
        feat = node_str[node_str.index('=')+1:node_str.index(']')]
        return feat
    return '?'


def get_sat_constraints(t, feats, rules, symbs, constraints):
    tree_id = str(id(t))
    t_lab = t.label
    node_id = tree_id + '_' + t_lab + '_NUM'
    symbs[node_id] = Symbol(node_id, INT)
    constraints.append(And(GE(symbs[node_id], Int(1)), LT(symbs[node_id], Int(3))))

    if t.is_terminal():
        if t_lab in PL:
            constraints.append(Equals(symbs[node_id], Int(2)))
        if t_lab == 'DT':
            if t.word in DT_SG_WORDS:
                constraints.append(Equals(symbs[node_id], Int(1)))
            elif t.word in DT_PL_WORDS:
                constraints.append(Equals(symbs[node_id], Int(2)))
    else:
        for sub in t.subs:
            get_sat_constraints(sub, feats, rules, symbs, constraints)

        for lhs, rhs_list in rules.items():
            lhs_label = get_label(lhs)
            if lhs_label != t_lab:
                continue
            else:
                for rhs in rhs_list:
                    if len(t.subs) != len(rhs) or \
                            [sub.label for sub in t.subs] != [get_label(rhs_node) for rhs_node in rhs]:
                        continue
                    else:
                        feat = get_feat(lhs)
                        if feat != '?':
                            constraints.append(Equals(symbs[node_id], Int(int(feat))))
                        for i, rhs_node in enumerate(rhs):
                            sub_node_id = str(id(t.subs[i])) + '_' + t.subs[i].label + '_NUM'
                            sub_feat = get_feat(rhs_node)
                            if sub_feat == '?':
                                constraints.append(Equals(symbs[node_id], symbs[sub_node_id]))
                            else:
                                constraints.append(Equals(symbs[sub_node_id], Int(int(sub_feat))))

    return symbs, constraints


def check_in_language(tree_str, conf_file):
    cfg_f, cfg_r = read_features(conf_file)
    sent_t = Tree.parse(tree_str.strip(), trunc=False)
    symbols, all_constraints = get_sat_constraints(sent_t, cfg_f, cfg_r, {}, [])
    problem = And(all_constraints)
    model = get_model(problem)
    if model:
        return tree_to_str(sent_t)
    else:
        return None


with open('test_small.txt', 'r') as f:
    parser = Parser()
    kbest = 4
    for sent_raw in f.readlines():
        sentence_origin = sent_raw.strip().split()
        result = parser.parse(sentence_origin, kbest)
        in_language_flag = False
        for cky_res in result:
            res = check_in_language(cky_res[1], CONF)
            if res is None:
                continue
            else:
                print(res)
                in_language_flag = True
                break
        if not in_language_flag:
            print('Not in the language : ' + sent_raw.strip())
