from typing import Callable, List, Tuple, Dict
import math
import logging

"""
The algorithms here are loosely based on the 1995 paper 'Analysis of Sliding
Window Techniques for Exponentiation' by C.K.Koç.
"""

def pow_step_by_step(x, exp, mod):
    """
    Naive method of computing x**exp % mod step by step. Takes exp
    multiplications.
    """

    y = 1
    for i in range(0, exp):
        y = (y * x) % mod
    return y

def pow_binary(x, exp, mod):
    """
    The most well known way to more efficiently compute x**exp % mod. This goes
    through the binary representation of the exponent from right to left and
    decides wether only to square or also multiply.

    Example: Let exp = 13 = 0b1011. This algorithm will then compute:

                   y ← 1
                   y ← y * x = x    [exp_0 = 1 => multiplication]
                   y ← y * y = x²
                   y ← y * x = x³   [exp_1 = 1 => multiplication]
                   y ← y * y = x⁶
                   y ← y * y = x¹²  [exp_2 = 0 => no multiplication]
                   y ← y * x = x¹³  [exp_3 = 1 => multiplication]
    """

    y = 1
    while exp != 0:
        if (exp % 2) != 0:
            y = (y * x) % mod
            exp = exp - 1
        exp = exp >> 1
        x = (x * x) % mod
    return y


def pow_window(
        x: int, exp: int, mod: int,
        partition_window: Callable[..., Tuple[List[Dict[str, int]], int]],
        *args
) -> int:
    """
    Computes and returns (x**exp) % mod by partitioning exp according to
    partition_window.

    partition_window is a callable which will be passed exp and *args. It's
    return type is somewhat complex: It needs to return a tuple containing the
    partitions as its first element and the bit-length of the biggest
    partition. The partitions themselves are a list of dictionaries. These
    dictionaries in turn are of the form {"value": some_val, "length":
    some_val}. A full return value might look like this:

    [
        [ { "value": 5, "length": 3 }, { "value": 2, "length": 2 } ],
        3
    ]

    The reasoning to include the bit-length of the biggest partition is that the
    partitioning function has more information about the partitioning process
    and can therefore decide on this value more efficiently than looping over
    all lengths. For a reference implementation of partition_window, see
    partition_window_same_width.
    """

    window_partitions, max_window_partition_length = partition_window(exp, *args)
    logging.debug("window_partitions           : %s" % str(window_partitions))
    logging.debug("max_window_partition_length : %d" % max_window_partition_length)

    # In reality, we would compute this for many different values of x,
    # window_size and mod and store it on disk.
    precomputed_powers_of_x = [
        x**i % mod for i in range(0, 2**max_window_partition_length, 1)
    ]
    logging.debug("precomputed_powers_of_x     : " + str(precomputed_powers_of_x))

    y = precomputed_powers_of_x[window_partitions[len(window_partitions) - 1]["value"]]; logging.debug("y: %d" % y)
    for i in reversed(range(0, len(window_partitions) - 1)):
        for j in range(0, window_partitions[i]["length"]):
            y = (y * y) % mod
        if window_partitions[i]["value"] != 0:
            y = (y * precomputed_powers_of_x[window_partitions[i]["value"]]) % mod
    return y


def partition_window_clnw(
        exp: int, nonzero_window_size: int
) -> [Tuple[List[Dict[str, int]]], int]:
    """
    Partitions exp into windows of variable length zero-words and
    nonzero_window_size length nonzero-words. CLNW stands for 'Constant Length
    Nonzero Windows'. The algorithm will scan the binary representation of exp
    from right to left and form the partitions.

    C.K.Koç explains this more formally in terms of the two states ZW and NW
    [page 3]:
    - ZW: Check the incoming single bit: if it is a 0, then stay in ZW; else go
      to NW.
    - NW: Stay in NW until all d bits are collected. Then check the incoming
      single bit: if it is a 0, then go to ZW; else go to NW.

    As an example, consider exp = 0b111001010001 and nonzero_window_size = 3. This
    function will partition exp like so:

                                111 00 101 0 001
    """

    if nonzero_window_size > exp.bit_length():
        raise Exception("nonzero_window_size is bigger than exp")

    window_partitions = []; max_length = 0
    position = 0; length = 0

    while position < exp.bit_length():
        if not exp & 1 << position:
            # ---------- [ZW] Zero-Word -------------
            logging.debug("starting position: %d" % position)
            while not exp & 1 << position:
                position = position + 1
                length = length + 1
            window_partitions.append({"value": 0, "length": length})
            logging.debug("found ZW: %6s ending at position %d" % (("0" * length), position))
            max_length = max(max_length, length); length = 0
        else:
            # ---------- [NW] Nonzero-Word ----------
            logging.debug("starting position: %d" % position)
            while length < nonzero_window_size:
                position = position + 1
                length = length + 1
            value = exp >> (position - length) & ((1 << length) - 1)
            window_partitions.append({"value": value, "length": length})
            logging.debug("found NW: %6s ending at position %d, length %d"
                  % ("{0:b}".format(value), position, length))
            max_length = max(max_length, length); length = 0
        pass

    return [window_partitions, max_length]


def partition_window_same_width(
        exp: int, window_size: int
) -> [Tuple[List[Dict[str, int]]], int]:
    """
    Partitions exp into windows of equal lenght. As an example, consider exp =
    215 and window_size = 3:

    Arithmetically, we rewrite exp as 215 = 3 * 2**6 + 2 * 2**3 + 7. More
    intuitively, we can algorithmically achieve this by splitting the binary
    representation of exp:

                              215 = 0b11010111
                              d_0 = 0b     111 = 7
                              d_1 = 0b  010    = 2
                              d_2 = 0b11       = 3
    """

    if window_size >= exp.bit_length():
        raise Exception("window_size is bigger than or equal to exp")

    window_partitions = [
        {
            "value": ((1 << window_size) - 1) & (exp >> i * window_size),
            "length": window_size
        }
        for i in range(0, math.ceil(exp.bit_length() / window_size))
    ]
    max_window_partition_length = window_size

    return [ window_partitions, max_window_partition_length ]


def pow_window_same_width(x, exp, mod, window_size):
    return pow_window(x, exp, mod, partition_window_same_width, window_size)

def pow_window_clnw(x, exp, mod, nonzero_window_size):
    return pow_window(x, exp, mod, partition_window_clnw, nonzero_window_size)