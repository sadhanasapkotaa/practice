"""Importing List Type"""
from typing import List

def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    This function merges overlapping intervals in a list.
    """
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0][:]]
    for start, end in intervals[1:]:
        last_end = merged[-1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
    return merged

if __name__ == "__main__":
    print(merge_intervals([[1,3],[3,4],[6,8],[8,10]]))
    print(merge_intervals([[1,2],[3,4]]))
