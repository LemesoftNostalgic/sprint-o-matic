# Sprint-O-Matic

![Sprint-O-Matic logo by Jyrki Leskela](/doc/logo.png)

## Johdanto

Sprint-O-Matic on harjoitussovellus sprinttisuunnistukseen.
Tein sen alun perin omaan käyttööni, jotta voisin monipuolistaa harjoittelua kylminä
talvipäivinä Suomessa. Sitten ajattelin, että joku muu saattaisi olla kiinnostunut
kokeilemaan sitä, joten tässä se nyt sitten on.

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

* [Sprint-O-Matic 2.0: satoja sprinttisuunnistukseen soveltuvia karttoja ympäri maailmaa](https://youtu.be/lmbBzbUQUbc)
* [Sprint-O-Matic varhainen prototyyppi, automaattisesti luotu kartta, jänismoodi, juoksumatto](https://youtu.be/VikFxwu9e0Q).
* [Sprint-O-Matic reittianalyysitila, kartta kuvitteellisesta keskiaikaisesta kaupungista](https://youtu.be/rI9zinYGOmc)
* [Oikean sprinttisuunnistuskartan käyttö Sprint-O-Maticin kanssa. Pikavauhtinen pelitila](https://youtu.be/Kn53WGpEUgo)

## Sisällysluettelo

   * [Asennus](#asennus)
   * [Käyttö](#käyttö)
   * [Uusien karttojen lisääminen Sprint-O-Maticiin](#uusien-karttojen-lisääminen-sprint-o-Maticiin)
     * [Pelaaminen yksityisillä kartoillasi](#pelaaminen-yksityisillä-kartoillasi)
     * [Tee karttasi näkyväksi Sprint-O-Maticin käyttäjille](#tee-karttasi-näkyväksi-oprint-o-maticin-käyttäjille)
     * [Maaston kuvauksen luominen](#maaston-kuvauksen-luominen)
   * [Tietoja tästä ohjelmistosta ja sen lisenssistä](#tietoja-tästä-ohjelmistosta-ja-sen-lisenssistä)
   * [Sekalaiset aiheet](#sekalaiset-aiheet)
   * [Komentorivin käyttö](#lomentorivin-käyttö)

## Asennus

Suositeltava tapa on ajaa ohjelmisto pythonilla suoraan lähdekoodina, koska se on helppoa ja turvallista:

1. Lataa ja pura lähdekoodipaketti [Release-kansiosta](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) koneellesi.
2. Asenna python3.10 tai uudempi: (python.org/Downloads)
   * Varmista python-asennuspakettia asentaessasi, että python on asetettu PATH-ympäristomuuttujaan sallimalla ympäristömuuttujien muutokset
3. Asenna tarvittavat python-moduulit komentoriviltä:
   * python -m pip install pygame
   * python -m pip install requests
   * python -m pip install argparse
   * python -m pip install overpy (sprint-o-matic v2.0.0 versiosta lähtien)
 
4. Käynnistä "main.py" sprint-o-matic:in sprint-o-matic -kansiosta (napsauta "main"-kuvaketta tai käytä komentoa "python main.py" komentoriviltä)
   * tai käytä komentoa "python main.py --fullScreen yes" jos haluat pelata koko näytön tilassa.

[Release-kansio](https://github.com/LemesoftNostalgic/sprint-o-matic/releases/latest) sisältää myös valmiiksi paketoidut sovellukset Linuxille ja Windowsille suoritettavina "exe"-tiedostoina. 
Windows executable ei ole "Windows signed" sovellus, mutta seurasin ohjetta [microsoftin vastaus tapauksiin, joissa Pyinstallerin luoma suoritettava tiedosto on merkitty väärin](https://answers.microsoft.com/en-us/windows/forum/all/where-executables-created-by-pyinstaller-are-being/09e58a6b-01f3-4e72-8765-6542ef7291f4). Jos kuitenkin pelaat varman päälle niin käytä edellä mainitulla tavalla suoraan
lähdekoodia "python"-ohjelman avulla.

Jos todella haluat, voit koota suoritettavat tiedostot itse lähdekoodista
käyttäen dopyinstaller.sh (Linux) tai dopyinstaller.bat (Windows) komentoja,
jotka ovat lähdekoodissa mukana. Kokoaminen vaatii pyinstaller-asennuksen:

* Python -m pip asennus pyinstaller
   * Varmista, että pyinstaller on PATH-ympäristömuuttujasi polussa.

### Laitteistovaatimukset

Sovellus on testattu Ubuntu 20.04 ja
Windows 10 -laitteissa. Sprint-O-Maticin käyttäminen vaatii suhteellisen nykyaikaisen
tietokoneen, koska sen hakualgoritmit suoritetaan useissa prosesseissa.
Sovelluksessa voi olla hiukan viiveitä matkalla ensimmäiselle rastille,
mutta viiveiden pitäisi kadota hetkisen päästä.

World-sarjan karttojen alustaminen kestää hieman tavanomaista kauemmin,
joskus jopa puolisen minuuttia.


## Käyttö

### Aloitusnäyttö

![Sprint-O-Maticin aloitusnäyttö, kirjoittanut Jyrki Leskela](/doc/InitialDisplay.png)

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

![Sprint-O-Maticin pelaaminen fantasiakartalla, kirjoittanut Jyrki Leskela](/doc/ExternalFantasyMap.png)

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
Tämä edellyttää [komentoriviparametrin](#komentorivin-käyttö) **--analyysi** 
käyttöä sovelluksen käynnistyksen yhteydessä.

Graafisen analyysin tulos näyttää tältä:

![Sprint-O-Matic-analyysin tulos, Jyrki Leskela](/doc/Analysis.png)

### Jänistila

![Sprint-O-Maticin pelattavuus tahdistimessa, kirjoittanut Jyrki Leskelä](/doc/GeneratedMapWithPacemaker.png)

Jänistilassa kierrät reitin yhdessä jänisjuoksijan kanssa. Jänisjuoksija on
henkilökohtainen virtuaalivalmentajasi. Se odottaa sinua jokaisella rastilla,
ja kilpailee sinua vastaan / kanssasi kullakin rastivälillä.

Silloin tällöin jänis päättää jättää yhden rastin väliin,
ja tulee mukaan taas seuraavalla. Älä huolestu, vaan jatka peliä normaalisti.

### Karttatyypit (World series / Infinite Oulu / External)

Sprint-O-Maticissa on kolme erilaista karttatyyppiä.

**Infinite Oulu** on automaattisesti luotu kaupunkikorttelikartta, joka kerta erilainen.
Infinite Oulu on Sprint-O-Matic-sovelluksen sisäinen järjestelmä.
Katso esimerkki edellisestä kuvasta.

![Sprint-O-Matic kartta Barcelonan alueelta, kirjoittanut Jyrki Leskelä](/doc/Barcelona.png)

+**Word series** Sprint-O-Matic v2.0.0 versiosta lähtien. Kasvava määrä
sprinttikarttoja maailman parhaista sprinttimaastoita.
Oulusta Helsinkiin, Tokiosta Pariisiin. Ensimmäinen versio kattaa 72
kaupunkia ja 662 karttaa. Määrä tulee tuosta vielä kasvamaan.
Toiminto käyttää pohjana OpenStreetMap-järjestelmän karttadataa.

![Sprint-O-Matic-pelikartta ulkoisella kartalla, kirjoittanut Jyrki Leskelä](/doc/tartu/ExternalMapWithRouteAnalysis.png)

Sprint-O-Matic:in voi myös linkittää **ulkoisiin** karttoihin. 
Sinun tarvitsee vain lähettää tarvittavat tiedot kartasta osoitteeseen
sprint-o-matic gmail com. Jos kartan lisenssi on riittävän salliva,
lisään sen linkkilistalle [https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links](https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links)
jolloin se tulee näkyviin Sprint-O-Maticiin. Voin jopa myöntää joillekin joukkueille
luvan pitää omaa karttalistaansa, jos kiinnostusta löytyy. Sovellus tarkistaa luettelot
aina käynnistyessään ja näyttää karttavalinnan yksitellen, kun käyttäjä painaa
aloitusnäytön "external/team"- ja "external/map"-painikkeita.
Alussa on jo valmiina yksi esimerkkijoukkue, jolla on muutamia karttoja. Toivottavasti
lisää tulee.

Tarkista seuraavasta kappaleesta tiedot, jotka vaaditaan, jotta kartta voidaan tehdä näkyväksi
Sprint-O-Maticin käyttäjille.


## Uusien karttojen käyttäminen Sprint-O-Matic:in kanssa

### Pelaaminen yksityisillä kartoillasi

Käyttämällä [komentorivi](#komentorivin-käyttö) parametreja **--mapFileName** ja 
**--lookupPngName** voit pelata paikalliseen tiedostojärjestelmääsi tallennetulla kartalla.
Karttatiedosto on vain kuva kartasta, mieluiten png-muodossa, ja 
"maaston kuvaus" on samankokoinen png-kuva, johon on merkitty 
maaston ominaisuudet tietyillä väreillä, katso luku
[maaston kuvauksen luominen](#maaston-kuvauksen-luominen).

Yksityisillä kartoilla pelaaminen on hyvä tapa kokeilla maaston kuvausta ennen kuin sen
tekee näkyväksi muille Sprint-O-Maticin käyttäjille.

### Tee karttasi näkyväksi Sprint-O-Maticin käyttäjille

Lisää kartta Sprint-O-Maticin karttaluetteloon, niin kaikki voivat pelata
sen kanssa. Karttaa koskevat perustiedot on lähetettävä osoitteeseen
sprint-o-matic gmail com linkityksen toteuttamiseksi:

- kartan nimi, tarpeeksi lyhyt, jotta se sopii aloitusnäyttöön painikkeen alle
- url-linkki karttakuvaan (png-muoto on suositeltavaa)
- lisenssitiedot karttaan liittyen
- tietoa kartan omistajasta/tekijästä
- URL-osoite maaston kuvaukseen (samankokoinen png-kuva kuin kartta)
- lisenssitiedot maaston kuvaukseen liittyen
- tietoa maaston kuvauksen omistajasta/tekijästä
- metriä/pikseli -kerroin
- kartan koon skaalauskerroin

Tässä on esimerkki yhden kartan tiedoista [sprint-o-maticin tämänhetkisessä ulkoisten karttojen luettelossa](https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links):

   ```json
    {
        "name": "Fantasy",
        "map-url": "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-map-image-example/main/FantasySprintMap.png?raw=true",
        "map-license": "CC BY-SA 4.0 Deed",
         "map-credits": "Jyrki Leskelä, 2024",
         "lookup-png-url": "https://raw.githubusercontent.com/LemesoftNostalgic/sprint-o-matic-map-image-example/main/fantasylookup.png?raw=true",
         "lookup-png-license": "CC BY-SA 4.0 Deed",
         "lookup-png-credits": "Jyrki Leskela, 2024",
         "meters-per-pixel": 0.5
         "default-zoom": 1.0
    }
   ```

**Vihje:** Jos et tiedä kuinka julkaista tiedostoja verkossa saadaksesi
kartan URL-osoitteen: helppo tapa tehdä se on [avaa ilmainen tili ja
kansio GitHub:ssa](https://github.com/signup) ja raahaa tiedostot sinne.
Sprint-o-Matic gmail com ymmärtää github-osoitteet, joten sinun ei ole
välttämätöntä kertoa tarkkaa URL-osoitetta github-osoitteiden kanssa.

Kaksi muuta asiaa, joihin on kiinnitettävä huomiota, ovat a) kartan lisenssi
ja b) maaston kuvauksen piirtäminen.

a) Lisenssiin liittyen: julkiselle listalle on mahdollista
sisällyttää vain suhteellisen sallivalla lisenssillä julkaistuja karttakuvia.
Käytännössä karttakuva näkyy kaikille Sprint-O-Matic-käyttäjille, kun se otetaan mukaan.
Paras tapa olisi että ehdokaskartta olisi julkaistu jollakin Creative Commons
-lisenssityypeistä. Tämä todennäköisesti rajoittaa valinnan vanhoihin karttoihin,
joilla ei ole enää kilpasuunnistuksellista käyttöä. Toisaalta näin voi saada
vanhentuneita mutta muuten hyviä karttoja vielä uusiokäyttöön.

b) Maaston kuvauksen luomisessa on jonkin verran käsityötä.
Seuraava kappale kertoo miten se tehdään.

### Maaston kuvauksen luominen

Periaatteessa sinun on luotava samankokoinen kuva kuin karttakuva.
Yksi helppo tapa on tehdä kopio alkuperäisestä karttakuvasta ja maalata kuvan päälle
kukin maastotyyppi sille kuuluvalla värikoodilla ja tallentaa lopputulos png-muodossa.

Värikoodit ovat seuraavat:

![Jyrki Leskelän Sprint-O-Matic-hakuvärit](/doc/lookupcolors.png)

Käytä kuvaeditoria, jossa voit valita värit tarkasti.
Olen käyttänyt [GIMP-editoria](https://www.gimp.org), koska se on minulle tuttu.
Maastomerkintöjen on vastattava täsmälleen kuvassa esitettyjä värikoodeja.
Lopussa on hyvä tarkistaa editoinnin tulos silmämääräisesti. Kiinnitä huomiota erityisesti
sprinttikartan mustalla värillä oleviin symboleihin: pääasiassa mustalla värillä
merkitään sprinttikartoissa kohdat, joiden läpi ei voi juosta,
mutta jotkut mustat merkinnät, kuten polut ja aitojen vinoviivat, ovat itse asiassa
läpijuostavia. Varo ettet maalaa niitäkin kielletyiksi omassa maastokuvauksessasi.

Katso [esimerkkikansiota](https://github.com/LemesoftNostalgic/sprint-o-matic-map-image-example)
jossa on pelattavia esimerkkejä karttakuvasta ja sitä vastaavasta
maastokuvauksesta. Nähtävillä on myös [YouTube-video, joka näyttää
kuinka tehdä maaston kuvaus GIMP:llä](https://youtu.be/_n0IRG1GfLI).
Sopivin resoluutio karttakuville ja maastokuvauksille on
välillä 1024-2048 pikseliä (leveys). Sprint-O-Matic on suunniteltu
toimimaan parhaiten sprinttikartoilla joiden mittakaava on noin
1:3000 - 1:5000.

Jos sinulla on erinomainen kartta, ja haluat olla mukana,
mutta sinulla ei ole aikaa tai
taitoa luoda maastokuvausta, ehdota sitä sprint-o-matic
gmail com:n kautta silti. Voin auttaa esimerkiksi muutaman maastokuvauksen
luonnissa jotta saadaan uusia karttoja mukaan. Hyvä kartta Sprint-O-Matic:ille
on sellainen, jossa on tarpeeksi aitoja ja muita esteitä, eli haastava sprinttikartta.
Myös hidas vihreä maasto on hyvä, mutta ei välttämätön.


## Tietoja tästä ohjelmistosta ja sen lisenssistä

Sovelluksen sisäosat on kirjoitettu pythonilla pygame-kirjaston avulla.
Kyseessä on harrastusprojekti, joten vaikka olen tavoitellut kohtalaista laatua
ajankäyttöni sallimissa rajoissa, niin laatu ei välttämättä
ole parhaiden kaupallisten ohjelmistojen tasolla.

Ohjelmisto on lisensoitu Apache-2.0-lisenssillä. Voit siis vapaasti
perustaa oman kehityshaaran sen parantelua tai lisäkehitystä varten.
Voit myös ehdottaa korjauksia "git pull request" mekanismilla.
Harrastusprojektimaisesta luonteesta johtuen kaikki apu on tietysti tervetullutta.
Tämänhetkinen idealista on seuraava:

Helpot jutut:

* lisää ulkoisia karttoja linkitettynä karttaluetteloon (katso yllä)
* Salli kuhunkin karttaan liittyvien käsinsuunniteltujen ratojen julkaiseminen
* Tiettyyn suuntaan hidastava maastokuvaus, parantaisi portaikkojen ja kukkuloiden
mallinnusta
* Rastien numerointi, rastimääritteet, jne.
* grafiikan parantelu
* Score-O -tyyppinen (n.s. rogaining, kerää pisteet missä tahansa järjestyksessä, aikaraja)
* tapahtumien/moninpelin tuki (joutuisi olemaan maksullinen toiminto kattaakseen palvelinkulut)

Hieman enemmän työtä vaatisi:

* automaattinen maastokuvausten luominen. Sprintin suunnistuskartoilla,
musta väri on ongelma. Sitä käytetään symboleille, joiden läpi voit juosta,
ja symboleille, joiden läpi et voi juosta. On jopa vaihtelua kartasta
ja kartoittajasta johtuen, mikä tekee tietokoneohjelmalle vaikeaksi ymmärtää
käytännön karttamerkintöjä, varsinkin vanhemmista kartoista.
* 3d (ihmissilmä on herkempi laadulle, kun sisältö on 3d,
siksi kunnollinen 3d-peli vaatii huomattavasti enemmän työtä kuin 2d-peli)
* Integrointi maantieteelliseen tietokantaan, tyyliin "pullautin".
Harjoittele "kaikkialla".


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
sprint-o-matic gmail com:iin.

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
teknisesti mahdollista langattomalla hiirellä. Ilmoita minulle sprint-o-matic gmail com:n
kautta, jos jonkun juoksumaton edustaja näyttää vihreää valoa tämänkaltaiselle käytölle.

### Tuki

Karttaehdotukset, ehdotukset joukkueista jotka ovat kiinnostuneita ylläpitämään
omaa karttaluetteloa, ja sovelluksen parannusideat voi lähettää
sprint-o-matic gmail com:iin.

## Komentorivin käyttö

Edistyneille käyttäjille on olemassa lisävaihtoehtoja komentorivin kautta.

On myös mahdollista pelata joko koko näytöllä tai ikkunassa.

**--fullScreen** Pelaatko koko näytöllä vai ikkunassa, yes tai no.

Reittianalyysien tallentaminen tiedostoon.

**--analyysi** Tallennetaan reittianalyysit tiedostoon

Vaihtoehdot, jotka ovat hyödyllisiä, jos haluat pelata omalla kartallasi.
Kun käytät niitä, et mene aloitusnäyttöön, vaan peli alkaa
heti:

**--mapFileName tiedoston-nimi** haluamasi suunnistuskartan tiedoston nimi, mieluusti png-muoto

**--lookupPngName tiedoston-nimi** maaston kuvauksen tiedoston nimi, png-muoto

**--metersPerPixel numero** Kuinka monta metriä karttapikseliä kohden

Ja koska et siirry aloitusnäyttöön, käyttäessäsi omaa karttatiedostoa,
joudut valitsemaan pelivalinnat komentoriviparametreilla:

**--trackLength numero** pienin raidan pituus metreinä

**--miniLegProbability numero** minijalkojen todennäköisyys (0,0-0,99)

**--shortLegProbability numero** lyhyiden jalkojen todennäköisyys (0,0-0,99)

**--mediumLegProbability numero** keskipitkien jalkojen todennäköisyys (0,0-0,99)

**--longLegProbability numero** pitkien jalkojen todennäköisyys (0,0-0,99)

**--extraLongLegProbability numero** erittäin pitkien jalkojen todennäköisyys (0,0-0,99)

**--continuous** Jatkuva pelisilmukka (tai yhden laukauksen peli)

**--pacemaker** Tahdistimen juoksija, jota vastaan kilpailla (1-3, 0 ei mitään)

Ja jos haluat suunnitella tietyn reitin:

**--routeFileName tiedoston-nimi** järjestetty lista rastien koordinaateista (tuple) json-formaatissa. Huom: ensimmäinen koordinaatti on lähtöpaikka, ja viimeinen koordinaatti on maali.

Ja lopuksi, jos haluat isännöidä yksityistä karttatietoluetteloasi.

**--ownMasterListing url-osoite** Korvaa oletusverkkolistaus toisella URL-osoitteella

**--externalExampleTeam teksti-nimi** Joukkueen valinta listauksesta

**--externalExample teksti-nimi** Karttavalinta listauksesta

On myös joitain muita vaihtoehtoja, jotka on tarkoitettu pääasiassa sovelluksen
testaukseen. Ne on dokumentoitu vain koodissa.
