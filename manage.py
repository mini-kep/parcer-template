import arrow
from parsers.getter import PARSERS
from parsers.dataset import Dataset 
from parsers.markdown import as_markdown

def save_reference_dataset(): 
    dataset = Dataset(parsers=PARSERS, 
                      start_date='2016-06-01', 
                      end_date='2016-12-31')
    dataset.extract()
    dataset.save_json('test_data_2016H2.json')
    
def print_markdown_descriptions(parsers=PARSERS):
    for p in parsers:
        print(as_markdown(p))
        print()
        
def upload_latest(parsers=PARSERS, dt=None):
    if dt is None:
       dt = arrow.now().shift(weeks=-2).format("YYYY-MM-DD")
    d = Dataset(parsers, dt)
    d.upload()


if __name__ == '__main__':
    #save_reference_dataset()
    #print_markdown_descriptions()
    upload_latest()
    pass

# COMMENT: longest time for last parser 

#Annual data from KEP pulication (Rosstat)
#Reading from https://raw.githubusercontent.com/mini-kep/parser-rosstat-kep/master/data/processed/latest/dfa.csv
#Time elapsed: 0.25 sec.
#Uploaded 524 datapoints
#Time elapsed: 0.02 sec.
#
#Quarterly data from KEP pulication (Rosstat)
#Reading from https://raw.githubusercontent.com/mini-kep/parser-rosstat-kep/master/data/processed/latest/dfq.csv
#Time elapsed: 0.28 sec.
#Uploaded 2537 datapoints
#Time elapsed: 1.68 sec.
#
#Monthly data from KEP pulication (Rosstat)
#Reading from https://raw.githubusercontent.com/mini-kep/parser-rosstat-kep/master/data/processed/latest/dfm.csv
#Time elapsed: 0.35 sec.
#Uploaded 7193 datapoints
#Time elapsed: 2.17 sec.
#
#Brent oil price (EIA)
#Reading from http://api.eia.gov/series/?api_key=15C0821C54636C57209B84FEEE3CE654&series_id=PET.RBRTE.D
#Time elapsed: 0.89 sec.
#Uploaded 7741 datapoints
#Time elapsed: 1.75 sec.
#
#Official USD/RUR exchange rate (Bank of Russia)
#Reading from http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/06/2017&date_req2=19/11/2017&VAL_NM_RQ=R01235
#Time elapsed: 0.16 sec.
#Uploaded 121 datapoints
#Time elapsed: 1.22 sec.
#
#US Treasuries interest rates (UST)
#Reading from http://www.treasury.gov/resource-center/data-chart-center/interest-rates/pages/XmlView.aspx?data=yieldyear&year=2017
#Time elapsed: 0.78 sec.
#Uploaded 2442 datapoints
#Time elapsed: 15.10 sec.
#
#Total extract and upload time: 24.63


# WONTFIX: changed endpoint url to http, not https:
# Error on bad SSL connection:
# SSLError: HTTPSConnectionPool(host='minikep-db.herokuapp.com', port=443): 
#    Max retries exceeded with url: /api/datapoints 
#    (Caused by SSLError(SSLError("bad handshake: Error([('SSL routines', 
#    'tls_process_server_certificate', 'certificate verify failed')],)",),))