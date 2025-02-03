import logging, logging.handlers
import subprocess, os, inspect, platform, time
from functools import wraps

'''
try:
    subprocess.run(['color'], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except:
    pass
'''

log_path = ""
dname = os.path.dirname
pattern = dname(dname(dname(__file__)))  # [log] -> [ATFramework] -> [Target Folder]

if platform.system() == "Windows":
    import ctypes


    class DbgViewHandler(logging.Handler):
        def emit(self, record):
            ctypes.windll.kernel32.OutputDebugStringW(self.format(record))

for frame in inspect.stack():
    if pattern in frame.filename and "site-packages" not in frame.filename:
        log_path = dname(frame.filename) + "/log"

os.makedirs(log_path, exist_ok=True)


def set_udid(udid):
    global log_path
    log_path = "%s/%s" % (log_path, udid)


def logger(*msg, function=None, line=None, file_name=None, log_name=None, write_to_file=True, level=1,
           _is_color=[False]):
    if not _is_color[0]:
        os.system("")
        _is_color[0] = True
    if not log_name:
        log_name = log_path + "/module.log"
        # print(f">>>  Output log file path = {log_name}")
    if function or line or file_name:
        line = line or inspect.stack()[2].frame.f_lineno
        name = file_name or os.path.basename(inspect.stack()[2].filename)
        function = function or inspect.stack()[2].function
    else:
        function = inspect.stack()[level].function
        line = line or inspect.stack()[level].frame.f_lineno
        name = os.path.basename(inspect.stack()[level].filename)

    cformat_pattern = "\033[92m%(asctime)s \033[97;4;1m<{}>\033[0m \033[96m[{}]\033[93;1m(line {})\033[0m %(message)s".format(
        name, function, line)
    format_pattern = "%(asctime)s <{}> [{}](line {}) - %(message)s".format(name, function, line)
    formatter = logging.Formatter(fmt=format_pattern, datefmt="%m/%d/%Y %I:%M:%S %p")
    cformatter = logging.Formatter(fmt=cformat_pattern, datefmt="%m/%d/%Y %I:%M:%S %p")
    _logger = logging.getLogger("ATFramework")
    if _logger.handlers:
        for hdlr in _logger.handlers[:]:
            _logger.removeHandler(hdlr)
    _logger.setLevel(logging.DEBUG)
    _console = logging.StreamHandler()
    _console.setLevel(logging.DEBUG)
    _console.setFormatter(cformatter)
    _logger.addHandler(_console)
    ft_rotating = logging.handlers.TimedRotatingFileHandler(log_name, when="D", interval=1, backupCount=0, delay=True, encoding="utf-8")
    ft_rotating.setLevel(logging.DEBUG)  # file_time_rotating
    ft_rotating.setFormatter(formatter)
    _logger.addHandler(ft_rotating)
    if platform.system() == "Windows":
        dbw = DbgViewHandler()
        dbw.setLevel(logging.DEBUG)
        dbw.setFormatter(formatter)
        _logger.addHandler(dbw)

    myMsg = ""
    for x in msg:
        myMsg = f"{myMsg} {x}"
    _logger.debug(myMsg)
    ft_rotating.close()


def qa_log(log_name=None, write_to_file=True):
    'decorator'
    if not log_name:
        log_name = os.path.dirname(__file__) + "/log/Product.log"
        os.makedirs(os.path.dirname(log_name), exist_ok=True)

    i = inspect.stack()[1]
    file_name = os.path.basename(i.filename)
    lineno = i.lineno

    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            log_pattern = ">> Start function " + \
                          ("args: %s" % str(args) if args else "") + \
                          (" kwargs: %s" % str(kwargs) if kwargs else "")
            logger(log_pattern, function=func.__name__, file_name=file_name, line=lineno, log_name=log_name)
            timer = time.time()
            ret = func(*args, **kwargs)
            logger(f"<< End function. Duration: {time.time() - timer} sec", function=func.__name__, file_name=file_name, line=lineno, log_name=log_name)
            return ret

        return inner

    return outer


if __name__ == "__main__":
    '''decorator sample'''


    @qa_log()
    def test(index, text="TEXT"):
        print(f"index={index} text={text}")


    test(33, text="sample")

    '''normal logger sample'''


    def xxx():
        logger("123123")


    xxx()

    logger("QA")
