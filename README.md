# Završni praktični rad

Implementacija algoritama za određivanje metričke dimenzije i dimenzije povezanosti neusmjerenih povezanih grafova te konstrukcija Horadamovih i metalnih kocki.

## Opis projekta

Cilj projekta je implementirati algoritme za pronalazak metričke baze i baze povezanosti grafa. Uz algoritme za određivanje navedenih dimenzija, implementirane su i funkcije za konstrukciju Horadamovih i metalnih kocki.

Za određivanje baza implementirane su dvije vrste algoritama:

- optimizirani algoritmi koji koriste povratno pretraživanje s odsijecanjem
- brute-force algoritmi koji ispituju podskupove vrhova rastuće kardinalnosti

Brute-force implementacije služe kao referentne implementacije za provjeru ispravnosti optimiziranih algoritama na manjim grafovima.

Projekt je implementiran u programskom jeziku Python uz korištenje biblioteke [NetworkX](https://networkx.org/) za rad s grafovima.

## Struktura projekta

- `utils.py` – pomoćne funkcije za rad s grafovima, vizualizaciju te optimizirani algoritmi za pronalazak metričke baze i baze povezanosti
- `utils_brute.py` – referentne brute-force implementacije za pronalazak metričke baze i baze povezanosti
- `horadam_kocke.py` – funkcija za konstrukciju Horadamovih kocki
- `metalne_kocke.py` – funkcija za konstrukciju metalnih kocki kao posebnog slučaja Horadamovih kocki
- `zavrsni.ipynb` – glavni Jupyter notebook s primjerima korištenja i eksperimentalnim rezultatima
- `requirements.txt` – popis potrebnih Python biblioteka

> Napomena: `zavrsni.ipynb` bit će dodan nakon izrade eksperimentalnog dijela projekta.

## Zahtjevi

Za pokretanje projekta potrebno je imati:

- Python 3.9 ili noviji
- Jupyter Notebook ili JupyterLab

Python 3.9 ili noviji potreban je zbog korištenja funkcionalnosti `functools.cache`.

## Instalacija

Preporučuje se korištenje virtualnog okruženja.

### Kloniranje repozitorija

```bash
git clone <URL_REPOZITORIJA>
cd <NAZIV_REPOZITORIJA>
```

### Kreiranje virtualnog okruženja

Na Windows sustavu:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Na Linux/macOS sustavu:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Instalacija potrebnih biblioteka

```bash
pip install -r requirements.txt
```

## Pokretanje

Nakon instalacije potrebnih biblioteka Jupyter Notebook može se pokrenuti naredbom:

```bash
jupyter notebook
```

Nakon izrade eksperimentalnog dijela projekta potrebno je otvoriti:

```text
zavrsni.ipynb
```

Pojedine funkcije mogu se koristiti i izravno iz Python datoteka.

# Korištene biblioteke

- [NetworkX](https://networkx.org/) – rad s grafovima, računanje udaljenosti i lokalnih vršnih povezanosti
- [NumPy](https://numpy.org/) – rad s matricama i ubrzani izračun L1 udaljenosti
- [Matplotlib](https://matplotlib.org/) – vizualizacija grafova
- [math](https://docs.python.org/3/library/math.html) – matematičke funkcije
- [functools](https://docs.python.org/3/library/functools.html) – memoizacija rekurzivne konstrukcije Horadamovih kocki
- [time](https://docs.python.org/3/library/time.html) – mjerenje vremena izvođenja

# `utils.py`

Datoteka `utils.py` sadrži pomoćne funkcije za rad s grafovima te optimizirane algoritme za određivanje metričke dimenzije i dimenzije povezanosti.

## `napravi_graf`

```python
napravi_graf(n, bridovi)
```

Funkcija gradi jednostavan neusmjeren graf s vrhovima označenima brojevima od `1` do `n`.

Primjer:

```python
G = napravi_graf(
    5,
    [(1, 2), (2, 3), (3, 4), (4, 5)]
)
```

Funkcija provjerava valjanost bridova te preskače:

- bridove koji sadrže vrh izvan zadanog raspona
- petlje
- već postojeće bridove

## `crtaj_graf`

```python
crtaj_graf(G)
```

Funkcija vizualizira zadani graf pomoću biblioteke Matplotlib.

Primjer:

```python
crtaj_graf(G)
```

# Metrička dimenzija

## `metricka_baza`

```python
metricka_baza(
    G,
    brza_l1=False,
    ispisi=True,
    vrati_vremena=False
)
```

Funkcija određuje metričku dimenziju povezanog neusmjerenog grafa i vraća jednu metričku bazu.

Primjer:

```python
mdim, baza = metricka_baza(G)
```

Ako je potrebno dobiti i vremena izvođenja:

```python
mdim, baza, vremena = metricka_baza(
    G,
    vrati_vremena=True
)
```

Rječnik `vremena` sadrži:

- `t_matrica` – vrijeme računanja matrice udaljenosti
- `t_L` – vrijeme računanja pomoćne matrice `L`
- `t_pretraga` – vrijeme pretraživanja
- `t_ukupno` – ukupno vrijeme izvođenja
- `posjeceni_cvorovi` – broj posjećenih čvorova stabla pretraživanja

## Ubrzani L1 izračun

Kod Horadamovih i metalnih kocki moguće je koristiti ubrzani izračun udaljenosti pomoću L1 metrike:

```python
mdim, baza = metricka_baza(
    G,
    brza_l1=True
)
```

Opcija `brza_l1=True` smije se koristiti samo kada je udaljenost grafa jednaka L1 udaljenosti oznaka vrhova. U ovom projektu to vrijedi za Horadamove i metalne kocke.

Kod korištenja ubrzanog izračuna udaljenosti izbjegava se računanje udaljenosti za svaki par vrhova pomoću BFS-a te se udaljenosti računaju izravno iz oznaka vrhova.

## Povratno pretraživanje s odsijecanjem

Optimizirani algoritam za pronalazak metričke baze koristi povratno pretraživanje s odsijecanjem.

Pretraživanje se provodi za skupove rastuće kardinalnosti. Za svaki trenutačno odabrani skup provjerava se mogu li preostali kandidati još uvijek dovesti do generatora.

Koriste se dva glavna pravila odsijecanja:

1. mora ostati dovoljno kandidata da se skup može nadopuniti do tražene kardinalnosti
2. svaki trenutno nerazlučen par vrhova mora imati kandidata koji ga još može razlučiti

Na taj se način izbjegavaju grane stabla pretraživanja koje ne mogu dovesti do rješenja.

Funkcija također broji broj posjećenih čvorova stabla pretraživanja. Taj se podatak koristi za eksperimentalnu analizu učinka odsijecanja.

# Dimenzija povezanosti

## `matrica_lokalnih_povezanosti`

```python
matrica_lokalnih_povezanosti(
    G,
    flow_func=None,
    nodes=None
)
```

Funkcija računa matricu lokalnih vršnih povezanosti `K`.

Za različite vrhove `u` i `v` vrijedi:

```text
K[u,v] = κ(u,v)
```

Na glavnoj dijagonali matrice postavlja se beskonačnost.

Za računanje lokalnih vršnih povezanosti koristi se funkcija `all_pairs_node_connectivity` iz biblioteke NetworkX.

Funkciji se može proslijediti algoritam maksimalnog toka, primjerice:

```python
nx.algorithms.flow.edmonds_karp
```

ili:

```python
nx.algorithms.flow.shortest_augmenting_path
```

## `baza_povezanosti`

```python
baza_povezanosti(
    G,
    flow_func=None,
    ispisi=True,
    vrati_vremena=False
)
```

Funkcija određuje dimenziju povezanosti povezanog neusmjerenog grafa i vraća jednu bazu povezanosti.

Primjer:

```python
cdim, baza = baza_povezanosti(G)
```

Za dobivanje vremena pojedinih faza:

```python
cdim, baza, vremena = baza_povezanosti(
    G,
    vrati_vremena=True
)
```

Rječnik `vremena` sadrži:

- `t_K` – vrijeme računanja matrice lokalnih povezanosti
- `t_uniformnost` – vrijeme provjere uniformne povezanosti
- `t_L` – vrijeme računanja pomoćne matrice `L`
- `t_pretraga` – vrijeme povratnog pretraživanja
- `t_nakon_K` – vrijeme potrebno nakon izračuna matrice `K`
- `t_ukupno` – ukupno vrijeme izvođenja
- `posjeceni_cvorovi` – broj posjećenih čvorova stabla pretraživanja

U slučaju kada se dimenzija povezanosti odredi izravno na temelju uniformne povezanosti, pretraživanje nije potrebno pa je broj posjećenih čvorova jednak nuli.

## Donja ograda

Optimizirani algoritam za dimenziju povezanosti koristi teorijsku donju ogradu kako bi smanjio broj veličina skupova koje je potrebno ispitivati.

Najprije se provjerava je li graf uniformno povezan. Ako jest, dimenzija povezanosti određuje se izravno.

U suprotnom se računa donja ograda na temelju broja vrhova i maksimalnog stupnja grafa. Pretraživanje se tada pokreće od dobivene donje granice.

Na taj se način smanjuje prostor pretraživanja u odnosu na potpuno ispitivanje svih podskupova.

# Zajednički algoritam pretraživanja

Za metričku dimenziju i dimenziju povezanosti koristi se zajednička pomoćna funkcija `_pronadi_generator`.

Funkcija radi nad matricom `M`, pri čemu:

- redci predstavljaju vrhove koje treba razlučiti
- stupci predstavljaju moguće kandidate za bazu
- kandidat `r` razlučuje par `(i,j)` ako vrijedi `M[i,r] != M[j,r]`

Za dodatno smanjenje prostora pretraživanja koristi se pomoćna matrica `L`.

Algoritam vraća prvu pronađenu bazu najmanje moguće kardinalnosti.

Budući da baza nije nužno jedinstvena, optimizirani algoritam vraća jednu od mogućih baza.

# `utils_brute.py`

Datoteka `utils_brute.py` sadrži referentne brute-force implementacije za određivanje metričke dimenzije i dimenzije povezanosti.

Brute-force algoritmi namijenjeni su prvenstveno provjeri ispravnosti optimiziranih algoritama na manjim grafovima.

Za razliku od optimiziranih algoritama, brute-force implementacije ne koriste povratno pretraživanje niti pravila odsijecanja. Umjesto toga ispituju podskupove vrhova po rastućoj kardinalnosti.

# Brute-force metrička dimenzija

## `metricka_baza_brute`

```python
metricka_baza_brute(
    G,
    ispisi=True,
    vrati_sve_baze=False,
    vrati_vremena=False
)
```

Funkcija određuje metričku dimenziju potpunim pregledom podskupova vrhova.

Najprije se računaju sve parne udaljenosti u grafu, a zatim se ispituju podskupovi vrhova kardinalnosti:

```text
1, 2, ..., n-1
```

Prva kardinalnost za koju postoji metrički generator predstavlja metričku dimenziju.

Primjer:

```python
mdim, baza = metricka_baza_brute(G)
```

Moguće je zatražiti sve metričke baze minimalne kardinalnosti:

```python
mdim, baze = metricka_baza_brute(
    G,
    vrati_sve_baze=True
)
```

Ako je uključeno mjerenje vremena:

```python
mdim, baza, vremena = metricka_baza_brute(
    G,
    vrati_vremena=True
)
```

Rječnik `vremena` sadrži:

- `t_udaljenosti` – vrijeme računanja udaljenosti
- `t_pretraga` – vrijeme brute-force pretraživanja
- `t_ukupno` – ukupno vrijeme izvođenja
- `razmotreni_podskupovi` – broj razmotrenih podskupova

Broj razmotrenih podskupova jednak je zbroju broja podskupova ispitanih za kardinalnosti od `1` do metričke dimenzije.

# Brute-force dimenzija povezanosti

## `baza_povezanosti_brute`

```python
baza_povezanosti_brute(
    G,
    flow_func=None,
    ispisi=True,
    vrati_sve_baze=False,
    vrati_vremena=False
)
```

Funkcija određuje dimenziju povezanosti potpunim pregledom podskupova vrhova.

Prije pretraživanja računaju se lokalne vršne povezanosti između svih parova vrhova.

Primjer:

```python
cdim, baza = baza_povezanosti_brute(G)
```

Moguće je dobiti i sve baze minimalne kardinalnosti:

```python
cdim, baze = baza_povezanosti_brute(
    G,
    vrati_sve_baze=True
)
```

Kod mjerenja vremena funkcija vraća:

- `t_kappa` – vrijeme računanja lokalnih vršnih povezanosti
- `t_pretraga` – vrijeme brute-force pretraživanja
- `t_ukupno` – ukupno vrijeme izvođenja
- `razmotreni_podskupovi` – broj razmotrenih podskupova

# Uloga brute-force algoritama

Brute-force algoritmi imaju eksponencijalni rast broja podskupova koje je potrebno ispitati pa nisu namijenjeni velikim grafovima.

U ovom projektu koriste se kao referentne implementacije za provjeru optimiziranih algoritama na manjim grafovima.

Dobivene vrijednosti metričke dimenzije i dimenzije povezanosti uspoređuju se s rezultatima optimiziranih algoritama.

Očekuje se da optimizirani i brute-force algoritam daju istu vrijednost dimenzije.

Dobivene baze ne moraju biti jednake jer graf može imati više različitih baza iste minimalne kardinalnosti.

# Horadamove kocke

## `horadam_kocke.py`

Datoteka `horadam_kocke.py` sadrži funkciju:

```python
horadam_cubes(n, a, b)
```

koja rekurzivno konstruira Horadamovu kocku.

Parametri funkcije su:

- `n` – duljina riječi
- `a` – prvi Horadamov parametar
- `b` – drugi Horadamov parametar

Funkcija vraća graf tipa:

```python
nx.Graph
```

čiji su vrhovi predstavljeni `n`-torkama cijelih brojeva.

Primjer:

```python
from horadam_kocke import horadam_cubes

G = horadam_cubes(4, 2, 1)
```

Konstrukcija se temelji na rekurzivnoj definiciji Horadamovih kocki.

Za ubrzavanje ponovljenih rekurzivnih izračuna koristi se memoizacija pomoću `functools.cache`.

# Metalne kocke

## `metalne_kocke.py`

Metalne kocke predstavljaju poseban slučaj Horadamovih kocki za:

```text
b = 1
```

Datoteka `metalne_kocke.py` sadrži funkciju:

```python
metallic_cubes(n, a)
```

koja interno poziva:

```python
horadam_cubes(n, a, 1)
```

Primjer:

```python
from metalne_kocke import metallic_cubes

G = metallic_cubes(4, 2)
```

Na taj način metalne kocke koriste istu osnovnu implementaciju kao Horadamove kocke.

# Usporedba algoritama maksimalnog toka

Za potrebe eksperimentalne analize implementirana je funkcija:

```python
usporedi_flow_algoritme(G, ponavljanja=3)
```

Funkcija uspoređuje tri egzaktna algoritma maksimalnog toka:

- Edmonds–Karp
- shortest augmenting path
- preflow-push

Primjer:

```python
rezultati = usporedi_flow_algoritme(
    G,
    ponavljanja=3
)
```

Za svaki algoritam mjerenje se ponavlja zadani broj puta.

Funkcija vraća:

- prosječno vrijeme
- medijan vremena
- minimalno vrijeme
- maksimalno vrijeme
- sva pojedinačna vremena

Osim usporedbe vremena izvođenja, provjerava se i daju li svi algoritmi istu matricu lokalnih povezanosti.

Ova funkcija služi isključivo za benchmark i odabir algoritma maksimalnog toka koji će se koristiti u eksperimentima. Nije dio samog algoritma za određivanje baze povezanosti.

# Mjerenje vremena

Za mjerenje vremena izvođenja koristi se:

```python
time.perf_counter()
```

Vrijeme se mjeri odvojeno za pojedine faze algoritama gdje je to potrebno.

Kod metričke dimenzije moguće je pratiti:

- računanje matrice udaljenosti
- računanje pomoćne matrice `L`
- povratno pretraživanje
- ukupno vrijeme izvođenja

Kod dimenzije povezanosti moguće je pratiti:

- računanje matrice lokalnih povezanosti `K`
- provjeru uniformne povezanosti
- računanje pomoćne matrice `L`
- povratno pretraživanje
- vrijeme nakon izračuna matrice `K`
- ukupno vrijeme izvođenja

Za optimizirane algoritme bilježi se i broj posjećenih čvorova stabla pretraživanja.

Za brute-force algoritme bilježi se broj razmotrenih podskupova.

U eksperimentalnom dijelu mjerenja se ponavljaju više puta, a za prikaz rezultata koriste se odgovarajuće statistike, poput prosječnog ili medijalnog vremena.

# Eksperimentalna analiza

Eksperimentalna analiza provodi se na Horadamovim kockama različitih parametara i veličina.

Ciljevi eksperimentalne analize su:

1. provjeriti ispravnost optimiziranih algoritama
2. usporediti optimizirane algoritme s brute-force implementacijama
3. analizirati vrijeme izvođenja algoritama
4. analizirati broj posjećenih čvorova stabla pretraživanja
5. pokazati utjecaj odsijecanja na smanjenje prostora pretraživanja
6. usporediti različite algoritme maksimalnog toka
7. odrediti najprikladniji algoritam maksimalnog toka za računanje matrice lokalnih povezanosti

Na manjim Horadamovim kockama rezultati optimiziranih algoritama uspoređuju se s rezultatima brute-force algoritama.

Kod provjere ispravnosti uspoređuju se dobivene vrijednosti metričke dimenzije i dimenzije povezanosti. Baze ne moraju biti jednake jer može postojati više baza iste minimalne kardinalnosti.

Za veće grafove koriste se optimizirani algoritmi jer potpuni pregled svih podskupova postaje računalno zahtjevan.

# Primjeri korištenja

## Primjer rada s proizvoljnim grafom

```python
from utils import napravi_graf, crtaj_graf, metricka_baza

G = napravi_graf(
    5,
    [(1, 2), (2, 3), (3, 4), (4, 5)]
)

crtaj_graf(G)

mdim, baza = metricka_baza(G)

print("Metrička dimenzija:", mdim)
print("Metrička baza:", baza)
```

## Primjer određivanja dimenzije povezanosti

```python
from utils import baza_povezanosti

cdim, baza = baza_povezanosti(G)

print("Dimenzija povezanosti:", cdim)
print("Baza povezanosti:", baza)
```

## Primjer konstrukcije Horadamove kocke

```python
from horadam_kocke import horadam_cubes

G = horadam_cubes(4, 2, 1)
```

## Primjer konstrukcije metalne kocke

```python
from metalne_kocke import metallic_cubes

G = metallic_cubes(4, 2)
```

## Primjer određivanja metričke dimenzije Horadamove kocke

Za Horadamove i metalne kocke može se koristiti ubrzani L1 izračun udaljenosti:

```python
from horadam_kocke import horadam_cubes
from utils import metricka_baza

G = horadam_cubes(4, 2, 1)

mdim, baza = metricka_baza(
    G,
    brza_l1=True
)

print("Metrička dimenzija:", mdim)
print("Metrička baza:", baza)
```

## Primjer mjerenja vremena

```python
mdim, baza, vremena = metricka_baza(
    G,
    brza_l1=True,
    vrati_vremena=True
)

print("Metrička dimenzija:", mdim)
print("Metrička baza:", baza)
print("Vrijeme:", vremena)
```

Za dimenziju povezanosti:

```python
cdim, baza, vremena = baza_povezanosti(
    G,
    vrati_vremena=True
)

print("Dimenzija povezanosti:", cdim)
print("Baza povezanosti:", baza)
print("Vrijeme:", vremena)
```

# Napomena o implementaciji

Implementirani algoritmi namijenjeni su povezanim neusmjerenim grafovima.

Optimizirani algoritmi i dalje u najgorem slučaju imaju eksponencijalnu složenost zbog problema pronalaska minimalnog generatora. Međutim, povratno pretraživanje, pravila odsijecanja i korištenje teorijskih donjih ograda mogu znatno smanjiti prostor pretraživanja u odnosu na potpuni brute-force pristup.

Poseban slučaj predstavlja računanje udaljenosti za Horadamove i metalne kocke. Budući da su njihovi vrhovi zapisani kao n-torke cijelih brojeva, za njih se može koristiti ubrzani L1 izračun kada je udaljenost grafa jednaka L1 udaljenosti oznaka vrhova.

# Rezultati

Detaljna eksperimentalna analiza rezultata bit će prikazana u Jupyter notebooku `zavrsni.ipynb`.

Eksperimenti uključuju:

- provjeru ispravnosti optimiziranih algoritama pomoću brute-force implementacija
- mjerenje vremena izvođenja
- usporedbu vremena brute-force i optimiziranih algoritama
- analizu broja posjećenih čvorova stabla pretraživanja
- analizu utjecaja odsijecanja
- analizu vremena računanja matrice lokalnih povezanosti
- usporedbu algoritama maksimalnog toka

# Autor

**Fran Topalić**

Završni praktični rad
