import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import base64
import json
import urllib.request as urllib2
import datetime
import pip._vendor.requests 

# Your constants
username = "anubhas"
access_key = "JvGShZ2Bm8RdgmGFbbx4ZtbOb6DeQ8nqSvtHDZdDY7PzqaZMTq"
JIRA_URL = "https://lambdatest.atlassian.net/"
JIRA_USERNAME = "anubhas@lambdatest.com"
JIRA_TOKEN = "ATATT3xFfGF0TYEBSlbW3fFVubfO1M2KPSF1jWZ67Ug_Jwc3sTLSUqOaf7R8Pq14rXs2nVBIsq6PFiERRKl601FD_u7lXpkQUijOynLt6Tjx-AZAjQXIZ2BEkMc9oqpwJbNzHdzFyUy3JouB6tTL1UJkn4Sx6It2IgvhTenZ8sm3CScl4Iqqnrs=F6AFAD29"
JIRA_PROJECT_KEY = "DEMO"
JIRA_ISSUE_TYPE = "Bug"

class LambdaTestApi:
    def getSessionDetails(self, session_id):
        try:
            uri = f"https://api.lambdatest.com/automation/api/v1/sessions"
            response = pip._vendor.requests.get.get(uri, auth=(username, access_key))
            json_response = response.json()
            return json_response
        except Exception as e:
            print("Error getting session details:", e)
            return {}

    def getValue(self, data, key):
        return data.get(key, "")

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

def getSessionId():
    try:
        uri = "https://api.lambdatest.com/automation/api/v1/sessions"
        response = pip._vendor.requests.get(uri, auth=(username, access_key))
        json_response = response.json()
        # print(json_response)
        # Assuming you want to get the first session ID, modify this accordingly
        session_id = json_response[2].get(session_id, "session_id")
        print  ("session id" + session_id)
        return session_id
        print  ("session id" + session_id)
    except Exception as e:
        print("Error getting session ID:", e)
        return ""
    # Implement other methods of LambdaTestApi class here

def main():
    # ltApi = LambdaTestApi()  # Create an instance of LambdaTestApi
    # session_id = getSessionId()  # Replace with the actual session ID
    print("")
    # # print("Session ID : "+session_id)
    # summary = "Test Case Failed - " + '{date:%Y-%m-%d %H:%M}'.format(date=datetime.datetime.now())
    # description = "Detailed description of the test case failure."
    # session_details = ltApi.getSessionDetails(session_id)
    # session_name = session_details.get("name", "session_id")
    # test_id = session_details.get("test_id", "session_id")
    # session_url = f"https://automation.lambdatest.com/test?sessionId={}"
    # additional_info = f"Response is {session_details}\nString sessionName = {session_name}\nString TestId = {test_id}\nString session_url = {session_url}"
    
    # issue_key = create_jira_bug(summary, description, additional_info)
    # if issue_key:
    #     print("Created issue:", issue_key)
    # else:
    #     print("Failed to create Jira issue.")

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
        session= driver.session_id
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        driver.set_window_size(1920, 1080)

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

        heading = driver.find_element(By.CSS_SELECTOR, ".container h2")
        if heading.is_displayed():
           # self.fail("Simulated test case failure for Jira issue creation")
            ltApi = LambdaTestApi()  # Create an instance of LambdaTestApi
            # session_id = getSessionId()  # Replace with the actual session ID
            # print("Session ID : "+session_id)
            summary = "Test Case Failed - " + '{date:%Y-%m-%d %H:%M}'.format(date=datetime.datetime.now())
            description = "Detailed description of the test case failure."
            # session_details = ltApi.getSessionDetails(session)
            # session_name = session_details.get("name", "session_id")
            # test_id = session_details.get("test_id", "session_id")
            session_url = f"https://automation.lambdatest.com/test?sessionId={session}"
            additional_info = f"String session_url = {session_url}"
            
            issue_key = create_jira_bug(summary, description, additional_info)
            if issue_key:
                print("Created issue:", issue_key)
            else:
                print("Failed to create Jira issue.")  
            main()

if __name__ == "__main__":
    unittest.main()
