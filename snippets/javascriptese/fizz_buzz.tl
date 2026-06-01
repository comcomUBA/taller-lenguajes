let fizzbuzz = |a| {
  let i = 0;

  while i < 100 {
    if (i % 3 == 0) && (i % 5 == 0) {
        print("FizzBuzz\n");
    } elsif i % 3 == 0 {
      print("Fizz\n");
    } elsif i % 5 == 0 {
      print("Buzz\n");
    } else {
      print(i);
      print("\n");
    }

    i = i + 1
  }
}

# Sin elsif
let fizzbuzz = |a| {
  let i = 0;

  while i < 100 {
    if (i % 3 == 0) && (i % 5 == 0) {
        print("FizzBuzz\n");
    } else {
      if i % 3 == 0 {
        print("Fizz\n");
      } else {
        if i % 5 == 0 {
          print("Buzz\n");
        } else {
          print(i);
          print("\n");
        }
      }
    }
    i = i + 1;
  }
}

