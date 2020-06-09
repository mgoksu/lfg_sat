
COMMENT_STR = '#'


def read_features(feat_file):
    feats = {}
    rules = {}
    with open(feat_file, 'r') as feat_f:
        for line_raw in feat_f:
            if line_raw[0] == COMMENT_STR:
                continue
            line = line_raw.strip()
            if not line:
                continue

            line_tokens = line.split()

            # feature
            if line_tokens[1] == '=':
                feat_name = line_tokens[0]
                vals = line_tokens[2:]
                if feat_name in feats:
                    raise Exception('Duplicate feature {}'.format(feat_name))
                feats[feat_name] = vals
            # feature grammar
            elif line_tokens[1] == '->':
                lhs = line_tokens[0]
                rhs = line_tokens[2:]
                rules.setdefault(lhs, []).append(rhs)
    return feats, rules
