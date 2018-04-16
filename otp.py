import re
import sys
import getpass


def reduce(txt_char, key_char, binop):
    letter = binop(ord(txt_char), ord(key_char))
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
    if re.search("[^A-Z]", txt) is not None:
        raise Exception(f"txt can only contain uppercase letters ('{txt}')")

    if re.search("[^A-Z]", key) is not None:
        raise Exception(f"key can only contain uppercase letters ('{key}')")

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

        if validate(txt=txt, key=key):
            key = key[:len(txt)]

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
