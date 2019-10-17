import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select


@pytest.mark.usefixtures("login")
class TestNewWindow:
    """
    Test suite for the new window opens
    """

    class there_is_window_other_than(object):
        def __init__(self, old_windows):
            self.old_windows = old_windows

        def __call__(self, driver):
            window_handles = driver.window_handles
            new_window_list = [window_handle for window_handle in window_handles if window_handle not in self.old_windows]
            if len(new_window_list) > 0:
                return new_window_list[0]
            else:
                return None

    def test_new_window_opens(self):
        print("1. Open Countries page")
        self.driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
        print("2. Wait for Countries page")
        assert self.utils.wait_for_page_with_title("Countries"), "Page with title 'Countries' is not open"
        print("3. Open first country in list")
        country = self.driver.find_element_by_css_selector("table.dataTable tr.row td:nth-child(5) a")
        country_name = country.text
        country.click()
        print("4. Wait for Edit Country page")
        assert self.utils.wait_for_page_with_title("Edit Country"), "Page with title 'Edit Country' is not open"
        assert self.driver.find_element_by_css_selector("input[name=name]").get_attribute("value") == country_name, "Incorrect page is open"
        print("5. Get all links on the page")
        links = self.driver.find_elements_by_css_selector("form a[target=_blank]")
        edit_page_id = self.driver.current_window_handle
        old_windows = self.driver.window_handles
        for link in links:
            print("Open new window")
            link.click()
            new_window = self.wait.until(self.there_is_window_other_than(old_windows))
            print("Switch to new window")
            self.driver.switch_to.window(new_window)
            assert self.driver.current_window_handle == new_window, "Impossible to switch to new window"
            print("New window title: {}".format(self.driver.title))
            print("Close new window")
            self.driver.close()
            print("Switch to Edit Country window")
            self.driver.switch_to.window(edit_page_id)