import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


@pytest.fixture(scope="function")
def setup_test(request):
    print("SetUp")
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    # driver = webdriver.Firefox()
    request.cls.driver = driver
    request.cls.wait = wait
    yield
    print("TearDown")
    driver.close()
