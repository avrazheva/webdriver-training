import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utils import Utils

CREDENTIALS = "admin"


@pytest.fixture(scope="function")
def setup_test(request):
    print("SetUp")
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    # driver = webdriver.Firefox()
    request.cls.driver = driver
    request.cls.wait = wait
    request.cls.utils = Utils(driver, wait)
    yield
    print("TearDown")
    driver.close()


@pytest.fixture(scope="function")
def login(request):
    print("Login As Admin")
    driver = webdriver.Chrome()
    # driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)
    driver.get("http://localhost/litecart/admin/")
    username = driver.find_element_by_name("username")
    username.clear()
    username.send_keys(CREDENTIALS)
    password = driver.find_element_by_name("password")
    password.clear()
    password.send_keys(CREDENTIALS)
    driver.find_element_by_name("login").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "widget-sales")))
    request.cls.driver = driver
    request.cls.wait = wait
    request.cls.utils = Utils(driver, wait)
    yield
    print("TearDown")
    driver.close()
