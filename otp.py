
import argparse
import random

parser = argparse.ArgumentParser('Encode plaintext, decode ciphertext, or generate a key.')

subparsers = parser.add_subparsers(help='Types of operations', dest='command')

enc_parser = subparsers.add_parser("enc")
dec_parser = subparsers.add_parser("dec")
key_parser = subparsers.add_parser("keygen")

key_parser.add_argument('length', help='Bit length of key', type=int, choices=range(1, 129),
                        metavar='{1-128}')
key_parser.add_argument('file', help='Output file (Optional. Default: "./data/newkey.txt")',
                    nargs='?', default='./data/newkey.txt')

args = parser.parse_args()

# print(args.command)
# print(args)

if (args.command == "keygen"):
    key = random.getrandbits(args.length)

    with open(args.file, 'w') as f:
        f.write(str(key))

    print("Key generated: " + str( format(key, 'b').zfill(args.length) ))
    print("Written to " + args.file)

