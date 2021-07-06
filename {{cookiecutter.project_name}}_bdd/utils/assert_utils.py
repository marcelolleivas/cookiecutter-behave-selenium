from hamcrest import assert_that, contains_string, equal_to, none, not_none


class Assert(object):
    """
    Wrapper functions on top of hamcrest assertions
    """

    @staticmethod
    def assert_true(condition, message=None) -> None:
        """
        Assert a condition is True
        Args:
            - condition: condition to be checked
            - message: message to be displayed in case of assertion fails
        """
        assert_that(condition, equal_to(True), message)

    @staticmethod
    def assert_false(condition, message=None) -> None:
        """
        Assert a condition is False
        Args:
            - condition: condition to be checked
            - message: message to be displayed in case of assertion fails
        """
        assert_that(condition, equal_to(False), message)

    @staticmethod
    def assert_equals(actual, expected, message=None) -> None:
        """
        Assert expected and actual values match
        Args:
            - actual: actual result
            - expected: expected result
            - message: message to be displayed in case of assertion fails
        """
        assert_that(actual, equal_to(expected), message)

    @staticmethod
    def assert_contains(actual, expected, message=None) -> None:
        """
        Assert expected contains actual value
        Args:
            - actual: actual result
            - expected: expected result
            - message: message to be displayed in case of assertion fails
        """
        assert_that(actual, contains_string(expected), message)

    @staticmethod
    def assert_not_equals(actual, expected, message=None) -> None:
        """
        Assert expected and actual value do not match
        Args:
            - actual: actual result
            - expected: expected result
            - message: message to be displayed in case of assertion fails
        """
        assert_that(actual, not (equal_to(expected)), message)

    @staticmethod
    def assert_none(condition, message=None) -> None:
        """
        Assert condition is None
        Args:
            - condition: condition to be checked
            - message: message to be displayed in case of assertion fails
        """
        assert_that(condition, none(), message)

    @staticmethod
    def assert_not_none(condition, message=None) -> None:
        """
        Assert condition is NOT None
        Args:
            - condition: condition to be checked
            - message: message to be displayed in case of assertion fails
        """
        assert_that(condition, not_none(), message)

    @staticmethod
    def assert_fail(message=None) -> None:
        """
        Force fail scenario
        Args:
            - message: message to be displayed in case of assertion fails
        """
        assert_that(False, equal_to(True), message)
