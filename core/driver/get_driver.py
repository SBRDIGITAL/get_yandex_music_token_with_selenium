from dataclasses import dataclass

import traceback, json, time, os

from typing import Any, Dict, List, Union

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.command import Command



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
        """ ## Публичный метод - возвращает объект браузера """
        return self.driver
    


@dataclass
class GetToken:
    """
    ## Получает токен яндекс музыки после авторизации

    ### Пример использования:
        if __name__ == "__main__":
            GetToken()
    """
    oauth_url: str = "https://oauth.yandex.ru/authorize?response_type=token&client_id="+\
        "23cabbbdc6cd418abb4b39c32c41195d"
    driver: Chrome = MyDriver().get_driver
    token: str = None
    sleep_time: Union[int, float] = 1
    token_file_path: str = os.path.join('token.txt')
    time_counter: int = 120

    def __post_init__(self) -> None:
        """ ## Методы, которые выполняются после инициализации класса """
        self._open_url()
        self._get_token()
        self._close_driver()
        self._write_token()


    def _open_url(self) -> None:
        """ ## Открывает url, которая указана в oauth_url """
        self.driver.get(self.oauth_url)

    def __get_perfomance_log(self) -> List[Any]:
        """ ## Возвращает логи """
        try:
            logs_raw = self.driver.get_log("performance")
        except:
            traceback.print_exc()
            logs_raw = []
        
        return logs_raw

    def __sleep(self) -> None:
        """ ## Делает паузу выполнения скрипта """
        time.sleep(self.sleep_time)

    def _check_time(self) -> None:
        """ ## Проверяет прошло ли 2 минуты с момента запуска скрипта """
        if self.time_counter == 0:
            try:
                print('За 2 минуты токен не был найден')
                self._close_driver()
                exit()
            except:
                traceback.print_exc()
                exit()

    def _get_token(self) -> None:
        while not self.token and self.__is_active():
            self._check_time()
            self.__sleep()
            logs_raw:List[Any] = self.__get_perfomance_log()
            for lr in logs_raw:
                log = json.loads(lr["message"])["message"]
                url_fragment:str = log.get('params', {}).get('frame', {}).get('urlFragment')
                if url_fragment:
                    self.token = url_fragment.split('&')[0].split('=')[1]

    def __is_active(self) -> None:
        try:
            self.driver.execute(Command.GET_ALL_COOKIES)
            return True
        except:
            traceback.print_exc()
            return False
    
    def _close_driver(self) -> None:
        """ ## Закрывает браузер """
        if self.driver:
            self.driver.close()

    def _write_token(self) -> None:
        """ ## Записывает токен в файл ил печатает в консоль если токен = None """
        with open(self.token_file_path, 'w', encoding='UTF-8') as tfile:
            tfile.write(self.token) if self.token else print('Токен не найден')