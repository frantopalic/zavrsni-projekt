# zavrsni-projekt
Projekt iz završnog praktičnog rada. Implementacija algoritama za pronalazak metričkih baza i baza povezanosti
neusmjerenih povezanih grafova te implementacija funkcija koje izgrađuju metalne kocke i Horadamove kocke.


## Sadržaj
- `utils.py` - funkcije za unos grafa, vizualizaciju grafa, pronalazak metričke baze i baze povezanosti
- `utils_brute.py` - brute-force funkcije za pronalazak metričke baze i baze povezanosti
- `metalne_kocke.py` - funkcija za kreiranje metalnih kocki (poziva `horadam_kocke.py`, $b=1$)
- `horadam_kocke.py` - funkcija za kreiranje Horadamovih kocki
- `zavrsni.ipynb` - glavni notebook s implementacijom i primjerima na konkretnim grafovima

Napomena: u datoteci `utils.py` su optimizirani algoritmi dok su u datoteci `utils_brute.py` odgovarajući
brute-force algoritmi koji služe za usporedbu.

## Zahtjevi
- Python ≥ 3.9 (koristi se `functools.cache`)

## Instalacija
```bash
pip install -r requirements.txt
```

## Pokretanje
1. Instalirati ovisnosti (vidi gore).
2. Pokrenuti Jupyter i otvoriti bilježnicu:
```bash
   jupyter notebook zavrsni.ipynb
```

## Biblioteke
- [NetworkX](https://networkx.org/) — rad s grafovima
- [NumPy](https://numpy.org/) — vektorizirani izračun L1 udaljenosti (`brza_l1=True`)
- [Matplotlib](https://matplotlib.org/) — vizualizacija grafova
- [math](https://docs.python.org/3/library/math.html) — matematičke funkcije
- [functools](https://docs.python.org/3/library/functools.html) — memoizacija rekurzivne konstrukcije kocki
- [time](https://docs.python.org/3/library/time.html) - mjerenje vremena izvođenja
