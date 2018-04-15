import sys
import getpass


def prepare_txt(txt):
    return "".join(filter(str.isalpha, txt)).upper()


def prepare_key(key):
    return key.upper()


def reduce(txt_char, key_char, binop):
    txt_char = ord(txt_char) - 65
    key_char = ord(key_char) - 65

    letter = binop(txt_char, key_char)
    letter %= 26
    letter += 65

    return chr(letter)


def opcrypt(txt, key, binop):
    return "".join(reduce(txt_char=i, key_char=j, binop=binop) for (i, j) in zip(txt, key))


def encrypt(txt, key):
    return opcrypt(txt=txt, key=key, binop=int.__add__)


def decrypt(txt, key):
    return opcrypt(txt=txt, key=key, binop=int.__sub__)


def validate(txt, key):
    len_txt = len(txt)
    len_key = len(key)

    if len_key < len_txt:
        raise Exception(f"key too short ({len_key}) for given txt ({len_txt})")

    return True


def main():
    mode = sys.argv[1]

    with open(sys.argv[2], "r") as key_file:
        txt = getpass.getpass("Enter text:")
        key = "".join(key_file.read().splitlines())

        txt = prepare_txt(txt=txt)
        key = prepare_key(key=key)

        if validate(txt=txt, key=key):
            if mode == "e":
                print(f"Encrypting '{txt}' with key '{key}'", file=sys.stderr)
                print(encrypt(txt=txt, key=key), file=sys.stdout)
            elif mode == "d":
                print(f"Decrypting '{txt}' with key '{key}'", file=sys.stderr)
                print(decrypt(txt=txt, key=key), file=sys.stdout)
            else:
                raise Exception(f"bad mode '{mode}'")


if __name__ == '__main__':
    main()
