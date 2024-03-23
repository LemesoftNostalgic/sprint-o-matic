## Komentorivin käyttö

Edistyneille käyttäjille on olemassa lisävaihtoehtoja komentorivin kautta.

On myös mahdollista pelata joko koko näytöllä tai ikkunassa.

**--fullScreen** Pelaatko koko näytöllä vai ikkunassa, yes tai no.

Reittianalyysit.

**--analysis** Tallennetaan reittianalyysit tiedostoon, yes tai no

**--accurate** Käytä hitaampaa mutta huomattavasti tarkempaa reittianalyysiä, vain Linux ympäristössä., yes tai no

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
