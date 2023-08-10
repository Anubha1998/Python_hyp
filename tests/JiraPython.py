import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import base64
import json
import urllib.request as urllib2
import datetime
import pip._vendor.requests
from selenium.common.exceptions import NoSuchElementException


# Your constants
username = "anubhas"
access_key = "JvGShZ2Bm8RdgmGFbbx4ZtbOb6DeQ8nqSvtHDZdDY7PzqaZMTq"
JIRA_URL = "https://lambdatest.atlassian.net/"
JIRA_USERNAME = "anubhas@lambdatest.com"
JIRA_TOKEN = "ATATT3xFfGF0HoaLjttAWXxd2zAKPk7kfrsV2gsN6hgcWvAcvC63xSm7wh8E0sGKIGgI1l6KM-3d7oK9EOJCoSgLmhWHFaK5_iaFOZSJWV051QmTBWxOGAaEZjhlOxF6xj1vuriTCWQq0F63LtrPfwqogWBO3_4rdNpnXVrcVjG3MDxVpyj9Y10=8719B704"
JIRA_PROJECT_KEY = "INDG"
JIRA_ISSUE_TYPE = "Bug"

def create_jira_bug(summary, description, additional_info):
    try:
        url = JIRA_URL + '/rest/api/2/issue/'
        credentials = f"{JIRA_USERNAME}:{JIRA_TOKEN}"
        base64_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {base64_credentials}'
        }

        data = {
            "fields": {
                "project": {
                    "key": JIRA_PROJECT_KEY
                },
                "summary": summary,
                "issuetype": {
                    "name": JIRA_ISSUE_TYPE
                },
                "description": f"{description}\n\nAdditional Info:\n{additional_info}"
            }
        }

        req = urllib2.Request(url, json.dumps(data).encode(), headers)
        response = urllib2.urlopen(req)
        response_data = json.loads(response.read())
        print("Jira API Response:", response_data)  # Debugging line
        return response_data['key']
    except Exception as e:
        print("Error creating Jira issue:", e)
        return None

class FirstSampleTest(unittest.TestCase):
    def setUp(self):
        options = ChromeOptions()
        options.browser_version = "114.0"
        options.platform_name = "Windows 10"
        
        lt_options = {
            "username": "anubhas",
            "accessKey": "JvGShZ2Bm8RdgmGFbbx4ZtbOb6DeQ8nqSvtHDZdDY7PzqaZMTq",
            "project": "Untitled",
            "w3c": True,
            "plugin": "python-python"
        }
        
        options.set_capability('LT:Options', lt_options)
        
        self.driver = webdriver.Remote(
            command_executor=f"http://{username}:{access_key}@hub.lambdatest.com/wd/hub",
            options=options
        )

    def tearDown(self):
        self.driver.quit()

    def test_demo_site(self):
        driver = self.driver
        session_id = driver.session_id  # Fixing variable name

        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        driver.set_window_size(1920, 1080)

        try:
            print('Loading URL')
            driver.get("https://stage-lambda-devops-use-only.lambdatestinternal.com/To-do-app/index.html")

            driver.find_element(By.NAME, "li1").click()
            location = driver.find_element(By.NAME, "li2")
            location.click()
            print("Clicked on the second element")

            driver.find_element(By.ID, "sampletodotext").send_keys("LambdaTest")
            add_button = driver.find_element(By.ID, "addbutton")
            add_button.click()
            print("Added LambdaTest checkbox")

            search = driver.find_element(By.CSS_SELECTOR, ".container h2")
            assert search.is_displayed(), "heading is not displayed"
            print(search.text)
            search.click()
            driver.implicitly_wait(3)

            heading = driver.find_element(By.CSS_SELECTOR, ".container h5")  # Fixing the CSS selector for 'heading'
            if heading.is_displayed():
                heading.click()
                driver.execute_script("lambda-status=passed")
                print("Tests are run successfully!")

        except NoSuchElementException:
            print("Heading element is not found. Test failed!")
            driver.execute_script("lambda-status=failed")
            summary = "Test Case Failed - " + '{date:%Y-%m-%d %H:%M}'.format(date=datetime.datetime.now())
            description = "Detailed description of the test case failure."
            session_url = f"https://automation.lambdatest.com/test?sessionId={session_id}"
            additional_info = f"String session_url = {session_url}"
            
            issue_key = create_jira_bug(summary, description, additional_info)
            if issue_key:
                print("Created issue:", issue_key)
            else:
                print("Failed to create Jira issue.")  

if __name__ == "__main__":
    unittest.main()
