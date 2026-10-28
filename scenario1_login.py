from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ==========================================
# SCENARIO 1: VALID LOGIN TEST
# ==========================================

# TEST DATA
EMAIL = "BSIT3C@gmail.com"
PASSWORD = "BSIT3C-QualityAssurance!"


# ==========================================
# STEP 1: CONFIGURE CHROME WINDOW
# ==========================================

options = webdriver.ChromeOptions()

# Open Chrome in a maximized window
options.add_argument("--start-maximized")

# Set browser zoom to 80%
options.add_argument("--force-device-scale-factor=0.8")

driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 60)

try:

    print("SCENARIO 1: VALID LOGIN TEST")
    print("-----------------------------------")

    # ======================================
    # STEP 2: OPEN THE WEBSITE
    # ======================================

    driver.get("https://sortrleaddistribution-client.onrender.com/")

    # Reset page zoom to 100%
    driver.execute_script("document.body.style.zoom='100%'")

    print("Website opened.")

    # ======================================
    # STEP 3: WAIT FOR EMAIL FIELD
    # ======================================

    email_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    )

    # ======================================
    # STEP 4: ENTER EMAIL
    # ======================================

    email_field.send_keys(EMAIL)

    print("Email entered.")

    # ======================================
    # STEP 5: FIND PASSWORD FIELD
    # ======================================

    password_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )

    # ======================================
    # STEP 6: ENTER PASSWORD
    # ======================================

    password_field.send_keys(PASSWORD)

    print("Password entered.")

    # ======================================
    # STEP 7: FIND LOGIN BUTTON
    # ======================================

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Log In']"))
    )

    # ======================================
    # STEP 8: CLICK LOGIN
    # ======================================

    login_button.click()

    print("Log In button clicked.")
    print("Waiting for Dashboard to load...")

    # ======================================
    # STEP 9: WAIT FOR DASHBOARD
    # ======================================

    dashboard = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    # ======================================
    # STEP 10: VERIFY RESULT
    # ======================================

    if dashboard.is_displayed():

        print()
        print("-----------------------------------")
        print("SCENARIO 1: TEST PASSED")
        print("User successfully logged in.")
        print("Dashboard is displayed.")
        print("-----------------------------------")

    else:

        print()
        print("-----------------------------------")
        print("TEST FAILED")
        print("Dashboard is not displayed.")
        print("-----------------------------------")

except TimeoutException:

    print()
    print("-----------------------------------")
    print("TEST FAILED")
    print("Dashboard did not load within 60 seconds.")
    print("-----------------------------------")

except Exception as error:

    print()
    print("-----------------------------------")
    print("TEST FAILED")
    print("An unexpected error occurred.")
    print(error)
    print("-----------------------------------")

finally:

    input("\nPress Enter to close the browser...")

    driver.quit()
