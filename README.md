[![Build Status](https://travis-ci.org/mini-kep/parsers.svg?branch=master)](https://travis-ci.org/mini-kep/parsers)
[![Coverage badge](https://codecov.io/gh/mini-kep/parsers/branch/master/graphs/badge.svg)](https://codecov.io/gh/mini-kep/parsers)

# Concept

Parsers extract data from sources to upload them to database. 

# Data structure

Parsers are used to scan a data source (file or other API) and emit a list of dictionaries.
Each dictionary represents one observation on a variable in time (datapoint).

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

#### Parser construction

Each parser is a child of `parsers.getter.base.ParserBase` class.

To make a new parser - inherit from `ParserBase` and change:
- observation start date (class attribute) 
- url constructor (property)
- response parsing function (method)

#### Parser methods

Parsers have `.extract()` and `.upload()` methods:
  - `.extract()` changes `.parsing_result`
  - `.upload()` changes `.items`

#### Parser work cycle 

Sample parser job:
```python
parser = KEP_Annual()
parser.extract()
parser.upload()
```

#### Arguments

Creating a parser without arguments forces parser to scan full dataset, 
and it is a burden on the original sources. Thus, parsers can return 
datapoints from a specific date to present: 

```python
from parsers.getter.cbr_fx import USDRUR
parser = CBR_USD(start_date='2017-09-01')
```

or for a fixed period in time:

```python
from parsers.getter.brent import Brent
parser = Brent('2017-09-15', '2017-10-17')
```

# Parser collection 

```Dataset``` class used to manipulate a group of parsers.

```python
from parsers import PARSERS

d = Dataset(PARSERS, start_date, end_date) 
d.extract()
d.upload()
d.save_json(filename)
```

# Typical jobs

`manage.py` has functions for typical parser jobs:
   - upload latest values to database 
   - save reference dataset as json file
   - print parser descriptions in markdown 
   
# Parser descriptions

Current list of parsers:

`getter.PARSERS`:

 - parsers.getter.kep.KEP_Annual,
 - parsers.getter.kep.KEP_Qtr,
 - parsers.getter.kep.KEP_Monthly,
 - parsers.getter.brent.Brent,
 - parsers.getter.cbr_fx.USDRUR,
 - parsers.getter.ust.UST

Use ```manage.markdown_descriptions()``` to update. 

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


Parser list
===========

#### repo: rosstat-kep
Produces output in <https://github.com/mini-kep/parser-rosstat-kep/tree/master/data/processed/latest>

Other parsers code is moved to this repo from following original sources:

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
<https://github.com/mini-kep/data-rosstat-isep>


Glossary
========

Types of parsers:

**repo** (*'heavy'*, *'dirty'*) - some parsers are styled to download the data, transform it and provide the output in local folder or URL. These ususally work on bad formats of data, eg Word, and require a lot of work to extract data because the source data is not structured well. 

*'thin'* (*'clean'*, *'API-parcer'*) - some parsers can do the job on query, yield datapoints and die fast and easily because source data is clean. These parsers usually do not require disk space to store intermeduate parsing result. 
