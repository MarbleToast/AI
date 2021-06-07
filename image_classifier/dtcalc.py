#%%
import os
import pandas as pd
import numpy as np
from fractions import Fraction

def get_entropy(feature, show_calc=False):
    formula_string = "Entropy is "
    probs = feature.value_counts(normalize=True)
    for p in probs:
        formula_string += (
            "-("+str(Fraction(p).limit_denominator())+
            ")log2("+str(Fraction(p).limit_denominator())+")"
        )

    impurity = -1 * np.sum(np.log2(probs) * probs)

    if show_calc:
        print(probs, sep="") 
        print(formula_string)
    return impurity


def get_info_gain(df, target, descriptive_feature):
    
    print('Descriptive feature:', descriptive_feature)
            
    target_entropy = get_entropy(df[target])

    entropy_list = list()
    weight_list = list()
    
    for level in df[descriptive_feature].unique():
        df_feature_level = df[df[descriptive_feature] == level]
        print("\nIf "+level+"...")
        entropy_level = get_entropy(df_feature_level[target], True)
        entropy_list.append(round(entropy_level, 3))
        weight_level = len(df_feature_level) / len(df)
        weight_list.append(round(weight_level, 3))

    print('\nimpurity of partitions:', entropy_list)
    print('weights of partitions:', [str(Fraction(w).limit_denominator()) for w in weight_list])

    remainder = np.sum(np.array(entropy_list) * np.array(weight_list))
    print('remaining impurity:', remainder)
    
    information_gain = target_entropy - remainder
    print('information gain:', information_gain)
    
    print('====================')

    return information_gain


fp = os.path.join(os.path.dirname(os.path.realpath(__file__)), "weekend.txt")
weekend_data = pd.read_csv(fp)

target_entropy = get_entropy(weekend_data["Outcome"])
print('target entropy:', target_entropy)
print("====================")

best_split = ("", -99999)
for feature in weekend_data.drop(columns="Outcome").columns:
    feature_info_gain = get_info_gain(weekend_data, "Outcome", feature)
    if feature_info_gain > best_split[1]: best_split = (feature, feature_info_gain)

print("Best split (info gain) =", best_split)