import unittest
from random import randint

import exponentiation

class TestExponentiation(unittest.TestCase):

    def test_pow_step_by_step(self):
        for i in range(0, 10):
            x   = randint(2, 2048)
            exp = randint(2, 2048)
            mod = randint(2, 2048)

            self.assertEqual(
                exponentiation.pow_step_by_step(x, exp, mod),
                x**exp % mod,
                """
                Exponentiation failed. Tried to compute %d**%d %% %d
                """ % (x, exp, mod)
            )


    def test_pow_binary(self):
        for i in range(0, 50):
            x   = randint(2, 2048)
            exp = randint(2, 2048)
            mod = randint(2, 2048)

            self.assertEqual(
                exponentiation.pow_binary(x, exp, mod),
                x**exp % mod,
                """
                Exponentiation failed. Tried to compute %d**%d %% %d
                """ % (x, exp, mod)
            )


    def test_partition_window_same_width(self):
        correct_data = [
            { "exp": 0b1010111, "window_size": 6, "result": [0b010111, 0b1] },
            { "exp": 0b11010111, "window_size": 3, "result": [0b111, 0b010, 0b11] },
            { "exp": 0b11010111, "window_size": 6, "result": [0b010111, 0b11] },
            { "exp": 0b1010001, "window_size": 6, "result": [0b010001, 0b1] },
            { "exp": 0b1100010, "window_size": 5, "result": [0b00010, 0b11] },
            { "exp": 0b1010110, "window_size": 3, "result": [0b110, 0b010, 0b1] },
        ]

        for d in correct_data:
            self.assertEqual(
                list(map(
                    lambda el: el["value"],
                    exponentiation.partition_window_same_width(d["exp"], d["window_size"])[0]
                )),
                d["result"],
                """
                Partitioning failed with exp = %d, window_size = %d
                """ % (d["exp"], d["window_size"])
            )


    def test_partition_window_clnw(self):
        correct_data = [
            {
                "exp": 0b111001010001,
                "nonzero_window_size": 3,
                "result": [
                    {"value": 0b001, "length": 3}, {"value": 0b0, "length": 1},
                    {"value": 0b101, "length": 3}, {"value": 0b00, "length": 2},
                    {"value": 0b111, "length": 3}
                ]
            },
        ]

        for d in correct_data:
            self.assertEqual(
                exponentiation.partition_window_clnw(d["exp"], d["nonzero_window_size"])[0],
                d["result"],
                """
                Partitioning failed with exp = %d, nonzero_window_size = %d
                """ % (d["exp"], d["nonzero_window_size"])
            )


    def test_pow_window_same_width(self):
        for i in range(0, 50):
            x   = randint(2, 2048)
            exp = randint(4, 2048)
            mod = randint(2, 2048)
            window_size = randint(2, exp.bit_length() - 1)

            self.assertEqual(
                exponentiation.pow_window_same_width(x, exp, mod, window_size),
                x**exp % mod,
                """
                Exponentiation failed. Tried to compute %d**%d %% %d with window size %d
                """ % (x, exp, mod, window_size)
            )


    def test_pow_window_clnw(self):
        for i in range(0, 50):
            x   = randint(2, 2048)
            exp = randint(4, 2048)
            mod = randint(2, 2048)
            nonzero_window_size = randint(2, exp.bit_length() - 1)

            self.assertEqual(
                exponentiation.pow_window_clnw(x, exp, mod, nonzero_window_size),
                x**exp % mod,
                """
                Exponentiation failed. Tried to compute %d**%d %% %d with window size %d
                """ % (x, exp, mod, nonzero_window_size)
            )


if __name__ == '__main__': unittest.main()