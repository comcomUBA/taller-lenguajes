let fib = |cnt| {
  let a = 0;
  let b = 1;
  let temp;

  while cnt > 0 {
    temp = b;
    b = a + b;
    a = temp;

    cnt = cnt - 1;
  }

  return b;
};

print("fib(0)", fib(0));
print("fib(1)", fib(1));
print("fib(5)", fib(5));
print("fib(10)", fib(10));
