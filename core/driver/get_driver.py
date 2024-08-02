from dataclasses import dataclass

from typing import Dict

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



@dataclass
class MyDriver:
    """
    ## Настройка драйвера Chrome

    ### Пример использования:
        - driver: Chrome = MyDriver().get_driver
        - driver.get("your_url")
    """
    driver: Chrome = None
    options: Options = ChromeOptions()
    capabilities: Dict[str, str] = None

    def __post_init__(self) -> None:
        """ ## Методы, которые выполняются после инициализации класса """
        self._setting_driver()
        self._get_driver()
        self.__maximize_window()

    def _setting_driver(self) -> None:
        """ ## Настройка перед запуском """
        self.capabilities = DesiredCapabilities.CHROME.copy()
        self.options.set_capability(name='goog:loggingPrefs', value={'performance': 'ALL'})

    def __maximize_window(self) -> None:
        """ ## Разворачивает окно на весь экран """
        self.driver.maximize_window()

    def _get_driver(self) -> None:
        """ ## Создаёт объект браузера """
        self.driver = Chrome(options=self.options)
        
    @property
    def get_driver(self) -> Chrome:
        """ ## Публичное свойство - возвращает объект браузера """
        return self.driver