from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ==========================================
# SCENARIO 4: CLICK THE CALL BUTTON (MICROSIP)
# ==========================================

# TEST ACCOUNT CREDENTIALS
EMAIL = "BSIT3C@gmail.com"
PASSWORD = "BSIT3C-QualityAssurance!"

# TEST DATA
LEAD_NAME = "Soriano, Ivan D."
LEAD_PHONE = "09123456789"

# ==========================================
# STEP 1: CONFIGURE CHROME
# ==========================================

options = webdriver.ChromeOptions()

# Open Chrome maximized
options.add_argument("--start-maximized")

# Use normal display scaling
options.add_argument("--force-device-scale-factor=1")

driver = webdriver.Chrome(options=options)

# Wait up to 60 seconds for elements to appear
wait = WebDriverWait(driver, 60)


try:

    print()
    print("==========================================")
    print("SCENARIO 4: CLICK THE CALL BUTTON (MICROSIP)")
    print("==========================================")

    # ==========================================
    # STEP 2: OPEN APPLICATION
    # ==========================================

    print("\nStep 1: Opening application...")

    driver.get("https://sortrleaddistribution-client.onrender.com/")

    print("Application opened successfully.")

    # ==========================================
    # STEP 3: ENTER LOGIN CREDENTIALS
    # ==========================================

    print("\nStep 2: Logging in...")

    email_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    )

    email_field.send_keys(EMAIL)
    print("Email entered.")

    password_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )

    password_field.send_keys(PASSWORD)
    print("Password entered.")

    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Log In']"))
    )

    login_button.click()
    print("Login button clicked.")

    # ==========================================
    # STEP 4: VERIFY SUCCESSFUL LOGIN
    # ==========================================

    print("\nStep 3: Waiting for Dashboard...")

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    print("------------------------------------------")
    print("TEST PASSED: Login successful.")
    print("Dashboard is displayed.")
    print("------------------------------------------")

    # ==========================================
    # STEP 5: OPEN LEADS PAGE
    # ==========================================

    print("\nStep 4: Opening Leads page...")

    leads_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Leads']"))
    )

    leads_link.click()

    wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                "//*[normalize-space()='ASSIGNED LEADS' "
                "or normalize-space()='LEADS']",
            )
        )
    )

    print("Leads page opened successfully.")

    # ==========================================
    # STEP 6: SEARCH FOR THE TARGET LEAD
    # ==========================================

    print("\nStep 5: Searching for target lead...")
    print(f"Target lead: {LEAD_NAME}")

    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Search"]')
        )
    )

    search_box.clear()
    search_box.send_keys(LEAD_NAME)

    print("Search term entered.")

    # ==========================================
    # STEP 7: VERIFY THE TARGET LEAD
    # ==========================================

    print("\nStep 6: Verifying target lead...")

    target_row = wait.until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                f"//*[@role='row']"
                f"[.//*[@title='{LEAD_NAME}' "
                f"or normalize-space()='{LEAD_NAME}']]",
            )
        )
    )

    if target_row.is_displayed():
        print("------------------------------------------")
        print("TEST PASSED: Target lead found.")
        print(f"Lead name: {LEAD_NAME}")
        print("------------------------------------------")

    # ==========================================
    # STEP 8: LOCATE MICROSIP CALL LINK
    # ==========================================

    print("\nStep 7: Locating MicroSIP call link...")

    call_link = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'a[aria-label="Call lead with MicroSIP"]')
        )
    )

    call_href = call_link.get_attribute("href")

    print("Call link located.")
    print("Call link:", call_href)

    # ==========================================
    # STEP 9: VERIFY THE PHONE NUMBER
    # ==========================================

    print("\nStep 8: Verifying target phone number...")

    normalized_phone = LEAD_PHONE.replace(" ", "").replace("-", "")

    normalized_href = call_href.replace(" ", "").replace("-", "") if call_href else ""

    # Confirm the link uses the callto protocol
    if not normalized_href.startswith("callto:"):
        raise Exception("The call link does not use the callto protocol.")

    # Confirm the link matches the expected phone number
    if normalized_phone not in normalized_href:
        raise Exception(
            "The call link does not match the target phone number. "
            "The call was not initiated."
        )

    print("TEST PASSED: Phone number verified.")
    print(f"Target phone number: {LEAD_PHONE}")

    # ==========================================
    # STEP 10: SCROLL CALL LINK INTO VIEW
    # ==========================================

    print("\nStep 9: Scrolling call link into view...")

    driver.execute_script(
        "arguments[0].scrollIntoView(" "{block: 'center', inline: 'center'});",
        call_link,
    )

    print("Call link is ready to be clicked.")

    # ==========================================
    # STEP 11: CLICK MICROSIP CALL LINK
    # ==========================================

    print("\nStep 10: Clicking MicroSIP call link...")

    call_link.click()

    # ==========================================
    # STEP 12: DISPLAY FINAL TEST RESULT
    # ==========================================

    print()
    print("==========================================")
    print("SCENARIO 4: TEST PASSED")
    print("------------------------------------------")
    print("Login successful.")
    print("Target lead found.")
    print("Phone number verified.")
    print("MicroSIP call link clicked.")
    print("Verify that MicroSIP opens with the intended number.")
    print("==========================================")


except TimeoutException:

    print()
    print("==========================================")
    print("SCENARIO 4: TEST FAILED")
    print("------------------------------------------")
    print("A required element did not appear in time.")
    print("Current URL:", driver.current_url)
    print("Check the last printed step for the failure.")
    print("==========================================")


except Exception as error:

    print()
    print("==========================================")
    print("SCENARIO 4: TEST FAILED")
    print("------------------------------------------")
    print("Error type:", type(error).__name__)
    print("Error details:", error)
    print("==========================================")


finally:

    input("\nPress Enter to close the browser...")

    driver.quit()
