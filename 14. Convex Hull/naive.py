def orientation(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return (y2 - y1) * (x3 - x2) - (y3 - y2) * (x2 - x1)



def jarvis(points):
    n = len(points)
    #szukam punktu najbardziej na lewo i na dole
    sorted_points = sorted(points, key=lambda x: (x[0], x[1]))
    lefty = points.index(sorted_points[0])
    hull = []
    p = lefty

    while True:
        hull.append(points[p])
        # Ustalam następny punkt q 
        if p + 1 < n:
            q = p + 1
        else:
            q = 0

        for r in range(n):
            #sprawdzam czy lewoskrętn, jak nie to uaktualniam q
            if orientation(points[p], points[r], points[q])<0:
                q = r
        p = q
        #przerywa pętle jak dojdzie do początkowego punktu
        if p == lefty:
            break
    return hull

def test(points):
    conv_hull = jarvis(points)
    print("Convex Hull:", conv_hull)

def main():
    points_1 = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)]
    points_2 = [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)]
    points_3 = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]

    print("Test 1:")
    test(points_1)
    print("\nTest 2:")
    test(points_2)
    print("\nTest 3:")
    test(points_3)

if __name__ == "__main__":
    main()