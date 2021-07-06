import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class SeleniumDriverFactory(object):
    """
    Driver factory to provide driver for running tests on web browsers.
    The settings for the DriverFactory is on behave.ini file.
    It runs the tests through selenium grid if 'selenium_grid', on behave.ini, is true.
    If is False, it executes the Driver Managers for running tests.
    Supported browsers:
        - firefox
        - chrome
    """

    def __init__(self, context):
        self.context = context
        self.browser = self.context.userdata.get("browser", "")
        self.version = self.context.userdata.get("version", "")
        self.platform = self.context.userdata.get("platform", "")
        self.use_grid = self.context.userdata.get("use_grid", "")

    def get_driver(self):
        if self.use_grid in [True, "true", "True", "TRUE", "1"]:
            selenium_grid_ip = self.context.userdata.get(
                "selenium_grid_ip", ""
            )
            selenium_grid_port = self.context.userdata.get(
                "selenium_grid_port", ""
            )

            # Default platform for selenium grid
            platform_name = ""

            selenium_desired_capabilities = {
                "browserName": str(self.browser),
                "javascriptEnabled": True,
            }

            return webdriver.Remote(
                command_executor=f"http://{str(selenium_grid_ip)}:{str(selenium_grid_port)}/wd/hub",
                desired_capabilities=selenium_desired_capabilities,
            )
        else:
            web_driver = getattr(self, self.browser)
            return web_driver()

    def firefox(self):
        profile = webdriver.FirefoxProfile()

        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference(
            "browser.download.manager.showWhenStarting", False
        )
        profile.set_preference("browser.download.dir", os.getcwd())
        profile.set_preference("app.update.auto", False)
        profile.set_preference("app.update.enabled", False)
        profile.set_preference("app.update.silent", False)
        profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "text/csv/xls/zip/exe/msi",
        )
        profile.set_preference("xpinstall.signatures.required", False)

        if self.use_grid in [False, "false", "False", "FALSE", "0"]:
            return webdriver.Firefox(
                executable_path=GeckoDriverManager().install()
            )
        else:
            return webdriver.Firefox(profile)

    def chrome(self):
        options = webdriver.ChromeOptions()

        if "windows" in self.platform:
            options.add_argument("--start-maximized")
            options.add_argument("--no-sandbox")
        if "osx" in self.platform:
            options.add_argument("--kiosk")

        if self.use_grid in [False, "false", "False", "FALSE", "0"]:
            return webdriver.Chrome(
                executable_path=ChromeDriverManager().install()
            )
        else:
            return webdriver.Chrome(chrome_options=options)
