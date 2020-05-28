import random

s_box = [i for i in range(251)]
random.shuffle (s_box)

inv_s_box = [0]*256

for (i, j) in enumerate(s_box):
  inv_s_box[j] = i

s_box = s_box + [0]*(256-251)

print("s_box")
for i in range(16):
  for j in range(16):
    print("{:02x}".format(s_box[i*16+j]), end=' ')
  print()

print(s_box)

print()
print("inverse s_box")
for i in range(16):
  for j in range(16):
    print("{:02x}".format(inv_s_box[i*16+j]), end=' ')
  print()
print(inv_s_box)