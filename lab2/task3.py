# variant 367945 % 5 == 0

import re


EMAIL_PATTERN = r'^[\w_\.]+@([A-Za-z\.]+\.[A-Za-z]+)$'


def check_email(string: str) -> str:
    """Check if email is valid and find domain

    Args:
        string (str): string with email

    Returns:
        str: domain or "FAIL" if email incorrect
    """

    domain = re.match(EMAIL_PATTERN, string)
    if domain is None:
        return 'FAIL'
    
    return domain.group(1)


if __name__ == '__main__':
    with open('task3.test.txt', 'r') as f:
        for line in f:
            string, answer = line.split('|')
            string, answer = string.strip(), answer.strip()
            result = check_email(string)
            print('Input string:\t\t', string)
            print('Answer:\t\t\t', answer)
            print('Checking result:\t', result)
            assert result == answer
