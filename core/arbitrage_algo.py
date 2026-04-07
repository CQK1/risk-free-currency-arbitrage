# -*- coding: utf-8 -*-
import numpy as np
import math

def bellman_ford_arbitrage(rate_matrix, currencies, fee):
    """
    Detects negative cycles (arbitrage opportunities) using the Bellman-Ford algorithm.
    Includes logarithmic transformation and transaction fees.
    """
    n = len(currencies)
    graph = np.zeros((n, n))
    
    # Mathematical transformation: -ln(Rate * (1 - fee))
    for i in range(n):
        for j in range(n):
            if i != j:
                actual_rate = rate_matrix[i][j] * (1 - fee / 100.0)
                if actual_rate > 0:
                    graph[i][j] = -math.log(actual_rate)
                else:
                    graph[i][j] = float('inf')
            else:
                graph[i][j] = 0

    dist = [float('inf')] * n
    dist[0] = 0
    pred = [-1] * n

    # Relax edges V-1 times
    for _ in range(n - 1):
        for u in range(n):
            for v in range(n):
                if u != v and dist[u] + graph[u][v] < dist[v]:
                    dist[v] = dist[u] + graph[u][v]
                    pred[v] = u

    # Detect negative cycle
    arbitrage_path = None
    for u in range(n):
        for v in range(n):
            if u != v and dist[u] + graph[u][v] < dist[v] - 1e-8:
                cycle = []
                curr = v
                for _ in range(n):
                    curr = pred[curr]

                cycle_start = curr
                cycle.append(cycle_start)
                curr = pred[curr]
                while curr != cycle_start:
                    cycle.append(curr)
                    curr = pred[curr]
                cycle.append(cycle_start)

                cycle.reverse()
                arbitrage_path = [currencies[i] for i in cycle]
                return arbitrage_path

    return None