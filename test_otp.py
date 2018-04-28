import unittest
from otp import encrypt, decrypt


class OtpTestCase(unittest.TestCase):
    """Tests for `otp.py`."""

    def test_encrypt_hello(self):
        """Encrypting HELLO with key XMCKL results in ciphertext EQNVZ"""
        self.assertEqual("EQNVZ", encrypt("HELLO", "XMCKL", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))

    def test_decrypt_hello(self):
        """Decrypting EQNVZ with key XMCKL results in plaintext HELLO"""
        self.assertEqual("HELLO", decrypt("EQNVZ", "XMCKL", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"))


if __name__ == '__main__':
    unittest.main()
