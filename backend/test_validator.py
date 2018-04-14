import unittest
from models import Validator

class TestCard(unittest.TestCase):

    def testMinLength(self):
        self.assertFalse(Validator.minLength(None, 2))
        self.assertFalse(Validator.minLength(None, -2))
        self.assertTrue(Validator.minLength('ab', 2))
        self.assertFalse(Validator.minLength('', 2))
        self.assertTrue(Validator.minLength('abcdefgh', 2))

    def testMaxLength(self):
        self.assertFalse(Validator.maxLength(None, 10))
        self.assertFalse(Validator.maxLength(None, -2))
        self.assertTrue(Validator.maxLength('abcd', 4))
        self.assertTrue(Validator.maxLength('', 2))
        self.assertFalse(Validator.maxLength('abcdefghijk', 10))

    def testIsLengthBetween(self):
        self.assertFalse(Validator.isLengthBetween(None, 2, 10))
        self.assertFalse(Validator.isLengthBetween('abcd', 5, 10))
        self.assertFalse(Validator.isLengthBetween('abcdefghijk', 5, 10))
        self.assertTrue(Validator.isLengthBetween('abcdef', 5, 10))
        self.assertTrue(Validator.isLengthBetween('abcdefghij', 5, 10))

    def testIsInt(self):
        self.assertTrue(Validator.isInt(10))
        self.assertTrue(Validator.isInt(0))
        self.assertTrue(Validator.isInt(-3))

        self.assertFalse(Validator.isInt(10.2))
        self.assertFalse(Validator.isInt(None))
        self.assertFalse(Validator.isInt(''))
        self.assertFalse(Validator.isInt('Aron'))

    def testIsLessThanOrEqual(self):
        self.assertFalse(Validator.isLessThanOrEqual(None, 10))
        self.assertFalse(Validator.isLessThanOrEqual('abc', 10))
        self.assertFalse(Validator.isLessThanOrEqual(11, 10))
        self.assertTrue(Validator.isLessThanOrEqual(10, 10))
        self.assertTrue(Validator.isLessThanOrEqual(8, 10))

    def testIsGreaterThanOrEqual(self):
        self.assertFalse(Validator.isGreaterThanOrEqual(None, 10))
        self.assertFalse(Validator.isGreaterThanOrEqual('abc', 10))
        self.assertFalse(Validator.isGreaterThanOrEqual(9, 10))
        self.assertTrue(Validator.isGreaterThanOrEqual(10, 10))
        self.assertTrue(Validator.isGreaterThanOrEqual(11, 10))

    def testIsBetween(self):
        self.assertFalse(Validator.isBetween(None, 2, 10))
        self.assertFalse(Validator.isBetween('', -1, 2))
        self.assertFalse(Validator.isBetween(0, 1, 1))
        self.assertFalse(Validator.isBetween(1, 1, 0))

        self.assertTrue(Validator.isBetween(1, 0, 1))
        self.assertTrue(Validator.isBetween(1, 1, 2))
        self.assertTrue(Validator.isBetween(1, 0, 3))

    def testIsPrintable(self):
        self.assertFalse(Validator.isPrintable('\n'))
        self.assertFalse(Validator.isPrintable('abc\n'))
        self.assertTrue(Validator.isPrintable('abc'))

    def testIsvalidEmail(self):
        self.assertFalse(Validator.isValidEmail('abc'))
        self.assertFalse(Validator.isValidEmail('abc.gmail'))
        self.assertFalse(Validator.isValidEmail('abc@gmail'))
        self.assertFalse(Validator.isValidEmail('abc@@mail.com'))

        self.assertTrue(Validator.isValidEmail('abc@gmail.com'))
        self.assertTrue(Validator.isValidEmail('abc.def@gmail.com'))

        data = {'username': 'abc', 'email': 'abd@def.com'}
        self.assertTrue(Validator.isValidPlayer(data))

if __name__ == "__main__":
    unittest.main()
