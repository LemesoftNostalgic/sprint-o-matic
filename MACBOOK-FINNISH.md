​
936 / 5 000
Käännöstulokset
Käännöstulos
### MacBookin asennus

Tämä on minun arvaukseni, mutta sitä ei ole testattu. Minulla ei ole MacBookia, jolla testata.

mene [Release-kansioon](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest), lataa ja pura _Lähdekoodi (tar.gz)_ koneellesi.

Jos sinulla ei ole vielä asennettuna python3.10:tä tai uudempaa, asenna se.
Ohjeet ovat osoitteessa [python.org/Downloads](python.org/Downloads).

Asenna sitten tarvittavat python-moduulit Terminal-sovelluksesta:

```
    python -m pip asennus pygame
    python -m pip -asennuspyynnöt
    python -m pip asentaa argparse
    python -m pip asennus overpy
```

Sitten voit käynnistää sovelluksen Terminal-sovelluksesta.
Siirry oikeaan kansioon ja anna seuraava komento:

```
    python main.py
```

Voit myös käyttää [komentoriviparametreja](#command-line-usage) näin, esimerkiksi jos haluat toimittaa analyysin tiedostona:

```
    python main.py --analyysi kyllä
```