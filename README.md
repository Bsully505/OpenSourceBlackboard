# OpenSourceBlackboard

## Application Details
This project is a GUI written in python which makes API calls after logging into one’s Blackboard account. It also includes a small unfinished API Wrapper for other people who want to work with the Blackboard API more easily.

## Requirements
* Must have a Quinnipiac Blackboard account. 
* Must be currently enrolled in classes
* Internet connection

## How to install all modules 
* pip install -r requirements.txt

## How to run this project GUI Side
1. Insert the jsession cookie into the .env file
2. Run python file BlackboardGUICaller.py
3. Enter your username and hit submit
3. Click GUI buttons to choose a class and then select an action for that class.

## How to run with selenium 
1. Make sure that you have selenium installed with chrome
2. Insert the path of your selenium driver in the selenium class
3. Change the boolean variable Sel in LoginPage class to True
4. Run python file BlackboardGUICaller.py
5. Enter your username including @quinnipiac.edu and password then hit submit
6. Approve your account with 2nd auth calling
7. Click GUI buttons to choose a class and then select an action for that class.

## Working with API wrapper
1. Create a instance of our class with the username and the jsession cookie 

## Credits
Authors Bryan Sullivan, Colin McNeill
Guidance: Alex Thimineur
