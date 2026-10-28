from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

# ==========================================
# SCENARIO 2: ADD A NEW LEAD
# ==========================================

# Replace with your test account credentials
EMAIL = "BSIT3C@gmail.com"
PASSWORD = "BSIT3C-QualityAssurance!"

# Use unique test data for each run
LEAD_NAME = "Soriano, Ivan D."
LEAD_TYPE = "Schools"
PHONE = "09123456789"
STREET = "131313 Test Street"
CITY = "San Fernando"
POSTCODE = "2000"
LEAD_EMAIL = "ivan@gmail.com"

# ==========================================
# STEP 1: OPEN CHROME
# ==========================================

driver = webdriver.Chrome()
driver.maximize_window()

wait = WebDriverWait(driver, 120)

try:
    print("SCENARIO 2: ADD A NEW LEAD")
    print("-----------------------------------")

    # ==========================================
    # STEP 2: OPEN THE WEBSITE
    # ==========================================

    driver.get("https://sortrleaddistribution-client.onrender.com/")
    print("Website opened.")

    # ==========================================
    # STEP 3: ENTER EMAIL
    # ==========================================

    email_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    )
    email_field.send_keys(EMAIL)
    print("Email entered.")

    # ==========================================
    # STEP 4: ENTER PASSWORD
    # ==========================================

    password_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )
    password_field.send_keys(PASSWORD)
    print("Password entered.")

    # ==========================================
    # STEP 5: CLICK LOG IN
    # ==========================================

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Log In']"))
    )
    login_button.click()
    print("Log In button clicked.")

    # ==========================================
    # STEP 6: WAIT FOR DASHBOARD
    # ==========================================

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )
    print("Login successful.")

    # ==========================================
    # STEP 7: OPEN ADD NEW LEAD
    # ==========================================

    add_lead_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Add New Lead']"))
    )
    add_lead_link.click()
    print("Add New Lead page opened.")

    # ==========================================
    # STEP 8: ENTER LEAD NAME
    # ==========================================

    name_field = wait.until(EC.visibility_of_element_located((By.NAME, "name")))
    name_field.send_keys(LEAD_NAME)
    print("Lead name entered.")

    # ==========================================
    # STEP 9: SELECT LEAD TYPE
    # ==========================================

    print(f"Selecting Lead Type: {LEAD_TYPE}...")

    # Locate the Material UI dropdown.
    type_dropdown = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[role="combobox"]'))
    )
    type_dropdown.click()

    print("Dropdown opened. Locating the requested option...")

    # Locate the exact option using its data-value.
    option_locator = (By.CSS_SELECTOR, f'li[role="option"][data-value="{LEAD_TYPE}"]')

    type_option = wait.until(EC.visibility_of_element_located(option_locator))

    # Scroll the option into the visible area of the dropdown.
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", type_option
    )

    # Wait briefly for the dropdown to finish scrolling,
    # then try a normal Selenium click first.
    try:
        wait.until(EC.element_to_be_clickable(option_locator)).click()

    except ElementClickInterceptedException:
        print("Option click was intercepted. " "Trying keyboard selection...")

        # Reopen the dropdown if it closed after the failed click.
        type_dropdown = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[role="combobox"]'))
        )
        type_dropdown.click()

        # Select the option through the dropdown keyboard.
        type_dropdown.send_keys(LEAD_TYPE)
        type_dropdown.send_keys(Keys.ENTER)

    # Verify that the selected value is Automotive.
    wait.until(
        lambda d: (
            LEAD_TYPE
            in [
                element.get_attribute("data-value")
                for element in d.find_elements(
                    By.CSS_SELECTOR, '[role="option"][aria-selected="true"]'
                )
            ]
            or LEAD_TYPE
            in [
                element.get_attribute("value")
                for element in d.find_elements(By.CSS_SELECTOR, '[role="combobox"]')
            ]
            or any(
                LEAD_TYPE in (element.text or "")
                for element in d.find_elements(By.CSS_SELECTOR, '[role="combobox"]')
            )
        )
    )

    print(f"[PASS] Lead type selected: {LEAD_TYPE}.")

    # ==========================================
    # STEP 10: ENTER PHONE NUMBER
    # ==========================================

    phone_field = wait.until(EC.visibility_of_element_located((By.NAME, "phonenumber")))
    phone_field.send_keys(PHONE)
    print("Phone number entered.")

    # ==========================================
    # STEP 11: ENTER STREET ADDRESS
    # ==========================================

    street_field = wait.until(
        EC.visibility_of_element_located((By.NAME, "streetaddress"))
    )
    street_field.send_keys(STREET)
    print("Street address entered.")

    # ==========================================
    # STEP 12: ENTER CITY
    # ==========================================

    city_field = wait.until(EC.visibility_of_element_located((By.NAME, "city")))
    city_field.send_keys(CITY)
    print("City entered.")

    # ==========================================
    # STEP 13: ENTER POSTCODE
    # ==========================================

    postcode_field = wait.until(EC.visibility_of_element_located((By.NAME, "postcode")))
    postcode_field.send_keys(POSTCODE)
    print("Postcode entered.")

    # ==========================================
    # STEP 14: ENTER LEAD EMAIL
    # ==========================================

    lead_email_field = wait.until(
        EC.visibility_of_element_located((By.NAME, "emailaddress"))
    )
    lead_email_field.send_keys(LEAD_EMAIL)
    print("Lead email entered.")

    print("Lead form completed.")

    # ==========================================
    # STEP 15: SUBMIT THE FORM
    # ==========================================

    submit_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
    )
    submit_button.click()
    print("Submit button clicked.")

    # ==========================================
    # STEP 16: VERIFY SUCCESS MESSAGE
    # ==========================================

    print("Waiting for success message...")

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='New lead added!']")
        )
    )

    print("-----------------------------------")
    print("SCENARIO 2: TEST PASSED")
    print("Success message: New lead added!")
    print(f"Lead created: {LEAD_NAME}")
    print("-----------------------------------")

    # ==========================================
    # STEP 17: WAIT FOR SUCCESS POPUP TO CLOSE
    # ==========================================

    print("Waiting for success popup to close...")

    wait.until(
        EC.invisibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='New lead added!']")
        )
    )

    wait.until(
        EC.invisibility_of_element_located((By.CSS_SELECTOR, ".MuiBackdrop-root"))
    )

    print("Success popup closed.")

    # ==========================================
    # STEP 18: OPEN THE LEADS PAGE
    # ==========================================

    print("Opening Leads page...")

    leads_link = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[contains(@class,'ps-menuitem-root')]"
                "[.//*[normalize-space()='Leads']]",
            )
        )
    )
    leads_link.click()
    print("Leads page opened.")

    # ==========================================
    # STEP 19: VERIFY THE CREATED LEAD
    # ==========================================

    print("Searching for the new lead...")

    created_lead = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[normalize-space()='{LEAD_NAME}']")
        )
    )

    if created_lead.is_displayed():
        print("-----------------------------------")
        print("DATABASE RECORD CHECK: PASSED")
        print(f"Verified lead: {LEAD_NAME}")
        print("The lead is visible on the Leads page.")
        print("-----------------------------------")

except TimeoutException:
    print("-----------------------------------")
    print("SCENARIO 2: TEST FAILED")
    print("A required element did not appear in time.")
    print("Check the last progress message above.")
    print("Current URL:", driver.current_url)
    print("-----------------------------------")

except Exception as error:
    print("-----------------------------------")
    print("SCENARIO 2: TEST FAILED")
    print("An unexpected error occurred:")
    print(error)
    print("-----------------------------------")

finally:
    input("\nPress Enter to close the browser...")
    driver.quit()
