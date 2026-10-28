from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
)
import re

# ==========================================
# SCENARIO 5: SEND AN EMAIL
# ==========================================

# TEST ACCOUNT CREDENTIALS
EMAIL = "YOUR_TEST_EMAIL"
PASSWORD = "YOUR_TEST_PASSWORD"

# TEST DATA
LEAD_NAME = "Bean & Leaf Coffee"
EXPECTED_RECIPIENT = "contact056@business056.example"

SUBJECT_TEMPLATE = (
    "Congratulations! You're Eligible for a Free Hot Water System Upgrade"
)

WEBSITE = "https://sortrleaddistribution-client.onrender.com/"

# ==========================================
# STEP 1: CONFIGURE CHROME
# ==========================================

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--force-device-scale-factor=1")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 60)
short_wait = WebDriverWait(driver, 10)

try:
    print()
    print("==========================================")
    print("SCENARIO 5: SEND AN EMAIL")
    print("==========================================")

    # ==========================================
    # STEP 2: OPEN APPLICATION
    # ==========================================

    print("\nStep 1: Opening application...")
    driver.get(WEBSITE)

    # ==========================================
    # STEP 3: LOG IN
    # ==========================================

    print("\nStep 2: Logging in...")

    wait.until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
    ).send_keys(EMAIL)

    driver.find_element(By.CSS_SELECTOR, 'input[type="password"]').send_keys(PASSWORD)

    driver.find_element(By.XPATH, "//button[normalize-space()='Log In']").click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='DASHBOARD']")
        )
    )

    print("TEST PASSED: Login successful.")

    # ==========================================
    # STEP 4: OPEN LEADS PAGE
    # ==========================================

    print("\nStep 3: Opening Leads page...")

    leads_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Leads']"))
    )

    leads_link.click()

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='ASSIGNED LEADS']")
        )
    )

    print("Leads page opened.")

    # ==========================================
    # STEP 5: SEARCH FOR TARGET LEAD
    # ==========================================

    print("\nStep 4: Searching for target lead...")

    search_box = wait.until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, 'input[placeholder="Search"]')
        )
    )

    search_box.clear()
    search_box.send_keys(LEAD_NAME)

    target_row_xpath = "//*[@role='row' and " f".//*[normalize-space()='{LEAD_NAME}']]"

    target_row = wait.until(
        EC.visibility_of_element_located((By.XPATH, target_row_xpath))
    )

    print("TEST PASSED: Target lead found.")

    # ==========================================
    # STEP 6: VERIFY RECIPIENT
    # ==========================================

    print("\nStep 5: Verifying recipient...")

    if EXPECTED_RECIPIENT.lower() not in target_row.text.lower():
        raise Exception(
            "Expected recipient was not found in the target lead row. "
            "Email was not sent."
        )

    print("Recipient verified:", EXPECTED_RECIPIENT)

    # ==========================================
    # STEP 7: LOCATE EMAIL ICON
    # ==========================================

    print("\nStep 6: Locating email icon...")

    email_button = None

    # First, try finding the icon inside the target row.
    try:
        icon = target_row.find_element(
            By.CSS_SELECTOR, 'svg[data-testid="AttachEmailIcon"]'
        )

        email_button = icon.find_element(By.XPATH, "./ancestor::button[1]")

    except Exception:
        print("Icon not found inside the target row.")
        print("Searching all email icons on the page...")

    # Fallback: search globally and identify the action
    # associated with the expected recipient.
    if email_button is None:
        icons = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'svg[data-testid="AttachEmailIcon"]')
            )
        )

        print("Email icons found:", len(icons))

        for icon in icons:
            try:
                candidate = icon.find_element(By.XPATH, "./ancestor::button[1]")
            except Exception:
                try:
                    candidate = icon.find_element(By.XPATH, "./ancestor::a[1]")
                except Exception:
                    continue

            surrounding_html = driver.execute_script(
                """
                let element = arguments[0];
                const recipient = arguments[1];

                for (let i = 0; i < 10 && element; i++) {
                    if (
                        (element.innerText || "").includes(recipient)
                    ) {
                        return element.outerHTML;
                    }

                    element = element.parentElement;
                }

                return "";
                """,
                candidate,
                EXPECTED_RECIPIENT,
            )

            if surrounding_html:
                email_button = candidate
                break

        if email_button is None:
            raise Exception(
                "Could not safely identify the email action " "for the target lead."
            )

    # ==========================================
    # STEP 8: CLICK EMAIL ICON
    # ==========================================

    print("\nStep 7: Clicking email icon...")

    driver.execute_script(
        "arguments[0].scrollIntoView(" "{block: 'center', inline: 'center'});",
        email_button,
    )

    wait.until(lambda d: email_button.is_displayed() and email_button.is_enabled())

    try:
        email_button.click()

    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", email_button)

    print("Email icon clicked.")

    # ==========================================
    # STEP 9: WAIT FOR EMAIL MODAL
    # ==========================================

    print("\nStep 8: Waiting for email modal...")

    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[normalize-space()='Send An Email']")
        )
    )

    print("Email modal opened.")

    # ==========================================
    # STEP 10: VERIFY MODAL RECIPIENT
    # ==========================================

    print("\nStep 9: Verifying modal recipient...")

    recipient_field_xpath = f"//input[@value='{EXPECTED_RECIPIENT}']"

    recipient_field = wait.until(
        EC.visibility_of_element_located((By.XPATH, recipient_field_xpath))
    )

    if recipient_field.get_attribute("value") != EXPECTED_RECIPIENT:
        raise Exception("Recipient mismatch. Email was not sent.")

    print("TEST PASSED: Modal recipient verified.")

    # ==========================================
    # STEP 11: SELECT SUBJECT TEMPLATE
    # ==========================================

    print("\nStep 10: Selecting subject template...")

    subject_dropdown = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//*[normalize-space()='Subject']"
                "/ancestor::div[contains(@class,'MuiFormControl-root')]"
                "//*[self::div or self::input]"
                "[@role='combobox' or @aria-haspopup='listbox']",
            )
        )
    )

    subject_dropdown.click()

    print("Subject dropdown opened.")

    # Handle the apostrophe in "You're" safely.
    subject_option_xpath = (
        "//*[@role='option' and normalize-space(.)="
        "concat('Congratulations! You', \"'\", "
        "'re Eligible for a Free Hot Water System Upgrade')]"
    )

    subject_option = wait.until(
        EC.element_to_be_clickable((By.XPATH, subject_option_xpath))
    )

    subject_option.click()

    print("Subject template selected.")

    # ==========================================
    # STEP 12: WAIT FOR TEMPLATE TEXT
    # ==========================================

    print("\nStep 11: Waiting for template text...")

    text_area_xpath = "//textarea[@name='text']"

    text_area = wait.until(
        EC.visibility_of_element_located((By.XPATH, text_area_xpath))
    )

    wait.until(
        lambda d: bool(
            d.find_element(By.XPATH, text_area_xpath).get_attribute("value").strip()
        )
    )

    message_text = text_area.get_attribute("value")

    print("TEST PASSED: Template text populated.")
    print("Message characters:", len(message_text))

    # ==========================================
    # STEP 13: DEFINE PLACEHOLDER VALUES
    # ==========================================

    print("\nStep 12: Preparing placeholder replacements...")

    # Replace these example values with approved information.
    PLACEHOLDER_VALUES = {
        "[Customer's Name]": "Alex Johnson",
        "[Your Contact Information]": "1300 000 000",
        "[Your Website URL]": "https://example.com",
        "[Telemarketer Name]": "Jordan Smith",
    }

    # ==========================================
    # STEP 14: EDIT TEMPLATE PLACEHOLDERS
    # ==========================================

    print("\nStep 13: Editing email placeholders...")

    for placeholder, replacement in PLACEHOLDER_VALUES.items():

        if placeholder not in message_text:
            raise Exception(f"Expected placeholder not found: {placeholder}")

        message_text = message_text.replace(placeholder, replacement)

        print(f"Replaced {placeholder}")

    # ==========================================
    # STEP 15: UPDATE EMAIL MESSAGE
    # ==========================================

    print("\nStep 14: Updating email message...")

    text_area = wait.until(
        EC.visibility_of_element_located((By.XPATH, text_area_xpath))
    )

    # Select and replace the entire textarea content.
    text_area.click()
    text_area.send_keys(Keys.CONTROL, "a")
    text_area.send_keys(Keys.BACKSPACE)
    text_area.send_keys(message_text)

    # Read the actual value back from the form.
    updated_message = text_area.get_attribute("value") or ""

    print("\nUpdated email message:")
    print("------------------------------------------")
    print(updated_message)
    print("------------------------------------------")

    # ==========================================
    # STEP 16: VERIFY PLACEHOLDERS
    # ==========================================

    print("\nStep 15: Checking remaining placeholders...")

    remaining_placeholders = re.findall(r"\[[^\]]+\]", updated_message)

    if remaining_placeholders:
        raise Exception(
            "Unedited placeholders remain: "
            + ", ".join(remaining_placeholders)
            + ". Email was NOT sent."
        )

    print("TEST PASSED: No square-bracket placeholders remain.")

    # ==========================================
    # STEP 17: LOCATE SEND BUTTON
    # ==========================================

    print("\nStep 16: Locating Send button...")

    # Actual HTML uses type="submit" and visible text "Send".
    send_button_xpath = "//button[@type='submit' and normalize-space()='Send']"

    send_button = short_wait.until(
        EC.presence_of_element_located((By.XPATH, send_button_xpath))
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", send_button
    )

    if not send_button.is_enabled():
        raise Exception("Send button is disabled. Email was not sent.")

    print("TEST PASSED: Send button located and enabled.")

    # ==========================================
    # STEP 18: FINAL SAFETY CHECKS
    # ==========================================

    print("\nStep 17: Performing final checks...")

    recipient_field = driver.find_element(By.XPATH, recipient_field_xpath)

    text_area = driver.find_element(By.XPATH, text_area_xpath)

    final_recipient = recipient_field.get_attribute("value")
    final_message = text_area.get_attribute("value") or ""

    if final_recipient != EXPECTED_RECIPIENT:
        raise Exception("Recipient changed before sending. Email was not sent.")

    if not final_message.strip():
        raise Exception("Email message is empty. Email was not sent.")

    remaining_placeholders = re.findall(r"\[[^\]]+\]", final_message)

    if remaining_placeholders:
        raise Exception(
            "Placeholders remain in the final message: "
            + ", ".join(remaining_placeholders)
            + ". Email was not sent."
        )

    print("Recipient:", final_recipient)
    print("Subject:", SUBJECT_TEMPLATE)
    print("Message is complete.")
    print("Final safety checks passed.")

    # ==========================================
    # STEP 19: SEND EMAIL
    # ==========================================

    print("\nStep 18: Clicking Send...")

    # Wait briefly for the actual Send button to be clickable.
    send_button = short_wait.until(
        EC.element_to_be_clickable((By.XPATH, send_button_xpath))
    )

    try:
        send_button.click()
        print("Standard Selenium click executed.")

    except Exception as click_error:
        print("Standard click failed:", type(click_error).__name__)
        print("Attempting JavaScript click...")

        send_button = driver.find_element(By.XPATH, send_button_xpath)

        driver.execute_script("arguments[0].click();", send_button)

        print("JavaScript click executed.")

    print("Send action attempted. Waiting for confirmation...")

    # ==========================================
    # STEP 20: VERIFY APPLICATION RESPONSE
    # ==========================================

    print("\nStep 19: Verifying email submission...")

    try:
        success_message = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(translate(normalize-space(.),"
                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
                    "'abcdefghijklmnopqrstuvwxyz'),"
                    "'email sent') or "
                    "contains(translate(normalize-space(.),"
                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ',"
                    "'abcdefghijklmnopqrstuvwxyz'),"
                    "'successfully sent')]",
                )
            )
        )

        print("------------------------------------------")
        print("TEST PASSED: Success confirmation detected.")
        print("Confirmation:", success_message.text)
        print("------------------------------------------")

    except TimeoutException:
        print("------------------------------------------")
        print("No recognizable success message was detected.")
        print("Check for validation errors or whether the modal closed.")
        print("Verify the email in the application or backend logs.")
        print("------------------------------------------")

    # ==========================================
    # STEP 21: FINAL SUMMARY
    # ==========================================

    print("\n==========================================")
    print("SCENARIO 5: AUTOMATION FINISHED")
    print("Login successful.")
    print("Target lead verified.")
    print("Recipient checked.")
    print("Subject template selected.")
    print("Placeholders replaced and verified.")
    print("Send action attempted.")
    print("Confirm successful sending in the application.")
    print("==========================================")

except TimeoutException:
    print("\nSCENARIO 5: TEST FAILED")
    print("A required element did not appear in time.")
    print("Current URL:", driver.current_url)

except Exception as error:
    print("\nSCENARIO 5: TEST FAILED")
    print("Error type:", type(error).__name__)
    print("Error details:", error)

finally:
    input("\nPress Enter to close the browser...")
    driver.quit()
