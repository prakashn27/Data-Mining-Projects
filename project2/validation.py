from __future__ import division
import math


def get_corrlation(distance_matrix, our_truth):
    num = 0.0
    meanD = meanO = 0.0
    for i in range(1, len(distance_matrix)):
        for j in range(1, len(distance_matrix[0])):
            meanD += distance_matrix[i][j]
    meanD = meanD / math.pow(len(distance_matrix), 2)

    for i in range(1, len(our_truth)):
        for j in range(1, len(our_truth[0])):
            meanO += our_truth[i][j]
    meanO = meanO / math.pow(len(our_truth), 2)

    den1 = 0.0
    den2 = 0.0
    for i in range(1, len(our_truth)):
        for j in range(1, len(our_truth[0])):
            num += (distance_matrix[i][j] - meanD) * (our_truth[i][j] - meanO)
            den1 += math.pow((distance_matrix[i][j] - meanD), 2)
            den2 += math.pow((our_truth[i][j] - meanD), 2)

    return float(num)/math.sqrt(den1 * den2)


def get_jaccard(ground_truth, our_truth):
    same = 0
    diff = 0
    for i in range(1, len(ground_truth)):
        for j in range(1, len(ground_truth[0])):
            if ground_truth[i][j] != our_truth[i][j]:
                diff += 1
            elif ground_truth[i][j] == 1 and our_truth[i][j] == 1:
                same += 1
    return same / (same + diff)


def get_rand(ground_truth, our_truth):
    same_1 = 0
    same_0 = 0
    diff = 0
    for i in range(1, len(ground_truth)):
        for j in range(1, len(ground_truth[0])):
            if ground_truth[i][j] != our_truth[i][j]:
                diff += 1
            elif ground_truth[i][j] == 1 and our_truth[i][j] == 1:
                same_1 += 1
            elif ground_truth[i][j] == 0 and our_truth[i][j] == 0:
                same_0 += 1

    return (same_0 + same_1) / (same_0 + same_1 + diff)


def find_distance(l1, l2):
    sum_sqrs = 0
    for i in range(len(l1)):
        sum_sqrs += math.pow(l1[i] - l2[i],2)
    return math.sqrt(sum_sqrs)
