let function = |a, b, c| do
    let string  = "hello, world";
    let number  = 3.14;
    let boolean = true;

    if a == number then
        print("a is pi");
    end

    while b > 0 do
        print("b is currently: ", b);
        b = b - 1;
    end
end;
