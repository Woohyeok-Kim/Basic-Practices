import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Automatically install the compatible version of ChromeDriver
chromedriver_autoinstaller.install()

# Setup the WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--start-maximized')  # Open the browser in maximized mode
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

# Access the website
url = 'https://www.when2meet.com/?25795446-ss8Wd'  # Replace with your target website
driver.get(url)

# Define the element ID
element_id = 'GroupTime1722474000'

# Find the element
print("now I'm starting to search")
element = driver.find_element(By.ID, element_id)

# Create an ActionChain to move the cursor to the element
actions = ActionChains(driver)
actions.move_to_element(element).perform()

# Find the input element by ID and type a name
input_element = driver.find_element(By.ID, 'name')
input_element.send_keys('김우혁')


# Wait for a moment to ensure the page has loaded the button
time.sleep(1)

print('just typed')
# Find the button element by its value attribute and click it
sign_in_button = driver.find_element(By.XPATH, '//input[@type="button" and @value="Sign In"]')
sign_in_button.click()
print('I signed in')

# Optional: Wait for a while to observe the result of the click
time.sleep(5)

input('Press Enter to close the browser..')

# # Pause for a moment to see the effect
# time.sleep(3)  # Adjust the sleep time as needed

# # Optionally, take a screenshot to verify the interaction
# driver.save_screenshot('whentomeet_test.png')

