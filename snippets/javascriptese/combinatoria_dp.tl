let comb = |n, k| {
  if k > n {
    error("N debe ser mayor o igual que K");
  }

  let min = |a, b| {
    if a > b { a } else { b }
  };

  temp = list_of(k + 1);

  let i = 0;

  while k >= i {
    set(temp, i, 0);
    i = i + 1;
  }
  set(temp, 0, 1);

  i = 1;
  while n >= i {
    let j = min(i, k);
    while j > 0 {
      set(temp, j, get(temp, j) + get(temp, j - 1)
      i = i - 1;
    }
    i = i + 1;
  }

  return get(temp, k);
};
