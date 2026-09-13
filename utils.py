import math
import time
from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


"""Pomoćne funkcije za rad s metričkom dimenzijom i dimenzijom povezanosti.

Za dimenziju povezanosti koriste se rezultati iz:
K. K. Gottwald, T. Hofmann, The connectivity dimension of a graph (2025).
"""


def napravi_graf(n, bridovi):
    """Gradi jednostavan neusmjeren graf s vrhovima 1, ..., n."""
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
    nx.draw_networkx_nodes(G, pos, node_color="#4C72B0", node_size=800)
    nx.draw_networkx_labels(
        G, pos, font_color="white", font_size=5, font_weight="bold"
    )
    nx.draw_networkx_edges(G, pos, edge_color="#333333", width=2)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# METRIČKA DIMENZIJA
# ---------------------------------------------------------------------------


def _l1_matrica(nodes):
    """Računa matricu L1 udaljenosti za vrhove zapisane kao n-torke cijelih brojeva.

    Ova se funkcija smije koristiti samo kada je poznato da je grafovska udaljenost
    jednaka L1 udaljenosti oznaka vrhova, kao kod Horadamovih, specijalno metalnih kocaka.
    """
    if not nodes:
        return np.empty((0, 0), dtype=np.int64)

    if not all(isinstance(v, tuple) for v in nodes):
        raise ValueError(
            "Za L1 izračun svi vrhovi moraju biti zapisani kao tuple-ovi."
        )

    duljine = {len(v) for v in nodes}
    if len(duljine) != 1:
        raise ValueError("Sve n-torke cijelih brojeva moraju biti jednake duljine.")

    arr = np.asarray(nodes, dtype=np.int64)
    broj_vrhova, duljina = arr.shape

    matrica = np.zeros((broj_vrhova, broj_vrhova), dtype=np.int64)
    for i in range(duljina):
        stupac = arr[:, i]
        matrica += np.abs(stupac[:, None] - stupac[None, :])

    return matrica


def _matrica_udaljenosti(G, nodes, brza_l1=False):
    """Vraća matricu udaljenosti u poretku vrhova iz liste nodes."""
    if brza_l1:
        return _l1_matrica(nodes)

    udaljenosti = dict(nx.all_pairs_shortest_path_length(G))
    n = len(nodes)
    D = np.empty((n, n), dtype=np.int64)
    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            D[i, j] = udaljenosti[u][v]
    return D


def _zadnji_razlikujuci_indeksi(M):
    """Računa L_ij = max{q : M[i,q] != M[j,q]} za sve i < j.

    Vraća cijelobrojnu simetričnu matricu L. Za matrice udaljenosti i matrice
    lokalnih povezanosti korištene u ovom radu skup iz definicije L_ij uvijek
    je neprazan.
    """
    n = M.shape[0]
    L = np.full((n, n), -1, dtype=np.int64)

    for i in range(n):
        for j in range(i + 1, n):
            razliciti = np.flatnonzero(M[i] != M[j])
            if razliciti.size == 0:
                raise ValueError(
                    f"Redci {i} i {j} matrice su jednaki; L_ij nije definiran."
                )
            zadnji = int(razliciti[-1])
            L[i, j] = zadnji
            L[j, i] = zadnji

    return L


def _pronadi_generator(M, L, k_start, k_kraj):
    """Traži jedan generator najmanje veličine u zadanom rasponu.

    Redci matrice M predstavljaju vrhove koje treba razlučiti, a stupci
    kandidatske vrhove. Kandidat r razlučuje par (i,j) ako M[i,r] != M[j,r].

    Pretraživanje koristi dva pravila odsijecanja:
      1. mora ostati dovoljno kandidata da se skup dopuni do veličine k;
      2. svaki trenutačno nerazlučen par mora imati razlikujući kandidat s
         indeksom većim od posljednjeg odabranog indeksa.

    Radi analize učinka odsijecanja, funkcija također broji posjećene
    čvorove stabla pretraživanja (svaki poziv funkcije pretrazi predstavlja
    jedan čvor, odnosno jedno djelomično odabrano rješenje). Broj se
    akumulira preko svih isprobanih vrijednosti k, uključujući one za koje
    generator nije pronađen.

    Povratna vrijednost
    -------------------
    (k, tuple_indeksa, ukupno_posjecenih_cvorova) ako je generator pronađen,
    inače None.
    """
    n = M.shape[0]
    svi_parovi = tuple((i, j) for i in range(n) for j in range(i + 1, n))
    ukupno_posjeceno = 0

    for k in range(k_start, k_kraj + 1):
        odabrano = []
        posjeceno = 0

        def pretrazi(p, nerazluceni):
            nonlocal posjeceno
            posjeceno += 1

            if len(odabrano) == k:
                return tuple(odabrano) if not nerazluceni else None

            preostalo_mjesta = k - len(odabrano)
            if n - p < preostalo_mjesta:
                return None

            # Posljednji dopušteni kandidat: nakon njegova odabira mora ostati
            # dovoljno vrhova za popunjavanje skupa do veličine k.
            zadnji_r = n - preostalo_mjesta

            for r in range(p, zadnji_r + 1):
                novi_nerazluceni = tuple(
                    (i, j) for (i, j) in nerazluceni if M[i, r] == M[j, r]
                )

                # Ako je par i dalje nerazlučen, a njegov zadnji mogući
                # razlikujući kandidat nije iza r, ova se grana može odbaciti.
                if any(L[i, j] <= r for (i, j) in novi_nerazluceni):
                    continue

                odabrano.append(r)
                rezultat = pretrazi(r + 1, novi_nerazluceni)
                if rezultat is not None:
                    return rezultat
                odabrano.pop()

            return None

        rezultat = pretrazi(0, svi_parovi)
        ukupno_posjeceno += posjeceno
        if rezultat is not None:
            return k, rezultat, ukupno_posjeceno

    return None


def metricka_baza(G, brza_l1=False, ispisi=True, vrati_vremena=False):
    """Određuje metričku dimenziju i jednu metričku bazu povezanog grafa.

    Parametri
    ---------
    G : nx.Graph
        Povezan neusmjeren graf.
    brza_l1 : bool
        Ako je True, udaljenosti se računaju L1 formulom. To je dopušteno
        samo za Horadamove/metalne kocke zapisane n-torkama cijelih brojeva.
    ispisi : bool
        Ako je True, ispisuje rezultat.
    vrati_vremena : bool
        Ako je True, uz rezultat vraća i rječnik s vremenima pojedinih faza
        te s brojem posjećenih čvorova stabla pretraživanja
        (ključ "posjeceni_cvorovi").

    Povratna vrijednost
    -------------------
    (mdim, baza) ili (mdim, baza, vremena)
    """
    if G.is_directed():
        raise ValueError("Ova implementacija očekuje neusmjeren graf.")
    if len(G) == 0:
        raise ValueError("Graf mora imati barem jedan vrh.")
    if not nx.is_connected(G):
        raise ValueError("Ova implementacija metričke baze očekuje povezan graf.")

    nodes = sorted(G.nodes())
    n = len(nodes)

    if n == 1:
        rezultat = (0, [])
        vremena = {
            "t_matrica": 0.0,
            "t_L": 0.0,
            "t_pretraga": 0.0,
            "t_ukupno": 0.0,
            "posjeceni_cvorovi": 0,
        }
        if ispisi:
            print("Metrička dimenzija: 0")
            print("Metrička baza: {}")
        return (*rezultat, vremena) if vrati_vremena else rezultat

    t0 = time.perf_counter()
    t = time.perf_counter()
    D = _matrica_udaljenosti(G, nodes, brza_l1=brza_l1)
    t_matrica = time.perf_counter() - t

    t = time.perf_counter()
    L = _zadnji_razlikujuci_indeksi(D)
    t_L = time.perf_counter() - t

    t = time.perf_counter()
    pronadeno = _pronadi_generator(D, L, k_start=1, k_kraj=n - 1)
    t_pretraga = time.perf_counter() - t

    if pronadeno is None:
        raise RuntimeError(
            "Nije pronađena metrička baza, iako za povezan graf reda n>=2 "
            "vrijedi mdim(G) <= n-1."
        )

    mdim, indeksi, posjeceni_cvorovi = pronadeno
    baza = [nodes[i] for i in indeksi]
    t_ukupno = time.perf_counter() - t0

    vremena = {
        "t_matrica": t_matrica,
        "t_L": t_L,
        "t_pretraga": t_pretraga,
        "t_ukupno": t_ukupno,
        "posjeceni_cvorovi": posjeceni_cvorovi,
    }

    if ispisi:
        print(f"Metrička dimenzija: {mdim}")
        print(f"Metrička baza: {{{', '.join(map(str, baza))}}}")

    return (mdim, baza, vremena) if vrati_vremena else (mdim, baza)


# ---------------------------------------------------------------------------
# DIMENZIJA POVEZANOSTI
# ---------------------------------------------------------------------------


def matrica_lokalnih_povezanosti(G, flow_func=None, nodes=None):
    """Računa matricu lokalnih vršnih povezanosti K.

    Za i != j vrijedi K[i,j] = kappa(v_i,v_j), a na dijagonali se postavlja
    beskonačno. NetworkXova funkcija all_pairs_node_connectivity ponovno
    koristi pomoćni digraf i rezidualnu mrežu za sve parove.

    Parametar flow_func može biti, primjerice,
    nx.algorithms.flow.edmonds_karp ili
    nx.algorithms.flow.shortest_augmenting_path.
    Ako je None, koristi se NetworkXov zadani egzaktni algoritam.
    """
    if G.is_directed():
        raise ValueError("Ova implementacija očekuje neusmjeren graf.")
    if len(G) == 0:
        raise ValueError("Graf mora imati barem jedan vrh.")
    if not nx.is_connected(G):
        raise ValueError(
            "Ova implementacija matrice lokalnih povezanosti očekuje povezan graf."
        )

    if nodes is None:
        nodes = sorted(G.nodes())
    else:
        nodes = list(nodes)

    n = len(nodes)
    K = np.full((n, n), np.inf, dtype=float)

    if n == 1:
        return K

    kappa = nx.all_pairs_node_connectivity(G, nbunch=nodes, flow_func=flow_func)

    for i in range(n):
        for j in range(i + 1, n):
            vrijednost = kappa[nodes[i]][nodes[j]]
            K[i, j] = vrijednost
            K[j, i] = vrijednost

    return K


def baza_povezanosti(G, flow_func=None, ispisi=True, vrati_vremena=False):
    """Određuje dimenziju povezanosti i jednu bazu povezanosti.

    Algoritam je namijenjen povezanim grafovima, osobito Horadamovim i
    metalnim kockama. Koristi:
      - jednu matricu lokalnih povezanosti K,
      - poseban slučaj uniformne povezanosti,
      - donju ogradu preko maksimalnog stupnja,
      - unaprijed izračunate vrijednosti L_ij,
      - povratno pretraživanje s odsijecanjem.

    Ako je vrati_vremena=True, rječnik vremena uključuje i broj posjećenih
    čvorova stabla pretraživanja (ključ "posjeceni_cvorovi"; 0 ako je
    cdim(G) određen izravno preko uniformne povezanosti, bez pretrage).

    Povratna vrijednost
    -------------------
    (cdim, baza) ili (cdim, baza, vremena)
    """
    if G.is_directed():
        raise ValueError("Ova implementacija očekuje neusmjeren graf.")
    if len(G) == 0:
        raise ValueError("Graf mora imati barem jedan vrh.")
    if not nx.is_connected(G):
        raise ValueError("Ova implementacija baze povezanosti očekuje povezan graf.")

    nodes = sorted(G.nodes())
    n = len(nodes)

    if n == 1:
        rezultat = (0, [])
        vremena = {
            "t_K": 0.0,
            "t_uniformnost": 0.0,
            "t_L": 0.0,
            "t_pretraga": 0.0,
            "t_nakon_K": 0.0,
            "t_ukupno": 0.0,
            "posjeceni_cvorovi": 0,
        }
        if ispisi:
            print("Dimenzija povezanosti: 0")
            print("Baza povezanosti: {}")
        return (*rezultat, vremena) if vrati_vremena else rezultat

    t0 = time.perf_counter()

    t = time.perf_counter()
    K = matrica_lokalnih_povezanosti(G, flow_func=flow_func, nodes=nodes)
    t_K = time.perf_counter() - t

    t_nakon_K_pocetak = time.perf_counter()

    # Teorem: cdim(G) = n - 1 ako i samo ako je povezani graf uniformno
    # k-povezan. Provjeravaju se samo elementi iznad dijagonale.
    t = time.perf_counter()
    vrijednosti_iznad_dijagonale = K[np.triu_indices(n, k=1)]
    uniforman = np.all(vrijednosti_iznad_dijagonale == vrijednosti_iznad_dijagonale[0])
    t_uniformnost = time.perf_counter() - t

    if uniforman:
        cdim = n - 1
        baza = nodes[:-1]
        t_ukupno = time.perf_counter() - t0
        t_nakon_K = time.perf_counter() - t_nakon_K_pocetak
        vremena = {
            "t_K": t_K,
            "t_uniformnost": t_uniformnost,
            "t_L": 0.0,
            "t_pretraga": 0.0,
            "t_nakon_K": t_nakon_K,
            "t_ukupno": t_ukupno,
            "posjeceni_cvorovi": 0,
        }
        if ispisi:
            print(f"Dimenzija povezanosti: {cdim}")
            print(f"Baza povezanosti: {{{', '.join(map(str, baza))}}}")
        return (cdim, baza, vremena) if vrati_vremena else (cdim, baza)

    # Budući da graf nije uniforman, n >= 3 i Delta >= 2.
    delta = max(dict(G.degree()).values())
    if delta < 2:
        raise RuntimeError("Neočekivan slučaj: neuniforman povezani graf s Delta < 2.")

    # Egzaktno računanje stropa logaritma bez pogreške zaokruživanja:
    # k0 je najmanji cijeli k za koji vrijedi 2 * Delta^k >= n + 1.
    k0 = 0
    potencija = 1
    while 2 * potencija < n + 1:
        potencija *= delta
        k0 += 1
    k0 = max(1, k0)

    t = time.perf_counter()
    L = _zadnji_razlikujuci_indeksi(K)
    t_L = time.perf_counter() - t

    t = time.perf_counter()
    # Nakon što je uniformni slučaj isključen, vrijedi cdim(G) <= n - 2.
    pronadeno = _pronadi_generator(K, L, k_start=k0, k_kraj=n - 2)
    t_pretraga = time.perf_counter() - t

    if pronadeno is None:
        raise RuntimeError(
            "Nije pronađena baza povezanosti u rasponu dopuštenom teorijskim "
            "granicama. Provjerite implementaciju ili ulazni graf."
        )

    cdim, indeksi, posjeceni_cvorovi = pronadeno
    baza = [nodes[i] for i in indeksi]

    t_nakon_K = time.perf_counter() - t_nakon_K_pocetak
    t_ukupno = time.perf_counter() - t0

    vremena = {
        "t_K": t_K,
        "t_uniformnost": t_uniformnost,
        "t_L": t_L,
        "t_pretraga": t_pretraga,
        "t_nakon_K": t_nakon_K,
        "t_ukupno": t_ukupno,
        "k0": k0,
        "Delta": delta,
        "posjeceni_cvorovi": posjeceni_cvorovi,
    }

    if ispisi:
        print(f"Dimenzija povezanosti: {cdim}")
        print(f"Baza povezanosti: {{{', '.join(map(str, baza))}}}")
        print(f"Donja ograda k0: {k0}")

    return (cdim, baza, vremena) if vrati_vremena else (cdim, baza)


# ---------------------------------------------------------------------------
# POMOĆ ZA EKSPERIMENTE: ODABIR ALGORITMA MAKSIMALNOG TOKA
# ---------------------------------------------------------------------------


def usporedi_flow_algoritme(G, ponavljanja=3):
    """Uspoređuje egzaktne flow-algoritme za računanje matrice K.

    Vraća rječnik s prosječnim, minimalnim i maksimalnim vremenom. Također
    provjerava da svi algoritmi daju istu matricu lokalnih povezanosti.

    Ova funkcija služi samo za benchmark i odabir postupka u eksperimentima;
    nije dio samog algoritma za određivanje baze povezanosti.
    """
    if ponavljanja < 1:
        raise ValueError("Broj ponavljanja mora biti barem 1.")

    algoritmi = {
        "edmonds_karp": nx.algorithms.flow.edmonds_karp,
        "shortest_augmenting_path": nx.algorithms.flow.shortest_augmenting_path,
        "preflow_push": nx.algorithms.flow.preflow_push,
    }

    rezultati = {}
    referentna_matrica = None

    for naziv, flow_func in algoritmi.items():
        vremena = []
        zadnja_matrica = None

        for _ in range(ponavljanja):
            t = time.perf_counter()
            zadnja_matrica = matrica_lokalnih_povezanosti(
                G, flow_func=flow_func
            )
            vremena.append(time.perf_counter() - t)

        if referentna_matrica is None:
            referentna_matrica = zadnja_matrica
        elif not np.array_equal(referentna_matrica, zadnja_matrica):
            raise RuntimeError(
                f"Algoritam {naziv} nije dao istu matricu lokalnih povezanosti."
            )

        rezultati[naziv] = {
            "prosjek": float(np.mean(vremena)),
            "medijan": float(np.median(vremena)),
            "minimum": float(np.min(vremena)),
            "maksimum": float(np.max(vremena)),
            "sva_vremena": vremena,
        }

    return rezultati