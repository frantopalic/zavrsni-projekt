import networkx as nx
import matplotlib.pyplot as plt


def napravi_graf(n, bridovi):
    """Gradi graf od zadanog broja vrhova i liste bridova."""
    G = nx.Graph() # Stvara se prazan neusmjeren graf
    G.add_nodes_from(range(1, n + 1)) # Dodaju se vrhovi oznaceni brojevima od 1 do n

    # Prolazak kroz sve bridove koji se dodaju
    for u, v in bridovi:
        # Provjera jesu li oba vrha unutar dopustenog raspona
        if not (1 <= u <= n and 1 <= v <= n):
            print(f"  Preskacem brid ({u},{v}): vrhovi moraju biti između 1 i {n}.")
            continue
        # Brid koji spaja vrh sa samim sobom nije dopusten
        if u == v:
            print(f"  Preskacem brid ({u},{v}): petlje nisu dopuštene.")
            continue
        # Provjera postoji li vec taj brid
        if G.has_edge(u, v):
            print(f"  Preskacem brid ({u},{v}): već postoji.")
            continue
        # Brid se dodaje u graf
        G.add_edge(u, v)

    return G


def crtaj_graf(G):
    """Vizualizira graf pomoću matplotlib i sprema sliku."""
    # Racunanje pozicija vrhova algoritmom za rasporedivanje
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(7, 5))
    plt.title("Prikaz grafa", fontsize=14, fontweight="bold")

    nx.draw_networkx_nodes(G, pos, node_color="#4C72B0", node_size=600) # Crtanje cvorova
    nx.draw_networkx_labels(G, pos, font_color="white", font_size=12, font_weight="bold") # Crtanje oznaka cvorova
    nx.draw_networkx_edges(G, pos, edge_color="#333333", width=2) # Crtanje bridova

    plt.axis("off")
    plt.tight_layout()
    plt.show()


def metricka_baza(G):
    """Pronalazi sve metrčke baze i metričku dimenziju grafa."""
    from itertools import combinations

    # Provjera je li graf povezan
    if not nx.is_connected(G):
        print("Graf nije povezan — metrička baza nije definirana.")
        return

    # Dohvacanje i sortiranje svih cvorova grafa
    nodes = sorted(G.nodes())
    n = len(nodes)

    # Racunanje najkracih udaljenosti izmedu svih parova vrhova
    dist = dict(nx.all_pairs_shortest_path_length(G))

    def je_metricki_generator(S):
        """Provjera je li skup S metricki generator grafa G.

        S je metricki generator ako za svaki par razlicithi vrhova u, v
        postoji vrh x iz S za koji su dist(u,x) i dist(v,x) razliciti.
        """
        S = list(S)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                u, v = nodes[i], nodes[j]
                # Ako niti jedan vrh iz S ne razlikuje par (u,v), S nije generator
                if not any(dist[u][w] != dist[v][w] for w in S):
                    return False
        return True

    # Trazi se metricki generator najmanje dimenzije tj. baza
    # Isprobavaju se sve velicine generatora k = 1, 2, 3, ...
    # Prva velicina k za koju postoje generatori je metricka dimenzija,
    # a ti generatori su baze
    for k in range(1, n):
        # Generiranje svih kombinacija vrhova velicine k i projvera koje su metricke baze
        baze = [list(S) for S in combinations(nodes, k) if je_metricki_generator(S)]
        if baze:
            print(f"\n=== Metrička baza ===\n")
            print(f"Metrička dimenzija : {k}")
            print(f"Broj baza          : {len(baze)}")
            print(f"\nSve metrčke baze:")
            for i, baza in enumerate(baze, 1):
                print(f"  Baza {i}: {{{', '.join(map(str, baza))}}}")
            return

    # Ako niti jedan podskup nije metricki generator, baza je cijeli skup vrhova
    print(f"\nMetrička baza je cijeli skup vrhova: {{{', '.join(map(str, nodes))}}}")


def baza_povezanosti(G):
    """Pronalazi sve baze povezanosti i dimenziju povezanosti grafa."""
    from itertools import combinations
    import math

    # Baza povezanosti nije definirana za nepovezane grafove
    if not nx.is_connected(G):
        print("Graf nije povezan — baza povezanosti nije definirana.")
        return

    # Dohvacanje svih grafova te sortiranje
    nodes = sorted(G.nodes())
    n = len(nodes)

    # Racunanje povezanosti izmedu svih parova vrhova
    # kappa[u][v] = maksimalan broj vrsno disjunktnih putova izmedu u i v
    kappa = nx.all_pairs_node_connectivity(G)

    def kappa_val(t, u):
        """Vraca povezanost izmedu vrhova t i u.
        Ako su t i u isti, vraca beskonacno"""
        if t == u:
            return math.inf
        return kappa[t][u]

    def je_generator_povezanosti(S):
        """Provjera je li skup S generator povezanosti grafa G.

        S je generator povezanosti ako za svaki par vrhova u, v
        postoji vrh x iz S za koji su kappa(t,u) i kappa(t,v) razliciti.
        """
        S = list(S)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                u, v = nodes[i], nodes[j]
                # Ako niti jedan vrh iz S ne razlikuje par (u,v), S nije generator
                if not any(kappa_val(t, u) != kappa_val(t, v) for t in S):
                    return False
        return True

    # Trazi se generator povezanosti najmanje dimenzije, tj. baza
    # Isprobavaju se sve velicine generatora k = 1,2,3,...
    # Prvi k za koji postoje generatori je dimenzija povezanosti,
    # a ti generatori su baze
    for k in range(1, n):
        # Generiranje svih kombinacija vrhova velicine k i provjera koje su baze povezanosti
        baze = [list(S) for S in combinations(nodes, k) if je_generator_povezanosti(S)]
        if baze:
            print(f"\n=== Baza povezanosti ===\n")
            print(f"Dimenzija povezanosti : {k}")
            print(f"Broj baza             : {len(baze)}")
            print(f"\nSve baze povezanosti:")
            for i, baza in enumerate(baze, 1):
                print(f"  Baza {i}: {{{', '.join(map(str, baza))}}}")
            return

    # Ako niti jedan podskup nije generator povezanosti, baza je cijeli skup vrhova
    print(f"\nBaza povezanosti je cijeli skup vrhova: {{{', '.join(map(str, nodes))}}}")
