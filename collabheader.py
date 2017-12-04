'''
a-create test user// design a document based on input() values
b-use test user//satisfied using a simple find query on user field
----------
filename operation - using filename initialize database or create one
function 1- For a user with a university //Find a user of subclass
			Find users with same interests and skills
			Within 10 miles of that user
			List output format[sort()]
			1. ---User with most skills and interests matched
				--User 1 Organization
				--Common interests and skills
			...
			...
			N. ---User with the least skills and interests matched
				--User N Organization
				--Common interests and skills

function 2- Given a user we first determine other users who have worked on the same project(s) as the user[we'll denote these as colleagues).
	    Determining those we then return a list of users who havve worked on the same project as these collegaues.
function 3- Given a User get their Personal Info in a timely fashion[finished]
location searcher- returns a list of data based on a given/user location[finished]
corp searcher- returns a list based on organizations[finished]
degree searcher- list based on degrees[finished]
skill searcher-  list based on skills[finished]
interest searcher-  list based on interests[finished]
#simple query for all documents
#cursor = cnDB.files_data.find()
#for document in cursor:
#	print(document)
idnumber = "44371987399"
#idnumber=input("Enter user id or username:")
#base functionality for function 3
cursor = cnDB.files_data.find({"User":idnumber})
for document in cursor:
	print(document)
#finding a user of subclass
cursor = cnDB.files_data.find({"User":{"$regex": "99"}})
for document in cursor:
	print(document)
'''
import csv
import pandas as pd
import sys, getopt, pprint
import collabheader

def helpmessage():
	print("func1 --- For a university user find users with same interests and skills within a 10 mile distance\n")
	print("func2 --- For a user find the trusted collegaues of colleages")
	print("func3 --- For a user return personal information")
	print("lsearch - For a location locate all users that correspond to it")
	print("osearch - For an organization return all affiliated users")
	print("dsearch - For a degree return a list of users with that degree")
	print("sksearch- For a skill return all users that have it")
	print("isearch - For an interests return all users that have it")
	print("help ---- Print this message and return to option prompt")