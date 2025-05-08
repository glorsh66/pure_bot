"""Automated web interaction script using Selenium and undetected-chromedriver.

This script automates clicking buttons on a webpage while handling dynamic content
and scrolling behavior. It uses undetected-chromedriver to avoid detection.
"""

import os
import time
import traceback
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc


# CSS class names
#Данные классы можно найти в инспекторе элементов в chrome dev tools
#Классы могут меняться, поэтому их нужно будет обновлять

EXCLUDED_BUTTON_CLASS = "bYXGwR" #Класс кнопки с нажатым лайком (для исключения)
LAST_DIV_CLASS = "sc-gYstsu"

# CSS selectors
BUTTON_SELECTOR = f"button:not(.{EXCLUDED_BUTTON_CLASS}):nth-child(3)" #кнопка для лайка
LAST_DIV_SELECTOR = f"div.{LAST_DIV_CLASS}:last-of-type" #див для просмотра следующей страницы


def setup_driver() -> uc.Chrome:
    """Initialize and configure the Chrome WebDriver.

    Returns:
        uc.Chrome: Configured Chrome WebDriver instance.
    """
    user_name = os.getenv('USERNAME')
    automation_profile = f"C:\\Users\\{user_name}\\AppData\\Local\\Chrome_Automation"

    options = uc.ChromeOptions()
    options.add_argument(f'--user-data-dir={automation_profile}')
    options.add_argument('--no-sandbox')

    return uc.Chrome(options=options, use_subprocess=True)


def click_buttons(driver: uc.Chrome, wait: WebDriverWait) -> None:
    """Find and click buttons on the page while handling scrolling.

    Args:
        driver: Chrome WebDriver instance
        wait: WebDriverWait instance for explicit waits
    """
    try:
        buttons = wait.until(EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, BUTTON_SELECTOR)
        ))
        print(f"Found buttons: {len(buttons)}")

        for i, button in enumerate(buttons[:-1]):
            if button.is_displayed():
                class_list = button.get_attribute("class").split()
                if EXCLUDED_BUTTON_CLASS not in class_list:
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", 
                        button
                    )
                    time.sleep(0.1)
                    ActionChains(driver).move_to_element(button).click().perform()
                    time.sleep(0.1)
                    print(f"Clicked button {i}")

        # Handle last button
        last_button = buttons[-1]
        driver.execute_script("arguments[0].scrollIntoView(true);", last_button)
        print("Scrolled to last button")

        # Handle last visible div
        try:
            last_visible_divs = wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, LAST_DIV_SELECTOR)
            ))
            last_visible_div = last_visible_divs[-1]
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", 
                last_visible_div
            )
            print("Scrolled to last div")
            time.sleep(0.1)
        except Exception as e:
            print(f"Error with div: {e}")
            print(traceback.format_exc())

        # Scroll page
        driver.execute_script("window.scrollBy(0, 500)")
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(0.1)
        print("Scrolled to new page")

    except Exception as e:
        print(f"An error occurred: {e}")
        print(traceback.format_exc())


def main():
    """Main execution function."""
    driver = setup_driver()
    driver.get("https://google.com")
    wait = WebDriverWait(driver, 3)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    print("Log to your google account")
    print("Then login to your pure account")   
    print("Press any key to start")    
    input()

    while True:
        click_buttons(driver, wait)


if __name__ == "__main__":
    main()
