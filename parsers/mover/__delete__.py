import requests
from parsers.config import UPLOAD_URL


def delete(params, token, endpoint=UPLOAD_URL): #pragma: no cover
    """Delete method."""
    return requests.delete(url=endpoint,
                           params=params,
                           headers={'API_TOKEN': token})


def delete_name(name):
    for freq in 'aqmd':
        d = dict(freq=freq,
                 name=name)
        delete(d, TOKEN).status_code   
    

if __name__ == "__main__": #pragma: no cover

    names =  [ \
    "GOV_EXPENSE_ACCUM_CONSOLIDATED_bln_rub",
    "GOV_EXPENSE_ACCUM_FEDERAL_bln_rub",
    "GOV_EXPENSE_ACCUM_SUBFEDERAL_bln_rub",
    "GOV_REVENUE_ACCUM_CONSOLIDATED_bln_rub",
    "GOV_REVENUE_ACCUM_FEDERAL_bln_rub",
    "GOV_REVENUE_ACCUM_SUBFEDERAL_bln_rub",
    "GOV_SURPLUS_ACCUM_FEDERAL_bln_rub",
    "GOV_SURPLUS_ACCUM_SUBFEDERAL_bln_rub"
]

    #TOKEN = it is a secret
    for name in names:
        delete_name(name)