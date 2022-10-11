# variant 
# 367945 % 6 == 1 -> Eyes ;
# 367945 % 5 == 0 -> Nose -
# 367945 % 7 == 4 -> Mouth \
# ;-\

import re


EMOJI_PATTERN = r';-\\'


def count_pattern(string: str, pattern: str) -> int:
    """Count pattern includes in string

    Args:
        string (str): text
        pattern (str): target pattern
        
    Returns:
        int: count of pattern in text
    """

    return len(re.findall(pattern, string))


if __name__ == '__main__':
    with open('task1.test.txt', 'r') as f:
        answers = map(int, f.readline().split())
        for answer, line in zip(answers, f):
            eval_answer = count_pattern(line, EMOJI_PATTERN)
            print(answer, eval_answer)
            assert answer == eval_answer