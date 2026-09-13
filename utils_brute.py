import math
import time
from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx


"""Brute-force referentne funkcije za provjeru optimiranih algoritama.

Ova datoteka namijenjena je prvenstveno provjeri ispravnosti algoritama
iz utils.py na manjim grafovima. Metrička baza i baza povezanosti određuju
se potpunim pregledom podskupova vrhova rastućih kardinalnosti, bez
povratnog pretraživanja i bez dodatnih pravila odsijecanja.
"""


def napravi_graf(n, bridovi):
    """Gradi jednostavan neusmjeren graf s vrhovima 1, ..., n."""
    if n < 1:
        raise ValueError("Broj vrhova n mora biti barem 1.")

    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))

    for u, v in bridovi:
        if not (1 <= u <= n and 1 <= v <= n):
            print(
                f"Preskačem brid ({u}, {v}): vrhovi moraju biti između 1 i {n}."
            )
            continue
        if u == v:
            print(f"Preskačem brid ({u}, {v}): petlje nisu dopuštene.")
            continue
        if G.has_edge(u, v):
            print(f"Preskačem brid ({u}, {v}): brid već postoji.")
            continue
        G.add_edge(u, v)

    return G


def crtaj_graf(G):
    """Vizualizira graf pomoću matplotliba."""
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(7, 5))
    plt.title("Prikaz grafa", fontsize=14, fontweight="bold")
    nx.draw_networkx_nodes(G, pos, node_color="#4C72B0", node_size=600)
    nx.draw_networkx_labels(
        G, pos, font_color="white", font_size=12, font_weight="bold"
    )
    nx.draw_networkx_edges(G, pos, edge_color="#333333", width=2)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def metricka_baza_brute(G, ispisi=True, vrati_sve_baze=False, vrati_vremena=False):
    """Brute-force određuje metričku dimenziju i metričku bazu povezanog grafa.

    Podskupovi vrhova ispituju se po rastućoj kardinalnosti. Prva
    kardinalnost za koju postoji metrički generator jest metrička dimenzija.

    Parametri
    ---------
    G : nx.Graph
        Povezan neusmjeren graf.
    ispisi : bool
        Ako je True, ispisuje rezultat.
    vrati_sve_baze : bool
        Ako je True, vraća sve metričke baze minimalne kardinalnosti.
        Inače vraća samo jednu metričku bazu.
    vrati_vremena : bool
        Ako je True, uz rezultat vraća i rječnik s vremenima pojedinih faza
        te s brojem razmotrenih podskupova (ključ "razmotreni_podskupovi").
        Budući da brute-force ne koristi nikakvo odsijecanje, taj je broj
        jednak zbroju ∑_{k=1}^{mdim} C(n, k), odnosno broju svih podskupova
        koji su morali biti provjereni prije pronalaska generatora.

    Povratna vrijednost
    -------------------
    (mdim, baza), (mdim, baze) ili isto uz dodani rječnik vremena
    """
    if G.is_directed():
        raise ValueError("Ova implementacija očekuje neusmjeren graf.")
    if len(G) == 0:
        raise ValueError("Graf mora imati barem jedan vrh.")
    if not nx.is_connected(G):
        raise ValueError("Ova brute-force implementacija očekuje povezan graf.")

    nodes = sorted(G.nodes())
    n = len(nodes)

    if n == 1:
        baze = [[]]
        vremena = {
            "t_udaljenosti": 0.0,
            "t_pretraga": 0.0,
            "t_ukupno": 0.0,
            "razmotreni_podskupovi": 0,
        }
        if ispisi:
            print("Metrička dimenzija: 0")
            print("Metrička baza: {}")
        rezultat = (0, baze) if vrati_sve_baze else (0, [])
        return (*rezultat, vremena) if vrati_vremena else rezultat

    t0 = time.perf_counter()

    t = time.perf_counter()
    udaljenosti = dict(nx.all_pairs_shortest_path_length(G))
    t_udaljenosti = time.perf_counter() - t

    razmotreni_podskupovi = 0

    def je_metricki_generator(S):
        nonlocal razmotreni_podskupovi
        razmotreni_podskupovi += 1
        for i in range(n):
            for j in range(i + 1, n):
                u, v = nodes[i], nodes[j]
                if not any(
                    udaljenosti[u][w] != udaljenosti[v][w]
                    for w in S
                ):
                    return False
        return True

    t = time.perf_counter()
    for k in range(1, n):
        baze = [
            list(S)
            for S in combinations(nodes, k)
            if je_metricki_generator(S)
        ]

        if baze:
            t_pretraga = time.perf_counter() - t
            t_ukupno = time.perf_counter() - t0
            vremena = {
                "t_udaljenosti": t_udaljenosti,
                "t_pretraga": t_pretraga,
                "t_ukupno": t_ukupno,
                "razmotreni_podskupovi": razmotreni_podskupovi,
            }

            if ispisi:
                print(f"Metrička dimenzija: {k}")
                if vrati_sve_baze:
                    print(f"Broj metričkih baza: {len(baze)}")
                    for i, baza in enumerate(baze, 1):
                        print(
                            f"Baza {i}: "
                            f"{{{', '.join(map(str, baza))}}}"
                        )
                else:
                    print(
                        "Metrička baza: "
                        f"{{{', '.join(map(str, baze[0]))}}}"
                    )

            rezultat = (k, baze) if vrati_sve_baze else (k, baze[0])
            return (*rezultat, vremena) if vrati_vremena else rezultat

    raise RuntimeError(
        "Nije pronađena metrička baza, iako za povezan graf reda n >= 2 "
        "vrijedi mdim(G) <= n - 1."
    )


def baza_povezanosti_brute(
    G,
    flow_func=None,
    ispisi=True,
    vrati_sve_baze=False,
    vrati_vremena=False,
):
    """Brute-force određuje dimenziju povezanosti i bazu povezanosti.

    Funkcija je namijenjena povezanim grafovima. Najprije se egzaktno
    računaju lokalne vršne povezanosti između svih parova vrhova, a zatim
    se svi podskupovi vrhova ispituju po rastućoj kardinalnosti.

    Parametri
    ---------
    G : nx.Graph
        Povezan neusmjeren graf.
    flow_func : funkcija ili None
        Egzaktni algoritam maksimalnog toka koji NetworkX koristi pri
        računanju lokalnih vršnih povezanosti. Ako je None, koristi se
        NetworkXov zadani algoritam.
    ispisi : bool
        Ako je True, ispisuje rezultat.
    vrati_sve_baze : bool
        Ako je True, vraća sve baze povezanosti minimalne kardinalnosti.
        Inače vraća samo jednu bazu.
    vrati_vremena : bool
        Ako je True, uz rezultat vraća i rječnik s vremenima pojedinih faza
        te s brojem razmotrenih podskupova (ključ "razmotreni_podskupovi").

    Povratna vrijednost
    -------------------
    (cdim, baza), (cdim, baze) ili isto uz dodani rječnik vremena
    """
    if G.is_directed():
        raise ValueError("Ova implementacija očekuje neusmjeren graf.")
    if len(G) == 0:
        raise ValueError("Graf mora imati barem jedan vrh.")
    if not nx.is_connected(G):
        raise ValueError(
            "Ova brute-force implementacija baze povezanosti "
            "očekuje povezan graf."
        )

    nodes = sorted(G.nodes())
    n = len(nodes)

    if n == 1:
        baze = [[]]
        vremena = {
            "t_kappa": 0.0,
            "t_pretraga": 0.0,
            "t_ukupno": 0.0,
            "razmotreni_podskupovi": 0,
        }
        if ispisi:
            print("Dimenzija povezanosti: 0")
            print("Baza povezanosti: {}")
        rezultat = (0, baze) if vrati_sve_baze else (0, [])
        return (*rezultat, vremena) if vrati_vremena else rezultat

    t0 = time.perf_counter()

    t = time.perf_counter()
    kappa = nx.all_pairs_node_connectivity(
        G,
        nbunch=nodes,
        flow_func=flow_func,
    )
    t_kappa = time.perf_counter() - t

    def kappa_val(t_, u):
        if t_ == u:
            return math.inf
        return kappa[t_][u]

    razmotreni_podskupovi = 0

    def je_generator_povezanosti(S):
        nonlocal razmotreni_podskupovi
        razmotreni_podskupovi += 1
        for i in range(n):
            for j in range(i + 1, n):
                u, v = nodes[i], nodes[j]
                if not any(
                    kappa_val(t_, u) != kappa_val(t_, v)
                    for t_ in S
                ):
                    return False
        return True

    t = time.perf_counter()
    for k in range(1, n):
        baze = [
            list(S)
            for S in combinations(nodes, k)
            if je_generator_povezanosti(S)
        ]

        if baze:
            t_pretraga = time.perf_counter() - t
            t_ukupno = time.perf_counter() - t0
            vremena = {
                "t_kappa": t_kappa,
                "t_pretraga": t_pretraga,
                "t_ukupno": t_ukupno,
                "razmotreni_podskupovi": razmotreni_podskupovi,
            }

            if ispisi:
                print(f"Dimenzija povezanosti: {k}")
                if vrati_sve_baze:
                    print(f"Broj baza povezanosti: {len(baze)}")
                    for i, baza in enumerate(baze, 1):
                        print(
                            f"Baza {i}: "
                            f"{{{', '.join(map(str, baza))}}}"
                        )
                else:
                    print(
                        "Baza povezanosti: "
                        f"{{{', '.join(map(str, baze[0]))}}}"
                    )

            rezultat = (k, baze) if vrati_sve_baze else (k, baze[0])
            return (*rezultat, vremena) if vrati_vremena else rezultat

    raise RuntimeError(
        "Nije pronađena baza povezanosti, iako za povezan graf reda n >= 2 "
        "vrijedi cdim(G) <= n - 1."
    )