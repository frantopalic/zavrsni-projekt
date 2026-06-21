import networkx as nx
import functools

from horadam_kocke import horadam_cubes


def metallic_cubes(n, a):
    """
    Konstruira metalnu kocku Π^a_n.

    Specijalni slučaj Horadamove kocke Π^{a,b}_n za b = 1

    Parametri:
        n (int): duljina stringova/vrhova, n >= 0
        a (int): parametar alfabeta {0, ..., a}, a >= 1
    """
    return horadam_cubes(n, a, 1)

def metallic_cubes1(n, a):

    if a < 1:
        raise ValueError("Parametar a mora biti >= 1")
    if n < 0:
        raise ValueError("Parametar n mora biti >= 0")

    @functools.cache
    def build(n):
        if n == 0:
            G = nx.Graph()
            G.add_node(())
            return G
        if n == 1:
            G = nx.Graph()
            for k in range(a):
                G.add_node((k,))
            for k in range(a - 1):
                G.add_edge((k,), (k + 1,))
            return G

        G = nx.Graph()
        G_prev1 = build(n - 1)
        G_prev2 = build(n - 2)

        for k in range(a):
            for v in G_prev1.nodes():
                G.add_node((k,) + v)
            for u, v in G_prev1.edges():
                G.add_edge((k,) + u, (k,) + v)

        for k in range(a - 1):
            for v in G_prev1.nodes():
                G.add_edge((k,) + v, (k + 1,) + v)

        for v in G_prev2.nodes():
            G.add_node((0, a) + v)
        for u, v in G_prev2.edges():
            G.add_edge((0, a) + u, (0, a) + v)

        for v in G_prev2.nodes():
            G.add_edge((0, a) + v, (0, a - 1) + v)

        return G

    return build(n)