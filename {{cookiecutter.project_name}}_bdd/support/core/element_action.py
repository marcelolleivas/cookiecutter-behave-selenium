from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from {{cookiecutter.project_name}}_bdd.utils.assert_utils import Assert


class ElementAction(object):
    """
    Action class to perform basic operations on webpage elements.
    """

    locator_strategies = [
        "XPATH",
        "ID",
        "NAME",
        "CLASS_NAME",
        "LINK_TEXT",
        "CSS_SELECTOR",
        "PARTIAL_LINK_TEXT",
        "TAG_NAME",
    ]

    def __init__(self, context):
        self.context = context

    def fetch_element(
        self, locator, is_list_of_elements=False, element_timeout=None
    ) -> WebElement:
        """
        Find the web element based on the specified locator.
        Before attempting to find the element, check if presence and visibility of it is found.
        Args:
            - locator: element locator
            - is_list_of_elements: when locator returns multiple elements, you should set it to True
            - element_timeout: It overrides 'element_fetch_timeout', settled in behave.ini.
        """
        strategy = locator[0]
        actual_locator = locator[1]

        if element_timeout is None:
            element_timeout = int(
                self.context.userdata.get("element_fetch_timeout", "")
            )
        try:
            if strategy not in ElementAction.locator_strategies:
                raise KeyError(
                    "Unsupported locator strategy"
                    f"Attempted Strategy : {strategy}"
                )
            try:
                WebDriverWait(self.context.driver, element_timeout).until(
                    EC.visibility_of_element_located(
                        (getattr(By, strategy), actual_locator)
                    )
                )
            except (TimeoutException, StaleElementReferenceException):
                self.context.logger.error(
                    f"Timed out after {str(element_timeout)} seconds waiting for element"
                    f"{str(actual_locator)} to be present",
                    exc_info=True,
                )

            if is_list_of_elements:
                return self.context.driver.find_elements(
                    getattr(By, strategy), actual_locator
                )

            try:
                element = self.context.driver.find_element(
                    getattr(By, strategy), actual_locator
                )
                return element
            except TypeError:
                return False

        except NoSuchElementException:
            raise NoSuchElementException(
                "Unable to locate element on page."
                f"Strategy: {str(strategy)}"
                f"Locator: {str(actual_locator)}"
            )

    def is_element_present(
        self, locator, replacement=None, timeout=None
    ) -> bool:
        """
        Verify if element is present on page.
        Args:
            - locator: element locator
            - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
            - timeout: It overrides 'element_fetch_timeout', settled in behave.ini
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        try:
            self.fetch_element(locator, element_timeout=timeout)
            return True
        except NoSuchElementException:
            return False

    def is_element_displayed(
        self, locator, replacement=None, timeout=None
    ) -> bool:
        """
        Verify if element is present on page.
        Is used in cases where element is present in DOM and you need to check whether
        it is displayed or not in the UI.
        Args:
            - locator: element locator
            - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
            - timeout: It overrides 'element_fetch_timeout', settled in behave.ini
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        try:
            if not self.fetch_element(locator, element_timeout=timeout):
                return False
            return self.fetch_element(
                locator, is_list_of_elements=timeout
            ).is_displayed()
        except Exception:
            return False

    def is_text_present(self, text) -> bool:
        """
        Verify if text is present on webpage.
        Args:
             - text: text to verify
        """
        try:
            body = self.fetch_element("TAG_NAME, body")
            is_text_present_in_body = text in body.text

            if is_text_present_in_body:
                self.context.logger.info(f"Body contains text {text}")
            else:
                self.context.logger.info(f"Body does not contains text {text}")
            return is_text_present_in_body
        except Exception as e:
            self.context.logger.error(
                f"Unable to check presence of text {text} on page. Error {e}"
            )

    def is_element_checked(
        self, locator, replacement=None, timeout=None
    ) -> bool:
        """
        Verify if element is checked.
        Args:
            - locator: element locator
            - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        try:
            is_element_checked = self.fetch_element(
                locator, element_timeout=timeout
            ).is_selected()
            self.context.logger.info(
                f"Checked status for element {locator} is"
                f"{str(is_element_checked)}"
            )
            return is_element_checked
        except Exception as e:
            self.context.logger.error(
                f"Unable to check checked status for element {locator}"
                f"Error: {e}"
            )
            return False

    def click(
        self, locator, replacement=None, click_using_java_script=False
    ) -> None:
        """
        Click on element.
        Args:
            - locator: locator on which to click
            - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
            - click_using_java_script: whether to click using java script
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        if click_using_java_script:
            _ele = self.fetch_element(locator)
            self.execute_java_script("arguments[0].click();", _ele)
            self.context.logger.info(
                f"Clicked on element {locator} using java script"
            )
        else:
            try:
                strategy = locator.split(",")[0].strip()
                actual_locator = locator.replace(f"{strategy},", "")
                timeout = int(
                    self.context.userdata.get("element_fetch_timeout", "")
                )

                WebDriverWait(self.context.driver, timeout).until(
                    EC.element_to_be_clickable(
                        (getattr(By, strategy), actual_locator)
                    )
                )

                _ele = self.fetch_element(locator)
                _ele.click()
                self.context.logger.info(f"Clicked on element {locator}")
            except Exception as e:
                self.context.logger.info(
                    f"Unable to click on element {locator}."
                    f"Error: {e}"
                    f"Trying to click using Action Chains."
                )
                try:
                    element = self.fetch_element(locator)

                    actions = ActionChains(self.context.driver)
                    actions.move_to_element(element)
                    actions.click(element)
                    actions.perform()

                    self.context.logger.info(
                        f"Action Chains - Clicked on element {locator}"
                    )
                except Exception as e:
                    self.context.logger.error(
                        f"Unable to click on element {locator}." f"Error: {e}",
                        exc_info=True,
                    )
                    Assert.assert_fail(f"Unable to click on element {locator}")

    def type(self, locator, text, replacement=None) -> None:
        """
        Type text in locator.
        Args:
             - locator: locator in which to type
             - text: text to type
             - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        try:
            _element = self.fetch_element(locator)
            _element.clear()
            _element.send_keys(text)
            self.context.info(f"Typed text {text} on element {locator}")
        except Exception as e:
            self.context.logger.error(
                f"Unable to type text {text} on element {locator}."
                f"Error: {e}",
                exc_info=True,
            )
            Assert.assert_fail(
                f"Unable to type text {text} on element {locator}"
            )

    def submit(self, locator, replacement=None) -> None:
        """
        Submit a form.
        Differentiates itself from click() when only perform on form button.
        Args:
            - locator: input submit button
            - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        try:
            _element = self.fetch_element(locator)
            _element.submit()
            self.context.logger.info(
                f"Submitted form clicking on element {locator}"
            )
        except Exception as e:
            self.context.logger.error(
                f"Unable to submit form clicking on element {locator}."
                f"Error: {e}"
            )
            Assert.assert_fail("Unable to submit form!")

    def get_text(self, locator, replacement=None) -> [str, None]:
        """
        Return text from locator.
        Args:
            - locator: locator from which to fetch text
            - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        try:
            element_text = self.fetch_element(locator).text
            self.context.logger.info(
                f"Get text returned {element_text} for element {locator}"
            )
            return element_text
        except Exception as e:
            self.context.logger.error(
                f"Unable to get text from element {locator}" f"Error: {e}",
                exc_info=True,
            )
            return None

    def check(self, locator, replacement=None) -> None:
        """
        Check element.
        Args:
            - locator: element locator
            - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        try:
            element = self.fetch_element(locator)
            if not element.is_selected():
                element.click()
                self.context.logger.info(
                    f"Checked checkbox having element {locator}"
                )
        except Exception as e:
            self.context.logger.error(
                f"Unable to check locator {locator}" f"Error: {e}",
                exc_info=True,
            )
            Assert.assert_fail(f"Unable to check locator {locator}")

    def uncheck(self, locator, replacement=None) -> None:
        """
        Uncheck element.
        Args:
            - locator: element locator
            - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        try:
            element = self.fetch_element(locator)
            if element.is_selected():
                element.click()
                self.context.logger.info(
                    f"Unchecked checkbox having element {locator}"
                )
        except Exception as e:
            self.context.logger.error(
                f"Unable to uncheck locator {locator}." f"Error: {e}",
                exc_info=True,
            )
            Assert.assert_fail(f"Unable to uncheck locator {locator}")

    def get_title(self) -> [str, None]:
        """
        Return browser title.
        """
        try:
            self.context.logger.info(
                f"Get title returned '{self.context.driver.title}'"
            )
            return self.context.driver.title
        except Exception as e:
            self.context.logger.error(
                "Unable to get browser title! Error: %s" % e, exc_info=True
            )
            return None

    def execute_java_script(self, script, element=None) -> None:
        """
        Execute raw java script statements.
        Args:
            - script: java script to execute
            - element: webdriver element on which to execute the java script
        """
        try:
            if element:
                return self.context.driver.execute_script(script, element)
            else:
                return self.context.driver.execute_script(script)
        except Exception as e:
            self.context.logger.error(
                f"Unable to execute java script {script}" f"Error: {e}",
                exc_info=True,
            )
            Assert.assert_fail(f"Unable to execute java script {script}")

    def select_by_visible_text(
        self,
        locator,
        option_text,
        replacement=None,
    ) -> None:
        """
        Select an option by visible option text.
        Args:
            - locator: locator of select element
            - option_text: option text by which to select the option
            - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
            - retry_by_browser_refresh: if set to True, when webdriver is not able to find any element,
            it will refresh the browser and try to find it again.
        """
        if replacement is not None:
            locator = locator.replace("$value", replacement)
        try:
            select = Select(self.fetch_element(locator))
            select.select_by_visible_text(option_text)

            self.context.logger.info(
                f"Selected element {locator} by visible text {option_text}"
            )
        except Exception as e:
            self.context.logger.error(
                f"Unable to select option {option_text}" f"Error: {e}",
                exc_info=True,
            )
            Assert.assert_fail(f"Unable to select option {option_text}")

    def press_key(self, locator, key, replacement=None) -> None:
        """
        Press keyboard key in locator.
        Args:
            - locator: locator in which to type
            - key: key to press
            - replacement: if locator contains dynamic part, i.e. '$value',
            it will be replaced by replacement variable
        """
        if replacement:
            locator = locator.replace("$value", replacement)
        try:
            self.fetch_element(locator).send_keys(key)
            self.context.logger.info(f"Pressed key {key} on element {locator}")
        except Exception as e:
            self.context.logger.error(
                f"Unable to press key {key} on element {locator}"
                f"Error: {e}",
                exc_info=True,
            )
            Assert.assert_fail(
                f"Unable to press key {key} on element {locator}"
            )
