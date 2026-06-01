let comb = |n, k|
  if k > n:
    error("N debe ser mayor o igual que K")
  end

  let min = |a, b|
    if a > b: a else b end
  end;

  temp = list_of(k + 1);

  let i = 0;

  while k >= i do
    set(temp, i, 0);
    i = i + 1
  end
  temp[0] = 1;
  set(temp, 0, 1);

  i = 1;
  while n >= i do
    let j = min(i, k);
    while j > 0 do
      set(temp, j, temp[j] + temp[j - 1]);
      i = i - 1
    end
    i = i + 1
  end

  return temp[k]
end
