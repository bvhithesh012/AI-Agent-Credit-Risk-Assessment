while True:
    try:
        n = int(input("Enter how many numbers: "))
        if n < 0:
            print("Please enter 0 or a positive integer.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a whole number.")

total = 0

for i in range(n):
    while True:
        try:
            num = int(input(f"Enter number {i + 1}: "))
            total += num
            break
        except ValueError:
            print("Invalid input. Please enter a whole number.")

print("Sum =", total)
