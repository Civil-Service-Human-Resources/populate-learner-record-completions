import modules.utils.ArrayUtil as ArrayUtil

def test_compare_string_array_returns_true_if_arrays_are_exactly_the_same():
    array1 = ["a", "b", "c"]
    array2 = ["a", "b", "c"]
    
    same_ids = ArrayUtil.compare_string_arrays(array1, array2)
    assert same_ids

def test_compare_string_array_returns_true_if_arrays_are_the_same_but_different_order():
    array1 = ["a", "b", "c"]
    array2 = ["a", "c", "b"]
    
    same_ids = ArrayUtil.compare_string_arrays(array1, array2)
    assert same_ids

def test_compare_string_array_returns_false_if_two_arrays_have_different_sizes():
    array1 = ["a", "b", "c"]
    array2 = ["a", "b"]
    
    same_ids = ArrayUtil.compare_string_arrays(array1, array2)
    assert not same_ids

def test_compare_string_array_returns_false_if_two_arrays_have_same_size_but_different_values():
    array1 = ["a", "b", "c"]
    array2 = ["a", "b", "d"]
    
    same_ids = ArrayUtil.compare_string_arrays(array1, array2)
    assert not same_ids