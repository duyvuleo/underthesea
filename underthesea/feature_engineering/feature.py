# ===========================
# token syntax
# ===========================
#         _ row 1
#        /  _ row 2
#       /  /  _ column
#      /  /  /
#    T[0,2][0]
#          .is_digit
#            \_ function
#
# ===========================
# sample tagged sentence
# ===========================
# this     A
# is       B
# a        C
# sample   D
# sentence E
#

import re


def text_lower(word):
    return word.lower()


def text_istitle(word):
    if len(word) == 0:
        return False
    try:
        titles = [s[0] for s in word.split(" ")]
        for token in titles:
            if token[0].istitle() is False:
                return False
        return True
    except:
        return False


def apply_function(name, word):
    functions = {
        "lower": text_lower,
        "istitle": text_istitle
    }
    return functions[name](word)


def template2features(sent, i, token_syntax, debug=True):
    """
    :type token: object
    """
    columns = []
    for j in range(len(sent[0])):
        columns.append([t[j] for t in sent])
    matched = re.match(
        "T\[(?P<index1>\-?\d+)(\,(?P<index2>\-?\d+))?\](\[(?P<column>.*)\])?(\.(?P<function>.*))?",
        token_syntax)
    column = matched.group("column")
    column = int(column) if column else 0
    index1 = int(matched.group("index1"))
    index2 = matched.group("index2")
    index2 = int(index2) if index2 else None
    func = matched.group("function")
    if debug:
        prefix = "%s=" % token_syntax
    else:
        prefix = ""
    if i + index1 < 0:
        return ["%sBOS" % prefix]
    if i + index1 >= len(sent):
        return ["%sEOS" % prefix]
    if index2 is not None:
        if i + index2 >= len(sent):
            return ["%sEOS" % prefix]
        word = " ".join(columns[column][i + index1: i + index2 + 1])
    else:
        word = sent[i + index1][column]
    if func is not None:
        result = apply_function(func, word)
    else:
        result = word
    return ["%s%s" % (prefix, result)]


def word2features(sent, i, template):
    features = []
    for token in template:
        features.extend(template2features(sent, i, token))
    return features


def sent2features(sentence, template):
    """ extract features in a sentence

    :type sentence: list of token, each token is a list of tag
    """
    return [word2features(sentence, i, template) for i in range(len(sentence))]


def sent2labels(sentence):
    """ extract labels in a sentence

    :type sentence: list of token, each token is a list of tag
    :return a list contains labels in sentence

    Example:
        sentence = [("Have", "V"), ("a", "D"), ("nice", A"), (day, "N")
    """
    return [label for token, label in sentence]
