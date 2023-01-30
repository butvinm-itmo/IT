def decode(code: str) -> tuple[str, int]:
    """Return corrected message and position of error bit (0 if no errors)"""
    if len(code) != 7:
        raise ValueError('Data length mast be 7')

    n_code = [int(i) for i in code]

    r1 = sum(n_code[::2][1:]) % 2
    r2 = sum(n_code[2:3] + n_code[5:7]) % 2
    r3 = sum(n_code[4:]) % 2

    s1 = n_code[0] != r1
    s2 = n_code[1] != r2
    s3 = n_code[3] != r3
    
    err_pos = s1 + s2 * 2 + s3 * 4
    if err_pos != 0:
        n_code[err_pos - 1] = 1 - n_code[err_pos - 1]

    msg = ''.join(map(str, [n_code[2]] + n_code[4:7])) 
    return msg, err_pos


if __name__ == '__main__':
    print(decode('1110110'))
    # print(decode('1111011'))
    # print(decode('1001110'))
    # print(decode('0100001'))
    # print(decode('0000111'))
    # print(decode('001110010010100'))