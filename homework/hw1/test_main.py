import unittest
from main import power2n_1, power2n_2b, power2n_3

class TestPower2n(unittest.TestCase):
    def test_results(self):
        n = 10
        expected = 1024
        self.assertEqual(power2n_1(n), expected)
        self.assertEqual(power2n_2b(n), expected)
        self.assertEqual(power2n_3(n), expected)

if __name__ == '__main__':
    unittest.main()
