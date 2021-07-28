from decouple import config
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(
    "https://www.amazon.co.uk/cart/localmarket?ref_=cart_go_cart_btn_fresh&almBrandId=QW1hem9uIEZyZXNo"
)
EMAIL = config("EMAIL")
PASS = config("PASS")

try:
    # Close pop-ups to access sign in button
    close_pop_ups = (
        WebDriverWait(driver, 40)
        .until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//*[@id="nav-main"]/div[1]/div/div/div[3]/span[1]/span/input',
                )
            )
        )
        .click()
    )
    sign_in_button = driver.find_element_by_xpath('//*[@id="a-autoid-2-announce"]')
    sign_in_button.click()

except:
    # Alternative Selector/s to be added for bug where the pop-up closes but sign-in button times out
    driver.quit()

email_input = driver.find_element_by_id("ap_email")

email_input.send_keys(EMAIL)

input_button = driver.find_element_by_class_name("a-button-input")
input_button.click()

pass_input = driver.find_element_by_id("ap_password")
pass_input.send_keys(PASS)

# Driver waits for DOM to settle before clicking sign in
delayed_input_button = (
    WebDriverWait(driver, 20)
    .until(EC.element_to_be_clickable((By.XPATH, '//*[@id="auth-signin-button"]')))
    .click()
)

try:
    go_to_basket = (
        WebDriverWait(driver, 20)
        .until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="rcx-alm-QW1hem9uIEZyZXNo-full-cart-link"]')
            )
        )
        .click()
    )
except:
    driver.quit()
    # Alternative Selector/s to be added for different version of landing page
    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="a-autoid-1-announce"]'))).click()


basket = driver.find_element_by_xpath(
    '//*[@id="sc-expanded-cart-localmarket"]/div[2]/div/div[2]/div/div[2]/div/div[2]'
)
# Basket will be iterated over to delete each item by index
print(basket.get_attribute("innerHTML"))

# for i in len(basket):
#     driver.find_element_by_value("Delete").click()
#     # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.VALUE, 'Delete'))).click()

# driver.quit()
