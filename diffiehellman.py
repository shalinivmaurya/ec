def main():
    p = int(input("Enter a prime number: "))
    g = int(input("Enter a generator number: "))
    x, y = map(int, input("Enter the sender's and receiver's secret key: ").split())

    print("Sender's part:")
    res11 = pow(g, x, p)
    print("Public key is", res11)

    print("Receiver's part:")
    res22 = pow(g, y, p)
    print("Public key is", res22)

    print("Public keys are exchanged.")

    ress11 = pow(res22, x, p)
    ress22 = pow(res11, y, p)

    if ress11 == ress22:
        print("The shared secret key is", ress11)
    else:
        print("Values don't match.")

    print("**** With man in the middle attack ****")

    x1, y1 = map(int, input("Enter the attacker's key: ").split())

    print("The attacker calculates this:")
    as11 = pow(g, x1, p)
    print("Fake sender's public key", as11)

    as22 = pow(g, y1, p)
    print("Fake receiver's public key", as22)

    print("Fake keys are exchanged.")

    aas11 = pow(as22, x, p)
    aas22 = pow(as11, y, p)

    if aas22 == aas11:
        print("Values match.")
    else:
        print("An attack has taken place. The values don't match. Values are:", aas11, aas22)


if __name__ == "__main__":
    main()
