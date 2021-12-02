
from dotenv import load_dotenv
import os
load_dotenv()

'''
What needs to be completed 
- Get the jsessioncookie / I have had problems getting the correct one. 
- allow other people to use the selenium aka change the webdriver path to fit other people as well
'''


from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time



class Login():
    JsessionCookie = ""
    def __init__(self,UName,PWord):
        
        #options makes it so that it stays open
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        #the url that is going to allow selenium to login
        url = "https://quinnipiac.blackboard.com/"


        driver = webdriver.Chrome('C:/Users/jacks/Downloads/chromedriver.exe',chrome_options=chrome_options)

        #driver = webdriver.Chrome('C:/Users/jacks/Downloads/chromedriver.exe')# this is when you dont want to see the browser






        driver.get(url)
        time.sleep(4)
        UN = driver.find_element_by_id('i0116')
        
        UN.send_keys(UName)
        time.sleep(4)
        sendIt = driver.find_element_by_id('idSIButton9')
        sendIt.click()
        #wait for the browser to go to next url
        time.sleep(4)

        password = driver.find_element_by_id('passwordInput')
        password.send_keys(PWord)

        time.sleep(4)
        LoginButton = driver.find_element_by_id("submitButton")
        LoginButton.click()

        time.sleep(4)
        verification = driver.find_element_by_id('idDiv_SAOTCS_Proofs')
        verification.click()


        

        try:
            determine = driver.find_element_by_id('idSIButton9').is_displayed()
        except: 
            determine = False
        while(determine==False):
            time.sleep(1)
            try:
                determine = driver.find_element_by_id('idSIButton9').is_displayed()
            except:
                determine = False


        driver.find_element_by_id('idSIButton9').click()

        time.sleep(2)
        got = False
        driver.get('https://quinnipiac.blackboard.com/learn/api/public/v1/courses')
        print(driver.get_cookies())
        print(driver.requests.get('Cookie'))
        for request in driver.requests:

            if(request.headers['Cookie'] and got ==False and request.headers['Cookie'].split('=')[0]=='JSESSIONID' and 'COOKIE_CONSENT_ACCEPTED' in  request.headers['Cookie']):
                self.JsessionCookie=  request.headers['Cookie']
                print(self.JsessionCookie)
                got = True
        

    def getJessionCookie(self):
        return self.JsessionCookie


if __name__ == '__main__':
    Login(os.getenv('UName'),os.getenv('PWord'))