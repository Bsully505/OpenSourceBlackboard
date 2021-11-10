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
        #self.printoutCourseIDs()
        #self.PrintCourseNamesWithIds()
        self.ChangeFrame("LoggedInAPITester")
        #self.printoutAnnouncements('_90503_1')
        #self.printoutGrades('_90503_1')
        #self.printoutAssignments()
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
            print(html2text.html2text(res['body']))
    
    def printoutGrades(self, CourseID):
        url = self.preUrl + '/learn/api/public/v1/courses/'+CourseID+'/gradebook/users/'+self.userID
        response = requests.request("GET", url, headers = self.header)
        list = response.json()['results']
        # only works when every array in results has both columnId and score
        #res = {list[i]['columnId']: list[i]['score'] for i in range(len(list))}
        #c = map(None, list['columnId'], list['score'])
        #print(response.json()['results'][0]['columnId'])
        newlist = {}
        for res in list:
            try: 
                print(res['columnId'])
                print(res['score'])
                newlist[res['columnId']] = res['score']
                #print(res['columnId'])
                #print(res['score'])
            except KeyError:
                print()
        print (newlist)
        
                

    def printoutAssignments(self):
        url = self.preUrl + '/learn/api/public/v1/calendars/items'
        response = requests.request("GET", url, headers = self.header)
        for res in response.json()['results']:
            #print(res)
            print(res['title'])
            DueDate = str(self.ConvertTimeToEST(res['end'].split('T')[0],res['end'].split('T')[1][:-5]))
            DueDate = DueDate.rsplit('-',1)[0]
            print('DUE DATE: '+ DueDate)
 

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

    def ConvertTimeToEST(self,date, time):
        #time  is going to come in like 2021-11-15 and 04:59:00
        dts =datetime.datetime.strptime(date+' '+time, '%Y-%m-%d %H:%M:%S')

        local = datetime.datetime.astimezone(datetime.datetime.now())
        
        local_tz = local.tzinfo
        local_tzname = local_tz.tzname(local)
        users = pytz.timezone(local_tzname)
        gmt = pytz.timezone('GMT')
        dategmt = gmt.localize(dts)
        
        dateUser = dategmt.astimezone(users)
        return dateUser


if __name__ == "__main__":
    app = mainApp()
    app.mainloop()
