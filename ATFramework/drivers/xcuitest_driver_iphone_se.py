from optparse import OptionParser
import inspect

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command as RemoteCommand
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.webelement import WebElement

class Element():
    config = {
    'height': 1,
    'width': 1,
    'ratio': 1,
    'x_offset': 0,
    'y_offset': 0,
    }
    @property
    def rect(self):
        temp = self._rect.copy()
        rect_new = {
        'height': temp['height'] * self.config['ratio'], 
        'width': temp['width'] * self.config['ratio'], 
        'x': temp['x']* self.config['ratio'] + self.config['x_offset'],
        'y': temp['y']* self.config['ratio'] + self.config['y_offset'],
        }
        for k,v in rect_new.items():
            rect_new[k] = int(v)
        return rect_new

    @property
    def location(self):
        temp = self._location.copy()
        location_new = {
        'x': temp['x'] * self.config['ratio']+ self.config['x_offset'], 
        'y': temp['y'] * self.config['ratio']+ self.config['y_offset'],
        }
        for k,v in location_new.items():
           location_new[k] = int(v)
        return location_new

    def set_config(self,config):
        # print(f'setting config :{config}')
        self.config = config


class Driver():
    def is_ipad(self):
        return self.capabilities.get('type',"").lower() == 'ipad'
    def is_iphone_se(self):
        return self.capabilities.get('type',"").lower() == 'iphone_se'
    @property
    def current_package(self):
        return self.execute_script('mobile:activeAppInfo')['bundleId']
    @property
    def current_bundle_id(self):
        return self.current_package
    def set_window_size(self,w=375,h=667):
        self._window_size = {'width':w,'height':h}
        self.y_offset = 21
        self.ratio = (self._window_size['height'] - 2*self.y_offset) / self._get_window_size()['height']
        self.x_offset = int((self._window_size['width'] - 
                    self._get_window_size()['width']* self.ratio) /2)
        # print(f'{self._window_size=}\n{self.ratio=}\n{self.x_offset=}')
    def get_window_size(self):
        try:
            return self._window_size
        except:
            return self._get_window_size()
    def create_web_element(self, element_id, w3c=False):
        """Creates a web element with the specified element_id.

        Overrides method in Selenium WebDriver in order to always give them
        Appium WebElement

        Args:
            element_id (int): The element id to create a web element
            w3c (bool): Whether the element is W3C or MJSONWP

        Returns:
            `MobileWebElement`
        """
        ret = WebElement(self, element_id, w3c)
        if isinstance(ret,WebElement):
            config = {
            'height': self._window_size['height'],
            'width': self._window_size['width'],
            'ratio': self.ratio,
            'x_offset': self.x_offset,
            'y_offset': self.y_offset,
            }
        ret.set_config(config)
        # print(f'{ret.rect=}')
        return ret
        
    def find_element(self, by=By.ID, value=None):
        """'Private' method used by the find_element_by_* methods.

        Override for Appium

        Usage:
            Use the corresponding find_element_by_* instead of this.

        Returns:
            `appium.webdriver.webelement.WebElement`

        :rtype: `MobileWebElement`
        """
        ret = self.execute(RemoteCommand.FIND_ELEMENT, {
            'using': by,
            'value': value})['value']
        if isinstance(ret,WebElement):
            ret.set_config({        
            'height': self._window_size['height'],
            'width': self._window_size['width'],
            'ratio': self.ratio,
            'x_offset': self.x_offset,
            'y_offset': self.y_offset,
            })    
        return ret

    def find_elements(self, by=By.ID, value=None):
        """'Private' method used by the find_elements_by_* methods.

        Override for Appium

        Usage:
            Use the corresponding find_elements_by_* instead of this.

        Returns:
            :obj:`list` of :obj:`appium.webdriver.webelement.WebElement`

        :rtype: list of `MobileWebElement`
        """
        ret = self.execute(RemoteCommand.FIND_ELEMENTS, {
            'using': by,
            'value': value})['value'] or []
        if isinstance(ret,WebElement):
            ret.set_config({
            'height': self._window_size['height'],
            'width': self._window_size['width'],
            'ratio': self.ratio,
            'x_offset': self.x_offset,
            'y_offset': self.y_offset,
            })
        return ret

e = inspect.getmembers(Element, predicate=inspect.isdatadescriptor)
e.extend(inspect.getmembers(Element, predicate=inspect.isfunction))
# print(e)
for k,v in e:
    if "__" in k: continue
    # print(f"WebElement add {k}")
    try:
        setattr(WebElement,f"_{k}",getattr(WebElement,k))
        # print(f"WebElement backup _{k}")
    except:
        pass
    setattr(WebElement,k,v)

d = inspect.getmembers(Driver, predicate=inspect.isdatadescriptor)
d.extend(inspect.getmembers(Driver, predicate=inspect.isfunction))
for k,v in d:
    # print(f'WebDriver add {k}')
    try:
        setattr(WebDriver,f"_{k}",getattr(WebDriver,k))
    except:
        pass
    setattr(WebDriver,k,v)
WebDriver._window_size = {'width':375,'height':667}
WebDriver.x_offset = 0
WebDriver.y_offset = 0
WebDriver.ratio = 1


# override rect
@property
def _rect(self):
    # print("=> rect correct")
    if self._w3c:
        return self._execute(Command.GET_ELEMENT_RECT)['value']
    else:
        rect = self.size.copy()
        rect.update(self._location) # new location
        return rect
WebElement._rect = _rect


