import random
import string

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Utils:
    """
    Utility class for commonly used functions
    """

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def is_success_message_shown(self, message) -> bool:
        """
        Check message is shown
        :param message: Message
        :return: True/False based on message is shown or not
        """
        message_element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".notice.success")))
        return message_element.text == message and message_element.is_displayed()

    def generate_random_string(self, length=8, digits=False) -> str:
        """
        Generate random digits or letters string with provided length
        :param length: string length
        :param digits: If true generates digits sequence otherwise letters
        :return: string
        """
        letters = string.ascii_letters if not digits else string.digits
        return ''.join(random.choice(letters) for i in range(length))

    def wait_for_page_with_title(self, page_title) -> bool:
        """
        Wait for page with title
        :param page_title: Page title
        :return: True/False based on page with title was opened or not
        """
        title = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
        return page_title == title.text
