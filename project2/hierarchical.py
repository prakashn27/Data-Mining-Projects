from sys import float_info
from optparse import OptionParser
from math import sqrt, pow


# get points from the text file
def get_points(fname):
    expr_value = {}
    with open(fname) as f:
        for line in f:
            spl = line.split()
            spl[-1] = spl[-1].replace("\r\n", "")
            gene_id = int(spl[0])
            expressions = map(float, spl[2:])
            expr_value[gene_id] = expressions
    return expr_value


def get_options():
    par = OptionParser()
    par.add_option('-f', '--file', dest='input', help='filename containing clustering data', default="data/test.txt")
    par.add_option('-c', '--cluster-number', dest='no_of_clusters', help='expansion factor', default=1, type='int')
    (options, args) = par.parse_args()
    return options


def get_euclidean_distance(centroid, point):
    # print centroid, point
    sum_of_squares = 0
    for i in range(len(centroid)):
        sum_of_squares += pow(centroid[i] - point[i], 2)
    return sqrt(sum_of_squares)


def update(dm, c1, c2, expr_value, merge_list):
    if c1 < c2:
        for i in range(1, len(expr_value) + 1):
            if dm[c1][i] > dm[c2][i]:
                if c1 != i:
                    dm[c1][i]=dm[c2][i]
                    dm[i][c1]= dm[c2][i]
            dm[c2][i] = dm[i][c2] = float_info.max
        temp2 = merge_list[c2]
        temp1 = merge_list[c1]
        if len(temp1) == 0:
            temp1.append(c1)
        if len(temp2) == 0:
            temp2.append(c2)
        print merge_list.get(c1), "<-----", merge_list.get(c2)
        merge_list[c1] = temp1 + temp2
        del merge_list[c2]
    elif c2 < c1:
        for i in range(1, len(expr_value) + 1):
            if dm[c2][i] > dm[c1][i]:
                if c2 != i:
                    dm[c2][i]=dm[c1][i]
                    dm[i][c2]= dm[c1][i]
            dm[c1][i] = dm[i][c1] = float_info.max
        temp2 = merge_list[c2]
        temp1 = merge_list[c1]
        if len(temp1) == 0:
            temp1.append(c1)
        if len(temp2) == 0:
            temp2.append(c2)
        print merge_list.get(c2), "<---$$$--", merge_list.get(c1)
        merge_list[c2] = temp2 + temp1
        del merge_list[c1]


def run():
    options = get_options()
    expr_value = get_points(options.input)
    no_of_clusters = options.no_of_clusters
    l = len(expr_value)
    distance_matrix = [[0 for col in range(l + 2)] for row in range(l + 2)]
    # print expr_value[517]
    for i in range(1, l + 1):
        for j in range(1, l + 1):
            list1 = expr_value[i]
            list2 = expr_value[j]
            if i == j:
                distance_matrix[i][j] = float_info.max
            else:
                distance_matrix[i][j] = get_euclidean_distance(list1, list2)
    # print distance_matrix[3]

    merge_list = {}
    for i in range(len(expr_value)):
        merge_list[i + 1] = list()
    count = 1
    while len(merge_list) > no_of_clusters:
        min = float_info.max
        cluster1 = 0
        cluster2 = 0
        for i in range(1, l + 1):
            for j in range(i + 1, l + 1):
                if distance_matrix[i][j] < min:
                    min = distance_matrix[i][j]
                    cluster1 = i
                    cluster2 = j
        # print cluster1, cluster2

        # update(distanceMatrix,cluster1,cluster2,exprValue, mergeList);
        print count
        count += 1
        update(distance_matrix, cluster1, cluster2, expr_value, merge_list)
        # temp1 = []
        # temp2 = []
        # if cluster1 < cluster2:
        #     for i in range(1, l + 1):
        #         if distance_matrix[cluster1][i] > distance_matrix[cluster2][i]:
        #             if cluster1 != i:
        #                 distance_matrix[cluster1][i] = distance_matrix[cluster2][i]
        #                 distance_matrix[i][cluster1] = distance_matrix[cluster2][i]
        #             distance_matrix[cluster2][i] = float_info.max
        #             distance_matrix[i][cluster2] = float_info.max
        #
        #     temp1 = merge_list[cluster1]
        #     temp2 = merge_list[cluster2]
        #     # print temp1, temp2, cluster1, cluster2
        #     if temp2 is None:
        #         print merge_list
        #     if temp1 == []:
        #         temp1.append(cluster1)
        #     if temp2 == []:
        #         temp2 = []
        #         temp2.append(cluster2)
        #     print temp1, "<--", temp2
        #     temp1 = temp1 + temp2
        #     merge_list[cluster1] = temp1
        #     del merge_list[cluster2]
        # elif cluster2 < cluster1:
        #     for i in range(1, l + 1):
        #         if distance_matrix[cluster1][i] > distance_matrix[cluster2][i]:
        #             if cluster1 != i:
        #                 distance_matrix[cluster2][i] = distance_matrix[cluster1][i]
        #                 distance_matrix[i][cluster2] = distance_matrix[cluster1][i]
        #             distance_matrix[cluster1][i] = float_info.max
        #             distance_matrix[i][cluster1] = float_info.max
        #     temp1 = merge_list.get(cluster1)
        #     temp2 = merge_list.get(cluster2)
        #     if temp1 == []:
        #         temp1.append(cluster1)
        #     if temp2 == []:
        #         temp2.append(cluster2)
        #     print temp2, "<--", temp1
        #     temp2 = temp1 + temp2
        #     merge_list[cluster2] = temp2
        #     del merge_list[cluster1]
        # break
    for i in merge_list:
        print i, ":", merge_list[i]
    # print merge_list
    print len(merge_list[1])
    print "done"


if __name__ == "__main__":
    run()
