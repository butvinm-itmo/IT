# variant 367945 % 6 == 1

import re


DUPLICATES_PATTERN = r'(\w+(?=\W))\W*(\1\W+)+'


def remove_duplicates(string: str) -> str:
    """Remove duplicate words

    Args:
        string (str): text

    Returns:
        str: text without duplicates
    """
    
    string = string.replace('  ', ' ')
    return re.sub(DUPLICATES_PATTERN, lambda x: x.groups()[-1], string)


if __name__ == '__main__':
    with open('task2.test.txt', 'r') as f:
        for line in f:
            mistaken, correct = line.split('|')
            mistaken, correct = mistaken.strip(), correct.strip()
            result = remove_duplicates(mistaken)
            print('Input with mistakes:\t', mistaken)
            print('Correct text:\t\t', correct)
            print('Removes result:\t\t', result)
            assert result == correct


