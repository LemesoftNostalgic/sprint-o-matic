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
sprint.o.matic miukumauku gmail.com linkityksen toteuttamiseksi:

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
Sprint.o.Matic miukumauku gmail.com ymmärtää github-osoitteet, joten sinun ei ole
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
sprint.o.matic miukumauku gmail.com:n kautta silti. Voin auttaa esimerkiksi muutaman maastokuvauksen
luonnissa jotta saadaan uusia karttoja mukaan. Hyvä kartta Sprint-O-Matic:ille
on sellainen, jossa on tarpeeksi aitoja ja muita esteitä, eli haastava sprinttikartta.
Myös hidas vihreä maasto on hyvä, mutta ei välttämätön.
