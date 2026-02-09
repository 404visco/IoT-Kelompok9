def makepoint(x,y):
    return (x,y)

def getAbsis(p):
    return p[0]
def getOrdinat(p):
    return p[1]

def isEqualTitik(t1,t2):
    return getAbsis(t1)==getAbsis(t2) and getOrdinat(t1)==getOrdinat(t2)

print(isEqualTitik(makepoint(4,4),makepoint(5,4)))