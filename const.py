
# NN	Common noun
# NNS	Plural common noun
# NNP	Proper noun
# NNPS	Plural proper noun
# PRP$	Possessive pronoun (his, her my)
# PRP	Personal pronoun (I, he, she, him, her)
# WP	Wh- pronoun (what, which, who, whom)
# WP$	Wh- possessive pronoun (whose)
# NN_ALL	All nouns of any type, including proper nouns
NN_LIST = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP$', 'PRP', 'WP', 'WP$', 'NN_ALL']
NN_PL = ['NNS', 'NNPS']

# MD	Modal verb (can, could, may, must)
# VB	Base verb (take)
# VBC     Future tense, conditional
# VBD	Past tense (took)
# VBF     Future tense
# VBG	Gerund, present participle (taking)
# VBN	Past participle (taken)
# VBP	Present tense (take)
# VBZ	Present 3rd person singular (takes)
# VB_ALL	All verbs of any type and tense
VERB_LIST = ['MD', 'VB', 'VBC', 'VBD', 'VBF', 'VBG', 'VBN', 'VBP', 'VBZ', 'VB_ALL']
VERB_PL = ['VBP']

# JJ Adjective
# JJR Comparative adjective
# JJS Superlative adjective
# JJ_ALL All adjectives of any type and variant
# RB Adverb
# RBR Comparative adverb
# RBS Superlative adverb
# WRB Wh - Adverb(how, where, why)
# RB_ALL All adverbs of any type and variant
AD_LIST = ['JJ', 'JJR', 'JJS', 'JJ_ALL', 'RB', 'RBR', 'RBS', 'WRB', 'RB_ALL']

# DT Determiner(a, the, an...)
# PDT Predeterminer(all, both...)
# WDT Wh - determiner(which)
DT_LIST = ['DT', 'PDT', 'WDT']
DT_PL = ['PDT']
DT_SG_WORDS = ['this', 'that']
DT_PL_WORDS = ['these', 'those']

# SYM Symbol
# POS Possessive Marker(', 's)
# LRB Open parenthesis
# RRB Close parenthesis
# , Comma
# -    Hyphen / dash
# :    Colon
# ;    Semi - Colon
# . Terminating punctuation(!, ., ?)
# ``    Open quote
# "	Close quote
# $    Currency symbol
SYM_LIST = ['SYM', 'POS', 'LRB', 'RRB', ',', '-', ':', ';', '.', '``', '"', '$']

# CD Cardinal
# DAT Date / Time
# CC Coordinating conjunction
# EX Existential there
# FW Foreign word
# IN Preposition / subordinating conjunction
# RP Particle
# TO To
# UH Interjection
MISC_LIST = ['CD', 'DAT', 'CC', 'EX', 'FW', 'IN', 'RP', 'TO', 'UH']


ALL = NN_LIST + VERB_LIST + AD_LIST + DT_LIST + SYM_LIST + MISC_LIST
PL = NN_PL + VERB_PL + DT_PL

