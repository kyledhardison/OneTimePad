
import argparse
import random
from sys import byteorder

parser = argparse.ArgumentParser('Encode plaintext, decode ciphertext, or generate a key.')

subparsers = parser.add_subparsers(help='Types of operations', dest='command')

enc_parser = subparsers.add_parser("enc")
dec_parser = subparsers.add_parser("dec")
key_parser = subparsers.add_parser("keygen")


enc_parser.add_argument('key', help="Key file")
enc_parser.add_argument('plaintext', help="Plaintext file")
enc_parser.add_argument('ciphertext', help="Ciphertext output file")


dec_parser.add_argument('key', help="Key file")
dec_parser.add_argument('ciphertext', help="Ciphertext file")
dec_parser.add_argument('result', help="Result output file")


key_parser.add_argument('length', help='Bit length of key', type=int, choices=range(1, 129),
                        metavar='{1-128}')
key_parser.add_argument('file', help='Output file (Optional. Default: "./data/newkey.txt")',
                    nargs='?', default='./data/newkey.txt')




args = parser.parse_args()

#TODO: Figure out a good binary representation. Storing a string with 1's and 0's may be the best, since it'll implicitly preserve key length
if (args.command == "keygen"):
    key = random.getrandbits(args.length)

    with open(args.file, 'w') as f:
        f.write(str(key))

    print("Bit length: " + str(key.bit_length()))

    # print("Key generated: " + str( format(key, 'b').zfill(args.length) ))
    print("Key generated: " + str( key.to_bytes(args.length, byteorder)))
    print("Written to " + args.file)

