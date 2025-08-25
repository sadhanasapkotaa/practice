"""Importing List"""
from typing import List

def subarray_sum_equals_k(nums: List[int], k: int) -> int:
    """
    This function finds the number of continuous subarrays
    whose sum equals to k.
    """
    count = 0
    prefix = 0
    seen = {0: 1}
    for x in nums:
        prefix += x
        count += seen.get(prefix - k, 0)
        seen[prefix] = seen.get(prefix, 0) + 1
    return count

if __name__ == "__main__":
    print(subarray_sum_equals_k([1,2,3], 3))  # 2 ([1,2], [3])
    print(subarray_sum_equals_k([1,1,1], 2))  # 2 ([1,1], [1,1])
