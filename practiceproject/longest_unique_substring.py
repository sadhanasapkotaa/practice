"""Longest Substring Without Repeating Characters"""

def length_of_longest_substring(s: str) -> int:
    """
    This function finds the length of the longest 
    substring without repeating characters.
    """
    last_index = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_index and last_index[ch] >= left:
            left = last_index[ch] + 1
        last_index[ch] = right
        best = max(best, right - left + 1)
    return best

if __name__ == "__main__":
    print(length_of_longest_substring("abcabcbb"))
    print(length_of_longest_substring("bbbbb"))
    print(length_of_longest_substring("pwwkew"))
