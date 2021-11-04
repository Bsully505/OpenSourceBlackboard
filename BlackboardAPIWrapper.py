import BlackboardGUICaller 
from datetime import date
import requests





class BlackboardAPIWrapper():
    global username
    global jsessionCookie
    global header
    global UserID
    global Term

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