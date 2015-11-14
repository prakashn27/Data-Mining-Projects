from sys import float_info
from optparse import OptionParser
from math import sqrt, pow
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
import validation as v


# get points from the text file
def get_points(fname):
    expr_value = {}
    map_of_clusters = {}
    with open(fname) as f:
        for line in f:
            spl = line.split()
            spl[-1] = spl[-1].replace("\r\n", "")
            gene_id = int(spl[0])
            cluster = int(spl[1])
            if cluster in map_of_clusters:
                map_of_clusters[cluster].append(gene_id)
            else:
                map_of_clusters[cluster] = [gene_id]
            expressions = map(float, spl[2:])
            expr_value[gene_id] = expressions
    return expr_value, map_of_clusters


def get_options():
    par = OptionParser()
    par.add_option('-f', '--file', dest='input', help='filename containing clustering data', default="data/cho.txt")
    par.add_option('-c', '--cluster-number', dest='no_of_clusters', help='expansion factor', default=5, type='int')
    (options, args) = par.parse_args()
    return options


def get_euclidean_distance(centroid, point):
    # print centroid, point
    sum_of_squares = 0
    for i in range(len(centroid)):
        sum_of_squares += pow(centroid[i] - point[i], 2)
    return sqrt(sum_of_squares)


def update(dm, c1, c2, expr_value, merge_list, dendrogram_list):
    # if c1 < c2:
    for i in range(1, len(expr_value) + 1):
        if dm[c1][i] > dm[c2][i]:
            if c1 != i:
                dm[c1][i] = dm[c2][i]
                dm[i][c1] = dm[c2][i]
        dm[c2][i] = dm[i][c2] = float_info.max
    temp2 = merge_list[c2]
    temp1 = merge_list[c1]
    var1 = None
    var2 = None
    obtained_length = None
    if len(temp1) == 0:
        temp1.append(c1)
        var1 = c1
    if len(temp2) == 0:
        temp2.append(c2)
        var2 = c2
    print merge_list.get(c1), "<-----", merge_list.get(c2)
    merge_list[c1] = temp1 + temp2
    obtained_length = len(temp1 + temp2)
    dendrogram_list.append(temp1 + temp2)
    if var1 is None:
        var1 = merge_list.get(c1)
    if var2 is None:
        var2 = merge_list.get(c2)
    del merge_list[c2]
    # print var1, var2, obtained_length, c1, c2, dendrogram_list
    return dendrogram_list.index(var1), dendrogram_list.index(var2), obtained_length
    # elif c2 < c1:
    #     for i in range(1, len(expr_value) + 1):
    #         if dm[c2][i] > dm[c1][i]:
    #             if c2 != i:
    #                 dm[c2][i]=dm[c1][i]
    #                 dm[i][c2]= dm[c1][i]
    #         dm[c1][i] = dm[i][c1] = float_info.max
    #     temp2 = merge_list[c2]
    #     temp1 = merge_list[c1]
    #     if len(temp1) == 0:
    #         temp1.append(c1)
    #     if len(temp2) == 0:
    #         temp2.append(c2)
    #     print merge_list.get(c2), "<---$$$--", merge_list.get(c1)
    #     merge_list[c2] = temp2 + temp1
    #     dendrogram_list.append(temp2 + temp1)
    #     del merge_list[c1]

def generate_dendrogram(Z):
    np.set_printoptions(precision=5, suppress=True)
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    result = np.array(Z)
    dendrogram(
        result,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,
    )
    plt.show()


def generate_graph():
    np.set_printoptions(precision=5, suppress=True)
    np.random.seed(4711)  # for repeatability of this tutorial
    a = np.random.multivariate_normal([10, 0], [[3, 1], [1, 4]], size=[100,])
    b = np.random.multivariate_normal([0, 20], [[3, 1], [1, 4]], size=[50,])
    X = np.concatenate((a, b),)
    # X = np.concatenate()
    print X
    print "shape of X is"
    print X.shape  # 150 samples with 2 dimensions
    plt.scatter(X[:,0], X[:,1])
    #plt.show()
    Z = linkage(X, 'single')
    print "Z value is"
    print type(Z)
    print type(Z[0])
    print Z
    # idxs = [33, 68, 62]
    # plt.figure(figsize=(10, 8))
    # plt.scatter(X[:,0], X[:,1])  # plot all points
    # plt.scatter(X[idxs,0], X[idxs,1], c='r')  # plot interesting points in red again
    # plt.show()
    # idxs = [15, 69, 41]
    # plt.scatter(X[idxs,0], X[idxs,1], c='y')
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    plt.show()

def run():
    options = get_options()
    expr_value, map_of_true_clusters = get_points(options.input)
    no_of_clusters = options.no_of_clusters
    l = len(expr_value)
    distance_matrix = [[0 for col in range(l + 2)] for row in range(l + 2)]
    dendogram_list = []
    dendogram_matrix = []
    # dendogram_list.append(None)
    for i in range(1, l + 1):
        dendogram_list.append(i)
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
        min_value = float_info.max
        cluster1 = 0
        cluster2 = 0
        for i in range(1, l + 1):
            for j in range(i + 1, l + 1):
                if distance_matrix[i][j] < min_value:
                    min_value = distance_matrix[i][j]
                    cluster1 = i
                    cluster2 = j
        # print count
        count += 1
        var1, var2, obtained_length = update(distance_matrix, cluster1, cluster2, expr_value, merge_list, dendogram_list)
        temp_list = [var1, var2, min_value, obtained_length]
        dendogram_matrix.append(temp_list)
    r = []
    for i in merge_list:
        # print i, ":", merge_list[i]
        r.append([np.array(merge_list[i])])
    # print merge_list
    print "done"
    # print map_of_true_clusters
    # print r
    # generate_graph(r)
    # print len(dendogram_list), count
    # print dendogram_list
    # print dendogram_matrix
    # generate_dendrogram(dendogram_matrix)
    output = []
    for entry in merge_list:
        output.append(merge_list[entry])

    # Validation
    # ====================================
    our_truth = [[0 for row in range(len(expr_value) + 1)] for col in range(len(expr_value) + 1)]
    for a in output:
        for i in range(len(a)):
            for j in range(len(a)):
                # print i, j, a
                our_truth[a[i]][a[j]] = 1
    # print "our truth"
    # print our_truth

    ground_truth = [[0 for row in range(len(expr_value) + 1)] for col in range(len(expr_value) + 1)]
    for entry in map_of_true_clusters:
        temp = map_of_true_clusters[entry]
        for i in range(len(temp)):
            for j in range(len(temp)):
                ground_truth[temp[i]][temp[j]] = 1
    # print ground_truth

    # construct the distance matrix
    distance_matrix = [[0.0 for row in range(len(expr_value) + 1)] for col in range(len(expr_value) + 1)]
    for i in range(1, len(expr_value) + 1):
        for j in range(1, len(expr_value) + 1):
            if i != j:
                list1 = expr_value[i]
                list2 = expr_value[j]
                distance_matrix[i][j] = v.find_distance(list1, list2)
            else:
                distance_matrix[i][j] = 0.0
    jac = v.get_jaccard(ground_truth, our_truth)
    cor = v.get_corrlation(distance_matrix, our_truth)

    print "Jaccard Coefficient is ", jac
    print "Correlation is ", cor


if __name__ == "__main__":
    # generate_graph()
    run()
