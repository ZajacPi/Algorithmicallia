import matplotlib.pyplot as plt
from jarvis import jarvis

def convex_Hull_plotting(points):
    plt.figure()
    for point in points:
        plt.plot(point[0], point[1], 'bo')
    out_points = jarvis(points)
    out_points.append(out_points[0])
    prev= out_points[0]
    for point in out_points:
        plt.plot(point[0], point[1], 'ro')
        plt.plot((prev[0], point[0]), (prev[1], point[1]), 'b-')
        prev = point
    plt.show()

def main():
    points_1 = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)] 
    points_3 = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)] 

    convex_Hull_plotting(points_3)

if __name__ == "__main__":
    main()