[![Build Status](https://travis-ci.org/mini-kep/parsers.svg?branch=master)](https://travis-ci.org/mini-kep/parsers)
[![Coverage badge](https://codecov.io/gh/mini-kep/parsers/branch/master/graphs/badge.svg)](https://codecov.io/gh/mini-kep/parsers)

# Concept

Parsers extract data from sources to upload them to database. 

# Data structure

Parsers are used to scan a data source (file or other API) and emit a list of dictionaries.
Each dictionary represents one observation (datapoint).

Datapoint dictionary has `date`, `freq`, `name` and `value` keys.

Example:

```python 
 {'date': '2017-09-26', 
  'freq': 'd', 
  'name': 'USDRUR_CB', 
  'value': Decimal(57.566)},
```

Same data structure is used to upload data to database.

# Individual parsers

Each parser is a child of `parsers.getter.base.ParserBase` class.
A parser has its own observation start date, url constructor, response parsing function,
the rest of functionality is inherited from `ParserBase`.

Parsers have `.extract()` and `.upload()` methods and an `items` property.

Creating a parser without argument forces to scan full dataset.

Sample parser job:
```python
parser = KEP_Annual()
parser.extract()
parser.upload()
```

Querying full dataset is a burden on the original sources. Thus, parsers can return 
datapoints from a specific date to present: 

```python
from parsers.getter.cbr_fx import USDRUR
datapoints = CBR_USD(start_date='2017-09-01').extract().items
```

or for a fixed period in time:

```python
from parsers.getter.brent import Brent
datapoints = Brent('2017-09-01', '2017-10-01').extract().items
```

#### List of parser classes:

```
from parsers import PARSERS

(parsers.getter.kep.KEP_Annual,
 parsers.getter.kep.KEP_Qtr,
 parsers.getter.kep.KEP_Monthly,
 parsers.getter.brent.Brent,
 parsers.getter.cbr_fx.USDRUR,
 parsers.getter.ust.UST)
```


# Parser collection 

```Dataset``` class used to manipulate data from all parsers as a collection.
Avaliable methods are:

```
Dataset(start_date, end_date).items
Dataset(start_date, end_date).save_json(filename)
Dataset(start_date, end_date).upload()

```

# Controller 

`manage.py` has functions for typical parser jobs:
   - save reference dataset as json file (a copy of the file used in database testing)
   - upload latest values to database (defaults to last 2 weeks)
   - print parser descriptions  
   

# Parser descriptions

Use ```manage.print_markdown_descriptions()``` to update. 

| Parser | KEP_Annual |
| ------ | ---------- |
| Description | Annual data from KEP publication (Rosstat) |
| Start date | 1999-01-01 |

| Parser | KEP_Qtr |
| ------ | ------- |
| Description | Quarterly data from KEP publication (Rosstat) |
| Start date | 1999-01-01 |

| Parser | KEP_Monthly |
| ------ | ----------- |
| Description | Monthly data from KEP publication (Rosstat) |
| Start date | 1999-01-01 |

| Parser | Brent |
| ------ | ----- |
| Description | Brent oil price (EIA) |
| Start date | 1987-05-20 |

| Parser | USDRUR |
| ------ | ------ |
| Description | Official USD/RUR exchange rate (Bank of Russia) |
| Start date | 1992-07-01 |

| Parser | UST |
| ------ | --- |
| Description | US Treasuries interest rates (UST) |
| Start date | 1990-01-01 |

Parser types
============

**repo** (*'heavy'*, *'dirty'*) - some parsers are styled to download the data, transform it and provide the output in local folder or URL. These ususally work on bad formats of data, eg Word, and require a lot of work to extract data because the source data is not structured well. 

*'thin'* (*'clean'*, *'API-parcer'*) - some parsers can do the job on query, yield datapoints and die fast and easily because source data is clean. These parsers usually do not require disk space to store intermeduate parsing result. 

Parser list
===========

#### repo: rosstat-kep
Produces output in <https://github.com/mini-kep/parser-rosstat-kep/tree/master/data/processed/latest>


Other parsers code is moved to this repo:

#### API parcer: cbr-usd (CB)
<https://github.com/ru-stat/parser-cbr-usd>

#### API parcer: Brent (EIA)
<https://github.com/epogrebnyak/data-fx-oil/blob/master/brent.py>
result: <https://github.com/epogrebnyak/data-fx-oil/blob/master/brent_daily.txt>

#### API parcer: yield curve (Treausry)
<https://github.com/epogrebnyak/ust>
result: <https://raw.githubusercontent.com/epogrebnyak/ust/master/ust.csv> (1.1 Mb)


Todo:

#### repo: rosstat-806-regional
<https://github.com/epogrebnyak/data-rosstat-806-regional>

#### repo: data-rosstat-isep
<https://github.com/epogrebnyak/data-rosstat-isep>
