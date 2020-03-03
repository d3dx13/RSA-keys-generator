import random
import time

def bin_to_int(input):
    return int(bin(0)[:2:] + input, 2)

def int_to_bin(input):
    return str(bin(input)[2::])

def generate(byteSize, bias_min, bias_max):
    global KEY_PUBLIC, KEY_PRIVATE, KEY_MOD
    def bin_generate(byte_len):
        byte_len = int(byte_len)
        res = '1'
        for i in range(byte_len - 1):
            res += str(random.randrange(0, 2))
        return bin_to_int(res)
    def extended_gcd(aa, bb):
        lastremainder, remainder = abs(aa), abs(bb)
        x, lastx, y, lasty = 0, 1, 1, 0
        while remainder:
            lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
            x, lastx = lastx - quotient * x, x
            y, lasty = lasty - quotient * y, y
        return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)
    def prime_regenerate():
        global first, second, t, KEY_MOD
        first = bin_generate(len_first)
        second = bin_generate(len_second)
        while (not (miller_rabin_prime(first, len_first, len_first))):
            first = bin_generate(len_first)
        print(time.time())
        while ((not (miller_rabin_prime(second, len_second, len_second))) or second == first):
            second = bin_generate(len_second)
        print(time.time())
        KEY_MOD = first * second
        t = (first - 1) * (second - 1)
    byteSize = int(byteSize)
    bias = random.randrange(int(bias_min), int(bias_max) + 1)
    print(byteSize, ' = byte len')
    print(bias, ' = bias')
    len_first = byteSize//2 - bias//2
    len_second = byteSize//2 + bias//2 + bias%2
    prime_regenerate()
    count = 0
    while True:
        count += 1
        KEY_PUBLIC = bin_generate(byteSize)
        while (not (miller_rabin_prime(KEY_PUBLIC, byteSize, byteSize))):
            KEY_PUBLIC = bin_generate(byteSize)
        print(time.time())
        g, x, y = extended_gcd(KEY_PUBLIC, t)
        if KEY_PUBLIC < t and g == 1:
            break
        if (count > 5):
            count = 0
            prime_regenerate()
    g, x, y = extended_gcd(KEY_PUBLIC, t)
    if g != 1:
        raise ValueError
    KEY_PRIVATE = x % t
    return KEY_PUBLIC, KEY_PRIVATE, KEY_MOD


def miller_rabin_prime(n, trials, stupid_trials):
    assert n >= 2
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    s = 0
    d = n - 1
    for i in range(2, min(stupid_trials, n-1)):
        if (n % i == 0):
            return False
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert ((2 ** s) * d == n - 1)
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, (2 ** i) * d, n) == n - 1:
                return False
        return True
    for i in range(trials):
        a = random.randrange(2, n)
        if try_composite(a):
            return False
    return True

byte_len = 2048+64+64*3
res = generate(byte_len, 30, 120)
tt = str(time.strftime("%d_%b_%Y__%H-%M-%S", time.gmtime()))
f = open(str(byte_len) + '_byte__' + tt +'.txt', 'w')
f.write('KEY_PUBLIC  == ' + str(res[0]) + '\n')
f.write('KEY_PRIVATE == ' + str(res[1]) + '\n')
f.write('KEY_MOD     == ' + str(res[2]) + '\n')
f.close()