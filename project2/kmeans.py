from math import pow, sqrt
from operator import add


# get points from the text file
def get_points(fname):
    points = []
    true_values = set()
    point_length = None
    with open(fname) as f:
        for line in f:
            spl = line.split('\t')
            spl[-1] = spl[-1].replace("\r\n", "")
            point = map(float, spl[2:])
            points.append((int(spl[0]), point))
            # points.append(spl)
            if point_length is None:
                point_length = len(point)
            true_values.add(int(spl[1]))
    return points, true_values, point_length

def get_euclidean_distance(p1, p2):
    sum = 0
    for i in range(len(p1)):
        sum += pow(p1[i] - p2[i], 2)
    return sqrt(sum)


# returns the distance from all centroids in list
def get_distance_from_centroid(point, centroids):
    # print point
    dist = []
    for c in centroids:
        dist.append(get_euclidean_distance(point[1], c))
    return dist

def get_centroid_for_cluster(clusters, point_length):
    res = []
    for c in clusters:
        print len(c)
        # n = len(c[0][1])
        n = point_length
        new_centroid = [0] * n
        for p in c:
            # print p[1], new_centroid
            new_centroid = map(add, new_centroid, p[1])
        # print new_centroid
        res.append([x/len(c) for x in new_centroid])
    return res


if __name__ == "__main__":
    fname = "data/iyer.txt"
    points, true_values, point_length = get_points(fname)
    # print points[1]
    k = max(true_values)
    centroids = [x[1] for x in points[:k]]
    clusters = []

    # clusters[0] = 10
    # print centroids
    # print points
    count = 0
    while True:
        for i in range(k):
            clusters.append([])
        count += 1
        print count
        for point in points:
            # calculate the distance from centroids
            dist = get_distance_from_centroid(point, centroids)
            cluster_id = dist.index(min(dist))
            clusters[cluster_id].append(point)
        # find the centroid of each cluster
        new_centroid = get_centroid_for_cluster(clusters, point_length)
        print centroids
        print new_centroid
        if centroids == new_centroid:
            break
        centroids = new_centroid
    print clusters




