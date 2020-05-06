from exponentiation import *
import logging


def main():
    # logging.getLogger().setLevel(logging.DEBUG)

    print("")

    # print("result: %d" % pow_window(
    #     123, 215, 511, partition_window_same_width, 3
    # ))
    # print("result: %d" % pow_window_same_width(
    #     x = 123, exp = 215, mod = 511, window_size = 3
    # ))
    # print("result: %d" % pow_window_clnw(
    #     x = 123, exp = 215, mod = 511, nonzero_window_size = 3
    # ))
    print("result: %d" % pow_window_clnw(
        x = 123, exp = 0b111001010001, mod = 511, nonzero_window_size = 3
    ))

if __name__ == '__main__': main()