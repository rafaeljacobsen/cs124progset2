import numpy as np
import sys

def genarraye(e):
    return np.random.choice([0,1],[e,e])

def normalmult(M1, M2):
    n=np.shape(M1)[0]
    output = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            a=M1[i, j]
            for k in range(n):
                output[i, j] += a * M2[k, j]
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
        M1=np.pad(M1,1)[1:,1:]
        M2=np.pad(M2,1)[1:,1:]
    half=np.shape(M1)[0]//2

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
        return output[:-1,:-1]
    else:
        return output

n=int(sys.argv[2])
filename=sys.argv[3]
matrix1=np.zeros((n,n))
matrix2=np.zeros((n,n))
with open(filename, "r", encoding="ascii") as f:
    text=f.read()
numbers=text.split('\n')
print(len(numbers))
for i in range(n):
    for j in range(n):
        matrix1[i,j]=int(numbers[i+n*j])
for i in range(n):
    for j in range(n):
        matrix2[i,j]=int(numbers[n**2+i+n*j])
output=newstrassen(matrix1,matrix2,16)
for i in range(n):
    print(int(output[i,i]))
