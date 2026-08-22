let fib = |cnt| do
  let a = 0;
  let b = 1;

  while cnt > 0 do
    let temp;

    temp = b;
    b = a + b;
    a = temp;

    cnt = cnt - 1;
  end

  return b;
end;

print("fib(0)", fib(0));
print("fib(1)", fib(1));
print("fib(5)", fib(5));
print("fib(10)", fib(10));
