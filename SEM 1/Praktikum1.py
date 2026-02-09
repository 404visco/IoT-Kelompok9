
#KUADRAT
def kuadrat2(x):
    return x*x

#IsAnA?
print('=== Is An A? ===')
def teshuruf(y):
    return y== 'A'
print(teshuruf(1)) #False
print(teshuruf(0)) #False
print(teshuruf('A')) #True

#IsPositif?
print('=== Is Positif? ===')
def tespositif(x):
    return x>=0
print(tespositif(-1)) #False
print(tespositif(1)) #True
print(tespositif(0)) #True

#LEAST SQUARE
print('=== LEAST SQUARE ===')
def jarak2titik(x1,y1,x2,y2):
    return (kuadrat2(x2-x1)+ kuadrat2(y2-y1))**0.5

print(jarak2titik(1,3,5,6))

#MEAN OLYMPIQUE
print('=== MEAN OLYMPIQUE ===')
def min2(a,b): 
    return (a+b-abs(a-b))/2
def min4(a,b,c,d): 
    return min2(min2(a,b),min2(c,d))

def max2(a,b): 
    return (a+b+abs(a-b))/2
def max4(a,b,c,d): 
    return max2(max2(a,b),max2(c,d))

def mo(a,b,c,d): 
    return (a+b+c+d-max4(a,b,c,d)-min4(a,b,c,d))/2
print(mo(8,12,10,20)) #11

#5 Bobot
print('=== BOBOT ===')
def nb(n,b):
    return (n*b)
def rata2berbobot(n1, n2, n3, n4, n5):
    return (n1*0.1 + n2*0.2 + n3*0.4 + n4*0.15 + n5*0.15)

print(rata2berbobot(90,70,30,40,80))

#
#def teskebenaran(z):
    #return z<5 or z>=500
#print(teskebenaran(5)) #False
#print(teskebenaran(4)) #True
#print(teskebenaran(100)) #False
#print(teskebenaran(500)) #True