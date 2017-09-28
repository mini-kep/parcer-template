Parser types
============

**repo** (*'heavy'*, *'dirty'*) - some parsers are styled to download the data, transform it and provide the output in local folder or URL. These ususally work on bad formats of data, eg Word, and require a lot of work to extract data because the source data is not structured well. 

**serverless** (*'thin'*, *'clean'*, *'API-parcer'*) - some parsers can do the job on query, yield datapoints and die fast and easily because source data is rather clean and fast to get. 


Parser list
===========

At various time following parsers were developed, ```rosstat-kep``` is most advanced one. Parsers are not structured to same template now. They do not have a common invoke method. All of them just write a CSV file to own repo.

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



