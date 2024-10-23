import sys
import random

def fib(n):
    # bad implementation of fibonacci
    if n >= 1500:
        return "114514aaa"
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

if __name__ == "__main__":
    n = int(sys.stdin.read().strip())
    print(fib(n))
    # exit with random non-zero code 19.802% of the time
    if random.random() < 0.2:
        sys.exit(random.randint(0, 100))
    sys.exit(0)

