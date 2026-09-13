import functools
import networkx as nx


def horadam_cubes(n, a, b):
    """
    Konstruira Horadamovu kocku Pi_n^{a,b} rekurzivno pomoću
    kanonske dekompozicije.

    Parametri
    ----------
    n : int
        Duljina riječi, n >= 0.
    a : int
        Parametar Horadamove kocke, a >= 1.
    b : int
        Parametar Horadamove kocke, b >= 1.

    Povratna vrijednost
    ------------------
    nx.Graph
        Horadamova kocka Pi_n^{a,b}. Vrhovi su predstavljeni
        n-torkama cijelih brojeva.
    """
    if n < 0:
        raise ValueError("Parametar n mora biti >= 0")
    if a < 1:
        raise ValueError("Parametar a mora biti >= 1")
    if b < 1:
        raise ValueError("Parametar b mora biti >= 1")

    @functools.cache
    def build(k):
        # Bazni slučaj: Pi_0^{a,b}
        if k == 0:
            G = nx.Graph()
            G.add_node(())
            return G

        # Bazni slučaj: Pi_1^{a,b} = P_a
        if k == 1:
            G = nx.Graph()
            G.add_nodes_from((i,) for i in range(a))
            G.add_edges_from(((i,), (i + 1,)) for i in range(a - 1))
            return G

        G_prev1 = build(k - 1)
        G_prev2 = build(k - 2)
        G = nx.Graph()

        # a kopija Pi_{k-1}^{a,b} s prefiksima 0, 1, ..., a-1
        for i in range(a):
            for v in G_prev1.nodes():
                G.add_node((i,) + v)
            for u, v in G_prev1.edges():
                G.add_edge((i,) + u, (i,) + v)

        # Bridovi između susjednih kopija Pi_{k-1}^{a,b}
        for i in range(a - 1):
            for v in G_prev1.nodes():
                G.add_edge((i,) + v, (i + 1,) + v)

        # b kopija Pi_{k-2}^{a,b} s prefiksima
        # (0,a), (0,a+1), ..., (0,a+b-1)
        for j in range(b):
            prefix = (0, a + j)
            for v in G_prev2.nodes():
                G.add_node(prefix + v)
            for u, v in G_prev2.edges():
                G.add_edge(prefix + u, prefix + v)

        # Bridovi između susjednih kopija Pi_{k-2}^{a,b}
        for j in range(b - 1):
            prefix1 = (0, a + j)
            prefix2 = (0, a + j + 1)
            for v in G_prev2.nodes():
                G.add_edge(prefix1 + v, prefix2 + v)

        # Spojni bridovi između dvaju dijelova kanonske dekompozicije
        for v in G_prev2.nodes():
            G.add_edge((0, a) + v, (0, a - 1) + v)

        return G

    return build(n)
