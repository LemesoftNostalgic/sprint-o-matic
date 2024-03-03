### Linuxin asennus

**Helppo tapa:**

mene [Release-kansioon](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) ja napsauta Linuxin nimeä
suoritettava _sprint-o-matic_. Siirry "Lataukset"-kansioon painikkeella
Pääte ja käynnistä sovellus seuraavasti:

```
      ./sprint-o-matic
```

Voit myös käyttää [komentoriviparametreja](#command-line-usage) näin, esimerkiksi jos haluat toimittaa analyysin tiedostona:

```
      ./sprint-o-matic --analyysi kyllä
```

**Suositeltu ja turvallisempi tapa:**

Tämä voi olla hieman erilainen verkkoselaimesi mukaan. Käytin Mozillaa
Firefox.

siirry kohtaan [Release-kansio](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) ja napsauta lähdekoodipaketin nimeä _Source code (zip)_. Selaimen pitäisi ladata se "Lataukset"-kansioon. Siirry "Lataukset"-kansioon ja napsauta hiiren oikealla painikkeella lähdekoodipakettia "sprint-o-matic-3.0.3" ja valitse valikosta "pura kaikki".

Jos sinulla ei ole vielä asennettuna python3.10:tä tai uudempaa, asenna se.
Ohjeet ovat osoitteessa [python.org/Downloads](python.org/Downloads).
Avaa Ubuntun ja Debianin pääte ja anna seuraavat komennot:

```
  sudo apt päivitys
  sudo apt install python3
  sudo apt asennus python3-pip
```

Asenna sitten tarvittavat python-moduulit:

```
    python3 -m pip asennus pygame
    python3 -m pip-asennuspyynnöt
    python3 -m pip asennus argparse
    python3 -m pip install overpy
```

Sitten voit käynnistää sovelluksen.
Siirry oikeaan kansioon ja anna seuraava komento:

```
    python3 main.py
```

Voit myös käyttää [komentoriviparametreja](#command-line-usage) näin, esimerkiksi jos haluat toimittaa analyysin tiedostona:

```
    python3 main.py --analyysi kyllä
```

**Pitkälle kehittynyt:**

Jos todella haluat, voit rakentaa suoritettavan tiedoston uudelleen
lähteistä dopyinstaller.sh:lla.

