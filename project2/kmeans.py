import sys
import math
from optparse import OptionParser


# get points from the text file
def get_points(fname):
    cluster_no = []
    expr_value = {}
    with open(fname) as f:
        for line in f:
            spl = line.split('\t')
            spl[-1] = spl[-1].replace("\r\n", "")
            gene_id = int(spl[0])
            expressions = map(float, spl[2:])
            expr_value[gene_id] = expressions
            cluster_no.append(0)
    # cluster_no.append(0)
    return expr_value, cluster_no


def get_euclidean_distance(centroid, point):
    # print centroid, point
    sum_of_squares = 0
    for i in range(len(centroid)):
        sum_of_squares += math.pow(centroid[i] - point[i], 2)
    return math.sqrt(sum_of_squares)


def get_new_centroids(clusters):
    new_centroids = []
    size = len(clusters[1][1])
    temp = [float(0)] * size
    for i in clusters:
        points_in_cluster = clusters[i]
        # print "points in cluster "
        # print points_in_cluster
        for p in points_in_cluster:
            # print p
            for i in range(len(p)):
                temp[i] += p[i]
        temp_list = []
        for k in range(size):
            temp[k] = temp[k]/len(points_in_cluster)
            temp_list.append(temp[k])
        new_centroids.append(temp_list)
    return  new_centroids


def get_options():
    par = OptionParser()
    par.add_option('-f', '--file', dest='input', help='filename containing clustering data', default="data/iyer.txt")
    par.add_option('-k', '--cluster-number', dest='no_of_clusters', help='expansion factor', default=10, type='int')
    (options, args) = par.parse_args()
    return options


def run():
    # fname = "data/cho.txt"
    options = get_options()

    fname = options.input
    no_of_clusters = options.no_of_clusters
    expr_value, cluster_no = get_points(fname)
    # print expr_value
    # print len(cluster_no)
    # no_of_clusters = 5 #
    # TODO: get the gene_id from the user. for simplicity taking as first k values
    gene_id_array = range(1, no_of_clusters + 1)

    old_centroids = []
    for i in range(no_of_clusters):
        old_centroids.append(expr_value.get(gene_id_array[i]))
    # print old_centroids
    # print len(old_centroids)

    count = 0
    # print len(old_centroids), len(expr_value)
    while True:
        clusters = {}
        cluster_and_gene_id = {}
        # print sys.float_info.max
        for cur_gene in range(1, len(expr_value) + 1): # since gene starts with 1
            min_dist = sys.float_info.max
            nearest_centroid = 0
            for cur_centroid in range(len(old_centroids)):
                # print len(old_centroids[cur_centroid])
                # print expr_value
                dist = get_euclidean_distance(old_centroids[cur_centroid], expr_value[cur_gene])
                if dist < min_dist:
                    min_dist = dist
                    nearest_centroid = cur_centroid
            if nearest_centroid in cluster_and_gene_id:
                t = cluster_and_gene_id[nearest_centroid]
                t.append(cur_gene)
            else:
                t = []
                t.append(cur_gene)
                cluster_and_gene_id[nearest_centroid] = t
            if nearest_centroid in clusters:
                t = clusters[nearest_centroid]
                t.append(expr_value[cur_gene])
            else:
                t = []
                t.append(expr_value[cur_gene])
                clusters[nearest_centroid] = t
        # print clusters
        # print cluster_and_gene_id
        new_centroids = get_new_centroids(clusters)
        # print old_centroids
        # print new_centroids
        got_result = True
        for i in range(len(new_centroids)):
            if new_centroids[i] != old_centroids[i]:
                got_resultflag = False
                break
        if not got_result:
            old_centroids = new_centroids
            count += 1
        else:
            print "How many Iterations is it taking to compute the cluster:", count
            for id in cluster_and_gene_id:
                print id + 1, "th cluster with " , str(len(cluster_and_gene_id[id])), " Points"
            print cluster_and_gene_id
            break
    print "clusters are done"

if __name__ == "__main__":
    run()





