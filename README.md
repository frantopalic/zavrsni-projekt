# Završni praktični projekt

Projekt iz završnog praktičnog rada koji se bavi implementacijom algoritama za pronalazak **metričkih baza** i **baza povezanosti** neusmjerenih povezanih grafova te izgradnjom **Horadamovih** i **metalnih kocki**.

Implementirani su optimizirani algoritmi koji koriste povratno pretraživanje s odsijecanjem, kao i odgovarajući brute-force algoritmi koji služe za provjeru ispravnosti i usporedbu vremena izvođenja.

## Sadržaj repozitorija

* `utils.py` – optimizirani algoritmi za pronalazak metričke baze i baze povezanosti te funkcije za računanje potrebnih matrica i mjerenje vremena izvođenja
* `utils_brute.py` – brute-force algoritmi za pronalazak metričke baze i baze povezanosti
* `horadam_kocke.py` – funkcije za izgradnju Horadamovih kocki
* `metalne_kocke.py` – funkcije za izgradnju metalnih kocki
* `zavrsni.ipynb` – glavni Jupyter notebook s primjerima korištenja i eksperimentima
* `requirements.txt` – popis potrebnih Python biblioteka

## Biblioteke

U projektu se koriste sljedeće biblioteke:

* [NetworkX](https://networkx.org/) – rad s grafovima, računanje udaljenosti i lokalnih povezanosti te algoritmi maksimalnog toka
* [NumPy](https://numpy.org/) – vektorizirani izračun L1 udaljenosti
* [Matplotlib](https://matplotlib.org/) – vizualizacija grafova
* [math](https://docs.python.org/3/library/math.html) – matematičke funkcije
* [functools](https://docs.python.org/3/library/functools.html) – memoizacija rekurzivne konstrukcije kocki
* [time](https://docs.python.org/3/library/time.html) – mjerenje vremena izvođenja

## Instalacija

Za pokretanje projekta potreban je Python 3.9 ili noviji.

Potrebne biblioteke mogu se instalirati naredbom:

```bash
pip install -r requirements.txt
```

## Pokretanje

Projekt se koristi kroz Jupyter Notebook.

Nakon instalacije potrebnih biblioteka pokrenuti Jupyter:

```bash
jupyter notebook zavrsni.ipynb
```

Zatim otvoriti `zavrsni.ipynb` i pokretati ćelije redom.

---

# `utils.py`

Datoteka `utils.py` sadrži optimizirane algoritme za određivanje metričke dimenzije i dimenzije povezanosti povezanog neusmjerenog grafa.

Za smanjenje broja ispitanih kandidata koristi se **povratno pretraživanje s odsijecanjem**.

## Metrička baza

### `metricka_baza`

Funkcija `metricka_baza` određuje metričku dimenziju grafa i pronalazi jednu metričku bazu.

Najprije se računaju udaljenosti između vrhova i spremaju u matricu `D`. Za Horadamove i metalne kocke može se koristiti opcija `brza_l1=True`, pri čemu se udaljenosti računaju izravno pomoću L1 udaljenosti oznaka vrhova.

Za svaki par vrhova unaprijed se računa vrijednost `L`, koja se koristi za određivanje kandidata koji još mogu razlikovati promatrani par vrhova.

Pretraživanje počinje od skupova najmanje kardinalnosti. Tijekom pretraživanja koriste se uvjeti odsijecanja kojima se odbacuju grane koje više ne mogu dovesti do valjanog generatora.

## Dimenzija povezanosti

### `matrica_lokalnih_povezanosti`

Funkcija `matrica_lokalnih_povezanosti` računa matricu lokalnih vršnih povezanosti `K`.

Za različite vrhove `u` i `v` vrijedi:

```text
K[u,v] = κ(u,v)
```

dok se na dijagonalu matrice postavlja vrijednost beskonačnosti.

Vrijednosti lokalnih povezanosti računaju se pomoću funkcije `nx.all_pairs_node_connectivity`, uz mogućnost odabira algoritma maksimalnog toka.

### `baza_povezanosti`

Funkcija `baza_povezanosti` određuje dimenziju povezanosti grafa i pronalazi bazu povezanosti.

Prije pretraživanja provjerava se je li graf uniformno `k`-povezan. Ako jest, rezultat se određuje izravno.

U suprotnom se računa teorijska donja ograda te se povratnim pretraživanjem ispituju potrebne veličine skupova. Pretraživanje se provodi samo za veličine od dobivene donje ograde do `n-2`.

## Povratno pretraživanje

Za pronalazak generatora koristi se zajednička funkcija `_pronadi_generator`.

Funkcija može raditi s:

* matricom udaljenosti `D` kod metričke dimenzije
* matricom lokalnih povezanosti `K` kod dimenzije povezanosti

Kandidat razlikuje dva vrha ako su odgovarajuće vrijednosti u njegovom stupcu različite.

Pretraživanje se provodi po rastućim indeksima kandidata, a pomoću odsijecanja izbjegavaju se grane stabla pretraživanja za koje nije moguće dobiti valjani generator.

## Mjerenje vremena izvođenja

Implementacija omogućuje mjerenje vremena pojedinih faza algoritama i broja posjećenih čvorova stabla pretraživanja.

Za metričku dimenziju mogu se mjeriti:

* vrijeme izgradnje matrice udaljenosti `D`
* vrijeme računanja matrice `L`
* vrijeme pretraživanja
* ukupan broj posjećenih čvorova stabla pretraživanja

Za dimenziju povezanosti dodatno se mogu izdvojiti:

* vrijeme računanja matrice lokalnih povezanosti `K`
* vrijeme provjere uniformne povezanosti
* vrijeme pretraživanja nakon izgradnje matrice `K`
* broj posjećenih čvorova stabla pretraživanja

## Usporedba algoritama maksimalnog toka

### `usporedi_flow_algoritme`

Funkcija `usporedi_flow_algoritme` služi za usporedbu algoritama maksimalnog toka koji se mogu koristiti pri računanju matrice lokalnih povezanosti `K`.

Uspoređuju se:

* Edmonds–Karp
* Shortest Augmenting Path
* Preflow-Push

Za svaki algoritam mjeri se vrijeme računanja matrice `K` kroz više ponavljanja. Također se provjerava daju li svi algoritmi jednaku matricu lokalnih povezanosti.

Ova funkcija služi za odabir algoritma maksimalnog toka koji će se koristiti u eksperimentima.

---

# `utils_brute.py`

Datoteka `utils_brute.py` sadrži brute-force algoritme za određivanje metričke dimenzije i dimenzije povezanosti povezanog neusmjerenog grafa.

Brute-force algoritmi ispituju potrebne podskupove vrhova po rastućoj kardinalnosti. Zbog eksponencijalne složenosti namijenjeni su prvenstveno manjim grafovima.

Osim za određivanje rezultata na manjim grafovima, koriste se za **provjeru ispravnosti optimiziranih algoritama**.

## `metricka_baza_brute`

Funkcija najprije računa udaljenosti između svih parova vrhova pomoću `nx.all_pairs_shortest_path_length`.

Nakon toga ispituje podskupove vrhova po rastućoj kardinalnosti. Prvi pronađeni skup koji razlikuje sve parove vrhova predstavlja metričku bazu.

## `baza_povezanosti_brute`

Funkcija najprije računa lokalne vršne povezanosti između svih parova vrhova pomoću `nx.all_pairs_node_connectivity`.

Nakon toga ispituje podskupove vrhova po rastućoj kardinalnosti sve dok ne pronađe bazu povezanosti.

Za lokalnu povezanost vrha sa samim sobom koristi se vrijednost beskonačnosti.

## Rezultati brute-force algoritama

Obje brute-force funkcije mogu vratiti:

* jednu bazu minimalne kardinalnosti ili sve takve baze
* vrijeme početnog izračuna
* vrijeme brute-force pretrage
* ukupno vrijeme izvođenja
* broj ispitanih podskupova vrhova

---

# `horadam_kocke.py`

Datoteka `horadam_kocke.py` sadrži funkcije za izgradnju Horadamovih kocki.

Horadamove kocke koriste se kao jedna od glavnih klasa grafova na kojima se ispituju implementirani algoritmi za metričku dimenziju i dimenziju povezanosti.

---

# `metalne_kocke.py`

Datoteka `metalne_kocke.py` sadrži funkcije za izgradnju metalnih kocki.

Metalne kocke koriste se za testiranje implementiranih algoritama i usporedbu dobivenih rezultata.

---

# `zavrsni.ipynb`

Datoteka `zavrsni.ipynb` glavni je Jupyter notebook projekta.

Notebook sadrži primjere:

* izgradnje Horadamovih kocki
* izgradnje metalnih kocki
* određivanja metričkih baza
* određivanja baza povezanosti
* korištenja optimiziranih algoritama
* korištenja brute-force algoritama
* provjere jednakosti rezultata optimiziranih i brute-force algoritama
* mjerenja vremena izvođenja
* usporedbe algoritama maksimalnog toka

---

# Testiranje i usporedba algoritama

Brute-force implementacije koriste se za provjeru ispravnosti optimiziranih algoritama na manjim grafovima.

Kod usporedbe rezultata provjerava se jednakost dobivene **metričke dimenzije** i **dimenzije povezanosti**. Same baze ne moraju biti jednake jer graf može imati više baza iste minimalne kardinalnosti.

Za manje Horadamove kocke uspoređuju se i vremena izvođenja brute-force i optimiziranih algoritama kako bi se pokazao utjecaj povratnog pretraživanja i odsijecanja na broj ispitanih kandidata i vrijeme izvođenja.

---

# Napomena

Implementacija je namijenjena **povezanim neusmjerenim grafovima**.

Opciju `brza_l1=True` treba koristiti samo kada je poznato da je grafovska udaljenost jednaka L1 udaljenosti oznaka vrhova, kao kod Horadamovih i metalnih kocki.

Optimizirani algoritmi i dalje u najgorem slučaju imaju eksponencijalnu složenost, ali korištenje odsijecanja i teorijskih granica može znatno smanjiti prostor pretraživanja.

Iako optimizirani algoritmi koriste odsijecanje i teorijske granice za smanjenje prostora pretraživanja, u najgorem slučaju i dalje imaju eksponencijalnu složenost.
