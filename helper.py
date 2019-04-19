import numpy as np
import pandas as pd

def my_gini(panda, col):
    grouping = panda.groupby(col)[col]
    prob_array = grouping.count()/panda[col].count()
    p = 0
    names = []
    for name,_ in grouping:
        names.append(name)
    for i in range(len(prob_array)):
        p+=np.square(prob_array[names[i]])
    return 1 - p

def weighted_gini(parent, child, col):
    weight = child[col].count()/parent[col].count()
    return weight*my_gini(child, col)

def gini_off_col(parent, offcol, col):
    gini_sum = 0
    names = []
    dataFrames = []
    grouping = parent.groupby(offcol)[offcol]
    for name,_ in grouping:
        dataFrames.append(parent[parent[offcol] == name])
    for df in dataFrames:
        gini_sum += weighted_gini(parent, df, col)
    return gini_sum

def my_entropy(panda, col):
    p = 0
    names = []
    grouping = panda.groupby(col)[col]
    pb = grouping.count()/panda[col].count()
    for name, _ in grouping:
        names.append(name)
    for i in range(len(names)):
        p+= pb[names[i]]*np.log2(pb[names[i]])
    return -p

def information_gain(panda, right, left, col):
    child_ent = (right[col].count()/panda[col].count())*my_entropy(right, col) + (left[col].count()/panda[col].count())*my_entropy(left, col)
    return my_entropy(panda, col) - child_ent

def my_misclass(panda, col):
    p = 0
    names = []
    grouping = panda.groupby(col)[col]
    prob_array = grouping.count()/panda[col].count()
    return 1 - max(prob_array)

def weighted_misclass(parent, child, col):
    weight = child[col].count()/parent[col].count()
    return weight*my_misclass(child, col)

def frequent_set(can,trans, i):
    freq = []
    for c in candidate[i]:
        sum_c = 0
        for t in trans:
            if c.issubset(t['items']):
                sum_c = sum_c +1
        sup = sum_c/len(transactions)
        #print(c, sup)
        if sup >= minsup:
            freq.append((c,sup))
    return freq

def candidate_gen(f, index):
    can = []
    if index == 0:
        for i in range(len(frequent[index])):
            for j in range(i+1, len(frequent[index])):
                (c1, _) = frequent[index][i]
                (c2, _) = frequent[index][j]
                can.append(c1.union(c2))
    else: 
        for i in range(len(frequent[index])):
            for j in range(i+1, len(frequent[index])):
                (c1, _) = frequent[index][i]
                (c2, _) = frequent[index][j]
                #print(c1, c2)
                if len(c1.difference(c2)) == 1:
                    if c1.union(c2) not in can:
                        can.append(c1.union(c2))
    return can

def list_to_set(lst):
    my_set = set()
    for i in lst:
        my_set.add(i)
    return my_set
