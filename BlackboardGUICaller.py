import tkinter as tk
from tkinter import ttk
import requests
from InCourse import InCourse
from LoginPage import LoginPage
from LoggedInAPITester import LoggedInAPITester
import json

#Bryans UserID = _74932_1
#the question that I(Bryan) have is how to get the courses faster
#the answer is to use a different api call which is in the course meembership folder

#first thing to do to get courses 
#get the username from user 
#do search https://quinnipiac.blackboard.com/learn/api/public/v1/users?userName=bcsullivan or user = username
#print out the courses

#problem that occurs 
#which courses should This app be interested in 
## this is fixed by checking all of the courses the student enrlled in and checking if they are of this semester by checking the externalID and if it contains, for this semester, 21FA

#things that Bryan has found out 
#when getting api calls and from json the way to acess the results is doing 
#for  val in response.json()['results'][0] and this will run a for loop on all outputs
#only the session id users courses can be accessed all others are 404 unauth



###
#My Plan is when creating the LoggedInAPITester frame to insert the couseName, CourseID as a string and able to split with regex of ","


###
class mainApp(tk.Tk):
        global username
        global password
        global userID
        courses = []
        preUrl = 'https://quinnipiac.blackboard.com/'
        header = {
        'Cookie': 'JSESSIONID=C5CCB4C19F8A8CCFABC47E1141B69483; BbClientCalenderTimeZone=America/New_York; web_client_cache_guid=2f5ecba6-3258-4b3d-977a-ecae91e35061; COOKIE_CONSENT_ACCEPTED=true; OptanonConsent=isIABGlobal=false&datestamp=Tue+Oct+26+2021+19:05:09+GMT-0400+(Eastern+Daylight+Time)&version=6.19.0&hosts=&consentId=e2b8dab3-930c-4d53-bb83-3fb8ac49b4f7&interactionCount=1&landingPath=https://www.blackboard.com/&groups=C0001:1,C0003:1,BG1:1,C0002:1,C0005:1,C0004:1; JSESSIONID=9E8E157C05C212F822725DC3C339E355; AWSELB=6FBB59590AD55E4479C8D5228AC967BB0DA2ED9920FD0104AE518E1D40FACC426803F95C7A6B32BF6DD3D862C1CD713BC0C9D816EACFBD71EF3251F933A12E1A0B164E8378; AWSELBCORS=6FBB59590AD55E4479C8D5228AC967BB0DA2ED9920FD0104AE518E1D40FACC426803F95C7A6B32BF6DD3D862C1CD713BC0C9D816EACFBD71EF3251F933A12E1A0B164E8378; BbRouter=expires:1635362107,id:6E894BCCD3395AC415DD7844F22A014D,signature:0dffc766c87a953d444f9c98a98963ecd725d00ffebbd81f86d4df114f531f5f,site:2bf58a57-0609-4ded-b883-0cffff2406fd,timeout:10800,user:cff58183d5a742ad9d5c0d751bc05a16,v:2,xsrf:645fa85d-2af0-411a-b645-10340a6f32b7'
        }

        global container

        def __init__(self, *args, **kwargs):

            
            tk.Tk.__init__(self, *args, **kwargs)
            self.container = tk.Frame(self)
            self.container.pack(side = "top", fill = "both", expand = True)
            self.geometry('200x150')
            self.container.grid_rowconfigure(0, weight = 1)
            self.container.grid_columnconfigure(0, weight = 1)

            self.frames = {}
            page_name = LoginPage.__name__
            frame = LoginPage(self.container, self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
            self.ChangeFrame("LoginPage")

        def addCourseFrame(self, fName,courseID,userID):
            page_name = fName
            frame = InCourse(self.container, self,courseID,self.userID)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")
            self.ChangeFrame(fName)

        def AddCourseFrame(self,userID):
            page_name = LoggedInAPITester.__name__
            frame = LoggedInAPITester(self.container, self,self.userID)
            self.frames[page_name] = frame
            print("UserID: "+ self.userID)
            frame.grid(row = 0, column = 0, sticky = "nsew")


        #very important function it gets the username to get the userid(the way that blackboard tracks students(student primary key)) and then basically starts the program
        def ValidateLogin(self,Username, Password):
            
            username = Username
            password = Password
            self.userID = self.getUserId(username)
            self.SetCourseIDInfo()
            self.AddCourseFrame(self.userID)
            #self.printoutCourseIDs()
            #self.PrintCourseNamesWithIds()
            self.ChangeFrame("LoggedInAPITester")
            #self.printoutAnnouncements('_90503_1')
            #self.printoutGrades('_90503_1')
            #self.printoutAssignments()
            self.getCoursesForThisSemester()



        def ChangeFrame(self,page):
            try:
                frame = self.frames[page]
                self.title(page)
                frame.tkraise()
            except OSError:
                print("Error")



        #not a function that is being used
        def importHeader(self):
            #example course id is _90767_1 this is for procedural generation
            #this would possibly be where selenium is used to capture the cookie of jsessionid
            print('get session cookie and set to header')
        
                
         #returns the userID of the username        
        def getUserId(self,username):
            url = 'https://quinnipiac.blackboard.com/learn/api/public/v1/users?userName='+username
            response = requests.request("GET",url,headers= self.header)
            print(response.json())
            return response.json()['results'][0]['id']

        def SetCourseIDInfo(self):
            url = "https://quinnipiac.blackboard.com/learn/api/public/v1/users/"+self.userID+"/courses"
            response = requests.request("GET",url, headers = self.header)
            #prints out the courses that the student is enrolled in 
            for res in response.json()['results']:
                self.courses.append(str(res['courseId']))
                #self.printoutCourseNameIndividual(res['courseId'])
                #print()
            
        
        def printoutCourseNameIndividual(self,courseId):
            url = self.preUrl + '/learn/api/public/v3/courses/'+courseId
            response = requests.request("GET",url,headers = self.header)
            print(response.json()['name'])

                
        def printoutCourseIDs(self):
            for i in self.courses:
                print(i)

        #Do not use this function it applies to every single class the student has enrolled in 
        def PrintCourseNames(self):
            for i in self.courses:
                print(self.printoutCourseNameIndividual(i))

        def PrintCourseNamesWithIds(self):
            for i in self.courses:
                print(self.printoutCourseNameIndividual(i))
                print(i)

        def printoutAnnouncements(self,CourseID):
            url = self.preUrl + '/learn/api/public/v1/courses/'+CourseID+'/announcements'
            response = requests.request("GET", url, headers = self.header)
            #print(response.json()['name'] + " it worked!")
            for res in response.json()['results']:
                print(res['title'])
                print(res['body'])
        
        def printoutGrades(self, CourseID):
            url = self.preUrl + '/learn/api/public/v1/courses/'+CourseID+'/gradebook/columns'
            response = requests.request("GET", url, headers = self.header)
            for res in response.json()['results']:
                #print(res)
                print(res['name'])
                print(res['score'])

        def printoutAssignments(self):
            url = self.preUrl + '/learn/api/public/v1/calendars/items'
            response = requests.request("GET", url, headers = self.header)
            for res in response.json()['results']:
                #print(res)
                print(res['title'])
                print(res['end'])

        def getCoursesForThisSemester(self):
            courses = []
            url = 'https://quinnipiac.blackboard.com/learn/api/public/v1/users/'+self.userID+'/courses?sort=lastAccessed(desc)&fields=courseId,course.externalId,course.name'
            response = requests.request("GET",url,headers = self.header)
            res = response.json()
            for val in res['results']:
                result = val['course']['externalId'].split('_')
                if(('21FA') in result[len(result)-1] ):
                    courses.append(result[0])
                    print(result[0])
               
        def getCourseIdsForThisSemester(self):
            courses = []
            url = 'https://quinnipiac.blackboard.com/learn/api/public/v1/users/'+self.userID+'/courses?sort=lastAccessed(desc)&fields=courseId,course.externalId,course.name'
            response = requests.request("GET",url,headers = self.header)
            res = response.json()
            for val in res['results']:
                result = val['course']['externalId'].split('_')
                if(('21FA') in result[len(result)-1] ):
                    courses.append(val['courseId'])
                    print(val['courseId'])
            return courses

        def getCourseIdsForThisSemester(self,userID):
            courses = []
            url = 'https://quinnipiac.blackboard.com/learn/api/public/v1/users/'+userID+'/courses?sort=lastAccessed(desc)&fields=courseId,course.externalId'
            response = requests.request("GET",url,headers = self.header)
            res = response.json()
            for val in res['results']:
                result = val['course']['externalId'].split('_')
                if(('21FA') in result[len(result)-1] ):
                    courses.append(val['courseId'])
                    print(val['courseId'])
            return courses

        def getCourseIdsandNamesForThisSemester(self,userID):
            courses = []
            url = 'https://quinnipiac.blackboard.com/learn/api/public/v1/users/'+userID+'/courses?sort=lastAccessed(desc)&fields=courseId,course.externalId,course.name'
            response = requests.request("GET",url,headers = self.header)
            res = response.json()
            for val in res['results']:
                result = val['course']['externalId'].split('_')
                if(('21FA') in result[len(result)-1] ):
                    courses.append(val['courseId']+','+val['course']['name'])
                    print(val['courseId'])
            return courses

        def getUserID(self):
            return self.userID


if __name__ == "__main__":
    app = mainApp()
    app.mainloop()
