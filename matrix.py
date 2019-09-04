import numpy as np
import numpy.linalg as la
import copy

J = np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0, -1, 0,0]], np.int32)
h1 = np.array([[1,0,0,0],[0,0,0,0],[0,0,-1,0],[0,0,0,0]])
I = np.array([[1,0],[0,1]])

def makemat(a,b,c,d):
    return np.array([[a,b],[c,d]], np.int32)

def contains(matrix, collection): # Tests if a matrix is in a collection
    for i in collection:
        if np.array_equal(i, matrix):
            return True
    
    return False

def invert(x, mod = 3):
    a = x[0,0]
    b = x[0,1]
    c = x[1,0]
    d = x[1,1]
    return np.array([[d, -b], [-c , a]], np.int32) % mod

def populatesl2(mod = 3): #mod is the modulus of the field the matrix entries are taken from
    sl2 = list()
    for a in range(mod):
        for b in range(mod):
            for c in range(mod):
                for d in range(mod):
                    x = makemat(a,b,c,d)
                    if contains(x, sl2) or (la.det(x) % 3) != 1:
                        continue
                    else:
                        sl2.append(x)
    return sl2

def conjclass(collection, mod):
    # Conjugacy classes parition a group
    # We conjugate each element. We then remove each element
    # in the resulting conjugacy class; it will only be conjugate to
    # class already created, since conjugaction is an equivalenc relation
    classes = list()
    coll = copy.deepcopy(collection)
    while len(coll) > 0:
        x = coll[0]
        conjclass = conjugate(x, coll, mod)
        classes.append(conjclass)
        
        # Remove the elements from our collection
        temp = list()
        for y in coll:
            if contains(y, conjclass):
                continue
            else:
                temp.append(y)
        
        coll = temp

    return classes

def conjugate(x, collection, mod = 3): # 
    conjclass = list()
    for m in collection:
        res = conj(x,m, mod)
        if contains(res, conjclass):
            continue
        else:
            conjclass.append(res)
        
    return conjclass

def conj(x, m, mod = 3):  # returns the matrix mxm^{-1}
    return np.matmul(np.matmul(m,x), invert(m,3)) % mod
    

sl2 = populatesl2(3)
c1 = conjugate(sl2[0], sl2, 3)
conjclass = conjclass(sl2, 3)
print(len(conjclass))
for x in conjclass:
    print(x)
    
total = 0
for x in conjclass:
    total += len(x)
    print(len(x))

print(total)
