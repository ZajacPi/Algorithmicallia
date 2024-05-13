class Matrix:
    def __init__(self, matrix_, default = 0):
        if isinstance(matrix_, tuple):
            self.a = matrix_[0]
            self.b = matrix_[1]
            self.matrix = [[default]*self.b]*self.a
            
        else:
            self.matrix = matrix_
            self.a = len(matrix_)
            self.b = len(matrix_[0])

    def size(self):
        return (self.a, self.b)
    
    def __add__(self, other):
        if self.size() != other.size():
            raise ValueError("Wrong matrix dimentions; while adding matrices their sizes should be equal")
        
        # result = []
        # for i in range(self.a):
        #     row = []
        #     for j in range(self.b):
        #         row.append(self.matrix[i][j]+other.matrix[i][j])
        #     result.append(row)
        
        # TO SAMO ZAPISANE LIST COMPREHENTION
        result = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.b)] for i in range(self.a)]
        
        #wynik zwrócony za pomocą nowego obiektu
        return Matrix(result)

    def __mul__(self, other):
        if self.b != other.a:  # liczba kolumn pierwszej macierzy musi być równa liczbie wierszy drugiej macierzy
            raise ValueError("Wrong matrix dimentions; while multiplying matrices number of columns of first matrix should be equal to number of second matrix")
       
        # result = []
        # for i in range(self.b):
        #     row = []
        #     for j in range(other.b):
        #         element = 0
        #         for k in range(self.a):
        #             element += self.matrix[i][k]*other.matrix[k][j]
        #         row.append(element)
        #     result.append(row)
        # result
        # new_body = Matrix(result)
        # return new_body
        
        # LIST COMPREHENTION
        result = [[sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.b)) for j in range(other.b)] for i in range(self.a)]
        return Matrix(result)
    
    #potrzebne do transpozycji
    def __getitem__(self, index):
        a, b = index
        return self.matrix[a][b]
    
    def __setitem__(self, index, val):
        a, b = index
        self.matrix[a][b] = val


    # ładne wypisywanie macierzy
    def __str__(self):
        output = ''
        for i in range(self.a):
            output += '|'
            for j in range(self.b):
                
                if self.matrix[i][j]<0:
                    output += str(self.matrix[i][j]) 
                else:
                    output += ' '
                    output += str(self.matrix[i][j]) 

                if j == self.b-1:
                    output +=' |'
                    output += '\n'
                    continue
                output += ' '
                
        return output


def transpose(M: Matrix):
    # transposed = [[0]*M.a for _ in range(M.b)]
    # for i in range(M.a):
    #     for j in range(M.b):
    #         transposed[j][i] = M[i, j]
    
    # Znowu ulepszone z list comprehention
    transposed = [[M[i, j] for i in range(M.a)] for j in range(M.b)]

    return Matrix(transposed)

m1 = Matrix(
[ [1, 0, 2],
  [-1, 3, 1] ]
)
m2 =Matrix((2,3), 1)

m3 = Matrix([
    [3, 1],
    [2, 1],
    [1, 0]
])
print(transpose(m1))
print(m1 + m2)
print(m1*m3)



# #TEST SIZE() I WYŚWIETLANIE
# m1 = Matrix(
# [ [1, 0, 2],
#   [-1, 3, 1] ]
# )
# print(m1)
# print(m1.size())

# # TEST MNOŻENIA
# m2 = Matrix(
# [ [3, 1],
#   [2, 1],
#   [1, 0]]
# )

# print(m1*m2)

# # TEST DODAWANIA

# m3 = Matrix(
# [ [1, 0, 2],
#   [-1, 3, 1] ]
# )

# print(m1+m3)

# #TEST TRANSPOZYCJI

# print(transpose(m1))

