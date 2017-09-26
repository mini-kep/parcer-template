# 

From [src/parsers.py](https://github.com/mini-kep/parsers/blob/master/src/parsers.py) we need to invoke following scripts:

<https://github.com/mini-kep/parser-rosstat-kep/blob/master/src/getter.py#L34-L37>

| Parser | RosstatKEP |
| ------ | ---------- |
| Description | Parse sections of Rosstat 'KEP' publication |
| URL | [http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/st...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391) |
| Frequency | Annual, quarterly, monthly |
| Variables | CPI_rog, RUR_EUR_eop |


<https://github.com/ru-stat/parser-cbr-usd/blob/master/cbr_usd.py>

| Parser | CBR_USD |
| ------ | ------- |
| Description | Retrieve Bank of Russia official USD to RUB exchange rate |
| URL | [http://www.cbr.ru/scripts/Root.asp?PrtId=SXML](http://www.cbr.ru/scripts/Root.asp?PrtId=SXML) |
| Frequency | Daily |
| Variables | USDRUR_CB |

<https://github.com/epogrebnyak/data-fx-oil/blob/master/brent.py>

| Parser | BrentEIA |
| ------ | -------- |
| Description | Retrieve Brent oil price from US EIA |
| URL | [https://www.eia.gov/opendata/qb.php?category=241335](https://www.eia.gov/opendata/qb.php?category=241335) |
| Frequency | Daily |
| Variables | BRENT |
