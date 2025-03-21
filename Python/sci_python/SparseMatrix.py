# implementation of sparse matrix

class SparseMatrix:
    def __init__(self, n, m, values:dict):
        self.n , self.m = n, m
        for key in values:
            if key[0] > n or key[1] > m:
                raise ValueError( "Coordinates of element out of dimension")
        self.values = values
        
        
    def __mul__(self, other):
   
        new_matrix = self.values
        if type(other) in {int,float}: 
            for key, value in new_matrix.items():
                new_matrix[key] = other * value
    

        elif type(other) is SparseMatrix:
            if self.m != other.n:
                raise ValueError("Matrices have wrong dimension. Rows of first doesn't equals to Cols of second.")

# If A * B = C and A have n x m dimension and B have m x k dimension - C will have n x k dimesion 
            new_n = self.m
            new_m = other.m
            new_matrix = {}
            for i in range(self.n):
                for j in range(self.m):
                    for k in range(other.m):
                        # Calculate inner product of all rows by all columns
                        if (i, j) in self.values.keys() and (j, k) in other.values.keys():
                            if (i, k) not in new_matrix.keys():
                                 new_matrix[(i, k)] = self.values[(i, j)] * other.values[(j, k)]
                            else:
                                 new_matrix[(i, k)] += self.values[(i, j)] * other.values[(j, k)]

                    
                    
        else:
            raise ValueError("Multiplication is supported only for numbers and matrices")
        
        return SparseMatrix(self.n, other.m,new_matrix) 
                
    def __add__(self, other):
            if type(other) is not SparseMatrix:
                raise TypeError("One of operands is not matrix")
            if self.n != other.n or self.m != other.m:
                raise ValueError("Matrices have to equal dimension")
                
            new_matrix = {i : 0 for i in set(self.values.keys()) | set(other.values.keys())}
            for key in new_matrix.keys():
                    new_matrix[key] = other.values[key] + self.values[key]
            
            return SparseMatrix(self.n, self.m, new_matrix)
            
            
    def __sub__(self,other):
            if type(other) is not SparseMatrix:
                raise TypeError("One of operands is not matrix")
            if self.n != other.n or self.m != other.m:
                raise ValueError("Matrices have to equal dimension")

            new_matrix = {i : 0 for i in set(self.values.keys()) | set(other.values.keys())}
            for key in new_matrix.keys():
                    new_matrix[key] = self.values[key] - other.values[key]

            return SparseMatrix(self.n, self.m, new_matrix)


    def __str__(self):
            text = []
            for i in range(self.n):
                for j in range(self.m):
                    if (i,j) not in self.values:
                        text.append('0,')
                    else:
                        text.append(str(self.values[(i,j)]) + ',')
                text.append('\n')

            return "".join(text)



