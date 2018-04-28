import sys
import getpass
import argparse


def reduce(txt_char, key_char, charset, binop):
    letter = binop(charset.index(txt_char), charset.index(key_char))
    letter %= len(charset)

    return charset[letter]


def opcrypt(txt, key, charset, binop):
    return "".join(reduce(txt_char=i, key_char=j, charset=charset, binop=binop) for (i, j) in zip(txt, key))


def encrypt(txt, key, charset):
    return opcrypt(txt=txt, key=key, charset=charset, binop=int.__add__)


def decrypt(txt, key, charset):
    return opcrypt(txt=txt, key=key, charset=charset, binop=int.__sub__)


def validate(txt, key, charset):
    txt_set_diff = set(txt).difference(charset)
    key_set_diff = set(key).difference(charset)

    if len(txt_set_diff) > 0:
        raise Exception(f"txt contains illegal characters {txt_set_diff}")

    if len(key_set_diff) > 0:
        raise Exception(f"key contains illegal characters {key_set_diff}")

    len_txt = len(txt)
    len_key = len(key)

    if len_key < len_txt:
        raise Exception("key too short (%d) for given txt (%d)" % (len_key, len_txt))

    return True


def main():
    parser = argparse.ArgumentParser(description="One-time pad")
    parser.add_argument("-c", "--charset", help="path to charset file; pick required minimum", required=True)
    parser.add_argument("-k", "--keyfile", help="path to the key file", required=True)
    parser.add_argument("-o", "--offset", help="key offset; defaults to 0", type=int, default=0)

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("-e", action='store_true', help="encrypt")
    mode_group.add_argument("-d", action='store_true', help="decrypt")

    args = parser.parse_args()

    with open(args.charset, "r") as charset_file:
        charset = "".join(charset_file.read().splitlines())

        with open(args.keyfile, "r") as key_file:
            txt = getpass.getpass("Enter text:")

            key = "".join(key_file.read().splitlines())
            key = key[args.offset:args.offset + len(txt)]

            if validate(txt=txt, key=key, charset=charset):
                if args.e:
                    print("Encrypting '%s' with key '%s'" % (txt, key), file=sys.stderr)
                    print(encrypt(txt=txt, key=key, charset=charset), file=sys.stdout)
                elif args.d:
                    print("Decrypting '%s' with key '%s'" % (txt, key), file=sys.stderr)
                    print(decrypt(txt=txt, key=key, charset=charset), file=sys.stdout)
                else:
                    raise Exception("bad mode")


if __name__ == '__main__':
    main()
