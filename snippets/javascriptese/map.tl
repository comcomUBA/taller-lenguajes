let map = |list, func| {
  let results = list_of(size(list));
  let i = 0;

  while i < size(list) {
    set(results, i, func(get(list, i)));
    i = i + 1;
  }

  return results;
};

print(map([4, 56, 67, 34, 34], |a| { return a % 2; }));
