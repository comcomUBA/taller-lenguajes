
|asd| asd + 1


if cond do return 123 end

let bfs = |adj_list, visit| do
  let queue = [0];
  let visited = [];

  while not is_empty(queue) do
    let node = pop(queue);

    if not contains(visited, node) then
      visit(node);
      push(visited, node);
      concat(queue, adj_list[node])
    end
  end
end;

bfs([[1, 2], [0, 1, 3], [0, 3], [1, 3]], print)
