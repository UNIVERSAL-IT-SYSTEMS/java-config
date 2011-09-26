import os, unittest

from java_config_2.Version import Version, InvalidVersionStringError

class TestVersion(unittest.TestCase):

    def setUp(self):
        pass

    def test_version_equal(self):
        self.assertTrue(Version('1.1') == Version('1.1'))
        self.assertTrue(Version('1.1') >= Version('1.1'))
        self.assertTrue(Version('1.1') <= Version('1.1'))

        self.assertFalse(Version('1.1') != Version('1.1'))

    def test_version_unequal(self):
        self.assertTrue(Version('1.1') < Version('1.1.0'))
        self.assertTrue(Version('1.1') < Version('1.2'))
        self.assertTrue(Version('1.1') < Version('2.0.0'))

        self.assertFalse(Version('1.1') > Version('1.1.0'))
        self.assertFalse(Version('1.1') > Version('1.2'))
        self.assertFalse(Version('1.1') > Version('2.0.0'))

    def test_compare_to(self):
        self.assertTrue(Version('1.1').compare_to(Version('1.1.0')) < 0)
        self.assertTrue(Version('1.1').compare_to(Version('1.1')) == 0)
        self.assertTrue(Version('1.1').compare_to(Version('1.0')) > 0)

    def test_not_a_version(self):
        with self.assertRaises(InvalidVersionStringError):
            Version('1.3b')
        with self.assertRaises(InvalidVersionStringError):
            Version(2222)
        with self.assertRaises(InvalidVersionStringError):
            Version('')
        with self.assertRaises(InvalidVersionStringError):
            Version(None)
