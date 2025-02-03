import logging,logging.handlers,os,inspect,platform
from functools import wraps


try:
    os.system('color')
except:
    pass

log_path = ""
dname = os.path.dirname
pattern = dname(dname(dname(__file__))) # [log] -> [ATFramework] -> [Target Folder]


if platform.system() == "Windows":
    import ctypes
    class DbgViewHandler(logging.Handler):
        def emit(self, record):
            ctypes.windll.kernel32.OutputDebugStringW(self.format(record))

for frame in inspect.stack():
    if pattern in frame.filename:
        log_path = dname(frame.filename) + "/log"

os.makedirs( log_path , exist_ok=True)

def set_udid(udid):
    global log_path
    log_path = "%s/%s" % (log_path, udid)

def logger(*msg,function=None,file_name=None,write_to_file=True,line=True):

    if not file_name:
        file_name = log_path + "/module.log"
    if not function:
        function = inspect.stack()[1].function
        line = inspect.stack()[1].frame.f_lineno
        name = os.path.basename(inspect.stack()[1].filename)
    else:
        line = inspect.stack()[2].frame.f_lineno
        name = os.path.basename(inspect.stack()[2].filename)
    cformat_pattern = "\033[92m%(asctime)s \033[97;4;1m<{}>\033[0m \033[96m[{}]\033[93;1m(line {})\033[0m %(message)s".format(name,function,line)
    format_pattern = "%(asctime)s <{}> [{}](line {}) - %(message)s".format(name,function,line)
    formatter = logging.Formatter(fmt=format_pattern,datefmt="%m/%d/%Y %I:%M:%S %p")
    cformatter = logging.Formatter(fmt=cformat_pattern,datefmt="%m/%d/%Y %I:%M:%S %p")
    _logger = logging.getLogger("ATFramework")
    if _logger.handlers:
        for hdlr in _logger.handlers[:]:
            _logger.removeHandler(hdlr)
    _logger.setLevel(logging.DEBUG)
    _console = logging.StreamHandler()
    _console.setLevel(logging.DEBUG) 
    _console.setFormatter(cformatter)
    _logger.addHandler(_console)
    ft_rotating = logging.handlers.TimedRotatingFileHandler(file_name,when="D",interval=1,backupCount=0,delay=True)
    ft_rotating.setLevel(logging.DEBUG) #file_time_rotating
    ft_rotating.setFormatter(formatter)
    _logger.addHandler(ft_rotating)
    if platform.system() == "Windows":
        dbw = DbgViewHandler()
        dbw.setLevel(logging.DEBUG)
        dbw.setFormatter(formatter)
        _logger.addHandler(dbw)
    
    myMsg = [str(x) for x in msg]
    _logger.debug(str(*myMsg))
    ft_rotating.close()
    
    
def qa_log(file_name=None,write_to_file=True):
    'decorator'
    if not file_name:
        file_name = os.path.dirname(__file__)+"/log/Product.log"
        os.makedirs(log_path, exist_ok=True)
    def outer(func):
        @wraps(func)
        def inner(*args,**kwargs):
            log_pattern= "Start function "  + \
            ("args: %s" % str(args) if args else "") + \
            (" kwargs: %s" % str(kwargs) if kwargs else "")
            logger(log_pattern,function = func.__name__,file_name=file_name)
            ret = func(*args,**kwargs)
            logger("End function ",function = func.__name__,file_name=file_name)
            return ret
        return inner
    return outer


if __name__ == "__main__":
    '''decorator sameple'''
    @qa_log()
    def test(index,text="TEXT"):
        print ("index={} text={}".format(index,text))
    test(33,text="sample")
    
    '''normal logger sample'''
    def xxx():
        logger("123123")
    xxx()