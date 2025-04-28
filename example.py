from seleniumbase import get_driver
from cerebellum import AnthropicPlanner, BrowserAgent, BrowserAgentOptions
import os
import uuid
from monkey_patch import custom_take_action
from state_tracker import StateTracker
import time

# Apply the monkey patch for action tracking
original_take_action = BrowserAgent.take_action
BrowserAgent.take_action = custom_take_action

def validate_form_submission(driver):
    """Check if the form was submitted successfully by looking for success message."""
    try:
        time.sleep(2)  # Wait for form submission
        # Look for common success message elements
        success_messages = driver.find_elements_by_xpath(
            "//*[contains(text(), 'success') or contains(text(), 'thank you') or contains(text(), 'received')]"
        )
        return len(success_messages) > 0
    except Exception as e:
        print(f"Form validation error: {e}")
        return False

def fill_contact_form(url, name, email, message, anthropic_api_key=None):
    """
    Automate filling out a contact form using AI-powered browser automation.
    
    Args:
        url (str): The URL of the contact form
        name (str): Name to enter in the form
        email (str): Email address to enter in the form
        message (str): Message to enter in the form
        anthropic_api_key (str, optional): API key for the AI service
    """
    # Set up the AI service API key if provided
    if anthropic_api_key:
        os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key

    # Create a unique temporary directory for Chrome
    user_data_dir = f"/tmp/user-data-{uuid.uuid4()}"
    os.makedirs(user_data_dir, exist_ok=True)

    # Configure Chrome options for headless operation
    chrome_options = {
        "user_data_dir": user_data_dir,
        "headless": True,
        "disable_gpu": True,
        "no_sandbox": True,
    }

    # Initialize the web driver
    driver = get_driver(browser="chrome", **chrome_options)

    try:
        # Set up the AI planner and options
        planner = AnthropicPlanner()
        options = BrowserAgentOptions(
            pause_after_each_action=True,
            max_steps=10  # Prevent infinite loops
        )

        # Define the goal for the AI agent
        goal = (
            f"1. Find the contact form on the page\n"
            f"2. Enter the name: {name}\n"
            f"3. Enter the email: {email}\n"
            f"4. Enter the message: {message}\n"
            f"5. Submit the form\n"
            f"6. Verify the submission was successful"
        )

        # Create and configure the browser agent
        agent = BrowserAgent(driver, planner, goal, options)
        agent.pause_after_each_action = False

        # Start the automation
        print("Starting form fill automation...")
        driver.get(url)
        agent.start()

        # Validate the result
        if validate_form_submission(driver):
            print("Form submitted successfully!")
            return True
        else:
            print("Form submission may have failed")
            return False

    finally:
        # Clean up
        driver.quit()

def main():
    # Example usage with environment variables
    url = os.environ.get("FORM_URL", "https://example.com/contact")
    name = os.environ.get("NAME", "John Doe")
    email = os.environ.get("EMAIL", "john@example.com")
    message = os.environ.get("MESSAGE", "Hello, this is a test message!")
    api_key = os.environ.get("ANTHROPIC_API_KEY", None)

    # Run the automation
    success = fill_contact_form(url, name, email, message, api_key)
    
    if success:
        print("✨ Automation completed successfully!")
    else:
        print("❌ Automation encountered some issues")

if __name__ == "__main__":
    main()
