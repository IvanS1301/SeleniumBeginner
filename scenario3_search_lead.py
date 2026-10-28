from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# ==========================================
# SCENARIO 3: SEARCH AND VERIFY A LEAD
# ==========================================

# Test data: Use a lead created in Scenario 2
LEAD_NAME = "Soriano, Ivan D."

# Replace these with your demo account credentials
EMAIL = "BSIT3C@gmail.com"
PASSWORD = "BSIT3C-QualityAssurance!"


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 60)

try:
    # STEP 1: Open the application
    driver.get("https://sortrleaddistribution-client.onrender.com/")

    driver.maximize_window()

    # STEP 2: Enter login credentials
    email_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    )
    email_field.send_keys(EMAIL)

    password_field = wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )
    password_field.send_keys(PASSWORD)

    # STEP 3: Click the Log In button
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Log In']"))
    )
    login_button.click()

    # STEP 4: Wait for the dashboard to load
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    print("Login successful.")

    # STEP 5: Open the Leads page
    leads_link = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[contains(@class,'ps-menuitem-root')"
                "][.//*[normalize-space()='Leads']]",
            )
        )
    )
    leads_link.click()

    # STEP 6: Wait for the Leads page heading
    wait.until(
        EC.visibility_of_element_located((By.XPATH, "//*[normalize-space()='LEADS']"))
    )

    print("Leads page opened.")

    # STEP 7: Find the Search input
    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Search"]')
        )
    )

    # STEP 8: Search for the existing lead
    search_box.clear()
    search_box.send_keys(LEAD_NAME)

    # STEP 9: Verify that the lead appears in the results
    matching_lead = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//*[normalize-space()='{LEAD_NAME}']")
        )
    )

    print("-----------------------------------")
    print("SCENARIO 3: TEST PASSED - Lead found!")
    print("Lead name:", matching_lead.text)
    print("The search returned the expected lead.")
    print("-----------------------------------")

except TimeoutException:
    print("-----------------------------------")
    print("TEST FAILED: Expected element not found.")
    print(
        "Check the login, page loading, search field, " "and whether the lead exists."
    )
    print("-----------------------------------")

except Exception as error:
    print("An unexpected error occurred:")
    print(error)

finally:
    input("\nPress Enter to close the browser...")
    driver.quit()
