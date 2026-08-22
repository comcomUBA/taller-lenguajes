let fizzbuzz = |a| do
  let i = 0;

  while i < 100 do
    if (i % 3 == 0) and (i % 5 == 0) then
      print("FizzBuzz\n");
    elsif i % 3 == 0 then
      print("Fizz\n");
    elsif i % 5 == 0 then
      print("Buzz\n");
    else
      print(i);
      print("\n");
    end

    i = i + 1;
  end
end;
