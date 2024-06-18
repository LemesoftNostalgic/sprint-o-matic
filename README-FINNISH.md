# Sprint-O-Matic

![Sprint-O-Matic logo by Jyrki Leskela](/doc/CompanyLogo.png)

_Suoraan web-sovellukseen_: [tinyurl.com/sprint-o-matic-webapp](https://lemesoftnostalgic.github.io/sprint-o-matic/)

## Johdanto

Sprint-O-Matic on harjoitussovellus sprinttisuunnistukseen.
Mitä sprinttisuunnistus sitten on? Se on nopeatempoinen suunnistuksen alalaji, jota
järjestetään yleensä urbaanissa ympäristössä. Katso lisätietoa
[Wikipedian artikkelista](https://en.wikipedia.org/wiki/Orienteering#Sprint) tai
[YouTuben sprinttisuunnistussisällöstä](https://www.youtube.com/results?search_query=sprint+orienteering).

Sprinttisuunnistus vaatii juoksunopeuden lisäksi
taitoa valita nopeasti paras reitti rastipisteeltä toiselle.
Tässä Sprint-O-Matic voi olla hyödyksi.
Se sisältää äärettömän määrän sprinttisuunnistuksen reitinvalintahaasteita
hauskan 2D-pelin muodossa. Katso seuraavat esittelyvideot saadaksesi
alustavan kuvan siitä miten peli toimii:

* [Sprint-O-Matic 8.0: karttamuistiharjoitus lisätty](https://youtu.be/DNg-9HHWzRM)
* [Sprint-O-Matic 7.0: web sovellus, toimii selaimessa ja puhelimessa](https://youtu.be/cxk0ZU6YtcE)
* [Sprint-O-Matic 5.0: parempi grafiikka ja enemmän karttoja](https://youtu.be/86cpFzc_-78)
* [Sprint-O-Matic 4.0: uusi "AMaze"-toiminto ensimmäisen rastivälin harjoitteluun](https://youtu.be/nepM0oAiFn8)
* [Sprint-O-Matic 3.0: nopeampi, satoja sprinttisuunnistukseen soveltuvia karttoja ympäri maailmaa, sisältää myös web-sovelluksen](https://youtu.be/lmbBzbUQUbc)
* [Sprint-O-Matic varhainen prototyyppi, automaattisesti luotu kartta, jänismoodi, juoksumatto](https://youtu.be/VikFxwu9e0Q).
* [Sprint-O-Matic reittianalyysitila, kartta kuvitteellisesta keskiaikaisesta kaupungista](https://youtu.be/rI9zinYGOmc)
* [Oikean sprinttisuunnistuskartan käyttö Sprint-O-Maticin kanssa. Pikavauhtinen pelitila](https://youtu.be/Kn53WGpEUgo)

## Sisällysluettelo

   * [Käyttö](#käyttö)
   * [Asennus](#asennus)
   * [Uusien karttojen käyttäminen Sprint-O-Maticin kanssa](#uusien-karttojen-käyttäminen-sprint-o-maticin-kanssa)
   * [Tietoja tästä ohjelmistosta ja sen lisenssistä](#tietoja-tästä-ohjelmistosta-ja-sen-lisenssistä)
   * [Muut aiheet](#muut-aiheet)

## Käyttö

### Aloitusnäyttö

![Sprint-O-Maticin aloitusnäyttö, kirjoittanut Jyrki Leskela](/doc/InitialDisplay.jpg)

Kun käynnistät sovelluksen, ensin tulee näkyviin aloitusnäyttö.
Se mahdollistaa radan pituuden ja rastivälien pituuden määrittämisen,
sekä pelitilan ja kartan valitsemisen. Aloitusnäyttöä voidaan käyttää näppäimistöltä
(sininen nuoli liikkuu näppäimistön nuolinäppäimillä, enter/space tekee valinnan, esc-näppäimestä poistutaan) tai
hiirellä (vasen/oikea painike siirtää sinistä nuolta ja keskipainike tekee valinnan.
Hiiren ohjaus saattaa kuulostaa epäintuitiiviselta,
mutta se on tehty niin että sovellusta pystyy käyttämään hiiri kädessä vaikkapa seisaallaan. Hiiren ei siis
tarvitse olla pöydällä.

Kun olet valinnut kaikki asetukset, siirrä sininen osoitin maaliympyrään ja valitse.
Peli voi alkaa.

### Pelin kulku

Pelin ohjaus on samankaltaista kuin aloitusnäytön ohjaus: nuolinäppäimistä tai hiiren
painikkeista käännetään suuntaa vasemmalle tai oikealle, esc tai keskipainike keskeyttää pelin.
Käyttö on tarkoituksella niin yksinkertaista että pelatessa ei tarvitse istua
epäterveellisesti pöydän ääressä. Langatonta hiirtä käyttäen voit vaikka treenata samanaikaisesti.

![Sprint-O-Maticin pelaaminen fantasiakartalla, kirjoittanut Jyrki Leskela](/doc/ExternalFantasyMap.jpg)

### Reittianalyysi-tilat (repeat, once, fast)

Kaikissa reittianalyysitiloissa liikut rastilta toiselle yksin.
Kun saavutat kunkin rastin, edellisen rastivälin reittisi näytetään hetkeksi, 
ja vertailuna näytetään optimaalisin reitti, jonka sovellus pystyi löytämään.

Maalissa saat nähdäksesi käytetyn ajan, kuljetun matkan ja virheprosentin verrattuna
optimireittiin. Reittianalyysitiloja on kolme:

* repeat: kierrä satunnaisia ratoja samalla kartalla yhä uudelleen ja uudelleen
* once: suorita rata kerran ja palaa aloitusnäyttöön
* fast: kaksinkertaistaa juoksijan nopeuden antaakseen hieman enemmän haastetta

On myös mahdollista saada analyysitulokset pelin jälkeen tiedostona levyllesi.
Tämä edellyttää [komentoriviparametrin](/FINNISH-CMDLINE.md) **--analysis**
käyttöä sovelluksen käynnistyksen yhteydessä. Voit käyttää myös
komentoriviparametria **--accurate** jos sinulla on nopea Linux PC ja haluat
parhaan reitin arvion olevan tarkempi.

Graafisen analyysin tulos näyttää tältä:

![Sprint-O-Matic-analyysin tulos, Jyrki Leskela](/doc/Analysis.png)

### A Maze

![Sprint-O-Matic gameplay in a maze mode by Jyrki Leskelä](/doc/AMaze.jpg)

A Maze -tilassa harjoittelet ensimmäiselle rastille lähtöä. Saat näkyviisi viisi satunnaista ensimmäistä rastiväliä yksi kerrallaan. Tehtäväsi on kääntää kartta kymmenessä sekunnissa optimaaliseen lähtösuuntaan.

Kymmenen sekunnin päästä saat tuloksen, sekä vertailuksi Sprint-O-Maticin ehdotuksen
parhaasta lähtösuunnasta.

### Karttamuistiharjoitus (osittainen valkoisen kartan suunnistus)

![Sprint-O-Matic pelaaminen karttamuistitilassa by Jyrki Leskelä](/doc/WhiteMapExercise.jpg)

Muistitilassa harjoittelet karttamuisitiasi. Jokaisella rastivälillä sinulla on aluksi 5 sekuntia aikaa katsoa kokonaista karttaa, jonka jälkeen osa kartasta peittyy valkoisilla laatikoilla. Käytä karttamuistiasi ja mielikuvitustasi päästäksesi rastilta toiselle.

### Jänistila

![Sprint-O-Maticin pelattavuus jänistilassa, kirjoittanut Jyrki Leskelä](/doc/GeneratedMapWithPacemaker.jpg)

Jänistilassa kierrät reitin yhdessä jänisjuoksijan kanssa. Jänisjuoksija on
henkilökohtainen virtuaalivalmentajasi. Se odottaa sinua jokaisella rastilla,
ja kilpailee sinua vastaan / kanssasi kullakin rastivälillä.

Silloin tällöin jänis päättää jättää yhden rastin väliin,
ja tulee mukaan taas seuraavalla. Älä huolestu, vaan jatka peliä normaalisti.

### Karttatyypit (World series / Infinite Oulu / External)

Sprint-O-Maticissa on kolme erilaista karttatyyppiä.

**Infinite Oulu** on automaattisesti luotu kaupunkikorttelikartta, joka kerta erilainen.
Infinite Oulu on Sprint-O-Matic-sovelluksen sisäinen järjestelmä.

![Sprint-O-Matic kartta Barcelonan alueelta, kirjoittanut Jyrki Leskelä](/doc/Barcelona.jpg)

+**Word series** Sprint-O-Matic v2.0.0 versiosta lähtien. Kasvava määrä
sprinttikarttoja maailman parhaista sprinttimaastoita.
Oulusta Helsinkiin, Tokiosta Pariisiin. Ensimmäinen versio kattaa 72
kaupunkia ja 662 karttaa. Määrä tulee tuosta vielä kasvamaan.
Toiminto käyttää pohjana OpenStreetMap-järjestelmän karttadataa.
Uusia kaupunkeja tai sijainteja voi ehdottaa yksinkertaisesti
lähettämällä viesti sähköpostiin sprint.o.matic miukumauku gmail.com.

![Sprint-O-Matic-pelikartta ulkoisella kartalla, kirjoittanut Jyrki Leskelä](/doc/tartu/ExternalMapWithRouteAnalysis.png)

Sprint-O-Maticin voi myös linkittää **ulkoisiin** karttoihin.
Sinun tarvitsee vain lähettää tarvittavat tiedot kartasta osoitteeseen
sprint.o.matic miukumauku gmail.com. Jos kartan lisenssi on riittävän salliva,
lisään sen linkkilistalle [https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links](https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links)
jolloin se tulee näkyviin Sprint-O-Maticiin. Voin jopa myöntää joillekin joukkueille
luvan pitää omaa karttalistaansa, jos kiinnostusta löytyy. Sovellus tarkistaa luettelot
aina käynnistyessään ja näyttää karttavalinnan yksitellen, kun käyttäjä painaa
aloitusnäytön "external/team"- ja "external/map"-painikkeita.
Alussa on jo valmiina yksi esimerkkijoukkue, jolla on muutamia karttoja. Toivottavasti
lisää tulee.

Tarkista seuraavasta kappaleesta tiedot, jotka vaaditaan, jotta kartta voidaan tehdä näkyväksi
Sprint-O-Maticin käyttäjille.


## Asennus

### Web-sovellus

Käytä web-versiota, jos haluat testata sovellusta heti.
Web-sovellus toimii melko hyvin nykyaikaisessa selaimessa, paitsi
äänen laatu, joka vaihtelee. Suosittelen silti web-versiota koska se
on aina ajan tasalla.

Web-sovellusta voi käyttää myös puhelimessa,
mutta silloin äänet eivät ole päällä, eikä grafiikka ole yhtä hyvä kuin
tietokoneessa.

  * [Web-sovellus käynnistyy tästä linkistä](https://lemesoftnostalgic.github.io/sprint-o-matic/)

### Ladattava sovellus

Sinun täytyy ladata ja asentaa sovellus jotta voit käyttää komentoriviparametrejä. Ladattava sovellus on hiukan nopeampi kuin web-sovellus ja pelattavuudeltaan hieman parempi.

  * [Windows-asennus](/WINDOWS-FINNISH.md)
  * [Linux-asennus](/LINUX-FINNISH.md)
  * [MacBook-asennus](/MACBOOK-FINNISH.md)

  * [Ohjeet komentoriviparametrien käyttöön](/FINNISH-CMDLINE.md)

### Laitteistovaatimukset

Sovellus on testattu Ubuntu 20.04 ja
Windows 10 -laitteissa.  Web-versio tarvitsee suhteellisen modernin selaimen.
**--accurate** komentoparametrin käyttäminen vaatii suhteellisen nykyaikaisen
tietokoneen, koska sen hakualgoritmit suoritetaan useissa prosesseissa.


## Uusien karttojen käyttäminen Sprint-O-Maticin kanssa

On olemassa kaksi tapaa saada lisää karttoja Sprint-O-Maticiin

- Etsi kinnostava sijainti vaikkapa Google Maps sovelluksesta ja lähetä ehdotus eli paikan koordinaatit osoitteeseen sprint.o.matic at gmail.com.
- Oikeiden sprittisuunnistuskarttojen käyttäminen Sprint-O-Maticin kanssa: [ohje](/README-FINNISH-MAPS.md)

## Tietoja tästä ohjelmistosta ja sen lisenssistä

Sovelluksen sisäosat on kirjoitettu pythonilla pygame-kirjaston avulla.
Kyseessä on harrastusprojekti, joten vaikka olen tavoitellut kohtalaista laatua
ajankäyttöni sallimissa rajoissa, niin laatu ei välttämättä
ole parhaiden kaupallisten ohjelmistojen tasolla.

Ohjelmisto on lisensoitu Apache-2.0-lisenssillä. Voit siis vapaasti
perustaa oman kehityshaaran sen parantelua tai lisäkehitystä varten.
Voit myös ehdottaa korjauksia "git pull request" mekanismilla.

Tämänhetkinen idealista ilmaisversiolle on seuraava:

* Ohjelma tarjolle sovelluskauppaan (Androis, iPhone)
* lisää ulkoisia karttoja linkitettynä karttaluetteloon [ohje](/README-FINNISH-MAPS.md)
* Lisää erilaisia harjoituksia, esim: pistesuunnistus tai knockout sprintti
* Korkeusmerkinnät -> ylämäestä hitaampi kuin alamäestä
* Rastien numerointi, rastimääritteet, jne.
* Moninpelin tuki (joutuisi olemaan maksullinen toiminto kattaakseen palvelinkulut)
* 3d tila

Sprint-O-Maticista on myös PRO-versio, aluksi omaan käyttööni,
julkaisukelpoisessa muodossa ehkä joskus 2026 tienoilla:

* automaattinen maastokuvausten luominen olemassaolevan sprinttikartan pohjalta.
* Tarkan resoluution sprinttikarttojen generointi suoraan maastodatasta.
* Käsinsuunniteltujen ratojen ja tapahtumien editoinnin tuki.

## Muut aiheet

### Tietoja pelaajahahmoista

Pelin pikselöidyt juoksijat voivat näyttää pieniltä, mutta jos mietit asiaa karttojen
mittakaavassa, eli noin yksi metri pikseliä kohden, saat oikean kuvan.
Juoksijat ovat itse asiassa 5-7 metriä korkeita hirviöitä. Siihen liittyy tarina.

Juoksijat elävät kaukaisessa tulevaisuudessa, aikakaudella, jossa ihmiset viettävät aikansa
virtuaalimaailmassa, jossa käytössä olevien pikselien määrää on rajoitettu valtion
säästötoimien takia. Pikseleitä on kullekin kansalaiselle vain vähän, mutta niiden kokoa
voi toki kasvattaa.

**Sprint-O-Man** Sovelluksen päähenkilö, sininen jättiläinen jonka intohimona
on sprinttisuunnistus. Puoliksi cowboy, puoliksi "Native American".

**Aino Inkeri (A.I.) Kiburtz** Jänisjuoksija ja ylpeä tekoäly joka perustuu
historialliseen materiaaliin Matthias Kiburtzista, tunnetusta sprinttisuunnistajasta.
Sprint-O-Manin paras ystävä.

**Pertti-Uolevi (P.A.) Keinonen, e.v.v.k.** Jänisjuoksija ja
heavy metal -fani. Nimetty genren kulta-ajalta peräisin olevan historiallisen
heavy metal -kitaristin, Pertti Keinosen, mukaan.

**Lex Martin Luthoer, Chem. Engr.** Vauhdikas jänisjuoksija ja kiistanalainen hahmo
kemian taitojensa vuoksi. Epäilty dopingista, mutta ei ole jäänyt kiinni.

### Tietoja tämän sovelluksen luojasta

Harrastin pelikoodausta 80-luvulla, nimimerkillä "Lemesoft". Kyseinen nimimerkki on
nykyään varattu olemassaolevalle yritykselle joten tein uuden nimimerkin "LemesoftNostalgic"
tätä harrasteprojektia varten.

Aikani menee työhön, treeneihin, ja muuhun elämiseen. Harrasteohjelmointiin ei ole
kovin paljon aikaa. Yritän silti vastata isoimpiin ongelmiin, jos niistä ilmoitetaan
sprint.o.matic miukumauku gmail.com:iin.

### Tietoja ratageneraattorista

Oletusarvoisesti Sprint-O-Matic luo uuden radan jokaiselle juoksulle.
Yleensä radat ovat hyviä, mutta eivät joka kerta. Jos satut saamaan
huonon radan, paina vain heti esc-painiketta ja aloita uudelleen. Ei ole järkeä
pelata huonoa rataa kokonaan läpi.

### Ohje: Interaktiivisten sovellusten käyttö juoksumatolla juostessa

Sprint-O-Matic on pelin kaltainen interaktiivinen sovellus.
Varoitus varsinkin ameriikan markkinoille: Sprint-O-Maticin turvallisuutta ei ole
testattu kunnolla juoksumattokäytössä. Siksi minun on ohjeistettava että ei pelata
samaan aikaan juoksumatolla juosten, vaikka se onkin
teknisesti mahdollista langattomalla hiirellä. Ilmoita minulle sprint.o.matic miukumauku gmail.com:n
kautta, jos jonkun juoksumaton edustaja näyttää vihreää valoa tämänkaltaiselle käytölle.

### Tuki

Karttaehdotukset, ehdotukset joukkueista jotka ovat kiinnostuneita ylläpitämään
omaa karttaluetteloa, ja sovelluksen parannusideat voi lähettää
sprint.o.matic miukumauku gmail.com:iin.
