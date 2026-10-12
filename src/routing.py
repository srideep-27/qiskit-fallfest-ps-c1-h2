"""Helpers for checking whether processor qubits are connected."""

from collections import deque


def shortest_path(coupling_edges, start, goal):
    """Find the shortest path between two qubits in the coupling graph."""
    graph = {}

    for first, second in coupling_edges:
        graph.setdefault(first, set()).add(second)
        graph.setdefault(second, set()).add(first)

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        for neighbor in graph.get(current, set()):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None


def swaps_needed(coupling_edges, control, target):
    """Return the minimum SWAP count needed to bring two qubits together.

    Adjacent qubits need no SWAPs. For a path of length 2, one SWAP is
    needed; in general, the count is path length minus 1.
    """
    path = shortest_path(coupling_edges, control, target)

    if path is None:
        return None

    return max(0, len(path) - 2)