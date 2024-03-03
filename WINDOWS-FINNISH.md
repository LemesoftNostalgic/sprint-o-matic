### Windowsin asennus

**Helppo tapa:**

Mene [Release-kansioon](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) ja napsauta suoritettavan tiedoston _sprint-o-matic-notsigned.exe_
nimeä. Hyväksy sitten selaimen pyyntö tallentaa tiedosto. Se tulee ladata
"Downloads"-kansioon (tai "Ladatut tiedostot" suomenkielisessä versiossa).

Käynnistä komentokehote kirjoittamalla "cmd" tehtäväpalkkiin.
Katso Googlesta lisää ohjeita Windows-komentokehotteen käyttöön, jos et ole
aiemmin tutustunut siihen. Kun olet komentokehotteessa,
siirry oikeaan kansioon ja käynnistä sovellus. Yleensä komennot ovat seuraavat:

```
    cd Downloads
    sprint-o-matic-notsigned.exe
```

Jos olet ladannut useita versioita, Windows on saattanut lisätä ylimääräistä
tekstiä
uudempiin versioihin. Jos uusin on _sprint-o-matic-notsigned(1).exe_
käynnistä sitten näin:

```
    "sprint-o-matic-notsigned(1).exe"
```

Voit myös käyttää komentoriviparametreja näin, esimerkiksi jos haluat toimittaa analyysin tiedostona:

```
    sprint-o-matic-notsigned.exe --analysis yes
```

**Suositeltu ja turvallisempi tapa:**

Tämä voi olla hieman erilainen verkkoselaimesi mukaan. Käytin Mozillaa
Firefox.

siirry kohtaan [Release-kansio](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) ja napsauta lähdekoodipaketin nimeä _Source code (zip)_. Selaimen pitäisi ladata se "Lataukset"-kansioon. Siirry "Lataukset"-kansioon ja napsauta hiiren oikealla painikkeella lähdekoodipakettia "sprint-o-matic-3.0.3" ja valitse valikosta "pura kaikki".

Jos sinulla ei ole vielä asennettuna python3.10:tä tai uudempaa, asenna se.
Ohjeet ovat osoitteessa [python.org/Downloads](python.org/Downloads).
Siellä pitäisi olla uusimman asennuspaketin painike. Seuraa
ohjeet asennuspaketin tallentamiseksi Dowloads-kansioon.
Siirry sitten Lataukset-kansioon ja kaksoisnapsauta python-3.10.2-amd64
-kuvaketta ja python-asennusohjelman pitäisi käynnistyä.
Nyt näet asennusikkunan. **Valitse ensin pieni ruutu "Add python.exe" vasemmalla polkuun. Vasta sen jälkeen napsauta "Asenna nyt"**.
Odota asennuksen päättymistä.

Käynnistä komentokehote kirjoittamalla "cmd" tehtäväpalkkiin.
Googleta lisää ohjeita komentokehotteen käyttöön, jos et tunne sitä
se. Kun olet komentokehotteessa, asenna tarvittavat python-moduulit
seuraavin komennoin:

```
    python -m pip install pygame
    python -m pip install requests
    python -m pip install argparse
    python -m pip install overpy
```

Käynnistä komentokehote kirjoittamalla "cmd" tehtäväpalkkiin.
Googleta lisää ohjeita komentokehotteen käyttöön, jos et tunne sitä
se. Kun olet komentokehotteessa, siirry oikeaan kansioon ja käynnistä
sovellus. Yleensä komennot ovat seuraavanlaiset:

```
    cd Downloads
    cd sprint-o-matic-3.0.3
    cd sprint-o-matic-3.0.3
    python main.py
```

Voit myös käyttää komentoriviparametreja näin, esimerkiksi jos haluat toimittaa analyysin tiedostona:

```
    python main.py --analysis yes
```

**Pitkälle kehittynyt:**

Jos todella haluat, voit rakentaa suoritettavan tiedoston uudelleen
lähdekoodista käyttämällä dopyinstaller.bat-tiedostoa, joka toimitetaan lähdekoodin mukana.
