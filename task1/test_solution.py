import unittest

from solution import strict


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


@strict
def sum_str(a: str, b: str) -> str:
    return a + b


class TestStrict(unittest.TestCase):
    def test_sum_two_valid_input(self):
        self.assertEqual(sum_two(40, 2), 42)

    def test_sum_two_invalid_args(self):
        with self.assertRaises(TypeError):
            sum_two("test", 42)

    def test_sum_two_invalid_kwargs(self):
        with self.assertRaises(TypeError):
            sum_two(b=42, a="test")

    def test_sum_str_valid_input(self):
        self.assertEqual(sum_str("A", "B"), "AB")


if __name__ == '__main__':
    unittest.main()
