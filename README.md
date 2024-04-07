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
