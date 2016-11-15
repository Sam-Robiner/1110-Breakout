def exponent(b,c):
    if c == 0:
        return 1
    else:
        return b * (exponent(b,c-1))