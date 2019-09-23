import pytest
from selenium import webdriver


@pytest.mark.usefixtures("setup_test")
class TestSecondLesson:
    """
    Test suite for the second lesson
    """

    @pytest.fixture(scope="function")
    def setup_test(cls):
        print("SetUp")
        cls.driver = webdriver.Chrome()
        yield
        print("TearDown")
        cls.driver.close()

    def test_second_lesson(self):
        self.driver.get("https://software-testing.ru/")
