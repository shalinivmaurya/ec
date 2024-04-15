import base64,random,string,time# check aes is correct using this https://www.kavaliro.com/wp-content/uploads/2014/03/AES.pdf
sbox = [
    ["63", "7C", "77", "7B", "F2", "6B", "6F", "C5", "30", "01", "67", "2B", "FE", "D7", "AB", "76"],
    ["CA", "82", "C9", "7D", "FA", "59", "47", "F0", "AD", "D4", "A2", "AF", "9C", "A4", "72", "C0"],
    ["B7", "FD", "93", "26", "36", "3F", "F7", "CC", "34", "A5", "E5", "F1", "71", "D8", "31", "15"],
    ["04", "C7", "23", "C3", "18", "96", "05", "9A", "07", "12", "80", "E2", "EB", "27", "B2", "75"],
    ["09", "83", "2C", "1A", "1B", "6E", "5A", "A0", "52", "3B", "D6", "B3", "29", "E3", "2F", "84"],
    ["53", "D1", "00", "ED", "20", "FC", "B1", "5B", "6A", "CB", "BE", "39", "4A", "4C", "58", "CF"],
    ["D0", "EF", "AA", "FB", "43", "4D", "33", "85", "45", "F9", "02", "7F", "50", "3C", "9F", "A8"],
    ["51", "A3", "40", "8F", "92", "9D", "38", "F5", "BC", "B6", "DA", "21", "10", "FF", "F3", "D2"],
    ["CD", "0C", "13", "EC", "5F", "97", "44", "17", "C4", "A7", "7E", "3D", "64", "5D", "19", "73"],
    ["60", "81", "4F", "DC", "22", "2A", "90", "88", "46", "EE", "B8", "14", "DE", "5E", "0B", "DB"],
    ["E0", "32", "3A", "0A", "49", "06", "24", "5C", "C2", "D3", "AC", "62", "91", "95", "E4", "79"],
    ["E7", "C8", "37", "6D", "8D", "D5", "4E", "A9", "6C", "56", "F4", "EA", "65", "7A", "AE", "08"],
    ["BA", "78", "25", "2E", "1C", "A6", "B4", "C6", "E8", "DD", "74", "1F", "4B", "BD", "8B", "8A"],
    ["70", "3E", "B5", "66", "48", "03", "F6", "0E", "61", "35", "57", "B9", "86", "C1", "1D", "9E"],
    ["E1", "F8", "98", "11", "69", "D9", "8E", "94", "9B", "1E", "87", "E9", "CE", "55", "28", "DF"],
    ["8C", "A1", "89", "0D", "BF", "E6", "42", "68", "41", "99", "2D", "0F", "B0", "54", "BB", "16"]
]
Sbox_inv = [
    ["52", "09", "6A", "D5", "30", "36", "A5", "38", "BF", "40", "A3", "9E", "81", "F3", "D7", "FB"],
    ["7C", "E3", "39", "82", "9B", "2F", "FF", "87", "34", "8E", "43", "44", "C4", "DE", "E9", "CB"],
    ["54", "7B", "94", "32", "A6", "C2", "23", "3D", "EE", "4C", "95", "0B", "42", "FA", "C3", "4E"],
    ["08", "2E", "A1", "66", "28", "D9", "24", "B2", "76", "5B", "A2", "49", "6D", "8B", "D1", "25"],
    ["72", "F8", "F6", "64", "86", "68", "98", "16", "D4", "A4", "5C", "CC", "5D", "65", "B6", "92"],
    ["6C", "70", "48", "50", "FD", "ED", "B9", "DA", "5E", "15", "46", "57", "A7", "8D", "9D", "84"],
    ["90", "D8", "AB", "00", "8C", "BC", "D3", "0A", "F7", "E4", "58", "05", "B8", "B3", "45", "06"],
    ["D0", "2C", "1E", "8F", "CA", "3F", "0F", "02", "C1", "AF", "BD", "03", "01", "13", "8A", "6B"],
    ["3A", "91", "11", "41", "4F", "67", "DC", "EA", "97", "F2", "CF", "CE", "F0", "B4", "E6", "73"],
    ["96", "AC", "74", "22", "E7", "AD", "35", "85", "E2", "F9", "37", "E8", "1C", "75", "DF", "6E"],
    ["47", "F1", "1A", "71", "1D", "29", "C5", "89", "6F", "B7", "62", "0E", "AA", "18", "BE", "1B"],
    ["FC", "56", "3E", "4B", "C6", "D2", "79", "20", "9A", "DB", "C0", "FE", "78", "CD", "5A", "F4"],
    ["1F", "DD", "A8", "33", "88", "07", "C7", "31", "B1", "12", "10", "59", "27", "80", "EC", "5F"],
    ["60", "51", "7F", "A9", "19", "B5", "4A", "0D", "2D", "E5", "7A", "9F", "93", "C9", "9C", "EF"],
    ["A0", "E0", "3B", "4D", "AE", "2A", "F5", "B0", "C8", "EB", "BB", "3C", "83", "53", "99", "61"],
    ["17", "2B", "04", "7E", "BA", "77", "D6", "26", "E1", "69", "14", "63", "55", "21", "0C", "7D"]
]


Rcon = ["01", "02", "04", "08", "10", "20", "40", "80", "1b", "36"]
def mix_columns(state):
 
    # AES mix column matrix
    mix_column_matrix = [
        [2, 3, 1, 1],
        [1, 2, 3, 1],
        [1, 1, 2, 3],
        [3, 1, 1, 2]
    ]

    result_state = []
    for i in range(4):
        new_column = []
        for j in range(4):
            # Perform matrix multiplication on the current column
            val = 0
            for k in range(4):
                val ^= aes_mul(mix_column_matrix[i][k], int(state[k][j],16))
            new_column.append(hex(val)[2:])
        result_state.append(new_column)

    return result_state
def inv_mix_columns(state):
   
    # AES inverse mix column matrix
    inv_mix_column_matrix = [
        ["0E", "0B", "0D", "09"],
        ["09", "0E", "0B", "0D"],
        ["0D", "09", "0E", "0B"],
        ["0B", "0D", "09", "0E"]
    ]

    result_state = []
    for i in range(4):
        new_column = []
        for j in range(4):
            # Perform matrix multiplication on the current column
            val = 0
            for k in range(4):
                val ^= aes_mul(int(inv_mix_column_matrix[i][k],16), int(state[k][j],16))
            new_column.append(hex(val)[2:])
        result_state.append(new_column)

    return result_state

def aes_mul(a, b):

    # The irreducible polynomial in AES multiplication
    poly = 0x11b
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= poly
        b >>= 1
    return result

def InvSBOX(val):
    row = int(val[:1],16)
    col = int(val[1:],16)
    return Sbox_inv[row][col]   



def splitList(original_list):
    result_list = [char for string in original_list for char in string]
    return result_list
def hex_xor(hex_str1, hex_str2):
    # Convert hexadecimal strings to integers
    int_val1 = int(hex_str1, 16)
    int_val2 = int(hex_str2, 16)
    
    # Perform XOR operation
    result = int_val1 ^ int_val2
    
    # Convert result back to hexadecimal string
    hex_result = format(result, 'X')
    
    # Ensure the result has even length by padding with zero if necessary
    hex_result = hex_result.zfill(len(hex_str1))
    
    return hex_result
def SBOX(val):
    row = int(val[:1],16)
    col = int(val[1:],16)
    return sbox[row][col]
def LeftShift(word, No):
    NewWord = [None] * 4
    for i in range(4):
        NewWord[i] = word[(i + No) % 4]
    return NewWord
def circular_shift_up(matrix):
    shifted_matrix = []
    for column_idx in range(len(matrix[0])):
        shifted_column = []
        for row_idx in range(len(matrix)):
            shifted_row_idx = (row_idx - column_idx) % len(matrix)
            shifted_column.append(matrix[shifted_row_idx][column_idx])
        shifted_matrix.append(shifted_column)
    return shifted_matrix

def circular_shift_down(matrix):
    shifted_matrix = []
    for column_idx in range(len(matrix[0])):
        shifted_column = []
        for row_idx in range(len(matrix)):
            shifted_row_idx = (row_idx + column_idx) % len(matrix)
            shifted_column.append(matrix[shifted_row_idx][column_idx])
        shifted_matrix.append(shifted_column)
    return shifted_matrix

def RightShift(word,No):
    NewWord = list()
    for i in range(0,4):
        NewWord.append(word[(i-No)%4])
    return NewWord
def binToHexa(n):
   
    # convert binary to int
    num = int(n,10)
     
    # convert int to hexadecimal
    hex_num = hex(num)
    return(hex_num)
def g(w,rno):
    A = LeftShift(w,1)
   
    S = [SBOX(word) for word in A]
    
    
    ans = [
    (hex_xor(word[:1], Rcon[rno][:1]) + hex_xor(word[1:], Rcon[rno][1:]))
    if word == S[0]  # Check if word is the first element of S
    else (word) # Placeholder for other cases
    for word in S
]
    
    return ans
def HexToMatrix(val):
    matrix=[]
    l=0
    for i in range(0,4):
        row = []
        for j in range(0,4):
            row.append(val[l:l+2])
            l = l+2
        matrix.append(row)
    return matrix
def KeyGeneration(key):
    KeyMatrix = (HexToMatrix(key))
    
    Words = list()
    
    Words.append(KeyMatrix[0])
    Words.append(KeyMatrix[1])
    Words.append(KeyMatrix[2])
    Words.append(KeyMatrix[3])
    
   

    for i in range(4,44):
        if(i%4==0):
            #print(g(Words[i-1],int((i/4)-1)))
            z = splitList(g(Words[i-1],int(((i//4)-1))))
           
            # ((i/4)-1)*4 
            W = splitList(Words[int(((i//4)-1)*4)])
    #for a,b in zip(z,W):
     #   print(hex(int(hex_xor(a, b))))
            ans = [hex(int(hex_xor(a, b),16))[2:] for a, b in zip(z, W)]
            a = []
            for num in range(0,len(ans),2):
                a.append(ans[num]+ans[num+1])

            Words.append(a)
            #print("A:",a)
        else:
            z = splitList(Words[i-1])
           # print("i:",i)
           # print("z:",z)
            W = splitList(Words[int(i%4 + ((i//4)-1)*4)])
            #print("word:",W)
            #print(f"i value:{int(((i-4)/4)*4)} and i:{i}")
            ans = [hex(int(hex_xor(a, b),16))[2:] for a, b in zip(z, W)]
            
            a = []
            for num in range(0,len(ans),2):
                a.append(ans[num]+ans[num+1])

            Words.append(a)
            #print("a:",a)
            
    

    return Words
def ListXor(list1,list2):
    a = (list1)
    
    
    b = (list2)
    
    ans = [hex(int(hex_xor(A, B),16))[2:] for A, B in zip(a, b)]
    ans1 = ["0"+ele if(len(ele)%2!=0) else ele for ele in ans]
    #print("ans1:",ans1)
    #print("ans:",ans)
    '''if len(ans) % 2 != 0:
        ans.append('0')  # Append a dummy element if the length is odd
    
    a1 = []
    for num in range(0,len(ans),2):
            a1.append(ans[num]+ans[num+1])
    return a1'''
    return ans1

def Encryption(plaintext,keys):
    PlainMatrix = HexToMatrix(plaintext)
    #print("PlainMatrix[0]:",PlainMatrix[0])
    #print(PlainMatrix)
    Ans = [ListXor(PlainMatrix[j],keys[j]) for j in range(0,len(PlainMatrix))]
    #print("Ans:",Ans)
    Answers = []
    Answers.append(Ans)
    
    
    
    for i in range(1,11):
        #add round key with previous
         
         Ans = Answers[i-1]
         #print("ans:",Ans)
         # sub bytes
         #Ans1 = [item for sublist in Ans for item in sublist]
         Ans1 = [[SBOX(item) for item in sublist] for sublist in Ans]
         
        # print("ans1:",Ans1)
         # shift row
         shiftAns = circular_shift_down(Ans1)
         
         #mixcolumn
         if(i!=10):
            MixAns = mix_columns(shiftAns)
            Mix = [["0"+ele if len(ele)%2!=0 else ele for ele in sublist] for sublist in MixAns]
            
            transposed_list = [list(column) for column in zip(*Mix)]

          
         #print("mix:",MixAns)
            
            RoundAns = [ListXor(transposed_list[j],keys[(i)*4+j]) for j in range(0,len(transposed_list))]
           
            Answers.append(RoundAns)
            
         else:
            transposed_list = [list(column) for column in zip(*shiftAns)]

            
            RoundAns = [ListXor(transposed_list[j],keys[(i)*4+j]) for j in range(0,len(transposed_list))]
          
            Answers.append(RoundAns)
            
    return Answers[10]
 
       
    
    return 

def Decryption(cipherText,keys,key):
    PlainMatrix = (cipherText)
    Ans = [ListXor(PlainMatrix[j],keys[40+j]) for j in range(0,len(PlainMatrix))]
   
    Answers = []
    Answers.append(Ans)
    #print(Answers)
    

    for i in range(1,11):
        #add round key with previous
         Ans = Answers[i-1]
         #print("ans:",Ans)
         # inverse shift row
         shiftAns = circular_shift_down(Ans)
         
         shiftAns1 = [["0"+ele if(len(ele)%2!=0) else ele for ele in  sublist] for sublist in shiftAns]
         #shiftAns1 =  ["0"+ele if (len(ele)%2!=0) else ele for ele in shiftAns]
         # inverse sub bytes
         #Ans1 = [item for sublist in Ans for item in sublist]
        
         Ans1 = [[InvSBOX(item) for item in sublist] for sublist in shiftAns1]
         #print("ans1:",Ans1)
         # Add round key
         transposed_list = Ans1#[list(column) for column in zip(*Ans1)]
         RoundAns = [ListXor(transposed_list[j],keys[(10-i)*4+j]) for j in range(0,len(transposed_list))]
         #print("shiftAns:",shiftAns)
         #mixcolumn
         #RoundAns = [list(column) for column in zip(*RoundAns)]
         t_list = [list(column) for column in zip(*RoundAns)]
         MixAns = inv_mix_columns(t_list)
         #print("mix:",MixAns)
         if i==10:
            Answers.append(RoundAns)
         else:
            Answers.append(MixAns)
         
         
         
    return Answers[10]
key = "5468617473206D79204B756E67204675"
def string_to_hex(input_string):
    # Encode the input string into bytes using UTF-8 encoding
    byte_string = input_string.encode('utf-8')
    
    # Convert bytes to hexadecimal representation
    hex_string = byte_string.hex()
    
    return hex_string
def hex_to_string(hex_string):

    byte_string = bytes.fromhex(hex_string)
    
    decoded_string = base64.b64encode(byte_string).decode('utf-8')
    
    return decoded_string
begin = time.time()
keys = (KeyGeneration(key))


data = ""
with open("yatin.txt","r") as file:
    data = file.read().strip()
HexData = string_to_hex(data)
while len(HexData)%64!=0:
    HexData = "0" +  HexData



cipher=""
for i in range(0,len(HexData),64):
    t = HexData[i:i+64]
    a = Encryption(t,keys)
    result_string = ''.join([''.join(row) for row in a])
    cipher+=result_string
i_lowercase) for _ in range(10))

filename = f"{random_name}.txt"
with open(filename,"w") as file1:
    file1.write(hex_to_string(cipher))
print(f"encrypted file name:{filename}")
end = time.time()

print(f"encryption time:{end-begin}")

