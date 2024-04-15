import math 
import random
import string
import time
import re
import os
PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4,
            26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
IP = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
]
Sbox = [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
];# Initialising hex string 
FP = [
            40, 8, 48, 16, 56, 24, 64, 32,
            39, 7, 47, 15, 55, 23, 63, 31,
            38, 6, 46, 14, 54, 22, 62, 30,
            37, 5, 45, 13, 53, 21, 61, 29,
            36, 4, 44, 12, 52, 20, 60, 28,
            35, 3, 43, 11, 51, 19, 59, 27,
            34, 2, 42, 10, 50, 18, 58, 26,
            33, 1, 41, 9, 49, 17, 57, 25
]
ini_string = "abcdefabcdef"


# Code to convert hex to binary 
res = "{0:064b}".format(int(ini_string, 16)) 
def fp(key):
    ans = ""
    for i in range(0,64):
        ans += key[FP[i]-1]
    return ans
def ip(key):
    ans = ""
    for i in range(0,64):
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
    result_bit_string = "".join(result_bits)

    return result_bit_string
def sbox(text):
    ans = ""
    for i in range(0,8):
        a = text[i:i+6]
        row = int(a[0] + a[5],2)
        col = int(a[1]+a[2]+a[3]+a[4],2)
        ans+= "{0:04b}".format(int(Sbox[row][col]))
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
'''
def binToHexa(n):
   
    # convert binary to int
    num = int(n, 2)
     
    # convert int to hexadecimal
    hex_num = hex(num)
    return(hex_num)'''
def pc1(key):
    permutedKeys = list()
    a = ""
    
    b = ""
    
    for i in range(0,28):
        a += key[PC1[i]-1]
    for i in range(28,56):
        b += key[PC1[i]-1]
    permutedKeys.append(a)
    permutedKeys.append(b)
    return permutedKeys
def pc2(key):
    permutedKeys = ""
    for i in range(0,48):
        permutedKeys += key[PC2[i]-1]

    return permutedKeys
def KeyGeneration(key):
    permutedKey = pc1(key)
    C = list()
    D = list()
    keys = list()
    C.append(bitwise_left_shift(permutedKey[0],1))
    D.append(bitwise_left_shift(permutedKey[1],1))
    keys.append(pc2(C[0]+D[0]))
    for i in range(1,16):
        if(i == 1 | i==8 | i==15):
            C.append(bitwise_left_shift(C[i-1],1))
            D.append(bitwise_left_shift(C[i-1],1))
            keys.append(pc2(C[i]+D[i]))
        else:
            C.append(bitwise_left_shift(C[i-1],2))
            D.append(bitwise_left_shift(C[i-1],2))
            keys.append(pc2(C[i]+D[i]))
    
    return keys

def encryption(plaintext,keys):
    cipher = ip(plaintext)
    L= list()
    R = list()
    L.append(cipher[0:32])
    R.append(cipher[32:64])
    for i in range(1,16):
        Li = R[i-1]
        Ri = bitwise_xor(L[i-1],(bitwise_xor(R[i-1],sbox(keys[i])))) 
        L.append(Li)
        R.append(Ri)
    
    return fp(L[15]+R[15])
'''def decryption(ciphertext, keys):
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
    return fp(L[-1] + R[-1])'''

# For decryption
def binary_to_ascii_manual(binary_string):
 

  if len(binary_string) % 8 != 0:
    raise ValueError("Binary string must be a multiple of 8 bits")

  # Split the binary string into groups of 8 bits
  chunks = [binary_string[i:i + 8] for i in range(0, len(binary_string), 8)]

  # Convert each chunk to an integer and then to ASCII character
  ascii_chars = list()
  for chunk in chunks:
      if((int(chunk, 2))==0):
          continue
      else:
          ascii_chars.append(chr(int(chunk, 2)))
     # print(f"{chr(int(chunk, 2))}-{(int(chunk, 2))}")
  #ascii_chars = [chr(int(chunk, 2)) for chunk in chunks]
  
  # Join the characters into a single string (assuming only one character)
  return "".join(ascii_chars)
def text_to_binary(text):
    """Converts any text input to its binary representation.

    Args:
        text: The text to be converted to binary.

    Returns:
        A string containing the binary representation of the text.
    """

    binary_string = ""
    for char in text:
       # Convert the character to its Unicode code point
       code_point = ord(char)

       # Convert the code point to its 8-bit binary representation (padded with zeros)
       binary_string += f"{code_point:08b}"

       # Alternative way using f-strings:
       # binary_string += f"{code_point:08b}"

    return binary_string
def ascii_to_binary_manual(ascii_string):


  # Convert each character to its decimal code point
  code_points = [ord(char) for char in ascii_string]

  # Check if all characters are valid ASCII (0 to 127)
  if any(code_point > 127 for code_point in code_points):
         raise ValueError("Input string contains non-ASCII characters")

  # Convert each code point to its 8-bit binary representation (padded with zeros)
  binary_string = "".join([bin(code_point)[2:].zfill(8) for code_point in code_points])

  return binary_string

keys = KeyGeneration(res)
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
'''def binary_to_hex(binary_string):
    decimal_representation = int(binary_string, 2)
    hex_representation = hex(decimal_representation)[2:]  # [2:] is used to remove the '0x' prefix
    return hex_representation'''


'''
PT = "01234567899abced"
print("plaintext:",PT)
integer_value = int(PT, 16)

BinPlainText = "{0:064b}".format(integer_value)
# For encryption
encrypted_text = encryption(BinPlainText, keys)
print("encrypted text:"+binToHexa(encrypted_text))
#keys.reverse()
# For decryption
decrypted_text = encryption(encrypted_text, keys)
print("decrupted text:"+binToHexa(decrypted_text))
'''
def remove_non_ascii(text):
    return re.sub(r'[^\x00-\x7F]+', "", text)
begin = time.time()
#f = open("yatin.txt","r")
#text = f.read().strip()
#text_bytes = text_to_binary(text)
#hex1 = text.encode("utf-8").hex()


res1 = text_bytes
while len(res1)%64!=0:
    res1 = "0"+res1
#print(binary_to_hex(res1))
#print(binary_to_ascii_manual(res1))
cipher = ""
for i in range(0,len(res1),64):
    
    t = res1[i:i+64]
    #while(len(t)<64):
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

enc = text_to_binary(text)

#print(ascii_to_binary_manual(text))
#text_bytes = bytes(text, "ascii")
#hex1 = text.encode("utf-8").hex()


#cipher = "".join(["{0:08b}".format(x) for x in text_bytes])
#print(cipher)

plain = ""

for i in range(0,len(enc),64):
    
    t = enc[i:i+64]
    #while(len(t)<64):
     #   t = "0"+t
    a = encryption(t,keys) 
    
    plain += a
 
# Generate random characters for the filename
random_name = "".join(random.choice(string.ascii_lowercase) for _ in range(10))

  # Combine the random name with the extension
#filename = f"{random_name}.txt"
#print("Decrypted file:",filename)
#file2 = open(filename,"w")
#print(binary_to_ascii_manual(plain))
#dec = remove_non_ascii(binary_to_ascii_manual(plain).strip())
#file2.write(dec)


end = time.time()
print(f"Total time of the program is {end - begin}") 
#plainFile = create_random_file(binary_to_ascii_manual(plain))
#print("decrypted file:",plainFile)
#bytes_data = ascii_to_binary_manual(binary_to_ascii_manual(plain))








