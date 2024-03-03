### Linuxin asennus

**Helppo tapa:**

mene [Release-kansioon](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) ja napsauta suoritettavan tiedoston _sprint-o-matic_ nimeä.
Siirry "Download"-kansioon Terminal-ohjelmalla ja käynnistä sovellus
seuraavasti:

```
      ./sprint-o-matic
```

Voit myös käyttää komentoriviparametreja näin, esimerkiksi jos haluat toimittaa analyysin tiedostona:

```
      ./sprint-o-matic --analysis yes
```

**Suositeltu ja turvallisempi tapa:**

Tämä voi olla hieman erilainen verkkoselaimesi mukaan. Käytin Mozilla
Firefox -selainta.

Siirry sivulle [Release-kansio](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) ja napsauta lähdekoodipaketin _Source code (zip)_  nimeä. Selaimen pitäisi ladata se "Downloads"-kansioon. Siirry "Downloads"-kansioon ja napsauta hiiren oikealla painikkeella lähdekoodipakettia "sprint-o-matic-3.0.3" ja valitse valikosta "Extract..".

Jos sinulla ei ole vielä asennettuna python3.10:tä tai uudempaa, asenna se.
Ohjeet ovat osoitteessa [python.org/Downloads](python.org/Downloads).
Avaa Ubuntun tai Debianin Terminal-sovellus ja anna seuraavat komennot:

```
  sudo apt update
  sudo apt install python3
  sudo apt install python3-pip
```

Asenna sitten tarvittavat python-moduulit:

```
    python3 -m pip install pygame
    python3 -m pip install requests
    python3 -m pip install argparse
    python3 -m pip install overpy
```

Sitten voit käynnistää sovelluksen.
Siirry oikeaan kansioon ja anna seuraava komento:

```
    python3 main.py
```

Voit myös käyttää komentoriviparametreja näin, esimerkiksi jos haluat toimittaa analyysin tiedostona:

```
    python3 main.py --analysis yes
```

**Pitkälle kehittynyt:**

Jos todella haluat, voit rakentaa suoritettavan tiedoston uudelleen
lähdekoodista dopyinstaller.sh:lla.
