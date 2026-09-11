# Završni praktični projekt

Projekt iz završnog praktičnog rada. Implementacija algoritama za pronalazak metričkih baza i baza povezanosti neusmjerenih povezanih grafova te implementacija funkcija za izgradnju metalnih kocki i Horadamovih kocki.

## Sadržaj

* `utils.py` - optimirani algoritmi za pronalazak metričke baze i baze povezanosti, računanje potrebnih matrica i mjerenje vremena izvođenja
* `utils_brute.py` - brute-force algoritmi za pronalazak metričke baze i baze povezanosti
* `metalne_kocke.py` - funkcija za izgradnju metalnih kocki
* `horadam_kocke.py` - funkcija za izgradnju Horadamovih kocki
* `zavrsni.ipynb` - glavni Jupyter notebook s implementacijom, primjerima i eksperimentima

Optimirani algoritmi koriste povratno pretraživanje s odsijecanjem kako bi smanjili broj nepotrebno ispitanih podskupova vrhova. Brute-force algoritmi ispituju sve potrebne podskupove te se koriste prvenstveno za manje grafove i provjeru ispravnosti optimiziranih algoritama.

## Zahtjevi

* Python ≥ 3.9
* Jupyter Notebook
* NetworkX
* NumPy
* Matplotlib

## Instalacija

1. Klonirati repozitorij.
2. Instalirati potrebne biblioteke:

```bash
pip install -r requirements.txt
```

## Pokretanje

Pokrenuti Jupyter Notebook:

```bash
jupyter notebook zavrsni.ipynb
```

Nakon toga otvoriti datoteku `zavrsni.ipynb` i pokretati ćelije redom.

## Implementirani algoritmi

### Metrička dimenzija

Funkcija `metricka_baza` određuje metričku dimenziju grafa i vraća jednu metričku bazu. Udaljenosti između vrhova spremaju se u matricu udaljenosti `D`.

Za Horadamove i metalne kocke moguće je koristiti opciju `brza_l1=True`, kojom se udaljenosti računaju izravno pomoću L1 udaljenosti oznaka vrhova.

Pretraživanje koristi povratno pretraživanje s odsijecanjem. Prilikom pretraživanja odbacuju se grane koje više ne mogu dovesti do valjanog generatora.

### Dimenzija povezanosti

Funkcija `baza_povezanosti` određuje dimenziju povezanosti grafa i bazu povezanosti.

Prije pretraživanja provjerava se je li graf uniformno k-povezan. Ako jest, rezultat se određuje izravno. U suprotnom se računa teorijska donja ograda i pokreće povratno pretraživanje.

Za računanje lokalnih vršnih povezanosti koristi se matrica `K`. Dostupna je mogućnost odabira algoritma maksimalnog toka.

### Brute-force algoritmi

U datoteci `utils_brute.py` nalaze se funkcije:

* `metricka_baza_brute`
* `baza_povezanosti_brute`

Brute-force algoritmi ispituju podskupove vrhova po rastućoj kardinalnosti te pronalaze najmanji generator. Zbog eksponencijalne složenosti namijenjeni su prvenstveno manjim grafovima.

Brute-force implementacije koriste se i za provjeru ispravnosti optimiranih algoritama.

## Mjerenje vremena izvođenja

Implementacija omogućuje mjerenje vremena pojedinih faza algoritama i ukupnog vremena izvođenja.

Za metričku dimenziju mogu se mjeriti:

* vrijeme izgradnje matrice udaljenosti `D`
* vrijeme izračuna matrice `L`
* vrijeme povratnog pretraživanja
* ukupan broj posjećenih čvorova stabla pretraživanja

Za dimenziju povezanosti dodatno se mogu izdvojiti:

* vrijeme izračuna matrice lokalnih povezanosti `K`
* vrijeme provjere uniformne k-povezanosti
* vrijeme pretraživanja nakon izgradnje matrice `K`
* broj posjećenih čvorova stabla pretraživanja.

## Usporedba algoritama maksimalnog toka

Funkcija `usporedi_flow_algoritme` služi za usporedbu algoritama maksimalnog toka koji se mogu koristiti pri izračunu matrice lokalnih povezanosti `K`.

Uspoređuju se:

* Edmonds–Karp
* Shortest Augmenting Path
* Preflow-Push

Za svaki algoritam mjeri se vrijeme izvođenja kroz više ponavljanja te se provjerava daju li svi algoritmi jednaku matricu `K`.

## Biblioteke

* [NetworkX](https://networkx.org/) — rad s grafovima, računanje udaljenosti, lokalnih povezanosti i algoritama maksimalnog toka
* [NumPy](https://numpy.org/) — vektorizirani izračun L1 udaljenosti
* [Matplotlib](https://matplotlib.org/) — vizualizacija grafova
* [math](https://docs.python.org/3/library/math.html) — matematičke funkcije
* [functools](https://docs.python.org/3/library/functools.html) — memoizacija rekurzivne konstrukcije kocki
* [time](https://docs.python.org/3/library/time.html) — mjerenje vremena izvođenja

## Napomena

Implementacija je namijenjena povezanim neusmjerenim grafovima.

Opciju `brza_l1=True` treba koristiti samo za grafove za koje je poznato da je grafovska udaljenost jednaka L1 udaljenosti oznaka vrhova, kao što su Horadamove i metalne kocke.

Iako optimizirani algoritmi koriste odsijecanje i teorijske granice za smanjenje prostora pretraživanja, u najgorem slučaju i dalje imaju eksponencijalnu složenost.
