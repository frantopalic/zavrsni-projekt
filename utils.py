import networkx as nx
import matplotlib.pyplot as plt
import math

"""Svi teoremi koji se koriste su iz 
Gottwald, K. K., & Hofmann, T. (2025). The connectivity dimension of a graph"""

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
    """Vizualizira graf pomocu matplotlib i sprema sliku."""
    # Racunanje pozicija vrhova algoritmom za rasporedivanje
    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(7, 5))
    plt.title("Prikaz grafa", fontsize=14, fontweight="bold")

    nx.draw_networkx_nodes(G, pos, node_color="#4C72B0", node_size=800) # Crtanje cvorova
    nx.draw_networkx_labels(G, pos, font_color="white", font_size=5, font_weight="bold") # Crtanje oznaka cvorova
    nx.draw_networkx_edges(G, pos, edge_color="#333333", width=2) # Crtanje bridova

    plt.axis("off")
    plt.tight_layout()
    plt.show()


def metricka_baza(G):
    """Pronalazi sve metrcke baze i metricku dimenziju grafa.

    Koristi backtracking s pruningom umjesto provjere svih kombinacija:
    skup S se gradi vrh po vrh, a grana pretrage se odbacuje (prune) cim
    postoji par vrhova koji vise ne moze biti razluceni preostalim
    (jos neiskoristenim) kandidatima.
    """
    # Provjera je li graf povezan
    if not nx.is_connected(G):
        print("Graf nije povezan — metrička baza nije definirana.")
        return

    # Dohvacanje i sortiranje svih cvorova grafa
    nodes = sorted(G.nodes())
    n = len(nodes)

    # Racunanje najkracih udaljenosti izmedu svih parova vrhova
    dist = dict(nx.all_pairs_shortest_path_length(G))

    # Svi parovi vrhova (indeksi u listi 'nodes') koje josh treba razluciti
    svi_parovi = [(i, j) for i in range(n) for j in range(i + 1, n)]

    def razlikuje(w, u, v):
        """Provjera razlikuje li vrh w (oznaka, ne indeks) par vrhova u, v."""
        return dist[u][w] != dist[v][w]

    def trazi_baze(k):
        """Trazi sve metricke generatore velicine k backtrackingom.

        Vraca listu pronadenih baza (svaka kao lista oznaka vrhova),
        ili praznu listu ako generator velicine k ne postoji.
        """
        baze = []
        odabrano = []  # trenutno odabrani vrhovi (indeksi u 'nodes')

        def backtrack(start_idx, nerazluceni):
            """start_idx: od kojeg indeksa u 'nodes' birati sljedeci vrh
            (osigurava rastuci poredak pa nema duplikata).
            nerazluceni: skup parova (i,j) koje odabrani vrhovi jos ne razlikuju.
            """
            # Bazni slucaj: odabrali smo k vrhova
            if len(odabrano) == k:
                if not nerazluceni:
                    baze.append([nodes[i] for i in odabrano])
                return

            # PRUNING 1: nema dovoljno preostalih kandidata da popunimo S
            preostalo_mjesta = k - len(odabrano)
            preostalo_kandidata = n - start_idx
            if preostalo_kandidata < preostalo_mjesta:
                return

            # Isprobavanje sljedeceg vrha za dodati u S
            for idx in range(start_idx, n):
                w = nodes[idx]

                # Azuriranje skupa nerazlucenih parova nakon dodavanja w
                novi_nerazluceni = set()
                for (i, j) in nerazluceni:
                    if razlikuje(w, nodes[i], nodes[j]):
                        continue  # w razlikuje ovaj par, vise ne smeta
                    novi_nerazluceni.add((i, j))

                odabrano.append(idx)

                # PRUNING 2: provjeravamo mozemo li preostalim (neiskoristenim)
                # vrhovima jos razluciti sve sto je u novi_nerazluceni;
                # ako za neki nerazluceni par nijedan preostali vrh ne pomaze,
                # grana je beskorisna pa ju odmah odbacujemo
                preostali_kandidati = nodes[idx + 1:]
                moguce = True
                for (i, j) in novi_nerazluceni:
                    u, v = nodes[i], nodes[j]
                    if not any(razlikuje(x, u, v) for x in preostali_kandidati):
                        moguce = False
                        break

                if moguce:
                    backtrack(idx + 1, novi_nerazluceni)

                odabrano.pop()

        backtrack(0, set(svi_parovi))
        return baze

    # Isprobavaju se sve velicine generatora k = 1, 2, 3, ...
    # Prva velicina k za koju backtracking pronade generatore je
    # metricka dimenzija, a ti generatori su baze
    for k in range(1, n):
        baze = trazi_baze(k)
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


def _kappa_val(kappa, t, u):
    """Vraca povezanost izmedu vrhova t i u iz gotovog kappa rjecnika.
    Ako su t i u isti, vraca beskonacno."""
    if t == u:
        return math.inf
    return kappa[t][u]


def _trazi_baze_backtrack(G, nodes, n, kappa, k):
    """Trazi sve generatore povezanosti velicine k backtrackingom

    Vraca listu pronadenih baza (svaka kao lista oznaka vrhova),
    ili praznu listu ako generator velicine k ne postoji.
    """
    def razlikuje(t, u, v):
        return _kappa_val(kappa, t, u) != _kappa_val(kappa, t, v)

    svi_parovi = [(i, j) for i in range(n) for j in range(i + 1, n)]
    baze = []
    odabrano = []

    def backtrack(start_idx, nerazluceni):
        if len(odabrano) == k:
            if not nerazluceni:
                baze.append([nodes[i] for i in odabrano])
            return

        # PRUNING 1: nema dovoljno preostalih kandidata da popunimo S
        preostalo_mjesta = k - len(odabrano)
        preostalo_kandidata = n - start_idx
        if preostalo_kandidata < preostalo_mjesta:
            return

        for idx in range(start_idx, n):
            t = nodes[idx]
            novi_nerazluceni = set()
            for (i, j) in nerazluceni:
                if razlikuje(t, nodes[i], nodes[j]):
                    continue
                novi_nerazluceni.add((i, j))

            odabrano.append(idx)

            # PRUNING 2: provjeravamo mozemo li preostalim vrhovima jos
            # razluciti sve sto je u novi_nerazluceni
            preostali_kandidati = nodes[idx + 1:]
            moguce = True
            for (i, j) in novi_nerazluceni:
                u, v = nodes[i], nodes[j]
                if not any(razlikuje(x, u, v) for x in preostali_kandidati):
                    moguce = False
                    break

            if moguce:
                backtrack(idx + 1, novi_nerazluceni)

            odabrano.pop()

    backtrack(0, set(svi_parovi))
    return baze


def _backtracking_search(G, nodes, n, kappa):
    """Trazi minimalni k i sve pripadne baze cistim backtrackingom,
    koristeci donju ogradu iz Teorema 4 za k_start.

    Poziva se samo kad G nema mostova (svi mostovi vec obradeni
    Korolarom 15 prije poziva ove funkcije), sto znaci da je G 2-povezan
    (b(G) = 1).
    """
    delta = max(d for _, d in G.degree())
    k_start = math.ceil(math.log((n + 1) / 2, delta)) if delta >= 2 else 1
    k_start = min(k_start, n - 1)

    for k in range(k_start, n):
        baze = _trazi_baze_backtrack(G, nodes, n, kappa, k)
        if baze:
            return k, baze

    # Teorijski se ne bi trebalo dogoditi (cdim <= n-1 uvijek), ali za svaki slucaj:
    return n, [nodes]


def _provjeri_forsiranje(G_sub, baze_sub):
    """Provjerava forsira li graf G_sub 1-reprezentaciju (Lema 13 / Korolar 16):
    graf forsira 1-reprezentaciju ako svaka njegova baza ima vrh v izvan baze
    s kappa(v, w) = 1 za svaki w iz baze.

    Vraca listu (baza, v) parova ako G_sub forsira 1-reprezentaciju
    (v je taj poseban vrh za svaku bazu), ili None ako ne forsira.
    """
    nodes_sub = list(G_sub.nodes())

    # Trivijalan graf (jedan vrh) uvijek forsira (prazna reprezentacija)
    if len(nodes_sub) == 1:
        return [([], nodes_sub[0])]

    kappa_sub = nx.all_pairs_node_connectivity(G_sub)
    rezultat = []
    for baza in baze_sub:
        baza_set = set(baza)
        v_pronaden = None
        for v in nodes_sub:
            if v in baza_set:
                continue
            if all(_kappa_val(kappa_sub, v, w) == 1 for w in baza):
                v_pronaden = v
                break
        if v_pronaden is None:
            # Ova konkretna baza nema takav vrh -> graf ne forsira 1-reprezentaciju
            return None
        rezultat.append((baza, v_pronaden))
    return rezultat


def _resolve(G):
    """Rekurzivno racuna (cdim(G), sve_baze(G)) za povezan graf G.

    Redoslijed provjera (od najjeftinije prema backtrackingu):
      1. Bazni slucaj: graf s jednim vrhom -> cdim = 0.
      2. Teorem 3: ako je G uniformno povezan (sve kappa vrijednosti medu
         parovima vrhova jednake), onda cdim(G) = n - 1, bez pretrage.
      3. Korolar 15 (specijalni slucaj Leme 13 za H = most): ako G ima
         most, cdim(G) se racuna egzaktno iz cdim dviju manjih komponenti
         nastalih uklanjanjem mosta, rekurzivno - bez backtrackinga na G.
      4. Ako nista od navedenog ne vrijedi (G je 2-povezan), pribjegava se
         cistom backtrackingu s donjim ogradama (Teorem 4).
    """
    nodes = sorted(G.nodes())
    n = len(nodes)

    # 1. Bazni slucaj
    if n == 1:
        return 0, [[]]

    kappa = nx.all_pairs_node_connectivity(G)

    # 2. Teorem 3: cdim(G) = n-1 ako i samo ako je G uniformno k-povezan
    sve_vrijednosti = set()
    for i in range(n):
        for j in range(i + 1, n):
            sve_vrijednosti.add(_kappa_val(kappa, nodes[i], nodes[j]))
    if len(sve_vrijednosti) == 1:
        baze = [[v for v in nodes if v != x] for x in nodes]
        return n - 1, baze

    # 3. Korolar 15: egzaktna dekompozicija preko mosta
    mostovi = list(nx.bridges(G))
    if mostovi:
        u, v = mostovi[0]
        G_bez_mosta = G.copy()
        G_bez_mosta.remove_edge(u, v)
        komponenta_u = nx.node_connected_component(G_bez_mosta, u)
        komponenta_v = nx.node_connected_component(G_bez_mosta, v)
        G1 = G.subgraph(komponenta_u).copy()
        G2 = G.subgraph(komponenta_v).copy()

        cdim1, baze1 = _resolve(G1)
        cdim2, baze2 = _resolve(G2)

        forsira1 = _provjeri_forsiranje(G1, baze1)
        forsira2 = _provjeri_forsiranje(G2, baze2)

        if forsira1 is not None and forsira2 is not None:
            # Oba dijela forsiraju 1-reprezentaciju -> cdim = cdim1+cdim2+1
            cdim = cdim1 + cdim2 + 1
            baze = []
            for baza1, v1 in forsira1:
                for baza2, v2 in forsira2:
                    baze.append(baza1 + baza2 + [v2])
                    baze.append(baza1 + baza2 + [v1])
        else:
            cdim = cdim1 + cdim2
            baze = [baza1 + baza2 for baza1 in baze1 for baza2 in baze2]

        return cdim, baze

    # 4. G je 2-povezan (nema mostova) -> cisti backtracking s donjim ogradama
    return _backtracking_search(G, nodes, n, kappa)


def baza_povezanosti(G):
    """Pronalazi sve baze povezanosti i dimenziju povezanosti grafa.

    Umjesto direktnog backtrackinga na cijelom grafu, prvo se pokusavaju
    primijeniti jeftinije egzaktne metode:
      - Teorem 3 (uniformna povezanost => cdim = n-1),
      - Korolar 15 / Lema 13 (egzaktna rekurzivna dekompozicija preko
        mostova grafa),
    a tek ako niti jedna od njih nije primjenjiva, koristi se backtracking
    s pruningom, uz donje ograde iz
    Teorema 4 i Teorema 17 za pocetnu vrijednost k_start.
    """
    if not nx.is_connected(G):
        print("Graf nije povezan — baza povezanosti nije definirana.")
        return

    cdim, baze = _resolve(G)

    print(f"\n=== Baza povezanosti ===\n")
    print(f"Dimenzija povezanosti : {cdim}")
    print(f"Broj baza             : {len(baze)}")
    print(f"\nSve baze povezanosti:")
    for i, baza in enumerate(baze, 1):
        print(f"  Baza {i}: {{{', '.join(map(str, baza))}}}")