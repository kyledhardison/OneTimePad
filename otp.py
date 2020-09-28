
import argparse
import random
from sys import byteorder


def encrypt(keyFile, plaintextFile, ciphertextFile):
    """
    Use XOR to encrypt plaintext using a key

    @param keyFile: The file from which to read the encryption key
    @param plaintextFile: The file from wich to read the plaintext
    @param ciphertextFile: The file to write the resulting ciphertext to
    """
    with open(keyFile, "r") as f:
        key = f.read()

    with open(plaintextFile, "r") as f:
        plaintextString = f.read()
    
    # Convert each ASCII character to a series of 8 bits and join them all together in to a string
    plaintext = "".join(format(ord(x), "b").zfill(8) for x in plaintextString)

    keyLength = len(key)
    plaintextLength = len(plaintext)

    # Confirm that key lengths are the same, warn and exit if not
    if keyLength != plaintextLength:
        print("ERROR: key length and plain text length are different! Encryption cannot be completed. ")
        print("Key Length: " + str(keyLength) + " bits")
        print("Plain text length: " + str(plaintextLength) + " bits")
        return

    # XOR key and plaintext, then convert result to a bit string, preserving length.
    result = int(key, 2) ^ int(plaintext, 2)
    result = str(format(result, "b").zfill(keyLength))

    with open(ciphertextFile, "w") as f:
        f.write(result)
    
    print("Plaintext:  " + str(plaintext))
    print("Key:        " + str(key))
    print("Ciphertext: " + str(result))
    print("Output written to " + ciphertextFile)


def decrypt(keyFile, ciphertextFile, resultFile):
    """
    Use XOR to decrypt ciphertext using a key

    @param keyFile: The file from which to read the encryption key
    @param ciphertextFile: The file from wich to read the ciphertext
    @param resultFile: The file to write the resulting plaintext to
    """
    with open(keyFile, "r") as f:
        key = f.read()

    with open(ciphertextFile, "r") as f:
        ciphertextString = f.read()

    keyLength = len(key)
    ciphertextLength = len(ciphertextString)

    # Confirm that key lengths are the same, warn and exit if not
    if keyLength != ciphertextLength:
        print("ERROR: key length and cipher text length are different! Decryption cannot be completed. ")
        print("Key Length: " + str(keyLength) + " bits")
        print("Cipher text length: " + str(ciphertextLength) + " bits")
        return

    # XOR key and ciphertext, then convert result to a bit string, preserving length.
    result = int(key, 2) ^ int(ciphertextString, 2)
    result = str(format(result, "b").zfill(keyLength))

    # Step through the result binary string 8 bits at a time, parsing each to an ascii character.
    resultAscii = ''.join(chr(int(result[i*8:i*8+8],2)) for i in range(len(result)//8))

    print("Key:        " + str(key))
    print("Ciphertext: " + str(ciphertextString))
    print("Plaintext:  " + str(result))
    print("Plaintext in ASCII: " + str(resultAscii))
    print("Output written to " + ciphertextFile)

    with open(resultFile, "w") as f:
        f.write(resultAscii)


# Generate a random key of a given length, then write to a file
def keygen(length, file):
    """
    Generate a random key 

    @param length: The length of the key, in bits
    @param file: The output file where the key is written
    """
    # Generate random bits
    key = random.getrandbits(length)  

    # Convert key to a string representing the bits, using zfill to preserve length and not drop leading zeroes
    keyBitString = str(format(key, "b").zfill(length)) 

    with open(file, "w") as f:
        f.write(keyBitString)

    print("Key generated: " + keyBitString)
    print("Key written to " + file)


# Main function
if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser("Encode plaintext, decode ciphertext, or generate a key.")

    subparsers = parser.add_subparsers(help="Types of operations", dest="command")

    enc_parser = subparsers.add_parser("enc")
    dec_parser = subparsers.add_parser("dec")
    key_parser = subparsers.add_parser("keygen")

    enc_parser.add_argument("key", help="Key file")
    enc_parser.add_argument("plaintext", help="Plaintext file")
    enc_parser.add_argument("ciphertext", help="Ciphertext output file")

    dec_parser.add_argument("key", help="Key file")
    dec_parser.add_argument("ciphertext", help="Ciphertext file")
    dec_parser.add_argument("result", help="Result output file")

    key_parser.add_argument("length", help="Bit length of key", type=int, choices=range(1, 129),
                            metavar="{1-128}")
    key_parser.add_argument("file", help="Output file (Optional. Default: \"./data/newkey.txt\")",
                        nargs="?", default="./data/newkey.txt")

    args = parser.parse_args()

    # Run the chosen function based on passed arguments
    if (args.command == "enc"):
        encrypt(args.key, args.plaintext, args.ciphertext)
    elif (args.command == "dec"):
        decrypt(args.key, args.ciphertext, args.result)
    elif (args.command == "keygen"):
        keygen(args.length, args.file)

