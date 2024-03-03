### MacBookin asennus

Tämä on minun arvaukseni, mutta sitä ei ole testattu. Minulla ei ole MacBookia, jolla testata.

mene [Release-kansioon](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest), lataa ja pura _Source Code (tar.gz)_ koneellesi.

Jos sinulla ei ole vielä asennettuna python3.10:tä tai uudempaa, asenna se.
Ohjeet ovat osoitteessa [python.org/Downloads](python.org/Downloads).

Asenna sitten tarvittavat python-moduulit Terminal-sovelluksen kautta:

```
    python -m pip install pygame
    python -m pip install requests
    python -m pip install argparse
    python -m pip install overpy
```

Sitten voit käynnistää sovelluksen Terminal-sovelluksen kautta.
Siirry oikeaan kansioon ja anna seuraava komento:

```
    python main.py
```

Voit myös käyttää komentoriviparametreja näin, esimerkiksi jos haluat toimittaa analyysin tiedostona:

```
    python main.py --analysis yes
```