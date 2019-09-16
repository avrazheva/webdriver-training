import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def setup_test(request):
    print("SetUp")
    driver = webdriver.Chrome()
    request.cls.driver = driver
    yield
    print("TearDown")
    driver.close()
