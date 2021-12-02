import random
import matplotlib.pyplot as plt


# vygeneruje prvych 20 bodov
def generateStartingPoints():
    pa = []
    count = 0
    while count != 20:
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

    while count != 20000:
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
def printGraph(k, clusters_arr, h):
    colors = ["black", "green", "orange", "red", "blue", "magenta", "yellow", "purple", "pink", "gray", "brown",
              "salmon", "chocolate", "lightgreen", "hotpink", "navy", "violet", "gold", "olive", "cyan", " lime",
              "olivedrab"]
    for i in range(k):
        points_x, points_y = createXY_arrays(clusters_arr[i])
        plt.scatter(points_x, points_y, 1, marker="o", facecolors="none", edgecolors=colors[i])
        #plt.scatter(points_x, points_y, 1)
    #plt.savefig("obr/" + str(h) + ".png")
    plt.show()


def k_mean(k, other_points):
    points_x, points_y = createXY_arrays(other_points)
    plt.scatter(points_x, points_y, 1, color='black', marker="o", facecolors="none", edgecolors="black")
    plt.savefig("0.png")

    plt.show()

    clusters = []
    centroids = generateStartingPoints()

    for i in centroids:  # prida centroidy do klusterov
        new = [i]
        clusters.append(new)

    # first iteration
    clusters = assign_clusters(other_points, centroids, clusters)

    for i in clusters:  # vymaze centroidy z clusterov
        del i[0]

    printGraph(k, clusters, 0)

    # other iterations
    clusters_old = []
    h = 1
    while True:
        centroids.clear()

        for i in range(k):
            c = 0
            average_x = 0
            average_y = 0
            if clusters[i]:
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
        for i in clusters:  # vymaze centroidy z clusterov
            del i[0]

        if clusters_old == clusters:
            break

        clusters_old.clear()
        for i in clusters:
            clusters_old.append(i)
        h += 1
    printGraph(k, clusters, h)

    # return clusters


def main():
    other_points = []

    points_array = generateStartingPoints()
    generateOtherPoints(points_array, other_points)
    # matrix_of_distances = create_matrix_of_distances(other_points)

    k = 20
    # clusters_arr = k_mean(k, other_points)

    k_mean(k, other_points)


if __name__ == '__main__':
    main()