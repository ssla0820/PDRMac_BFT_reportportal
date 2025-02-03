from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .log import logger

def element_exist_click(driver,locator,timeout=3,ignore=True):
    try:
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located(locator))
        element.click()
        return element
    except Exception as e:
        if ignore:
            logger("{} is not found, but ignore it. {} || {}".format(locator , str(e), e))
            return True
        else:
            return None
            

def element_shot(driver):
    rect = el(L.main.project.select).rect
    path = os.getenv('temp', os.path.dirname(__file__))
    path_full = "%s/temp.png" % path
    driver.get_screenshot_as_file(path_full)
    im = cv2.imread(path_full)
    im_crop = im[rect['y'] : rect['y']+rect['height'],rect['x']:rect['x']+rect['width']]
    path_crop = "%s/%s.png" % (path,uuid.uuid4())
    cv2.imwrite(path_crop, im_crop)
    print (path_crop)
