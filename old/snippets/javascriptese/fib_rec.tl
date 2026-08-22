let fib = |a| {
  if (a == 1) or (a == 0) {
    return 1;
  } else {
    return fib(a - 1) + fib(a - 2);
  }
};

print("fib(0)", fib(0));
print("fib(1)", fib(1));
print("fib(5)", fib(5));
print("fib(10)", fib(10));
