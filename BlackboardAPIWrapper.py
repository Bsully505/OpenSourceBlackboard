import BlackboardGUICaller 
from datetime import date
import requests





class BlackboardAPIWrapper():
    global username
    global jsessionCookie
    global header
    global UserID
    global Term
    preUrl = 'https://quinnipiac.blackboard.com/'

    def __init__(self,username, jsessionCookie ):
        self.username = username
        self.jsessionCookie = jsessionCookie
        self.header = {
            'Cookie': jsessionCookie
            }
        
    #to determine the term for 
    def DetermineTerm(self):
        if(date.today().month>7):
            return(str(date.today().year%100)+"FA")
        return(str(date.today().year%100)+"SP")

    #to get the userId from the user 
    def getUserId(self):
        url = 'https://quinnipiac.blackboard.com/learn/api/public/v1/users?userName='+self.username
        response = requests.request("GET",url,headers= self.header)
        return response.json()['results'][0]['id']

    def getCoursesForThisSemester(self):
        courses = []
        url = 'https://quinnipiac.blackboard.com/learn/api/public/v1/users/'+self.getUserId()+'/courses?sort=lastAccessed(desc)&fields=courseId,course.externalId,course.name'
        response = requests.request("GET",url,headers = self.header)
        res = response.json()
        for val in res['results']:
            result = val['course']['externalId'].split('_')
            if(self.DetermineTerm() in result[len(result)-1] ):
                if(result is not None):
                    courses.append(result[0])               
        return courses


    def GetCourseID(self):
        url = "https://quinnipiac.blackboard.com/learn/api/public/v1/users/"+self.userID+"/courses"
        response = requests.request("GET",url, headers = self.header)
        #prints out the courses that the student is enrolled in 
        courses={}
        for res in response.json()['results']:
            courses.append(str(res['courseId']))
        return courses

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

        SecondUrl = self.preUrl+'/learn/api/public/v1/courses/'+CourseID+'/gradebook/columns'
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
       