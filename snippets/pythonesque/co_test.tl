let call_range = |start, end, f| do
  let i = start;

  while i < end do
    i = i + 1;
    f(i);
  end

  return "Done!";
end;
let comm = |i| do
  print("comm:Yielding", i);
  print("comm:Got", yield(i));
end;
let generator = start(call_range, [0, 10, comm]);
print("Starting", generator);
print("Resume", resume(generator, 100));
print("Resume", resume(generator, 101));
print("Resume", resume(generator, 102));
print("Resume", resume(generator, 103));
print("Resume", resume(generator, 104));
print("Resume", resume(generator, 105));
print("Resume", resume(generator, 106));
print("Resume", resume(generator, 107));
print("Resume", resume(generator, 108));
print("Resume", resume(generator, 109));
print("Resume", resume(generator, 110));
print("Resume", resume(generator, 111));
