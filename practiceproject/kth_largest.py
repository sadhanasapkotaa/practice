"""Importing typing and heapq"""
from typing import List
import heapq

def kth_largest(nums: List[int], k: int) -> int:
    """
    This function finds the k-th largest element in a list.
    """
    return heapq.nlargest(k, nums)[-1]

if __name__ == "__main__":
    print(kth_largest([3,2,1,5,6,4], 2))
    print(kth_largest([3,2,3,1,2,4,5,5,6], 4))
