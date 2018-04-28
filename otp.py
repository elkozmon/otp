import sys
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
        raise Exception("txt contains illegal characters %s" % txt_set_diff)

    if len(key_set_diff) > 0:
        raise Exception("key contains illegal characters %s" % key_set_diff)

    len_txt = len(txt)
    len_key = len(key)

    if len_key < len_txt:
        raise Exception("key too short (%d) for given txt (%d)" % (len_key, len_txt))

    return True


def get_charset(file):
    with open(file, "r") as charset_file:
        return "".join(charset_file.read().splitlines())


def get_txt(file):
    if file == "-":
        return input("Enter text: ")
    else:
        with open(file, "r") as txt_file:
            return "".join(txt_file.read().splitlines())


def get_key(file):
    with open(file, "r") as key_file:
        return "".join(key_file.read().splitlines())


def main():
    parser = argparse.ArgumentParser(description="One-time pad")
    parser.add_argument("-c", "--charsetfile", required=True,
                        help="path to charset file; pick required minimum")
    parser.add_argument("-k", "--keyfile", required=True,
                        help="path to the key file")
    parser.add_argument("-o", "--offset", type=int, default=0,
                        help="key offset; defaults to 0")

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("-e", action='store_true', help="encrypt")
    mode_group.add_argument("-d", action='store_true', help="decrypt")

    parser.add_argument("txtfile", metavar='TXTFILE', action='store',
                        help="file with text to en/decrypt. use single dash '-' to read from stdin")

    args = parser.parse_args()

    charset = get_charset(args.charsetfile)
    txt = get_txt(args.txtfile)
    key = get_key(args.keyfile)

    key = key[args.offset:args.offset + len(txt)]

    if validate(txt=txt, key=key, charset=charset):
        if args.e:
            print("Encrypting '%s' with key '%s'" % (txt, key), file=sys.stderr)
            print(encrypt(txt=txt, key=key, charset=charset), file=sys.stdout)
        elif args.d:
            print("Decrypting '%s' with key '%s'" % (txt, key), file=sys.stderr)
            print(decrypt(txt=txt, key=key, charset=charset), file=sys.stdout)
        else:
            parser.print_help()


if __name__ == '__main__':
    main()
