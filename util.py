import simplejson 
import datetime as dt
import pandas as pd

#Global Initialization
jsonpath = "json/"

def dateRange(period , datelist = [] , add = False ,current = None ):
    if period is None:
        return None
    if add is True:
        range = pd.bdate_range(periods = period, freq = "C" ,holidays = datelist, end = current  , weekmask = "Mon Tue Wed Thu Fri" )
    else:
        end = dt.date.today().strftime("%Y-%m-%d")
        range = pd.bdate_range(periods = period, freq = "C" ,holidays = datelist, end = end  , weekmask = "Mon Tue Wed Thu Fri" )
    return range.date

def to_json(dictdata , filename , enclose = False , key = '' , **kwargs):
    if isinstance(dictdata , pd.DataFrame):
        if isinstance(dictdata.index , pd.MultiIndex):
            multi_to_single(dictdata , 'symbol')
            dictdata.index = dictdata.index.map(str)
    dictdata = to_dict(dictdata)
    if enclose:
        dictdata = enclose_dict(dictdata , key)
    dictdata = add_dict_details(dictdata , filename , **kwargs)
    with open(jsonpath + filename + '.json', 'w') as f:
        simplejson.dump(dictdata , f , indent = 4 , ignore_nan = True )