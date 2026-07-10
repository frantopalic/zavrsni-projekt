# zavrsni-projekt

Projekt iz završnog praktičnog rada. Implementacija algoritma za pronalazak metričkih baza i baza povezanosti neusmjerenih povezanih grafova
te implementacija funkcija koje izgrađuju metallic kocke i Horadam kocke.

## Sadržaj

 - `utils.py` - funkcije (za unos grafa, vizualizaciju grafa, pronalazak metričke baze i baze povezanosti)
 - `metalne_kocke` - funkcija (za kreiranje metallic kocki)
 - `horadam_kocke` - funkcija (za kreiranje Horadam kocki)
 - `zavrsni.ipynb` - glavni notebook s implementacijom i primjerima na konkretnim grafovima

## Instalacija

```bash
pip install -r requirements.txt
```

## Pokretanje

Potrebno je otvoriti `zavrsni.ipynb` u Jupyter Notebooku.

## Biblioteke

- [NetworkX](https://networkx.org/) — rad s grafovima
- [Matplotlib](https://matplotlib.org/) — vizualizacija grafova
- [math](https://docs.python.org/3/library/math.html) — matematičke funkcije
- [functools](https://docs.python.org/3/library/functools.html) — memoizacija (`functools.cache`) rekurzivne konstrukcije metalnih i Horadamovih kocki
