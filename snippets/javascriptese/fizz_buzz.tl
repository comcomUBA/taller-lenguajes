let fizzbuzz = |a| {
  let i = 0;

  while i < 100 {
    if (i % 3 == 0) and (i % 5 == 0) {
      print("FizzBuzz")
    } elsif i % 3 == 0 {
      print("Fizz")
    } elsif i % 5 == 0 {
      print("Buzz")
    } else {
      print(i)
    };

    i = i + 1
  }
};

fizzbuzz(10)
