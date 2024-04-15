
import time
def PointDoubling(a,b,p,list1,list2):
	x1 = list1[0]
	y1 = list1[1]
	x2 = list2[0]
	y2 = list2[1]
	if(list1==list2):
		L = ((3*(x1*x1)+a)*(pow((2*y1),-1,p)))%p
		#print("lamdba value is:",L)
		x3 = (L*L-2*x1)%p
		y3 = (L*(x1-x3)-y1)%p
		#print(f"x3 and y3 is ({x3},{y3})")
		ansList = [x3,y3]
		return ansList
	else:
		L = (((y2-y1)%p)*pow((x2-x1),-1,p))%p
		#print("lamdba value is:",L)
		x3 = (L*L-x1-x2)%p
		y3 = (L*(x2-x3)-y2)%p
		#print(f"x3 and y3 is ({x3},{y3})")
		ansList = [x3,y3]
		return ansList
	


#print("equation of elliptical curve is:y^2=x^3+a*x+b")
a = 0#int(input("enter value of a:"))
b = 7#int(input("enter value of b:"))
p = 2503#int(input("enter prime number of finite field:"))
d = 3#int(input("enter value of d:"))
k = 2#int(input("enter value of k:"))
px = 3#int(input("enter x value of plain text point:"))
py = 0#int(input("enter y value of plain text point:"))
gx = 5#int(input("enter x value of base point:"))
gy = 1#int(input("enter y value of base point:"))
begin = time.time()
# list2 is most recent one and list1 is the original one
list1 = [gx,gy]
list2 = [gx,gy]
# Key generation
for i in range(0,d-1):
	ans = PointDoubling(a,b,p,list1,list2)
	list2 = ans
Q = list2

# Encryption
list2 = [gx,gy]
for i in range(0,k-1):
	ans = PointDoubling(a,b,p,list1,list2)
	list2 = ans
C1 = list2
list1 = Q
list2 = Q
for i in range(0,k-1):
	ans = PointDoubling(a,b,p,list1,list2)
	list2 = ans
S = list2

list1 = [px,py]
list2 = S
C2 = PointDoubling(a,b,p,list1,list2)
print(f"C1:{C1} and C2:{C2}")
end = time.time()
print(f"encryption time:{end-begin}")
begin = time.time()
#Decryption
list1 = C1
list2 = C1
for i in range(0,d-1):
	ans = PointDoubling(a,b,p,list1,list2)
	list2 = ans
S = list2

S1 = [list2[0],(-(list2[1]))%p]

list1 = C2
list2 = S1
P = PointDoubling(a,b,p,list1,list2)
print(f"plain text:{P}")
end = time.time()
print(f"decryption time:{end-begin}")