
import random,string,time

def modular_exponentiation(base, exponent, modulus):
        result = 1
        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus
            base = (base * base) % modulus
            exponent //= 2
        return result
def encrypt(PT,e,n):
    #encryptedList = []
    PTlist = [ord(char) for char in PT]
    CT = ""
    for i in PTlist:
        ele = modular_exponentiation(i,e,n)
        print("ele:",ele)
        CT += chr(ele % (2**16))  # Modulo by 1114112 to ensure value is in range

       # encryptedList.append(ele)
    #print("encrypted list:",encryptedList)
    return CT
def decrypt(CT,d,n):
    #decryptedList = []
    CTlist = [ord(char) for char in CT]
    PT = ""
    for i in CTlist:
        ele = modular_exponentiation(i,d,n)
        print("ele:",ele)
        CT += chr(ele % (2**16)) 
        #decryptedList.append(ele)
    #print("decrypted list:",decryptedList)
    return PT

def gcd(a, b):
    while b > 0:
        r = a % b
        a = b
        b = r
    return a

p = 3
q = 5
n = p * q
phi = (p - 1) * (q - 1)


list_of_e = [i for i in range(2, phi) if gcd(phi, i) == 1]
e = random.choice(list_of_e)
print("e:",e)
d = pow(e, -1, phi)
print("d:",d)
begin = time.time()
f = open("yatin.txt","r")
text = f.read().strip()
PT = text
CT = encrypt(PT,e,n)

# Generate random characters for the filename
random_name = "".join(random.choice(string.ascii_lowercase) for _ in range(10))

  # Combine the random name with the extension
filename = f"{random_name}.txt"
print("Encrypted file:", filename)

with open(filename, "w") as file2:
        file2.write(CT)
end =time.time()
print(f"encryption time:{end-begin}")
begin = time.time()
data = ""
with open(filename,"r") as file2:
     data = file2.read()
random_name = "".join(random.choice(string.ascii_lowercase) for _ in range(10))

  # Combine the random name with the extension
filename = f"{random_name}.txt"

print("decrypted file:",filename)
PT = decrypt(data,d,n)
with open(filename,"w") as file1:
     file1.write(PT)
end = time.time()
print(f"decryption time:{end-begin}")







	
    


