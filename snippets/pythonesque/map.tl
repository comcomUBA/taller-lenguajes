let map = |list, func| do
  let results = list_of(size(list));
  let i = 0;

  while i < size(list) do
    set(results, i, func(get(list, i)));
    i = i + 1;
  end

  return results;
end;

map([4, 56, 67, 34, 34], |a| do return a % 2; end);
