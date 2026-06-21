import networkx as nx
import functools


def horadam_cubes(n, a, b):
    """
    Konstruira Horadamo kocku Pi^{a,b}_n rekurzivno koristeći kanonsku
    dekompoziciju iz (Podrug, L. (2024). Horadam cubes) Teorem 1:

        Π^{a,b}_n = Π^{a,b}_{n-1} ⊕ ... ⊕ Π^{a,b}_{n-1} ⊕ Π^{a,b}_{n-2} ⊕ ... ⊕ Π_{a,b}_{n-2}
                     P_a □ Π^{a,b}_{n-1}  ⊕  P_b □ Π^{a,b}_{n-2}

    gdje P_a i P_b oznacavaju putove duljina a i b, redom, a □ je kartezijski produkt
    grafova, te sadrzi bridove koji povezuju podgrafove:
        0a · Π^{a,b}_{n-2}  i  0(a-1) · Π^{a,b}_{n-2}  ⊂  0 · Π^{a,b}_{n-1},
    tj. uzme se a+b medusobno nepovezanih kopija pa se dodaju bridovi koji ih spajaju
    u kartezijske produkte P_a □ Π^{a,b}_{n-1} i P_b □ Π^{a,b}_{n-2}, te konacno "mostni"
    bridovi koji spajaju ta dva dijela u jedinstven povezan graf.

    Petlje najprije kreiraju odvojene kopije (⊕ dio), a onda se zasebnim petljama dodaju bridovi
    puta P_a i puta P_b i mostni bridovi

    Vrhovi su prefiksirani na sljedeći način:
      - a kopija Π^{a,b}_{n-1}, s prefiksima 0, 1, ..., a-1
        (spojene u put P_a kroz kartezijski produkt)
      - b kopija Π^{a,b}_{n-2}, s prefiksima (0,a), (0,a+1), ..., (0,a+b-1)
        (spojene u put P_b kroz kartezijski produkt)
      - dodatni "mostni" bridovi spajaju (0,a,β) ↔ (0,a-1,β) za svaki
        β ∈ S^{a,b}_{n-2}, čime se prva od b kopija lijepi na zadnju
        od a kopija (postujuci ogranicenje da slovo a smije doci samo
        nakon 0)
      - vrh (0, a) + β dolazi iz prve Π^{a,b}_{n-2} kopije
      - vrh (0, a-1) + β dolazi iz zadnje Π^{a,b}_{n-1} kopije - ali samo
        onaj dio te kopije koji pocinje s 0

        
    Memoizacija (functools.cache) osigurava da se svaki podgraf
    Π^{a,b}_k gradi samo jednom.

    Parametri:
        n (int): duljina stringova/vrhova, n >= 0
        a (int): broj "obicnih" slova/generatora, a >= 1
        b (int): broj "velikih" (dvoznamenkastih) primitivnih blokova, b >= 0

    """
    if a < 1:
        raise ValueError("Parametar a mora biti >= 1")
    if b < 0:
        raise ValueError("Parametar b mora biti >= 0")
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
        G_prev1 = build(n - 1)  # Π^{a,b}_{n-1}
        G_prev2 = build(n - 2)  # Π^{a,b}_{n-2}

        # a kopija Π^{a,b}_{n-1} s prefiksima 0, 1, ..., a-1
        for k in range(a):
            for v in G_prev1.nodes():
                G.add_node((k,) + v)
            for u, v in G_prev1.edges():
                G.add_edge((k,) + u, (k,) + v)

        # Bridovi duz puta P_a izmedu susjednih kopija (kartezijski produkt)
        for k in range(a - 1):
            for v in G_prev1.nodes():
                G.add_edge((k,) + v, (k + 1,) + v)

        # b kopija Π^{a,b}_{n-2} s prefiksima (0,a), (0,a+1), ..., (0,a+b-1)
        for j in range(b):
            prefix = (0, a + j)
            for v in G_prev2.nodes():
                G.add_node(prefix + v)
            for u, v in G_prev2.edges():
                G.add_edge(prefix + u, prefix + v)

        # Bridovi duz puta P_b izmedu susjednih kopija (kartezijski produkt)
        for j in range(b - 1):
            prefix1 = (0, a + j)
            prefix2 = (0, a + j + 1)
            for v in G_prev2.nodes():
                G.add_edge(prefix1 + v, prefix2 + v)

        # "Mostni" bridovi: (0, a, β) ↔ (0, a-1, β) za svaki β ∈ S^{a,b}_{n-2}
        # Spaja prvu od b kopija (prefiks 0a) sa zadnjom od a kopija
        # (prefiks 0(a-1)), postujuci uvjet da a smije doci samo nakon 0.
        # Ako je b == 0, nema kopija Π^{a,b}_{n-2} pa nema ni ovih bridova.
        if b > 0:
            for v in G_prev2.nodes():
                G.add_edge((0, a) + v, (0, a - 1) + v)

        return G

    return build(n)