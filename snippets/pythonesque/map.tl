map = |list, func|
  let results = list_of(size(list));
  let i = 0;

  while i < size(list):
    results[i] = func(temp[i]);
    i = i + 1
  end

  results
end

map([4, 56, 67, 34, 34], |a| a % 2 end)
