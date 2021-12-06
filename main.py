import random
import matplotlib.pyplot as plt
import time


# vygeneruje prvych 20 bodov
def generateStartingPoints(k):
    pa = []
    count = 0
    while count != k:
        new = []
        x = random.randrange(-5000, 5001)
        y = random.randrange(-5000, 5001)
        new.append(x)
        new.append(y)
        if new not in pa:  # osetrenie aby tam neboli duplikaty
            pa.append(new)
            count += 1
    return pa


# vygeneruje zvyšne body
def generateOtherPoints(pa, op):
    count = 0

    while count != 1000:
        rand_num = random.randrange(0, len(pa))
        random_point = pa[rand_num]
        point = []
        for i in random_point:
            point.append(i)

        x_offset = int(random.gauss(point[0], 200))
        y_offset = int(random.gauss(point[1], 200))
        point[0] = x_offset
        point[1] = y_offset

        if point not in op and -5000 < point[0] < 5000 and -5000 < point[1] < 5000:
            op.append(point)
            count += 1


def createXY_arrays(pa):
    points_x = []
    points_y = []
    for i in pa:
        points_x.append(i[0])
        points_y.append(i[1])
    return points_x, points_y


# priradí k centroidam najlbizsie body
def assign_clusters(other_points, centroids, clusters):
    for i in other_points:
        index = 0
        best_dist = 82548254
        best_centroid = []
        for j in centroids:
            distance = ((j[0] - i[0]) ** 2 + (j[1] - i[1]) ** 2) ** 0.5
            if distance < best_dist:
                best_dist = distance
                best_centroid = j

        for y in range(len(clusters)):
            if clusters[y][0] == best_centroid:
                index = y
                break
        clusters[index].append(i)

        # index = centroids.index(best_centroid)
        # clusters[index].append(i)

    return clusters


# vykresli body
def printGraph(k, clusters_arr, title, h):
    colors = ["black", "green", "orange", "red", "blue", "magenta", "yellow", "purple", "pink", "gray", "brown",
              "salmon", "chocolate", "lightgreen", "hotpink", "navy", "violet", "gold", "olive", "cyan", " lime",
              "olivedrab"]
    for i in range(k):
        points_x, points_y = createXY_arrays(clusters_arr[i])
        plt.scatter(points_x, points_y, 1, marker="o", facecolors="none", edgecolors=colors[i])
        # plt.scatter(points_x, points_y, 1)
    #plt.savefig("obr/" + str(h) + ".png")
    plt.suptitle(title)
    plt.show()


def k_mean(k, other_points):
    clusters = []
    centroids = generateStartingPoints(k)
    for i in centroids:  # prida centroidy do klusterov
        new = [i]
        clusters.append(new)

    # first iteration
    clusters = assign_clusters(other_points, centroids, clusters)

    """
    for i in clusters:  # vymaze centroidy z clusterov
        del i[0]
    """
    #printGraph(k, clusters, 0, "Centroid - 0 iterations")

    # other iterations
    clusters_old = []
    h = 1
    while True:
        centroids.clear()

        for i in range(k):
            c = 0
            average_x = 0
            average_y = 0
            if len(clusters[i]) > 1:
                while c != len(clusters[i]):
                    average_x += clusters[i][c][0]
                    average_y += clusters[i][c][1]
                    c += 1
                average_x = average_x / c
                average_y = average_y / c
                new_centroid = [int(average_x), int(average_y)]
                centroids.append(new_centroid)
            else:
                new_centroid = [random.randrange(-5000, 5001), random.randrange(-5000, 5001)]
                centroids.append(new_centroid)

        clusters.clear()
        for i in centroids:
            new = [i]
            clusters.append(new)

        clusters = assign_clusters(other_points, centroids, clusters)
        """
        for i in clusters:  # vymaze centroidy z clusterov
            del i[0]
        """
        if clusters_old == clusters:
            break

        clusters_old.clear()
        for i in clusters:
            clusters_old.append(i)
        h += 1

    return clusters


def k_mean_medoid(k, other_points):
    clusters = []
    medoids = generateStartingPoints(k)

    for i in medoids:  # prida medoidy do klusterov
        new = [i]
        clusters.append(new)

    # first iteration
    clusters = assign_clusters(other_points, medoids, clusters)

    #printGraph(k, clusters, 0, "Medoid - 0 iterations")

    # other iterations
    clusters_old = []
    h = 1
    while True:
        medoids.clear()

        for i in clusters:
            medoid = None
            smallest_dist = 82548254
            for q in i:
                distance = 0
                for p in i:
                    if distance > smallest_dist:
                        break
                    distance += ((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2) ** 0.5
                if distance < smallest_dist:
                    smallest_dist = distance
                    medoid = q
            medoids.append(medoid)

        clusters.clear()
        for i in medoids:
            new = [i]
            clusters.append(new)

        clusters = assign_clusters(other_points, medoids, clusters)

        if clusters_old == clusters:
            break

        clusters_old.clear()
        for i in clusters:
            clusters_old.append(i)
        h += 1
    return clusters


def divisive(k, other_points):
    clusters = []
    centroids = []
    clusters = k_mean(2, other_points)
    h = 0
    #printGraph(len(clusters), clusters, "Divisive", h)
    for i in clusters:
        centroids.append(i[0])
    h += 1
    while k != len(clusters):
        biggest_cluster = None
        biggest = 0
        for i in clusters:
            if len(i) > 1:
                centroid = i[0]
                distance = 0
                for q in i:
                    distance += ((q[0] - centroid[0]) ** 2 + (q[1] - centroid[1]) ** 2) ** 0.5
                average = distance / len(i)
                if average > biggest:
                    biggest = average
                    biggest_cluster = i
        clusters.remove(biggest_cluster)
        in_cluster = k_mean(2, biggest_cluster)
        clusters.append(in_cluster[0])
        clusters.append(in_cluster[1])
        #printGraph(len(clusters), clusters, "Divisive", h)
        h += 1
    for i in clusters:
        del i[0]
    return clusters


def aglo(k, other_points):
    clusters = []

    for i in other_points:
        new = [i]
        clusters.append(new)

    centroids = []
    while k != len(clusters):
        centroids.clear()
        # do clustrov prida na začiatok centroidy
        hh = 5
        for i in clusters:
            if len(i) == 1:
                centroids.append(i[0])
            elif len(i) == 0:
                new_centroid = [random.randrange(-5000, 5001), random.randrange(-5000, 5001)]
                centroids.append(new_centroid)
            else:
                average_x = 0
                average_y = 0
                for q in i:
                    average_x += q[0]
                    average_y += q[1]
                average_x = average_x / len(i)
                average_y = average_y / len(i)
                centroid = [int(average_x), int(average_y)]
                centroids.append(centroid)
                i.insert(0, centroid)

        # zisti 2 najblizsie centroidy
        smallest_dist = 82548254
        q = 0
        p = 0
        centroid1 = []
        centroid2 = []
        for i in range(len(clusters)):
            for y in range(len(clusters)):
                distance = ((clusters[i][0][0] - clusters[y][0][0]) ** 2 + (clusters[i][0][1] - clusters[y][0][1]) ** 2) ** 0.5
                if distance != 0 and distance < smallest_dist:
                    smallest_dist = distance
                    centroid1 = clusters[i][0]
                    centroid2 = clusters[y][0]
                    q = i
                    p = y

        # podla centroid spoji clustre
        stop = False
        for i in clusters:
            for y in clusters:
                if i[0] == centroid1 and y[0] == centroid2:
                    new = []
                    new_can_x = centroid1[0] + centroid2[0]
                    new_can_y = centroid1[1] + centroid2[1]
                    new_cen = [int(new_can_x)/2, int(new_can_y)/2]
                    new.append(new_cen)
                    if len(i) != 1:
                        del i[0]
                    for j in i:
                        new.append(j)
                    if len(y) != 1:
                        del y[0]
                    for j in y:
                        new.append(j)
                    clusters.remove(i)
                    clusters.remove(y)
                    clusters.append(new)
                    stop = True
                    break
            if stop:
                break

    return clusters


def main():
    other_points = []

    points_array = generateStartingPoints(20)
    generateOtherPoints(points_array, other_points)

    points_x, points_y = createXY_arrays(other_points)
    plt.scatter(points_x, points_y, 1, color='black', marker="o", facecolors="none", edgecolors="black")
    plt.suptitle("Start")
    plt.show()
    # matrix_of_distances = create_matrix_of_distances(other_points)

    k = 20

    # k-mean centroid
    time_start = time.time()
    c1 = k_mean(k, other_points)
    time_end = time.time()
    printGraph(k, c1, "Centroid", 0)
    print("K-means - centroid pri " + str(k) + " zhlukoch zabral " + str(time_end - time_start))

    # k-mean medoid
    time_start = time.time()
    c2 = k_mean_medoid(k, other_points)
    time_end = time.time()
    printGraph(k, c2, "Medoid", 0)
    print("K-means - medoid pri " + str(k) + " zhlukoch zabral " + str(time_end - time_start))

    # divisive
    time_start = time.time()
    c3 = divisive(k, other_points)
    time_end = time.time()
    printGraph(k, c3, "Divisive", 0)
    print("Divízne zhlukovanie pri " + str(k) + " zhlukoch zabral " + str(time_end - time_start))

    # aglomerative
    time_start = time.time()
    c4 = aglo(k, other_points)
    time_end = time.time()
    printGraph(k, c4, "Aglomerative", 0)
    print("Aglomerativne zhlukovanie pri " + str(k) + " zhlukoch zabral " + str(time_end - time_start))


if __name__ == '__main__':
    main()
