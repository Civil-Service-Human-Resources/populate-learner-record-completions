from typing import List

def compare_string_arrays(array1: List[str], array2: List[str]):
    array1.sort()
    array2.sort()

    return array1 == array2