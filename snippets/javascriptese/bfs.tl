bfs = |adj_list, visit| {
  let queue = [0];
  let visited = [];

  while not is_empty(queue) {
    let node = pop(queue);

    if not contains(visited, node) {
      visit(node);
      push(visited, node);
      concat(queue, adj_list[node])
    }
  }
}

bfs([[1, 2], [0, 1, 3], [0, 3], [1, 3]], print)
