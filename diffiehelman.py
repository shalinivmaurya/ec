print("DIFFIE HELLMAN ")

def main():
    p = int(input("Enter a prime number (p): "))
    g = int(input("Enter a generator number (g): "))
    s = int(input("Enter the sender's key (s): "))
    r = int(input("Enter the receiver's key (r): "))
 
    ss = (g ** s) % p  
    rr = (g ** r) % p  
 
    ps = (rr ** s) % p  
    pr = (ss ** r) % p  
 
    print("Value of ss (sender's public key):", ss)
    print("Value of rr (receiver's public key):", rr)
 
 
    if ps == pr:
        print("ps and pr are equal,the shared secret key is:",ps)
    else:
        print("ps and pr are not equal")
 
 
if __name__ == "__main__":
    main()
