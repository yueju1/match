n = 0

a = [1, 2, 3, 4, 5]
print(a)
for i in range(len(a)):
    while a[i] > 3:
        n += 1
        continue

print(n)


def main():
    global my_variable
    my_variable = 10

if __name__ == "__main__":
    main()
    print(my_variable)
