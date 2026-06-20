import networkx as nx
import functools

from horadam_kocke import horadam_cubes


def metallic_cubes(n, a):
    """
    Konstruira metalnu kocku Pi^a_n.

    Specijalni slučaj Horadamove kocke Pi^{a,b}_n za b = 1
    (vidi horadam_cubes za opću konstrukciju i kanonsku dekompoziciju
    iz Teorema 1).

    Parametri:
        n (int): duljina stringova/vrhova, n >= 0
        a (int): parametar alfabeta {0, ..., a}, a >= 1
    """
    return horadam_cubes(n, a, 1)

def metallic_cubes1(n, a):
    """
    Konstruira metalnu kocku Pi^a_n rekurzivno koristeći kanonsku dekompoziciju:

        Pi^a_n = (P_a □ Pi^a_{n-1}) ⊕ Pi^a_{n-2}

    gdje je P_a put na a vrhova, □ je kartezijski produkt grafova,
    a bridovi između dvije komponente su:
        (0, a, β) ↔ (0, a-1, β)  za svaki β ∈ S^a_{n-2}

    Memoizacija (functools.cache) osigurava da se svaki podgraf
    Pi^a_k gradi samo jednom.

    Parametri:
        n (int): duljina stringova/vrhova, n >= 0
        a (int): parametar alfabeta {0, ..., a}, a >= 1
    """
    if a < 1:
        raise ValueError("Parametar a mora biti >= 1")
    if n < 0:
        raise ValueError("Parametar n mora biti >= 0")

    @functools.cache
    def build(n):
        # Bazni slučajevi
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
        G_prev1 = build(n - 1)  # Pi^a_{n-1}
        G_prev2 = build(n - 2)  # Pi^a_{n-2}

        # a kopija Pi^a_{n-1} s prefiksima 0, 1, ..., a-1
        for k in range(a):
            for v in G_prev1.nodes():
                G.add_node((k,) + v)
            for u, v in G_prev1.edges():
                G.add_edge((k,) + u, (k,) + v)

        # Bridovi duž puta P_a između susjednih kopija (kartezijski produkt)
        for k in range(a - 1):
            for v in G_prev1.nodes():
                G.add_edge((k,) + v, (k + 1,) + v)

        # Kopija Pi^a_{n-2} s prefiksom (0, a)
        for v in G_prev2.nodes():
            G.add_node((0, a) + v)
        for u, v in G_prev2.edges():
            G.add_edge((0, a) + u, (0, a) + v)

        # Bridovi između (0, a, β) i (0, a-1, β) za svaki β ∈ S^a_{n-2}
        # (pozicija 1 se mijenja za ±1: a-1 ↔ a, što je dozvoljeno jer prethodi 0)
        for v in G_prev2.nodes():
            G.add_edge((0, a) + v, (0, a - 1) + v)

        return G

    return build(n)