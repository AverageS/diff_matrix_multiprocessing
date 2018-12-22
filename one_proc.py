import itertools as its
from pprint import pprint

s = [3, 0, 6, 2, 7, 4, 5, 1]
ss = [s[x] for x in s]

Ps1 = [[0 for _ in range(8)] for _ in range(8)]

for i, j in its.product(s, s):
    value = i ^ j
    image = s[i] ^ s[j]
    Ps1[value][image] += 1

pprint(Ps1)

Ps2 = []

for value in range(0, 8):
    row = [0 for _ in range(8)]
    for i in range(0, 8):
        j = value ^ i
        image = s[i] ^ s[j]
        row[image] += 1
    Ps2.append(row)

# for i in range(8):
#     a = s[i]
#
#     v = [0]*8
#     for j in range(8):
#         v[j] = a ^ s[j]
#
#     ##
#     ##
#
#     b = ss[i]
#
#     vv = [0]*8
#     for j in range(8):
#         vv[j] = b ^ ss[j]
#
#     ##
#     ##
#
#     for x, y in zip(v, vv):
#         Ps2[x][y] += 1

pprint(Ps2)
print(Ps1 == Ps2)
