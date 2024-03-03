### Windowsin asennus

**Helppo tapa:**

mene [Release-kansioon](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) ja napsauta Windowsin nimeä
suoritettava _sprint-o-matic-notsigned.exe_. Hyväksy sitten selaimen pyyntö tallentaa tiedosto. Se tulee ladata "Lataukset"-kansioon.

Käynnistä komentokehote kirjoittamalla "cmd" tehtäväpalkkiin.
Google lisää ohjeita komentokehotteen käyttöön, jos et tunne sitä
se. Kun olet komentokehotteessa, siirry oikeaan kansioon ja aloita
hakemus. Yleensä komennot ovat seuraavat:

```
    cd-lataukset
    sprint-o-matic-notsigned.exe
```

Jos olet ladannut useita versioita, Windows on saattanut lisätä ylimääräistä tekstiä
uudempiin versioihin. Jos uusin on _sprint-o-matic-notsigned(1).exe_
aloita sitten näin:

```
    "sprint-o-matic-notsigned(1).exe"
```

Voit myös käyttää [komentoriviparametreja](#command-line-usage) näin, esimerkiksi jos haluat toimittaa analyysin tiedostona:

```
    sprint-o-matic-notsigned.exe --analyysi kyllä
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
Google lisää ohjeita komentokehotteen käyttöön, jos et tunne sitä
se. Kun olet komentokehotteessa, asenna tarvittavat python-moduulit
seuraavat komennot:

```
    python -m pip asennus pygame
    python -m pip -asennuspyynnöt
    python -m pip asentaa argparse
    python -m pip asennus overpy
```

Käynnistä komentokehote kirjoittamalla "cmd" tehtäväpalkkiin.
Google lisää ohjeita komentokehotteen käyttöön, jos et tunne sitä
se. Kun olet komentokehotteessa, siirry oikeaan kansioon ja aloita
hakemus. Yleensä komennot ovat seuraavanlaiset:

```
    cd-lataukset
    cd sprint-o-matic-3.0.3
    cd sprint-o-matic-3.0.3
    python main.py
```

Voit myös käyttää [komentoriviparametreja](#command-line-usage) näin, esimerkiksi jos haluat toimittaa analyysin tiedostona:

```
    python main.py --analyysi kyllä
```

**Pitkälle kehittynyt:**

Jos todella haluat, voit rakentaa suoritettavan tiedoston uudelleen
lähteistä käyttämällä dopyinstaller.bat-tiedostoa, joka toimitetaan lähdekoodin mukana.