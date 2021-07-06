import os
from json import load
from logging import config, getLogger
from os.path import isdir
from time import strftime

from {{cookiecutter.project_name}}_bdd.support.core.element_action import ElementAction
from {{cookiecutter.project_name}}_bdd.support.driver_factory import SeleniumDriverFactory
from {{cookiecutter.project_name}}_bdd.utils import constants


def before_all(context) -> None:
    """
    Set up test environment.
    Create driver based on the desired capabilities provided;
    Valid desired capabilities can be 'firefox' or 'chrome'.
    * For adding new drivers add a new static method in DriverFactory class.
    Args:
        - context: Holds contextual information during the running of tests
    """

    context.userdata = context.config.userdata

    context.logger = setup_logger()
    context.logger.info("\n")
    context.logger.info(
        "============================================================================================="
    )
    context.logger.info(
        f"TESTING STARTED AT : {strftime('%Y-%m-%d %H:%M:%S')}"
    )
    context.logger.info(
        "============================================================================================="
    )
    context.logger.info("\n")

    context.browser = context.userdata.get("application_url", "")

    # Get the appropriate driver for the browser specified in config file
    driver_factory = SeleniumDriverFactory(context)

    context.driver = driver_factory.get_driver()

    # Set driver implicit timeout. Webdriver will keep polling for the element for the specified timeout
    # period.
    timeout = int(context.userdata.get("implicit_timeout", ""))

    context.driver.implicitly_wait(timeout)
    context.logger.info(f"Driver implicit timeout is set to {str(timeout)}")

    context.application_url = str(context.userdata.get("application_url", ""))

    context.passed_scenarios = []
    context.failed_scenarios = []
    context.skipped_scenarios = []


def before_feature(context, feature) -> None:
    """
    Log starting of execution of feature
    Args:
        - context: Holds contextual information during the running of tests
        - feature: Holds contextual information about the feature during the running of tests
    """
    context.logger.info("\n")
    context.logger.info(
        "---------------------------------------------------------------------------------------------"
    )
    context.logger.info(f"STARTED EXECUTION OF FEATURE: {str(feature.name)}")
    context.logger.info(f"Tags: {str([str(item) for item in feature.tags])}")
    context.logger.info("Filename: " + str(feature.filename))
    context.logger.info(f"Line: {str(feature.line)}")
    context.logger.info(
        "---------------------------------------------------------------------------------------------"
    )

    context.driver.get(context.application_url)

    context.element_action = ElementAction(context)


def before_scenario(context, scenario) -> None:
    """
    Launch browser and open application
    Args:
        - context: Holds contextual information during the running of tests
        - scenario: Holds contextual information about scenario during the running of tests
    """
    context.logger.info("\n")
    context.logger.info(
        "---------------------------------------------------------------------------------------------"
    )
    context.logger.info(f"STARTED EXECUTION OF SCENARIO: {str(scenario.name)}")
    context.logger.info(f"Tags: {str([str(item) for item in scenario.tags])}")
    context.logger.info(f"Filename: {str(scenario.filename)}")
    context.logger.info(f"Line: {str(scenario.line)}")
    context.logger.info(
        "---------------------------------------------------------------------------------------------"
    )

    context.logger.info(f"Opening application url '{context.application_url}'")
    context.driver.get(context.application_url)
    context.driver.maximize_window()

    context.element_action = ElementAction(context)


def after_step(context, step) -> None:
    """
    Save screenshot in case of test step failure
    This function runs everytime after a step is executed. Check is step passed, then just log it and return
    if step fails and step is a part of portal scenario, take the screenshot of the failure. The screenshot file name
    is scenario_name.png where spaces within step name is replaced by '_'
    example: book_a_roundtrip_ticket_2016-12-01_12-34-32.png
    Args:
        - context: Holds contextual information during the running of tests
        - step: Holds contextual information about step during the running of tests
    """
    if step.status == "failed":
        context.logger.info(f"{step.name}: FAILED, Line: {str(step.line)}")

        try:
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")

            __current_scenario_name = context.scenario.name.split("--")[0]
            __screenshot_file_name = (
                f"screenshots{os.path.sep}{__current_scenario_name.replace(' ', '_')}-"
                f"{strftime('%Y-%m-%d_%H-%M-%S')}.png"
            )

            context.driver.save_screenshot(__screenshot_file_name)
            context.logger.info(
                f"Screenshot is captured in file '{__screenshot_file_name}'"
            )
        except Exception as e:
            context.logger.error(
                f"Unable to take screenshot!" f"Error: {e}", exc_info=True
            )

    else:
        context.logger.info(f"{step.name}: PASSED")


def after_scenario(context, scenario) -> None:
    """
    Close browser and quit driver
    Args:
        - context: Holds contextual information during the running of tests
        - scenario: Holds contextual information about scenario during the running of tests
    """

    context.logger.info("\n")
    context.logger.info(
        "---------------------------------------------------------------------------------------------"
    )
    context.logger.info(
        f"FINISHED EXECUTION OF SCENARIO: {str(scenario.name)}"
    )
    context.logger.info(f"Result: {scenario.status}")
    context.logger.info(
        f"Time taken: {str('{0:.2f}'.format(scenario.duration / 60))} mins, "
        f"{str('{0:.2f}'.format(scenario.duration % 60))} secs"
    )
    context.logger.info(
        "---------------------------------------------------------------------------------------------"
    )

    if context.driver is not None:
        try:
            context.driver.close()
        except Exception as e:
            context.logger.error(
                f"Unable to close browser window!" f"Error: {e}", exc_info=True
            )

        # try:
        #     context.driver.quit()
        # except Exception as e:
        #     context.logger.error(
        #         f"Unable to quit driver!" f"Error: {e}", exc_info=True
        #     )


def after_feature(context, feature):
    """
    Log finished execution of feature
    Args:
        - context: Holds contextual information during the running of tests
        - feature: Holds contextual information about feature during the running of tests
    """

    context.logger.info("\n")
    context.logger.info(
        "---------------------------------------------------------------------------------------------"
    )
    context.logger.info(f"FINISHED EXECUTION OF FEATURE: {str(feature.name)}")
    context.logger.info(f"Result: {feature.status}")
    context.logger.info(
        f"Time taken: {str('{0:.2f}'.format(feature.duration / 60))} mins, "
        f"{str('{0:.2f}'.format(feature.duration % 60))} secs"
    )
    context.logger.info(
        "---------------------------------------------------------------------------------------------"
    )


def after_all(context):
    """
    Log test finished
    Args:
        - context: Holds contextual information during the running of tests
    """

    context.logger.info("\n")
    context.logger.info(
        "============================================================================================="
    )
    context.logger.info(
        f"TESTING FINISHED AT : {strftime('%Y-%m-%d %H:%M:%S')}"
    )
    context.logger.info(
        "============================================================================================="
    )
    context.logger.info("\n")


def setup_logger():
    if not isdir(constants.LOG_FILE_DIR):
        os.makedirs(constants.LOG_FILE_DIR)

    with open(constants.LOGGER_CONFIG, "rt") as f:
        options = load(f)

    config.dictConfig(options)
    return getLogger(__name__)
