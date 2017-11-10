[![Build Status](https://travis-ci.org/mini-kep/parsers.svg?branch=master)](https://travis-ci.org/mini-kep/parsers)
[![Coverage badge](https://codecov.io/gh/mini-kep/parsers/branch/master/graphs/badge.svg)](https://codecov.io/gh/mini-kep/parsers)

Parsers add data from sources to database. 

```parsers.getters``` contain modules for individual parsers. Each parser module has a function 
that yields dictionaries with datapoints:
```python 
 {'date': '2017-09-26', 
  'freq': 'd', 
  'name': 'USDRUR_CB', 
  'value': 57.566},
```

```parsers.runner``` has parser handler classes (derived from ```ParserBase``` class)
that invoke getter functions and upload data to database:
   
   - ```all_items()``` method always invokes a getter function
   - ```upload()``` saves to database


```Dataset``` class used to manipulate all information, obtained from parsers. 
Full dataset can be obtained using code below.

```python 
from runner import Dataset

gen = Dataset.all_items()

```

Querying full dataset is a burden on the original API sources. Thus, individual parsers can return 
datapoints from a specific date to present: 

```python
from runner import CBR_USD

gen = CBR_USD(start='2017-09-01').items
```

and so can ```Dataset```:

```
gen = Dataset.items(start='2017-09-01')
```

Uploading to database is done by calling ```upload()``` method: 

```
CBR_USD(start='2017-11-01').upload()
Dataset('2017-11-01').upload()

```

Uploading large datasets may cause error, better use recent dates for upload. 


# Parser descriptions

Use ```print(Dataset.as_markdown())``` to update. 


| Parser | RosstatKEP_Monthly |
| ------ | ------------------ |
| Description | Monthly indicators from Rosstat 'KEP' publication |
| URL | [http://www.gks.ru/wps/wcm/connect/rossta...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391) |
| Frequency | Monthly |
| Start date | 1999-01-31 |

| Parser | RosstatKEP_Quarterly |
| ------ | -------------------- |
| Description | Quarterly indicators from Rosstat 'KEP' publication |
| URL | [http://www.gks.ru/wps/wcm/connect/rossta...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391) |
| Frequency | Quarterly |
| Start date | 1999-01-31 |

| Parser | RosstatKEP_Annual |
| ------ | ----------------- |
| Description | Annual indicators from Rosstat 'KEP' publication |
| URL | [http://www.gks.ru/wps/wcm/connect/rossta...](http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391) |
| Frequency | Annual |
| Start date | 1999-01-31 |

| Parser | CBR_USD |
| ------ | ------- |
| Description | Bank of Russia official USD to RUB exchange rate |
| URL | [http://www.cbr.ru/scripts/Root.asp?PrtId...](http://www.cbr.ru/scripts/Root.asp?PrtId=SXML) |
| Frequency | Daily |
| Start date | 1992-01-01 |

| Parser | BrentEIA |
| ------ | -------- |
| Description | Brent oil price from US EIA |
| URL | [https://www.eia.gov/opendata/qb.php?cate...](https://www.eia.gov/opendata/qb.php?category=241335) |
| Frequency | Daily |
| Start date | 1987-05-15 |

Parser types
============

**repo** (*'heavy'*, *'dirty'*) - some parsers are styled to download the data, transform it and provide the output in local folder or URL. These ususally work on bad formats of data, eg Word, and require a lot of work to extract data because the source data is not structured well. 

**serverless** (*'thin'*, *'clean'*, *'API-parcer'*) - some parsers can do the job on query, yield datapoints and die fast and easily because source data is rather clean and fast to get. 


Parser list
===========

At various time following parsers were developed, ```rosstat-kep``` is most advanced one. Original code listings are below.

#### repo: rosstat-kep
Produces output in <https://github.com/mini-kep/parser-rosstat-kep/tree/master/data/processed/latest>

#### API parcer: cbr-usd (CB)
<https://github.com/ru-stat/parser-cbr-usd>

#### API parcer: Brent (EIA)
<https://github.com/epogrebnyak/data-fx-oil/blob/master/brent.py>
result: <https://github.com/epogrebnyak/data-fx-oil/blob/master/brent_daily.txt>

To add
======

#### API parcer: yield curve (Treausry)
<https://github.com/epogrebnyak/ust>
result: <https://raw.githubusercontent.com/epogrebnyak/ust/master/ust.csv> (1.1 Mb)

#### repo: rosstat-806-regional
<https://github.com/epogrebnyak/data-rosstat-806-regional>
