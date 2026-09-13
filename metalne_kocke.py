from horadam_kocke import horadam_cubes


def metallic_cubes(n, a):
    """
    Konstruira metalnu kocku Pi_n^a kao poseban slučaj
    Horadamove kocke Pi_n^{a,b} za b = 1.

    Parametri
    ----------
    n : int
        Duljina riječi, n >= 0.
    a : int
        Parametar metalne kocke, a >= 1.

    Povratna vrijednost
    ------------------
    nx.Graph
        Metalna kocka Pi_n^a.
    """
    return horadam_cubes(n, a, 1)
