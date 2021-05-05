import os
import re


def measure_pkg(name: str) -> tuple[int, float, float]:
    """Measures pkg using bundle phobia

    Args:
        name (str): Package to be measured name

    Returns:
        tuple[int, float, float]: A tuple containing the number of dependencies, weight and gzipped weight in KB
    """

    os.system('bundle-phobia {} > result.txt'.format(name))

    # read result
    results = []
    with open('result.txt') as f:
        results = list(f)

    # check if error
    weight_line = next(
        (line for line in results if 'i {}'.format(name) in line), None)

    results = re.findall(
        r'.*has (\d+).*of (\d+.\d+).*\((\d+.?\d+).*', weight_line or '')

    os.remove('result.txt')

    return results[0] if results else (None, None, None)
