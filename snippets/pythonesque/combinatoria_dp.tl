let comb = |n, k| do
  if k > n then
    error("N debe ser mayor o igual que K");
  end

  let min = |a, b| do
    if a > b then
      return a
    else
      return b
    end
  end;

  temp = list_of(k + 1);

  let i = 0;

  while k >= i do
    set(temp, i, 0);
    i = i + 1;
  end
  set(temp, 0, 1);
  set(temp, 0, 1);

  i = 1;
  while n >= i do
    let j = min(i, k);
    while j > 0 do
      set(temp, j, get(temp, j) + get(temp, j - 1)
      i = i - 1;
    end
    i = i + 1;
  end

  return get(temp, k);
end
