import string

from django.test import TestCase

from eg_app.models import User
from eg_app.util.validators import (
    user_is_registered,
    validate_credentials_on_register,
    validate_email,
    validate_password,
    validate_password_pair,
)

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
        self.assertTrue(validate_email("random@buffalo.edu"))

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
        self.assertFalse(validate_password(""))
        self.assertFalse(validate_password(" "))
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
        self.assertTrue(
            validate_password("all the symbols `~!@#$%^&*())-=_+[]{}\\|;',./:\"<>?")
        )
        self.assertTrue(validate_password("a" * 12))
        self.assertTrue(validate_password("1" * 12))
        self.assertTrue(validate_password("A" * 255))
        self.assertTrue(validate_password(string.printable))


class TestValidatePasswordPair(TestCase):

    def test_too_short(self):
        self.assertFalse(validate_password_pair("", ""))
        self.assertFalse(validate_password_pair(" ", " "))
        self.assertFalse(validate_password_pair("EightChr", "EightChr"))
        self.assertFalse(validate_password_pair("ElevenChars", "ElevenChars"))

    def test_too_long(self):
        valid_alphabet: str = (
            string.ascii_letters
            + string.digits
            + string.punctuation
            + string.whitespace
        )
        for char in valid_alphabet:
            too_long_repeated_char = char * 256
            self.assertFalse(
                validate_password_pair(too_long_repeated_char, too_long_repeated_char)
            )

    def test_valid_all_lowercase(self):
        password = "alllowercaseacceptable"
        self.assertTrue(password, password)

    def test_off_by_one(self):
        password = "This password is off by one character"
        password_confirmation = "This password is of by one character"
        self.assertFalse(validate_password_pair(password, password_confirmation))

    def test_different_types(self):
        password: str = "thisisinadifferentrepresentatinoalformat"
        password_confirmation: str = b"thisisinadifferentrepresentationalformat".decode(
            encoding="utf-8"
        )
        self.assertFalse(validate_password_pair(password, password_confirmation))

    def test_totally_different(self):
        password: str = "thesepasswordsaretotallydifferent"
        password_confirmation: str = "seetheyhavenothingincommon"
        self.assertFalse(validate_password_pair(password, password_confirmation))

    def test_valids(self):
        valid_a = "uycgbiq3uyrgtni8reoicwgsyrh8ygowofs84ry9we8hfc9"
        valid_b = "t74893r7e6tfgvd dhfuyre76gdyhfiwetusy"
        valid_c = "uygfcibw8crv 87g8qg 87ewahf8rg0q87rg08s\t97rehnsco"
        valid_d = " 73v 3974 7r9 w all the symbols `~!@#$%^&*())-=_+[]{}\\|;',./:\"<>? 38f7con"  # noqa: E501
        valid_e = "^ITB&FIRDHB uyfbiuycgo8y I&^GB FCHFDEYUJHGFDFGHBVCDERTYUJHCFGCFTYHBVFGJNBVGFSQAXCOLKM"  # noqa: E501
        valid_f = "POTSUNYBUFFALO"
        self.assertTrue(validate_password_pair(valid_a, valid_a))
        self.assertTrue(validate_password_pair(valid_b, valid_b))
        self.assertTrue(validate_password_pair(valid_c, valid_c))
        self.assertTrue(validate_password_pair(valid_d, valid_d))
        self.assertTrue(validate_password_pair(valid_e, valid_e))
        self.assertTrue(validate_password_pair(valid_f, valid_f))

    def test_invalid(self):
        self.assertFalse(validate_password_pair("ow8437conreu", "ovwinchotn ofuseoh8"))
        self.assertFalse(
            validate_password_pair("befkuayguoaie7032t87rFV&F", "RE%^YHBVCDybgicw y")
        )


class TestUserIsRegistered(TestCase):
    def setUp(self):
        user_email = "user@buffalo.edu"
        user = User.objects.create_user(
            username=user_email, email=user_email, password="password1234"
        )
        user.save()

        another_email = "another@buffalo.edu"
        another = User.objects.create_user(
            username=another_email, email=another_email, password="thisisvalid."
        )
        another.save()

        test_email = "test@buffalo.edu"
        test = User.objects.create_user(
            username=test_email, email=test_email, password="thisissecure"
        )
        test.save()

    def test_user_is_already_registered(self):
        self.assertTrue(user_is_registered("user@buffalo.edu"))
        self.assertTrue(user_is_registered("another@buffalo.edu"))
        self.assertTrue(user_is_registered("test@buffalo.edu"))

    def test_user_is_not_already_registered(self):
        self.assertFalse(user_is_registered("person@buffalo.edu"))
        self.assertFalse(user_is_registered("bad@gmail.com"))
        self.assertFalse(user_is_registered("signup@gmail.com"))
        self.assertFalse(user_is_registered("buildbob@buffalo.edu"))


class ValidateCredentialsOnRegister(TestCase):
    def setUp(self):
        user_email = "user@buffalo.edu"
        user = User.objects.create_user(
            username=user_email, email=user_email, password="password1234"
        )
        user.save()

        another_email = "another@buffalo.edu"
        another = User.objects.create_user(
            username=another_email, email=another_email, password="thisisvalid."
        )
        another.save()

        test_email = "test@buffalo.edu"
        test = User.objects.create_user(
            username=test_email, email=test_email, password="thisissecure"
        )
        test.save()

    def test_new_user_passwords_mismatch(self):
        self.assertFalse(
            validate_credentials_on_register(
                "name@buffalo.edu", "NAMESUNYBUFFALO", "NAME12345"
            )
        )

    def test_new_user_good_credentials(self):
        self.assertTrue(
            validate_credentials_on_register(
                "name@buffalo.edu", "NAMESUNYBUFFALO", "NAMESUNYBUFFALO"
            )
        )

    def test_user_tries_to_re_register_incorrect_login(self):
        self.assertFalse(
            validate_credentials_on_register(
                "test@buffalo.edu", "password1235", "password1235"
            )
        )

    def test_user_tries_to_re_register_correct_login(self):
        self.assertFalse(
            validate_credentials_on_register(
                "test@buffalo.edu", "password1234", "password1234"
            )
        )

    def test_new_user_bad_email(self):
        self.assertFalse(
            validate_credentials_on_register(
                "bademail@gmail.com", "password1234", "password1234"
            )
        )
