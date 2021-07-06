from abc import ABC, abstractmethod

from {{cookiecutter.project_name}}_bdd.support.core.element_action import ElementAction
from {{cookiecutter.project_name}}_bdd.support.locators import base_page as base_page_locators


class BasePage(ABC):
    """
    All page classes must extend this class in order to use the webdriver actions.
    It contains actions to elements that all page classes shares too.
    """

    def __init__(self, context):
        self.context = context
        self.element_action = ElementAction(context)

    @abstractmethod
    def page_is_displayed(self):
        """
        Verifies an unique element is appearing on the screen
        """
        ...

    @abstractmethod
    def path_switcher(self):
        """
        Actions that the application will perform to navigate to the next pages
        """
        ...
