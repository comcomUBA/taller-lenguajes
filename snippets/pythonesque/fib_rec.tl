let fib = |a|
  if (a == 1) or (a == 0) then
    return 1
  else
    return fib(a - 1) + fib(a - 2)
  end
end
