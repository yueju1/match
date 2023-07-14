n = 0

a = [1, 2, 3, 4, 5]
print(a)
for i in range(len(a)):
    while a[i] > 3:
        n += 1
        continue

print(n)

