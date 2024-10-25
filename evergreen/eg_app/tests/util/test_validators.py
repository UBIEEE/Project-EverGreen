from django.test import TestCase
from eg_app.util.validators import validate_email, validate_password

# c-spell:disable - Don't spellcheck the emails

class TestValidateEmail(TestCase):

    def test_not_buffalo_email(self):
        self.assertFalse(validate_email("username@gmail.com"))

    def test_subdomain(self):
        self.assertTrue(validate_email("username@dcsl.buffalo.edu"))

    def test_deliverability(self):
        self.assertTrue(validate_email("username@buffalo.edu", True))
        self.assertTrue(validate_email("username@dcsl.buffalo.edu", True))
        self.assertFalse(validate_email("username@notreal.buffalo.edu", True))

    def test_valid_ubits(self):
        self.assertTrue(validate_email("abcd@buffalo.edu"))
        self.assertTrue(validate_email("longname@buffalo.edu"))
        self.assertTrue(validate_email("alfanum1@buffalo.edu"))
        self.assertTrue(validate_email("lt12@buffalo.edu"))
        self.assertTrue(validate_email("hello123@buffalo.edu"))

    def test_invalid_ubits(self):
        self.assertFalse(validate_email("abc@buffalo.edu"))
        self.assertFalse(validate_email("ninechars@buffalo.edu"))
        self.assertFalse(validate_email("1numfrst@buffalo.edu"))
        self.assertFalse(validate_email("mid4num@buffalo.edu"))
        self.assertFalse(validate_email("symbols!@buffalo.edu"))
        self.assertFalse(validate_email("123456@buffalo.edu"))

    def test_case_insensitive(self):
        self.assertTrue(validate_email("VALID@BUFFALO.EDU"))


class TestValidatePassword(TestCase):

    def test_too_short(self):
        self.assertFalse(validate_password("EightChr"))
        self.assertFalse(validate_password("ElevenChars"))

    def test_too_long(self):
        self.assertFalse(validate_password("a" * 256))

    def test_valid_passwords(self):
        self.assertTrue(validate_password("TwelveChars1"))
        self.assertTrue(validate_password("correcthorsebatterystaple"))
        self.assertTrue(validate_password("123456789012"))
        self.assertTrue(validate_password("NotANumberToBeSeen"))
        self.assertTrue(validate_password("notevenlowercase"))
        self.assertTrue(validate_password("all the symbols `~!@#$%^&*())-=_+[]{}\\|;',./:\"<>?"))
        self.assertTrue(validate_password("a" * 12))
        self.assertTrue(validate_password("1" * 12))
        self.assertTrue(validate_password("A" * 255))

