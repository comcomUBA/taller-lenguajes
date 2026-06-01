let fib = |cnt|
  let a = 0;
  let b = 1;

  while cnt > 0 do
    let temp;

    temp = b;
    b = a + b;
    a = temp;

    cnt = cnt - 1
  end

  return b
end
