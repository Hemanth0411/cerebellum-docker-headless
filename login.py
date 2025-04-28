from seleniumbase import get_driver
from cerebellum import AnthropicPlanner, BrowserAgent, BrowserAgentOptions
import os
import uuid
from monkey_patch import custom_take_action
import requests
import json
import time

# Apply the monkey patch for action tracking
original_take_action = BrowserAgent.take_action
BrowserAgent.take_action = custom_take_action

def extract_session_token(driver):
    """Extract session token from cookies, localStorage, or sessionStorage."""
    cookies = driver.get_cookies()
    print("DEBUG: All cookies after login:", cookies)
    # Write all cookies to a file for debugging
    with open("session_token.txt", "w") as f:
        f.write(json.dumps(cookies, indent=2))
    # Try common session cookie names
    for cookie in cookies:
        if cookie['name'] in ['session_token', 'token', 'auth_token', 'sessionid', 'JSESSIONID']:
            print(f"DEBUG: Found possible session cookie: {cookie['name']}={cookie['value']}")
            return cookie['value']
    # Try localStorage and sessionStorage
    try:
        local_storage = driver.execute_script("return {...window.localStorage};")
        print("DEBUG: localStorage:", local_storage)
        with open("local_storage.txt", "w") as f:
            f.write(json.dumps(local_storage, indent=2))
        for key, value in local_storage.items():
            if 'token' in key.lower():
                print(f"DEBUG: Found possible token in localStorage: {key}={value}")
                return value
    except Exception as e:
        print(f"DEBUG: Could not access localStorage: {e}")
    try:
        session_storage = driver.execute_script("return {...window.sessionStorage};")
        print("DEBUG: sessionStorage:", session_storage)
        with open("session_storage.txt", "w") as f:
            f.write(json.dumps(session_storage, indent=2))
        for key, value in session_storage.items():
            if 'token' in key.lower():
                print(f"DEBUG: Found possible token in sessionStorage: {key}={value}")
                return value
    except Exception as e:
        print(f"DEBUG: Could not access sessionStorage: {e}")
    return None

def validate_login_success(driver):
    """Check if login was successful by validating URL and error messages."""
    try:
        # Wait for URL change
        time.sleep(2)
        current_url = driver.current_url
        if "login" not in current_url.lower():
            return True
        # Check if login error messages are present
        error_elements = driver.find_elements_by_xpath("//*[contains(text(), 'error') or contains(text(), 'invalid')]")
        if not error_elements:
            return True
        return False
    except Exception as e:
        print(f"Login validation error: {e}")
        return False

def send_token_to_api(token, api_url):
    """Send extracted session token to specified API endpoint."""
    try:
        response = requests.post(api_url, json={'session_token': token})
        if response.status_code == 200:
            print("Session token sent successfully")
        else:
            print(f"Failed to send session token: {response.status_code}")
    except Exception as e:
        print(f"Error sending token to API: {e}")

def run_agent_and_get_token(url, username, password, anthropic_api_key=None, api_url=None):
    """
    Automate login process using AI-powered browser automation.
    
    Args:
        url (str): The login page URL
        username (str): Login username
        password (str): Login password
        anthropic_api_key (str, optional): API key for AI service
        api_url (str, optional): Endpoint to send extracted token
    """
    # Set up the AI service API key if provided
    if anthropic_api_key:
        os.environ["ANTHROPIC_API_KEY"] = anthropic_api_key

    user_data_dir = f"/tmp/user-data-{uuid.uuid4()}"
    os.makedirs(user_data_dir, exist_ok=True)

    chrome_options = {
        "user_data_dir": user_data_dir,
        "headless": True,
        "disable_gpu": True,
        "no_sandbox": True,
    }

    driver = get_driver(browser="chrome", **chrome_options)
    planner = AnthropicPlanner()
    options = BrowserAgentOptions(
        pause_after_each_action=True,
        max_steps=10  # Limit maximum steps to prevent infinite loops
    )
    goal = (
        f"1. Find and click on the login/signin button if on homepage\n"
        f"2. Once on login page, locate username/email field and enter: {username}\n"
        f"3. Locate password field and enter: {password}\n"
        f"4. Find and click the submit/login button\n"
        f"5. Stop once logged in successfully"
    )
    agent = BrowserAgent(driver, planner, goal, options)
    agent.pause_after_each_action = False

    try:
        driver.get(url)
        agent.start()
        if validate_login_success(driver):
            print("Login successful, extracting token...")
            session_token = extract_session_token(driver)
            if session_token:
                print(f"Session token extracted: {session_token}")
                if api_url:
                    send_token_to_api(session_token, api_url)
            else:
                print("Session token not found. Check session_token.txt, local_storage.txt, and session_storage.txt for details.")
            return session_token
        else:
            print("Login appears to have failed, stopping execution")
            return None
    finally:
        driver.quit()

def main():
    """Entry point: Configure and run login automation with environment variables."""
    root_url = os.environ.get("START_URL", "https://www.google.com")
    username = os.environ.get("USERNAME", "user")
    password = os.environ.get("PASSWORD", "pass")
    api_url = os.environ.get("API_URL", "http://host.docker.internal:5000/receive_token")
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", None)
    run_agent_and_get_token(root_url, username, password, anthropic_api_key, api_url)

if __name__ == "__main__":
    main()