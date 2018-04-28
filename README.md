# One-time pad

```
$ python otp.py -h
usage: otp.py [-h] -c CHARSETFILE -k KEYFILE [-o OFFSET] (-e | -d) TXTFILE

One-time pad

positional arguments:
  TXTFILE               file with text to en/decrypt. use single dash '-' to
                        read from stdin

optional arguments:
  -h, --help            show this help message and exit
  -c CHARSETFILE, --charsetfile CHARSETFILE
                        path to charset file; pick required minimum
  -k KEYFILE, --keyfile KEYFILE
                        path to the key file
  -o OFFSET, --offset OFFSET
                        key offset; defaults to 0
  -e                    encrypt
  -d                    decrypt
```

## Example usage

```sh
# read from file & encrypt
python otp.py -c charsets/alpha_ucase.set -k my_secret_key.txt -e my_plaintext.txt

# read from stdin & encrypt
echo -n HELLO | python otp.py -c charsets/alpha_ucase.set -k my_secret_key.txt -e -

# prompt for input & encrypt
python otp.py -c charsets/alpha_ucase.set -k my_secret_key.txt -e -
```
