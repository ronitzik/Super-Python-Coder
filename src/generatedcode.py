def is_prime(n):
    if not isinstance(n, int) or n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def main():
    while True:
        try:
            n = int(input("Please enter a number: "))
            break
        except ValueError:
            print("Invalid input, please enter an integer.")
    print(is_prime(n))


def run_tests():
    results = []
    results.append(is_prime(2) == True)
    results.append(is_prime(3) == True)
    results.append(is_prime(4) == False)
    results.append(is_prime(5) == True)
    results.append(is_prime(9) == False)
    results.append(is_prime(11) == True)
    results.append(is_prime(15) == False)
    results.append(is_prime(17) == True)
    results.append(is_prime(1) == False)
    results.append(is_prime(-3) == False)
    results.append(is_prime(0) == False)
    results.append(is_prime(25) == False)
    print("Test results:", results)


if __name__ == "__main__":
    main()
    run_tests()