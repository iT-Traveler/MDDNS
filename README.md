# MDDNS

Miro - Daan DNS service

## Auteurs

- [@DaandH](https://github.com/DaandH) | Daan den Hartog | SN: 1842828
- [@iT-Traveler](https://github.com/iT-Traveler) | Miro de Ruiter | SN: 1828968


## API curl commands

De MDDNS API is beschikbaar via https://mddns.azurewebsites.net. Onderstaand zijn voorbeeld commands met de verschillende mogelijkheden. Vervang de variabelen in deze [ ] haken.

| Doel | Command                |
| :-------- | :------------------------- |
| Nieuw DNS record maken | curl -X POST https://mddns.azurewebsites.net/subdomain/new -H "Content-type: application/json" -H "X-API-Key: [YOUR-API-KEY]" -d "{ \"subdomain\" : \"[YOUR-SUBDOMAIN]\", \"ip\" : \"[YOUR-IP-ADDRESS]\" }" |
| DNS Record updaten | curl -X PUT https://mddns.azurewebsites.net/subdomain/name/[YOUR-SUBDOMAIN] -H "Content-type: application/json" -H "X-API-Key: [YOUR-API-KEY]" -d "{ \"ip\" : \"[YOUR-IP-ADDRESS]\" }" |
| DNS record uitlezen | curl https://mddns.azurewebsites.net/subdomain/name/[YOUR-SUBDOMAIN] -H "X-API-Key: [YOUR-API-KEY]" |
| DNS record verwijderen | curl -X DELETE https://mddns.azurewebsites.net/subdomain/name/[YOUR-SUBDOMAIN] -H "X-API-Key: [YOUR-API-KEY] |

## AutoUpdater

Met de AutoUpdater veranderen de door jou gespecificeerde dns records automatisch op het moment dat het IP adres van de server veranderd. Dit kan zo vaak als je zelf wilt door middel van een cronjob, een voorbeeld is hier van beschikbaar.

Configuratie:
In het mddns-autoupdater-config.json bestand geef je op wat je api-key is, wat de api-ip adres is en welke subdomeinen er gemonitord moeten worden.
