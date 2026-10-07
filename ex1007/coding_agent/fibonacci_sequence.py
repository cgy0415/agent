def fibonacci_sequence(n):
    fib_sequence = [1, 1]
    while len(fib_sequence) < n:
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# 테스트: 처음 10개의 피보나치 수열 출력
print(fibonacci_sequence(10))