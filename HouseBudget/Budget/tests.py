from django.test import TestCase

# Create your tests here.
class MyFirstTestCase(TestCase):
    def test_success(self):
        assert 1 ==1, "jesli warunek nie przejdzie komunikat wyswietli sie wraz z błędem"
        self.assertTrue(True)

    def test_fail(self):
        self.assertTrue(False)

    def test_error(self):
        raise ValueError("Error has been raise")

