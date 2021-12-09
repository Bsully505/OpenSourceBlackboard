import tkinter as tk
from tkinter import ttk
import requests
from InCourse import InCourse
from LoginPage import LoginPage
from LoggedInAPITester import LoggedInAPITester
import json
import os
from dotenv import load_dotenv
import html2text
from datetime import date
import datetime
import pytz
import browsercookie
from SeleniumBlackBoard import Login

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

#what I have to do is to wait for selenium to set the Bbrouter cookie and then 
###






class mainApp(tk.Tk):
    load_dotenv()
    global username
    global password
    global userID
    global term
    courses = []
    preUrl = 'https://quinnipiac.blackboard.com/'
    header = {
    'Cookie': os.getenv('Header')
    }

    global container
    global driver
    def __init__(self, *args, **kwargs):
        
        self.term = self.DetermineTerm()
        
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
        self.ChangeFrame("LoggedInAPITester")
        self.getCoursesForThisSemester()
        
    def ValidateLoginWithSel(self,Username, Password):
        username = Username
        password = Password
        if(len(password)>5):
            self.driver = Login(username,password)
            username = username.split('@')[0]
            self.header['Cookie']= self.driver.getJessionCookie()
        res = self.driver.RequestUrl('https://quinnipiac.blackboard.com/learn/api/public/v1/users?userName='+username)
        self.userID = self.getUserId(username)
        self.SetCourseIDInfo()
        self.AddCourseFrame(self.userID)
        self.ChangeFrame("LoggedInAPITester")
        self.getCoursesForThisSemester()
          

    def DetermineTerm(self):
        if(date.today().month>7):
            return(str(date.today().year%100)+"FA")
        return(str(date.today().year%100)+"SP")

    def ChangeFrame(self,page):
        try:
            frame = self.frames[page]
            self.title(page)
            frame.tkraise()
        except OSError:
            print("Error")



    #not a function that is being used
    def importHeader(self,bbRouter):
        #example course id is _90767_1 this is for procedural generation
        #this would possibly be where selenium is used to capture the cookie of jsessionid
        self.header = {
            'Cookie': bbRouter
        }
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
        for res in response.json()['results']:
            print(res['title'])
            print(html2text.html2text(res['body']))

    def changeAnnouncementsLabel(self, CourseID):
        url = self.preUrl + '/learn/api/public/v1/courses/'+CourseID+'/announcements'
        response = requests.request("GET", url, headers = self.header)
        s = ""
        for res in response.json()['results']:
            s += res['title']
            s += "\n"
            s += html2text.html2text(res['body'])
        return s
    
    def changeAnnouncements(self, controller, CourseID, fullAnnouncements):
        fullAnnouncements.config(text = controller.changeAnnouncementsLabel(CourseID))
        return fullAnnouncements

    def printoutGrades(self, CourseID):
        url = self.preUrl + '/learn/api/public/v1/courses/'+CourseID+'/gradebook/users/'+self.userID
        response = requests.request("GET", url, headers = self.header)
        list = response.json()['results']
        # only works when every array in results has both columnId and score
        #res = {list[i]['columnId']: list[i]['score'] for i in range(len(list))}
        #c = map(None, list['columnId'], list['score'])
        #print(response.json()['results'][0]['columnId'])
       

        Score = {}
        for res in list:
            try: 
                Score[res['columnId']] = res['score']
            except KeyError:
                print()

        SecondUrl = self.preUrl+'/learn/api/public/v1/courses/' + CourseID + '/gradebook/columns'
        response = requests.request("GET", SecondUrl, headers = self.header)
        secondList = response.json()['results']
        Name = {}
        Possible= {}
        for res in secondList:
            try:
                if(Score[res['id']]):
                    Name[res['id']] = res['name']
                    Possible[res['id']]= res['score']['possible']
            except KeyError:
                print()
        for colId in Score:
            name = str(Name[colId])
            score = str(Score[colId])
            possible = str(Possible[colId])
            print(name +': '+score+'/'+possible)
       
        
                

    #def printoutAssignments(self):
    #    url = self.preUrl + '/learn/api/public/v1/calendars/items'
    #    response = requests.request("GET", url, headers = self.header)
    #    for res in response.json()['results']:
    #        print(res['title'])
    #        DueDate = str(self.ConvertTimeToEST(res['end'].split('T')[0],res['end'].split('T')[1][:-5]))
    #        DueDate = DueDate.rsplit('-',1)[0]
    #        print('DUE DATE: '+ DueDate)

    def changeAssignmentsLabel(self):
        url = self.preUrl + '/learn/api/public/v1/calendars/items'
        response = requests.request("GET", url, headers = self.header)
        s = ""
        for res in response.json()['results']:
            s += res['title']
            DueDate = str(self.ConvertTimeToEST(res['end'].split('T')[0],res['end'].split('T')[1][:-5]))
            DueDate = DueDate.rsplit('-',1)[0]
            s += "\n"
            s += "DUE DATE: " + DueDate + "\n"
        return s
    
    def changeAssignments(self, controller, fullAssignments):
        fullAssignments.config(text = controller.changeAssignmentsLabel())
        return fullAssignments
 

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
            

    #this does 
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
            if((self.term) in result[len(result)-1] ):
                courses.append(val['courseId']+','+val['course']['name'])
                print(val['courseId'])
        return courses

    def getUserID(self):
        return self.userID

    def getInitials(self, text):
        list = text.split(" ")
        res = ""
        if len(list)>1:
            for word in list:
                res += word[0]
            res = res.upper()
            return res
        return text
    
    def ConvertTimeToEST(self, date, time):
        #time  is going to come in like 2021-11-15 and 04:59:00
        dts =datetime.datetime.strptime(date+' '+time, '%Y-%m-%d %H:%M:%S')

        local = datetime.datetime.astimezone(datetime.datetime.now())
        
        local_tz = local.tzinfo
        #print(local_tz)
        local_tzname = local_tz.tzname(local)
        users = pytz.timezone(self.getInitials(local_tzname))
        gmt = pytz.timezone('GMT')
        dategmt = gmt.localize(dts)
        #print(local_tzname)
        
        dateUser = dategmt.astimezone(users)
        return dateUser


if __name__ == "__main__":
    app = mainApp()
    app.mainloop()
