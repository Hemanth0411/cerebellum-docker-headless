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

def validate_search_success(driver):
    """Check if search was successful by validating results presence."""
    try:
        time.sleep(2)
        # Check if search results are present
        search_results = driver.find_elements_by_css_selector('div.g')
        return len(search_results) > 0
    except Exception as e:
        print(f"Search validation error: {e}")
        return False

def run_search_agent(url, search_query, anthropic_api_key=None):
    """
    Automate Google search using AI-powered browser automation.
    
    Args:
        url (str): Google search URL
        search_query (str): Search terms to look up
        anthropic_api_key (str, optional): API key for AI service
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
        max_steps=10
    )
    goal = (
        f"1. Locate the Google search box\n"
        f"2. Enter the search query: {search_query}\n"
        f"3. Press Enter or click the search button\n"
        f"4. Wait for search results to load\n"
        f"5. Click on the most relevant result"
    )
    agent = BrowserAgent(driver, planner, goal, options)
    agent.pause_after_each_action = False

    try:
        driver.get(url)
        agent.start()
        if validate_search_success(driver):
            print("Search completed successfully")
            return True
        else:
            print("Search appears to have failed")
            return False
    finally:
        driver.quit()

def main():
    """Entry point: Configure and run search automation with environment variables."""
    root_url = os.environ.get("START_URL", "https://www.google.com")
    search_query = os.environ.get("SEARCH_QUERY", "Bitcoin creator Wikipedia")
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", None)
    run_search_agent(root_url, search_query, anthropic_api_key)

if __name__ == "__main__":
    main()