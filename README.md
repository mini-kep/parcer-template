[![Build Status](https://travis-ci.org/mini-kep/parsers.svg?branch=master)](https://travis-ci.org/mini-kep/parsers)
[![Coverage badge](https://codecov.io/gh/mini-kep/parsers/branch/master/graphs/badge.svg)](https://codecov.io/gh/mini-kep/parsers)

```parser/runner.py``` has parser classes to get data from sources. Aggregated dataset can be obtained using code below. It provides datapoints from the start of observation in each dataset. 

```python 
from runner import Dataset

gen = Dataset.yield_full_dataset()

```

Individual parsers can return datapoints from a specific date to present: 

```python
from runner import CBR_USD

gen = CBR_USD(start='2017-09-01').yield_dicts()
```

# Parser descriptions

| Parser | RosstatKEP_Monthly |
| ------ | ------------------ |
| Description | Monthly indicators from Rosstat 'KEP' publication |
| URL | [http://www.gks.ru/wps/wcm/connect/rossta...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391) |
| Frequency | Monthly |
| Variables | CPI, GDP, etc |

| Parser | RosstatKEP_Quarterly |
| ------ | -------------------- |
| Description | Quarterly indicators from Rosstat 'KEP' publication |
| URL | [http://www.gks.ru/wps/wcm/connect/rossta...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391) |
| Frequency | Quarterly |
| Variables | CPI, GDP, etc |

| Parser | RosstatKEP_Annual |
| ------ | ----------------- |
| Description | Annual indicators from Rosstat 'KEP' publication |
| URL | [http://www.gks.ru/wps/wcm/connect/rossta...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391) |
| Frequency | Annual |
| Variables | CPI, GDP, etc |

| Parser | CBR_USD |
| ------ | ------- |
| Description | Bank of Russia official USD to RUB exchange rate |
| URL | [http://www.cbr.ru/scripts/Root.asp?PrtId...](http://www.cbr.ru/scripts/Root.asp?PrtId=SXML) |
| Frequency | Daily |
| Variables | USDRUR_CB |

| Parser | BrentEIA |
| ------ | -------- |
| Description | Brent oil price from US EIA |
| URL | [https://www.eia.gov/opendata/qb.php?cate...](https://www.eia.gov/opendata/qb.php?category=241335) |
| Frequency | Daily |
| Variables | BRENT |
