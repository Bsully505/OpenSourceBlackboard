
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
    global driver
    JsessionCookie = ""
    def __init__(self,UName,PWord):
        
        #options makes it so that it stays open
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)

        #the url that is going to allow selenium to login
        url = "https://quinnipiac.blackboard.com/"


        self.driver = webdriver.Chrome('C:/Users/jacks/Downloads/chromedriver.exe',chrome_options=chrome_options)

        #driver = webdriver.Chrome('C:/Users/jacks/Downloads/chromedriver.exe')# this is when you dont want to see the browser






        self.driver.get(url)
        time.sleep(4)
        UN = self.driver.find_element_by_id('i0116')
        
        UN.send_keys(UName)
        time.sleep(4)
        sendIt = self.driver.find_element_by_id('idSIButton9')
        sendIt.click()
        #wait for the browser to go to next url
        time.sleep(4)

        password = self.driver.find_element_by_id('passwordInput')
        password.send_keys(PWord)

        time.sleep(4)
        LoginButton = self.driver.find_element_by_id("submitButton")
        LoginButton.click()

        time.sleep(4)
        verification = self.driver.find_element_by_id('idDiv_SAOTCS_Proofs')
        verification.click()


        

        try:
            determine = self.driver.find_element_by_id('idSIButton9').is_displayed()
        except: 
            determine = False
        while(determine==False):
            time.sleep(1)
            try:
                determine = self.driver.find_element_by_id('idSIButton9').is_displayed()
            except:
                determine = False


        self.driver.find_element_by_id('idSIButton9').click()

        time.sleep(2)
        got = False
        self.driver.get('https://quinnipiac.blackboard.com/learn/api/public/v1/courses')
        #print(driver.get_cookies())
        ##f= open("guru99.txt","w+")
        
        #f.write(f"driver Request: {self.driver.requests}")
        #f.close()
        #print(self.driver.session_id)
        
        #print(self.driver.requests.pop().headers.items())

        for request in self.driver.requests:
            if(request.headers['Cookie'] and got ==False and request.headers['Cookie'].split('=')[0]=='JSESSIONID' and 'BbRouter' in  request.headers['Cookie']):
                self.JsessionCookie= 'BbRouter' +request.headers['Cookie'].split('BbRouter')[1].split(';')[0]    
                
        

    def getJessionCookie(self):
        return self.JsessionCookie
    
    def RequestUrl(self,URL):
        print(self.driver.session_id)
        self.driver.close()
        return self.driver.session_id
    
    def EndConnection(self):
        self.driver.close()


if __name__ == '__main__':
    Login(os.getenv('UName'),os.getenv('PWord'))