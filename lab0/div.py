from string import hexdigits 
from math import factorial


FS = [1]

def get_fs(count: int):
    if len(FS) == count:
        return
    
    if len(FS) == 1:
        FS.append(2)
    else:
        FS.append(FS[-1] + FS[-2])

    get_fs(count)


def convert_Z(n: str, from_base: int, to_base: int):
    n = int(n, from_base)

    r = ''
    while n > 0:
        r += hexdigits[n % to_base]
        n //= to_base

    if not r:    
        r = '0'

    r = r[::-1]
    return r


def mantiss_to_dex(m: str, from_base: int):
    m = m.lower()
    r = 0
    for i, a in enumerate(m):
        r += hexdigits.find(a) * from_base**(- (i + 1)) 

    return r

def convert_R(r: str, from_base: int, to_base: int):
    r = r.lower()
    a, b = r.split(',')
    ar = convert_Z(a, from_base, to_base)

    b = mantiss_to_dex(b, from_base)
    br = ''
    for i in range(5):
        m = b * to_base
        n = int(m)
        br += hexdigits[n]
        if m - n != 0:
            b = m - n
        else:
            break

    return f'{ar}.{br}'    


def convert_to_fact(n: str, from_base: str):
    n = int(n, from_base)
    r = ''
    for i in range(2, 10*10):
        m = n % i 
        r += str(m)
        n //= i
        if n == 0:
            break
    
    r = r[::-1]
    return r


def convert_from_fact(n: str, to_base: int):
    r = 0
    l = len(n)
    for i, a in enumerate(n):
        r += factorial(l - i) * int(a) 
    
    if to_base != 10:
        r = convert_Z(r, 10, to_base)

    return r


def convert_from_fib(n: str, to_base: int):
    get_fs(40)
    r = 0
    l = len(n)
    for i, a in enumerate(n):
        r += FS[l - i - 1] * int(a) 

    if to_base != 10:
        r = convert_Z(r, 10, to_base)

    return r

def convert_from_neg(n: str, from_base: int, to_base: int):
    r = 0
    l = len(n)
    for i, a in enumerate(n):
        r += int(a) * from_base**(l - i - 1) 

    return r

print(convert_from_neg('2018', -10, 10))

# print(convert_from_fib('10010010101', 10))
# print(convert_from_fact('108', 10))

# print(convert_R('41,17', 8, 2)) # 6
# print(convert_R('0,100001', 2, 16)) # 7
# print(convert_R('0,000001', 2, 10)) # 8
# print(convert_R('45,19', 16, 10)) # 9
# print(convert_to_fact('232', 10)) # 10
# print(convert_from_fib('1001001', 10)) # 11
# print(convert_from_fib('1000000010', 10)) # 12
# print(convert_from_neg('1786', -10, 10)) # 13


