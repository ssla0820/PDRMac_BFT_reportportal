import re, sys, json
from urllib.parse import quote
from urllib import request
from typing import Final

url_prefix: Final = r'https://script.google.com/macros/s/AKfycbwjfLxxlJ1d5Vjr_-dkSwwkYk6NQRWnvhzUtGM7fKwkKy78HJWd/exec?data='

class Google_sheet():
    def __init__(self,data):
        if sys.version_info < (3, 8): raise Exception("[Error] ** Required Python 3.8+ **")
        self.execute(data)
    
    def execute(self,data):
        data_json = json.dumps(data).replace('\\\"',"\"")
        data_uri_encoded = quote(data_json)
        # print(url_prefix+data_uri_encoded)
        self.ret_raw = request.urlopen(url_prefix+data_uri_encoded).read().decode('utf-8')
        try:
            self.ret = json.loads(self.ret_raw)
        except json.decoder.JSONDecodeError:
            self.ret = {
                "result": re.findall(r'\"result\"[\w\W]*?:[\w\W]*?\"(.*?)\"[\w\W]*?',self.ret_raw)[0], 
                "data": re.findall(r'\"(?:reason|data)\"\s*?:\s*"(.*)"\s*?}',self.ret_raw)[0]
            }
    
    @property
    def result(self):
        return self.ret.get('result',"[Exception]")
    
    @property
    def data(self):
        try:
            self.data_raw = self.ret['data']
            if value := re.findall(r'"value"\s*:\s*"(.*?)"(?:\s*,\s*"\w*"\s*:|\s*})',self.data_raw): # parameter
                self.data_raw_temp = self.data_raw.replace(value[0],"")
                self.data_raw_temp = re.sub(r',\s*\"value\"\s*:\s*""\s*',"",self.data_raw_temp)
                self.data_raw_temp = re.sub(r'\"value"\s*:\s*""\s*,',"",self.data_raw_temp)
                data = eval(self.data_raw_temp)
                data.update({"value": value[0].replace('"' ,'\"' )})
            # elif self.data_raw := re.sub('(^")|("$)',"",self.data_raw).replace('"','\\"'):
                # print(f'{self.data_raw=}')
            else:
                data = eval(self.data_raw)
            return data[0][0] if (len(data) == 1 and len(data[0]) == 1)  else data
        except Exception:
            return ""

if __name__ == "__main__":
    parameter = {
        "spardsheet_id" : "1lLDSYlLj8X8dGtGebeybbkgRTJm79ZhDUvhGBH9F97I", 
        "sheet_name" : "MyTest", 
        "range" : "B1", 
        "value" : "333", 
        "cmd" : "query"
    }

    g = Google_sheet(parameter)
    print(g.data)