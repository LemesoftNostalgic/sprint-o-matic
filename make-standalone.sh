git clone https://github.com/LemesoftNostalgic/sprint-o-matic-map-image-example.git
cp sprint-o-matic-map-image-example/* sprintomatic/data/sprint-o-matic-map-image-example-main
rm -rf sprint-o-matic-map-image-example/


git clone https://github.com/LemesoftNostalgic/sprint-o-matic-world-maps-cache.git
mv sprint-o-matic-world-maps-cache/ sprintomatic/data/sprint-o-matic-world-maps-cache-main


git clone https://github.com/LemesoftNostalgic/sprint-o-matic-external-map-links.git
cp sprint-o-matic-external-map-links/*.json sprintomatic/data/sprint-o-matic-external-map-links-main/
rm -rf sprint-o-matic-external-map-links/


git clone https://github.com/LemesoftNostalgic/sprint-o-matic-sounds.git
mv sprint-o-matic-sounds/ sprintomatic/sounds
