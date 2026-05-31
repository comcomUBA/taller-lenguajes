let fib = |cnt|
  let a = 0;
  let b = 1;
  let temp;

  while cnt > 0:
    temp = b;
    b = a + b;
    a = temp;

    cnt = cnt - 1
  end

  return b
end
