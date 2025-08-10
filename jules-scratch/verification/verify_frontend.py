import time
from playwright.sync_api import sync_playwright, Page, expect

def run_verification(page: Page):
    """
    Navigates to the app, gets a prediction, and takes a screenshot.
    """
    print("--- Starting final verification attempt ---")
    # 1. Navigate to the app
    page.goto("http://localhost:3000/")
    print("Navigated to page.")

    # 2. Wait for page to be somewhat loaded
    page.wait_for_load_state("networkidle")
    print("Page is idle.")

    # 3. Click the "Get AI Prediction" button
    try:
        prediction_button = page.locator("button:has-text('Get AI Prediction')")
        expect(prediction_button).to_be_visible(timeout=15000)
        print("Prediction button found.")
        prediction_button.click()
        print("Clicked prediction button.")
    except Exception as e:
        print(f"Could not click prediction button: {e}")
        page.screenshot(path="jules-scratch/verification/error_before_click.png")
        return


    # 4. Wait for a fixed time to see what happens
    print("Waiting for 10 seconds to allow results to load...")
    time.sleep(10)

    # 5. Take a screenshot
    screenshot_path = "jules-scratch/verification/verification.png"
    page.screenshot(path=screenshot_path)
    print(f"Screenshot taken and saved to {screenshot_path}")

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        run_verification(page)
        browser.close()

if __name__ == "__main__":
    main()
