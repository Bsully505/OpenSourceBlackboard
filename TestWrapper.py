from BlackboardAPIWrapper import BlackboardAPIWrapper
from dotenv import load_dotenv
import os 


if __name__=="__main__":
    load_dotenv()
    wrapper = BlackboardAPIWrapper('bcsullivan',os.getenv('Header'),password= os.getenv('PWord'))
    #print(wrapper.getUserId())
    #print(wrapper.getCoursesForThisSemester())
    
