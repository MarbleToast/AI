#%%

import math
import pandas
import collections
import os

fp = os.path.join(os.path.dirname(os.path.realpath(__file__)), "weekend.txt")

def get_decision_entropy(decision):
    data_freq = dict(collections.Counter(decision))
    entropy = 0
    for d in data_freq:
        prob = data_freq[d]/len(decision)
        if prob > 0:
            entropy += prob * math.log2(prob)
    return -entropy


def get_2d_entropy(data: pandas.DataFrame, attribute):
    attr_values = set(data.get(attribute))
    for val in attr_values:
        rows = data.loc[data[0] == val]



def get_remainder(data: pandas.DataFrame):
    data_freq = dict(collections.Counter(data))
    remainders = []
    for d in data_freq:
        remainders.append((data_freq[d]/len(data)) * get_decision_entropy(data))
    print(remainders)
    return remainders


def get_info_gain(data: pandas.DataFrame, col: int):
    decision = data.get(data.columns[-1])
    print("Final column:", decision, sep="\n")
    decision_entropy = get_decision_entropy(decision)
    print("Decision entropy:", decision_entropy)
    
    return decision_entropy - get_remainder(data.get(col))


weekend_data = pandas.read_csv(fp, header=None)[:-3]
print(get_2d_entropy(weekend_data, 0))

