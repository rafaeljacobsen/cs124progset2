import numpy as np
import sys


#standard multiplication, $n^3$
def normalmult(M1, M2):
    n=np.shape(M1)[0] # dimension of M1
    output = np.zeros((n,n)) # init output matrix to 0
    for i in range(n):
        for j in range(n):
            a=M1[i, j] # take one entry of M1 at a time for optimization
            for k in range(n):
                output[i, k] += a * M2[j, k]
    return output


def newstrassen(matrix1,matrix2,cutoff):
    if np.shape(matrix1)[0]==1:
        return matrix1*matrix2
    if np.shape(matrix1)[0]<=cutoff:
        return normalmult(matrix1,matrix2)
    M1=matrix1.copy()
    M2=matrix2.copy()

    odd=False
    if np.shape(M1)[0]%2==1:
        odd=True
        M1=np.pad(M1, ((0,1), (0,1)), mode='constant')
        M2=np.pad(M2, ((0,1), (0,1)), mode='constant')
    half=np.shape(M1)[0]//2
    
    # block matrices (submatrices)
    A=M1[:half,:half]
    B=M1[:half,half:]
    C=M1[half:,:half]
    D=M1[half:,half:]
    E=M2[:half,:half]
    F=M2[:half,half:]
    G=M2[half:,:half]
    H=M2[half:,half:]
    
    temp1=np.zeros((half,half))
    temp2=np.zeros((half,half))
    
    # seven matrices (subtasks of divide and combine)
    np.subtract(F,H,out=temp1)
    P1=newstrassen(A,temp1,cutoff)
    np.add(A,B,out=temp1)
    P2=newstrassen(temp1,H,cutoff)
    np.add(C,D,out=temp1)
    P3=newstrassen(temp1,E,cutoff)
    np.subtract(G,E,out=temp1)
    P4=newstrassen(D,temp1,cutoff)
    np.add(A,D,out=temp1)
    np.add(E,H,out=temp2)
    P5=newstrassen(temp1,temp2,cutoff)
    np.subtract(B,D,out=temp1)
    np.add(G,H,out=temp2)
    P6=newstrassen(temp1,temp2,cutoff)
    np.subtract(C,A,out=temp1)
    np.add(E,F,out=temp2)
    P7=newstrassen(temp1,temp2,cutoff)

    # Combine
    output=np.zeros((2*half,2*half))
    np.add(P4,P5,out=temp1)
    np.add(temp1,P6,out=temp2)
    np.subtract(temp2,P2,out=output[:half,:half])
    np.add(P1,P2,out=output[:half,half:])
    np.add(P3,P4,out=output[half:,:half])
    np.add(P1,P5,out=temp1)
    np.add(temp1,P7,out=temp2)
    np.subtract(temp2,P3,out=output[half:,half:])


    if odd:
        return output[:-1,:-1] # remove padding
    else:
        return output

#reads input
n=int(sys.argv[2])
filename=sys.argv[3]
matrix1=np.zeros((n,n))
matrix2=np.zeros((n,n))
with open(filename, "r", encoding="ascii") as f:
    text=f.read()
numbers=text.split('\n')
for i in range(n):
    for j in range(n):
        matrix1[j,i]=int(numbers[i+n*j])
for i in range(n):
    for j in range(n):
        matrix2[j,i]=int(numbers[n**2+i+n*j])

#multiplies matrices, cutoff of 16
output=newstrassen(matrix1,matrix2,16)
for i in range(n):
    print(int(output[i,i]))
