import math 
import random
import string
import time
import os
PC10 = [3,5,2,7,4,10,1,9,8,6]
PC8 = [6,3,7,4,8,5,10,9]
P4 = [2,4,3,1]
#PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
 #           26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
  #          51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
IP = [2,6,3,1,4,8,5,7]
Sbox = [
           [1,0,3,2],
           [3,2,1,0],
           [0,2,1,3],
           [3,1,3,2]
];
Sbox1 = [
    [0,1,2,3],
    [2,0,1,3],
    [3,0,1,0],
    [2,1,0,3]
]# Initialising hex string 
FP = [4,1,3,5,7,2,8,6]



# Code to convert hex to binary 
res = "0101101011"
def p4(text):
    ans = ""
    for i in range(0,4):
        ans += text[P4[i]-1]
    return ans
def fp(key):
    ans = ""
    for i in range(0,8):
        ans += key[FP[i]-1]
    return ans
def ip(key):
    ans = ""
    for i in range(0,8):
        ans += key[IP[i]-1]
    return ans
def bitwise_xor(bit_array1, bit_array2):
    # Ensure both bit arrays have the same length
    if len(bit_array1) != len(bit_array2):
        raise ValueError("Bit arrays must have the same length")

    # Convert the bit arrays to lists of bits
    bits1 = list(bit_array1)
    bits2 = list(bit_array2)

    # Perform the XOR operation
    result_bits = [str(int(b1) ^ int(b2)) for b1, b2 in zip(bits1, bits2)]

    # Convert the result bits back to a string
    result_bit_string = ''.join(result_bits)

    return result_bit_string
def sbox1(text):
    ans = ""
    a = text[0:4]
    row = int(a[0]+a[3],2)
    col = int(a[1]+a[2],2)
    ans+= "{0:02b}".format(int(Sbox[row][col]))
    return ans
def sbox(text):
    ans = ""
    a = text[0:4]
    row = int(a[0]+a[3],2)
    col = int(a[1]+a[2],2)
    ans+= "{0:02b}".format(int(Sbox1[row][col]))
    return ans
def bitwise_left_shift(bit_array, shift_amount):
    # Convert the bit_array to a list of bits
    bits = list(bit_array)
    
    # Calculate the effective shift amount
    effective_shift = shift_amount % len(bits)
    
    # Perform the left shift operation
    shifted_bits = bits[effective_shift:] + bits[:effective_shift]
    #print(len(bits))
    # Ensure the result has the same length as the input bit array
    while len(shifted_bits)<len(bits):
        shifted_bits = "0"+shifted_bits
    
    # Convert the shifted bits back to a string
    shifted_bit_string = "".join(shifted_bits)
    #print(shifted_bit_string)
    
    return shifted_bit_string

def binToHexa(n):
   
    # convert binary to int
    num = int(n, 2)
     
    # convert int to hexadecimal
    hex_num = hex(num)
    return(hex_num)
def pc1(key):
    permutedKeys = list()
    ans = ""
    for i in range(1,10):
        ans += key[PC10[i]-1]
    left = ans[:5]
    right = ans[5:]
    left = bitwise_left_shift(left,1)
    right = bitwise_left_shift(right,1)
    permutedKeys.append(pc2(left+right))
    left = bitwise_left_shift(left,2)
    right = bitwise_left_shift(right,2)
    permutedKeys.append(pc2(left+right))
    return permutedKeys
def pc2(key):
    permutedKeys = ""
    for i in range(0,len(PC8)):
        permutedKeys += key[PC8[i]-1]


    return permutedKeys
def KeyGeneration(key):
    permutedKeys = list()
    ans = ""
    for i in range(0,10):
        ans += key[PC10[i]-1]
  
    left = ans[0:5]
    right = ans[5:10]
   
    left = bitwise_left_shift(left,1)
    right = bitwise_left_shift(right,1)
    
    permutedKeys.append(pc2(left+right))
    left = bitwise_left_shift(left,2)
    right = bitwise_left_shift(right,2)
    permutedKeys.append(pc2(left+right))
    return permutedKeys
EP = [4,1,2,3,2,3,4,1]
def encryption(plaintext,keys):
    cipher = ip(plaintext)
    L = cipher[:4]
    R = cipher[4:8]
    ans = ""
    for i in range(0,8):
        ans += R[EP[i]-1]
    ans = bitwise_xor(ans,keys[0])
    
    l = ans[0:4]
    r = ans[4:8]
    
    l = sbox(l)
    r = sbox1(r)
    
    ans = p4(l+r)
   
    ans = bitwise_xor(ans,L)
    ans = ans + R 
    L = ans[:4]
    R = ans[4:8]
    
    cipher = R + L
   
    L = cipher[:4]
    R = cipher[4:8]
    ans = ""
    for i in range(0,8):
        ans += R[EP[i]-1]
    ans = bitwise_xor(ans,keys[1])
    l = ans[0:4]
    r = ans[4:8]
    l = sbox(l)
    r = sbox1(r)
    ans = p4(l+r)
    ans = bitwise_xor(ans,L)
    ans = ans + R
    L = ans[:4]
    R = ans[4:8]
    cipher = L + R
    cipher = fp(cipher)
    return cipher
   



    

def decryption(ciphertext, keys):
    plaintext = ip(ciphertext)
    L = list()
    R = list()
    L.append(plaintext[0:32])
    R.append(plaintext[32:64])
    for i in range(15, 0, -1):  # Iterate from 15 to 1
        Ri = L[-1]
        Li = bitwise_xor(R[-1], (bitwise_xor(L[-1], sbox(keys[i]))))
        R.append(Ri)
        L.append(Li)
    return fp(L[-1] + R[-1])

# For decryption
def binary_to_ascii_manual(binary_string):
  """Converts a binary string to its ASCII equivalent manually.

  Args:
    binary_string: A string containing only 0s and 1s.

  Returns:
    The ASCII character represented by the binary string.

  Raises:
    ValueError: If the binary string is not a multiple of 8 bits.
  """

  if len(binary_string) % 8 != 0:
    raise ValueError("Binary string must be a multiple of 8 bits")

  # Split the binary string into groups of 8 bits
  chunks = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

  # Convert each chunk to an integer and then to ASCII character
  ascii_chars = [chr(int(chunk, 2)) for chunk in chunks]

  # Join the characters into a single string (assuming only one character)
  return "".join(ascii_chars)
def ascii_to_binary_manual(ascii_string):
  """Converts an ASCII string to its binary representation manually.

  Args:
    ascii_string: A string containing only ASCII characters.

  Returns:
    The binary string representation of the ASCII string.

  Raises:
    ValueError: If any character in the string is not an ASCII character.
  """

  # Convert each character to its decimal code point
  code_points = [ord(char) for char in ascii_string]

  # Check if all characters are valid ASCII (0 to 127)
 # if any(code_point > 127 for code_point in code_points):
  #  raise ValueError("Input string contains non-ASCII characters")

  # Convert each code point to its 8-bit binary representation (padded with zeros)
  binary_string = "".join([bin(code_point)[2:].zfill(8) for code_point in code_points])

  return binary_string

keys = KeyGeneration(res)
'''
PT = "10110010"
print("plain text:",PT)
A = encryption(PT,keys)
print("cipher text:",A)
keys.reverse()
print("decrypted:",encryption(A,keys))
'''
def create_random_file(text_to_write, extension=".txt"):
 

  # Generate random characters for the filename
  random_name = "".join(random.choice(string.ascii_lowercase) for _ in range(10))

  # Combine the random name with the extension
  filename = f"{random_name}{extension}"

  # Create the file and write the text
  with open(filename, "w") as f:
    f.write(text_to_write)

  # Return the generated filename
  return filename
def binary_to_hex(binary_string):
    decimal_representation = int(binary_string, 2)
    hex_representation = hex(decimal_representation)[2:]  # [2:] is used to remove the '0x' prefix
    return hex_representation



#PT = "01234567899abced"
#print("plaintext:",PT)
#integer_value = int(PT, 16)

#BinPlainText = "{0:064b}".format(integer_value)
# For encryption
#encrypted_text = encryption(BinPlainText, keys)
#print("encrypted text:"+binToHexa(encrypted_text))
#keys.reverse()
# For decryption
#decrypted_text = encryption(encrypted_text, keys)
#print("decrupted text:"+binToHexa(decrypted_text))

begin = time.time()
f = open("yatin.txt","r")
text = f.read().strip()
text_bytes = bytes(text, "ascii")
#hex1 = text.encode("utf-8").hex()


res1 = "".join(["{0:08b}".format(x) for x in text_bytes])
while len(res1)%8!=0:
    res1 = "0"+res1

#print(binary_to_hex(res1))

#print(binary_to_ascii_manual(res1))
cipher = ""
for i in range(0,len(res1),8):
    
    t = res1[i:i+8]
    #while(len(t)<8):
     #   t = "0"+t
    a = encryption(t,keys) 
    
    cipher += a

#print("ciphjer:"+binary_to_hex(cipher))
#print(binary_to_ascii_manual(cipher))
encryptedFile = create_random_file(binary_to_ascii_manual(cipher))
print("encrypted file",encryptedFile)
f1 = open(encryptedFile,"r")
text = f1.read().strip()
#print(text)
enc = ascii_to_binary_manual(text)
#print(ascii_to_binary_manual(text))
#text_bytes = bytes(text, "ascii")
#hex1 = text.encode("utf-8").hex()


#cipher = "".join(["{0:08b}".format(x) for x in text_bytes])
#print(cipher)
plain = ""
keys.reverse()
for i in range(0,len(enc),8):
    
    t = enc[i:i+8]
    #while(len(t)<8):
     #   t = "0"+t
    a = encryption(t,keys) 
    
    plain += a
  # Generate random characters for the filename
random_name = "".join(random.choice(string.ascii_lowercase) for _ in range(10))

  # Combine the random name with the extension
filename = f"{random_name}.txt"
print("Decrypted file:",filename)
file2 = open(filename,"w")
file2.write(binary_to_ascii_manual(plain))
#print(binary_to_ascii_manual(plain))
end = time.time()
print(f"Total time of the program is {end - begin}") 