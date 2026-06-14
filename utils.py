import networkx as nx
import matplotlib.pyplot as plt


def napravi_graf(n, bridovi):
    """Gradi NetworkX graf od zadanog broja vrhova i liste bridova."""
    G = nx.Graph()
    G.add_nodes_from(range(1, n + 1))

    for u, v in bridovi:
        if not (1 <= u <= n and 1 <= v <= n):
            print(f"  Preskacem brid ({u},{v}): vrhovi moraju biti između 1 i {n}.")
            continue
        if u == v:
            print(f"  Preskacem brid ({u},{v}): petlje nisu dopuštene.")
            continue
        if G.has_edge(u, v):
            print(f"  Preskacem brid ({u},{v}): već postoji.")
            continue
        G.add_edge(u, v)

    return G


def ispisi_info(G):
    """Ispisuje osnovne podatke, listu susjedstva i matricu susjedstva."""
    n = G.number_of_nodes()
    m = G.number_of_edges()

    print("\n=== Prikaz grafa ===\n")
    print(f"Broj vrhova : {n}")
    print(f"Broj bridova: {m}\n")

    print("Lista susjedstva:")
    for vrh in sorted(G.nodes()):
        susjedi = sorted(G.neighbors(vrh))
        susjedi_str = ", ".join(map(str, susjedi)) if susjedi else "—"
        print(f"  {vrh:>3} (stupanj {G.degree(vrh)}):  {susjedi_str}")

    print("\nMatrica susjedstva:")
    nodes = sorted(G.nodes())
    print("    " + "  ".join(f"{j:2}" for j in nodes))
    print("    " + "----" * n)
    for i in nodes:
        red = [" 1" if G.has_edge(i, j) else " 0" for j in nodes]
        print(f"  {i:2}|" + "  ".join(red))

    stupnjevi = [G.degree(v) for v in G.nodes()]
    print(f"\nMinimalni stupanj : {min(stupnjevi)}")
    print(f"Maksimalni stupanj: {max(stupnjevi)}")
    print(f"Suma stupnjeva    : {sum(stupnjevi)}  (= 2 × broj bridova)")
    print(f"Povezan           : {'Da' if nx.is_connected(G) else 'Ne'}")


def crtaj_graf(G):
    """Vizualizira graf pomoću matplotlib i sprema sliku."""
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(7, 5))
    plt.title("Prikaz grafa", fontsize=14, fontweight="bold")

    nx.draw_networkx_nodes(G, pos, node_color="#4C72B0", node_size=600)
    nx.draw_networkx_labels(G, pos, font_color="white", font_size=12, font_weight="bold")
    nx.draw_networkx_edges(G, pos, edge_color="#333333", width=2)

    edge_labels = {(u, v): f"{u}-{v}" for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.axis("off")
    plt.tight_layout()
    plt.show()


def metricka_baza(G):
    """Pronalazi sve metrčke baze i metričku dimenziju grafa."""
    from itertools import combinations

    if not nx.is_connected(G):
        print("Graf nije povezan — metrička baza nije definirana.")
        return

    nodes = sorted(G.nodes())
    n = len(nodes)

    dist = dict(nx.all_pairs_shortest_path_length(G))

    def je_metricki_generator(S):
        S = list(S)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                u, v = nodes[i], nodes[j]
                if not any(dist[u][w] != dist[v][w] for w in S):
                    return False
        return True

    for k in range(1, n):
        baze = [list(S) for S in combinations(nodes, k) if je_metricki_generator(S)]
        if baze:
            print(f"\n=== Metrička baza ===\n")
            print(f"Metrička dimenzija : {k}")
            print(f"Broj baza          : {len(baze)}")
            print(f"\nSve metrčke baze:")
            for i, baza in enumerate(baze, 1):
                print(f"  Baza {i}: {{{', '.join(map(str, baza))}}}")
            return

    print(f"\nMetrička baza je cijeli skup vrhova: {{{', '.join(map(str, nodes))}}}")

def baza_povezanosti(G):
    """Pronalazi sve baze povezanosti i dimenziju povezanosti grafa."""
    from itertools import combinations
    import math

    if not nx.is_connected(G):
        print("Graf nije povezan — baza povezanosti nije definirana.")
        return

    nodes = sorted(G.nodes())
    n = len(nodes)

    kappa = nx.all_pairs_node_connectivity(G)

    def kappa_val(t, u):
        if t == u:
            return math.inf
        return kappa[t][u]

    def je_generator_povezanosti(S):
        S = list(S)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                u, v = nodes[i], nodes[j]
                if not any(kappa_val(t, u) != kappa_val(t, v) for t in S):
                    return False
        return True

    for k in range(1, n):
        baze = [list(S) for S in combinations(nodes, k) if je_generator_povezanosti(S)]
        if baze:
            print(f"\n=== Baza povezanosti ===\n")
            print(f"Dimenzija povezanosti : {k}")
            print(f"Broj baza             : {len(baze)}")
            print(f"\nSve baze povezanosti:")
            for i, baza in enumerate(baze, 1):
                print(f"  Baza {i}: {{{', '.join(map(str, baza))}}}")
            return

    print(f"\nBaza povezanosti je cijeli skup vrhova: {{{', '.join(map(str, nodes))}}}")
