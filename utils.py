from collections import Counter

def get_most_present_values(lst):
    counter = Counter(lst)
    most_present = counter.most_common(20)
    return [value for value, _ in most_present]