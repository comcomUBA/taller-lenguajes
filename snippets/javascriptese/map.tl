let map = |list, func| {
  let results = list_of(size(list));
  let i = 0;

  while i < size(list) {
    set(results, i, func(get(list, i)));
    i = i + 1
  };

  results
};

print(map([-1, 56, 67, 34, 34], |a| a % 2))
