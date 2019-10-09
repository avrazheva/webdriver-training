import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

@pytest.mark.usefixtures("login")
class TestSorting:
    """
    Test suite for the http://localhost/litecart/admin/?app=countries&doc=countries page
    """

    def check_list_sorting(self, list) -> bool:
        """
        Check that list is in alphabetic order
        :param list: list
        :return: True/False based on list is in alphabetic order or not
        """
        previous_item = list[0]
        for item in list[1:]:
            if item[0] < previous_item[0]:
                return False
            previous_item = item
        return True

    def wait_for_page_with_title(self, page_title) -> bool:
        """
        Wait for page with title
        :param page_title: Page title
        :return: True/False based on page with title was opened or not
        """
        title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        return page_title == title.text

    def test_countries_sorting(self):
        print("1. Open Countries page")
        self.driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
        print("2. Wait for Countries page")
        assert self.wait_for_page_with_title("Countries"), "Page with title 'Countries' is not open"
        print("3. Get All Countries Names")
        country_names = self.driver.find_elements_by_css_selector("table.dataTable tr.row td:nth-child(5) a")
        names = [country_name.text for country_name in country_names]
        print("4. Check Country Names Sorting")
        assert self.check_list_sorting(names), "Countries names is not in alphabetic order."
        print("5. Check Country Zones Sorting")
        zones_column_elements = self.driver.find_elements_by_css_selector("tr.row td:nth-child(6)")
        non_empty_zones_indexes = [zones_column_elements.index(zone_column_element) for zone_column_element in zones_column_elements if int(zone_column_element.text) != 0]
        for index in non_empty_zones_indexes:
            country_name = self.driver.find_elements_by_css_selector("table.dataTable tr.row td:nth-child(5) a")[index]
            country_name_text = country_name.text
            print("Select Country Name '{}' to check zones".format(country_name_text))
            country_name.click()
            print("Wait for 'Edit Country' page")
            assert self.wait_for_page_with_title("Edit Country"), "Current page is not Edit Country"
            assert self.driver.find_element_by_css_selector("input[name=name]").get_attribute("value") == country_name_text, \
                "Current Edit Country page is not for '{}'".format(country_name_text)
            print("Get all zones name")
            zones_names_elements = self.driver.find_elements_by_xpath("//table[@class='dataTable']//td[3][input/@type='hidden']")
            zones_names = [zone_name.text for zone_name in zones_names_elements]
            print("Check zones sorting")
            assert self.check_list_sorting(zones_names), "Zones is not in alphabetic order"
            print("Return to 'Countries' page")
            self.driver.back()
            assert self.wait_for_page_with_title("Countries"), "Page with title 'Countries' is not open"

    def test_geo_zones_sorting(self):
        print("1. Open Geo Zones page")
        self.driver.get("http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones")
        print("2. Wait for Geo Zones page")
        assert self.wait_for_page_with_title("Geo Zones"), "Page with title 'Geo Zones' is not open"
        print("3. Get All Geo Zones")
        table_line_count = self.driver.find_elements_by_css_selector("table.dataTable tr.row")
        for index in range(len(table_line_count)):
            geo_zone = self.driver.find_elements_by_css_selector("table.dataTable tr.row td:nth-child(3) a")[index]
            geo_zone_text = geo_zone.text
            print("Select '{}' geo zone".format(geo_zone_text))
            geo_zone.click()
            assert self.wait_for_page_with_title("Edit Geo Zone"), "Page with title 'Edit Geo Zone' is not open"
            assert self.driver.find_element_by_css_selector("input[name=name]").get_attribute("value") ==  geo_zone_text
            print("Check Zones sorting")
            zones_drop_down = self.driver.find_elements_by_css_selector("select[name*=zone_code]")
            zones_names = [Select(zones_drop_down[zone_drop_down_id]).first_selected_option.text for zone_drop_down_id in range(len(zones_drop_down))]
            assert self.check_list_sorting(zones_names), "Country Zones are not in alphabetic order"
            print("Return to 'Countries' page")
            self.driver.back()
            assert self.wait_for_page_with_title("Geo Zones"), "Page with title 'Geo Zones' is not open"
