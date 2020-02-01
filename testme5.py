from collections import Counter

z1 = [[[1, 1], 2, 3], [[4, 5], 5, 6], [[4, 5], 5, 6], [2, 3, [1, 1]], [2, 5, [1, 1]]]

temp = Counter([tuple(sorted(x)) for x in z1])

z2 = [list(k) for k, v in temp.items() if v == 1]
print(z2)  # [[4, 5, 6], [1, 2, 5]]from collections import Counter

z1 = [[1, 2, 3], [4, 5, 6], [2, 3, 1], [2, 5, 1]]

temp = Counter([tuple(sorted(x)) for x in z1])

z2 = [list(k) for k, v in temp.items() if v == 1]
print(z2)  # [[4, 5, 6], [1, 2, 5]]
