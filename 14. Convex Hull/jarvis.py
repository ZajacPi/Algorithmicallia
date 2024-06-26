def direction(p1, p2, p3):
   x1, y1 = p1
   x2, y2 = p2
   x3, y3 = p3
   return (y2 - y1)*(x3 - x2) - (y3 - y2)*(x2 - x1)

def jarvis(points):
    #szukam punktu najbardziej na lewo i na dole
    points.sort(key=lambda x: (x[0], x[1]))
    p= points[0]
    conv_hull = [p]    
    q = points[1]

    #pętla się wykonuje dopóki nie wrócę do pierwszego punktu, czyli będzie on środkowym punktem
    while q != conv_hull[0]:

        if points[0] == p:
            q = points[1]
        else: 
            q = points[0]

        for r in points:
            if r == p:
                continue
            angle = direction(p, q, r)
            if angle >0:
                q=r
            elif angle ==0:
                #jeśli odległość p od r jest mniejsza niż p od q, to znaczy że "zawracam", więc nie pasuje
                if (r[0] - p[0])**2 + (r[1] - p[1])**2 > (q[0] - p[0])**2 + (q[1] - p[1])**2:
                    q=r

        conv_hull.append(q)
        p=q

    #na końcu się powtórzy pierwszy punkt, usuwam go
    conv_hull.pop()
    return conv_hull



def test(points):
    conv_hull = jarvis(points)
    print(conv_hull)

def main():
    points_1 = [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)] 
    points_2 = [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)] 
    points_3 = [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)] 

    test(points_1)
    test(points_2)
    test(points_3)

if __name__ == "__main__":
    main()