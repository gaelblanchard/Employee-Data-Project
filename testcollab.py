
import csv
import pandas as pd
import sys, getopt, pprint
import matplotlib.pyplot as plt
import collabheader
import collabgraphs
from pymongo import MongoClient, ASCENDING
from py2neo import Graph
from py2neo import authenticate
from py2neo.cypher import CypherError
from pylab import *
#file input options
if len(sys.argv) == 1:
#enter all filenames through command line
	file_1=input("Enter file with users with their full names: ")
	file_2=input("Enter file with the users and their projects: ")
	file_3=input("Enter file with the users and their organizations: ")
	file_4=input("Enter file with user and their skills: ")
	file_5=input("Enter file with user and their interests: ")
	file_6=input("Enter file with organizations and their distances: ")
elif len(sys.argv)== 7:
	file_1=sys.argv[1]
	file_2=sys.argv[2]
	file_3=sys.argv[3]
	file_4=sys.argv[4]
	file_5=sys.argv[5]
	file_6=sys.argv[6]
elif len(sys.argv)== 2:
	if sys.argv[1]=="help":
		collabheader.helpmessage()
	else:
		print("Enter Filenames not enough provided.")
		file_1=input("Enter file with users with their full names: ")
		file_2=input("Enter file with the users and their projects: ")
		file_3=input("Enter file with the users and their organizations: ")
		file_4=input("Enter file with user and their skills: ")
		file_5=input("Enter file with user and their interests: ")
		file_6=input("Enter file with organizations and their distances: ")
else:
	print("You need to enter six files through command line enter files through program:")
	#enter all filenames
	file_1=input("Enter file with users with their full names: ")
	file_2=input("Enter file with the users and their projects: ")
	file_3=input("Enter file with the users and their organizations: ")
	file_4=input("Enter file with user and their skills: ")
	file_5=input("Enter file with user and their interests: ")
	file_6=input("Enter file with organizations and their distances: ")
#end of file input
#MongoDB
client = MongoClient()
cnDB = client.primerodos
#Neo4j
graph=Graph()
authenticate("localhost:7474","neo4j","neo4j")
graph = Graph("http://localhost:7474/db/data/")
cypher=graph.cypher
graphformat = {"User" : "user_id" , "Skill" : "name" , "Interest" : "name" , "Organization" : "name" , "Project" : "name"}
for each in graphformat:
	try:
		graph.schema.create_uniqueness_constraint(each, graphformat[each])
	except:
		pass
#Loading and Adding to the Databases
cnDB.files_data.create_index([('user_id', ASCENDING)], unique=True)
cypher = graph.cypher
#Load User File add Username Phonenumber Address
theUserfile = open(file_1,"r")
theUserReader = csv.DictReader(theUserfile, fieldnames=['user_id','first_name','last_name','phonenumber','username','address'])
cypher =graph.cypher
for each in theUserReader:
	try:
		user_id = cnDB.files_data.insert_one(each).inserted_id
	except:
		pass
	try:
		create = cypher.execute("MERGE (user:User {user_id:{a}, first_name:{b}, last_name:{c}, phonenumber:{d}, username:{e}, address:{f}}) RETURN user",a=each['user_id'],b=each['first_name'],c=each['last_name'],d=each['phonenumber'],e=each['username'],f=each['address'])
	except CypherError as err:
		print("err")
#Create relations after all projects are created so no duplicates are written
#relateprojects = cypher.execute("MATCH (a:User),(b:Project) WHERE a.project.name = b.name MERGE (a)-[rel:workedon]->(b) RETURN r")
#file_3 load organization file
theOrganizationfile = open(file_3,"r")
theOrganizationReader = csv.DictReader(theOrganizationfile, fieldnames=['user_id','organization','organization_type'])
cypher=graph.cypher
for each in theOrganizationReader:
	try:
		org_insert = cnDB.files_data.update({'user_id':each['user_id']},{'$set':{'organization':{'name': each['organization'], 'type':each['organization_type']}}})
	except:
		pass
	try:
		create = cypher.execute("MATCH (user {user_id:{a}}) SET user.organization.name={b},user.organization.type={c} RETURN user", a=each['user_id'],b=each['organization'],c=each['organization_type'])
	except CypherError as err:
		print("........34")
	try:
		create = cypher.execute("MERGE (org:Org {name:{a}, type:{b}})", a=each['organization'],b=each['organization_type'])
	except CypherError as err:
		print("......l")
	try:
		create = cypher.execute("MATCH (org:Org {name:{b}}), (user:User {user_id:{a}})"+"MERGE (user)-[rel:workedat]->(org)",a=each['user_id'],b=each['organization'])
	except CypherError as err:
		print("ntoworking")
#create = cypher.execute("MATCH (a:User),(b:Org) WHERE a.organization.name = b.name CREATE (a)-[r:workedat]->(b) RETURN r")
#file_4 load skill file
#file_2 load project file create project relations
theProjectfile = open(file_2,"r")
theProjectReader = csv.DictReader(theProjectfile, fieldnames=['user_id','project'])
cypher=graph.cypher
for each in theProjectReader:
	try:
		project_insert = cnDB.files_data.update({'user_id':each['user_id']},{'$set':{'projects': {'name':each['project']}}})
	except:
		pass
	try:
		create = cypher.execute("MERGE (project:Project {name:{a}})", a=each['project'])
		#mergeprojects = cypher.execute("MATCH (user:User) MERGE (project:Project {name: {a}}) RETURN user.username, user.project, project", a=each['project'])
	except CypherError as err:
		print("....x")
	try:
		create = cypher.execute("MATCH (project:Project {name:{b}}), (user:User {user_id:{a}})"+"MERGE (user)-[rel:workedon]->(project)",a=each['user_id'],b=each['project'])
	except CypherError as err:
		print("....r")
theSkillfile = open(file_4,"r")
theSkillReader = csv.DictReader(theSkillfile, fieldnames=['user_id','skill','skill level'])
cypher=graph.cypher
for each in theSkillReader:
	try:
		each['skill level']=int(each['skill level'])
	except ValueError:
		continue
	try:
		skill_insert = cnDB.files_data.update({'user_id':each['user_id']},{'$set':{'skill':{'name':each['skill'], 'level':each['skill level']}}})
	except:
		print("....a")
	try:
		create = cypher.execute("MERGE (skill:Skill {name:{a},level:{b}})",a=each['skill'],b=each['skill level'])
	except CypherError as err:
		print("....z")
	try:
		create = cypher.execute("MATCH (skill:Skill {name:{a}}),(user:User {user_id:{c}})"+"MERGE (user)-[rel:skilledin {weight: {b}}]->(skill)", a=each['skill'],b=each['skill level'],c=each['user_id'])
	except CypherError as err:
		print(".....b")
#relateskills = cypher.execute("MATCH (a:User),(b:Skill) WHERE a.skill = b.name MERGE (a)-[rel:skilledin]->(b) RETURN r")
#file_5 load interest file
theInterestfile = open(file_5,"r")
theInterestReader= csv.DictReader(theInterestfile, fieldnames=['user_id','interest','interest level'])
cypher=graph.cypher
for each in theInterestReader:
	try:
		each['interest level']=int(each['interest level'])
	except ValueError:
		continue
	try:
		interest_insert = cnDB.files_data.update({'user_id':each['user_id']},{'$set':{'interest':{'name':each['interest'], 'level':each['interest level']}}})
	except CypherError as err:
		print("err")
	try:
		create = cypher.execute("MERGE (interest:Interest {name:{a}, level:{b}})",a=each['interest'],b=each['interest level'])
	except CypherError as err:
		print("......d")
	try:
		create = cypher.execute("MATCH (interest:Interest {name:{a}}), (user:User {user_id:{c}})"+"MERGE (user)-[r:interestedin {level: {b}}]->(interest)",a=each['interest'],b=each['interest level'],c=each['user_id'])
	except CypherError as err:
		print("......c")
#relateinterests = cypher.execute("MATCH (a:User),(b:Interest) WHERE a.interest = b.name MERGE (a)-[rel:interestedin]->(b) RETURN r")
#file_6 load distance file
theDistancefile = open(file_6,"r")
theDistanceReader = csv.DictReader(theDistancefile, fieldnames=['organization_1','organization_2','distance'])
cypher=graph.cypher
for each in theDistanceReader:
	try:
		each['distance'] = float(each['distance'])
	except ValueError:
		continue
	try:
		create=cypher.execute("MATCH (org1:Org {name:{a}}),(org2:Org {name:{b}})"+"CREATE (org1)-[rel:distance {miles: {c}}]->(org2)",a=each['organization_1'],b=each['organization_2'],c=each['distance'])
	except CypherError as err:
		print("......")
#orgtoorgrelation = cypher.execute("MATCH (a:Organization),(b:Organization) MERGE (a)<-[rel:distance}->")
allpossibilities = "Possible commands:\nfunc1\nfunc2\nosearch\notypesearch\nisearch\nsksearch\nfnsearch\nlnsearch\npnsearch\nunsearch\nasearch\nhelp\nexit\nclear and exit"
totalcnDBsize = cnDB.files_data.find().count()
print(totalcnDBsize)
print(allpossibilities)
while True:
	inputqueryCommands = input("Enter a command to execute:")
	if inputqueryCommands.strip()=="func1":
		userinput=input("Enter username: ")
		gettheuser = cypher.execute("MATCH (user:User {username:{a}})-[:interestedin]->(interest)<-[getvalue:interestedin]-(otheruser:User) MATCH (otheruser:User)-[:workedat]->(org:Org) MATCH (anotheruser:User)-[:workedat]->(b:Org) MATCH (org:Org)<-[r:distance]->(b:Org) WHERE r.miles <= 10 MATCH (b:Org)<-[:workedat]-(user:User) WITH otheruser,collect(b.name) as organization,collect(interest.name) as matchedinterest,collect(r.miles) as distance,collect(getvalue.level) as interestlevel RETURN otheruser.username, otheruser.first_name, otheruser.last_name,  organization, matchedinterest, distance, interestlevel", a=userinput)
		print(gettheuser)
	elif inputqueryCommands.strip()=="func2":
		userinput = input("Enter username to return trusted colleagues: ")
		gettrustedcolleagues = cypher.execute("match (user:User {username:{usersinput}}),(thecollabuser:User)-[:workedon]->(project)<-[:workedon]-(theothercollabuser:User),(thecollabuser)-[:interestedin]-(interest) WITH user,thecollabuser, collect(user.username) as originaluser, collect(thecollabuser.phonenumber) as phonenumber, theothercollabuser, collect (project.name) as collabproject, collect(interest.name) as particularinterests WHERE thecollabuser.user_id<>user.user_id AND theothercollabuser.user_id<>user.user_id AND thecollabuser<>theothercollabuser RETURN DISTINCT originaluser,thecollabuser.username,collabproject,phonenumber, particularinterests ORDER BY thecollabuser.username DESCENDING",usersinput = userinput)
		print(gettrustedcolleagues)
	elif inputqueryCommands.strip()=="func3":
		idnumber=input("Enter user id or username:")
		cursor = cnDB.files_data.find({"username":idnumber},{"first_name":1,"last_name":1,"phonenumber":1,"address":1,"organization":1})
		for document in cursor:
			print(document)
		print("")		
	elif inputqueryCommands.strip()=="osearch":
		searchcorps=input("Enter organization:")
		cursor = cnDB.files_data.find({"organization.name":{"$regex":searchcorps}})
		databasesize=cnDB.files_data.find().count()
		cursorsize = cnDB.files_data.find({"organization.name":{"$regex":searchcorps}}).count()
		for document in cursor:
			print(document)
		orglabel = searchcorps
		printpiegraph=input("Do you want to print pie graph y/n: ")
		if printpiegraph.strip()=="y":
			collabgraphs.printgraph(orglabel,cursorsize,totalcnDBsize)
			print("piegraph complete.")
	elif inputqueryCommands.strip()=="otypesearch":
		searchcorpstype=input("Enter organization type:")
		cursor = cnDB.files_data.find({"organization.type":{"$regex":searchcorpstype}})
		cursorsize = cnDB.files_data.find({"organization.type":{"$regex":searchcorpstype}}).count()
		for document in cursor:
			print(document)
		orglabel=searchcorpstype
		printpiegraph=input("Do you want to print pie graph y/n: ")
		if printpiegraph.strip()=="y":
			collabgraphs.printgraph(orglabel,cursorsize,totalcnDBsize)
			print("piegraph complete.")
	elif inputqueryCommands.strip()=="isearch":
		searchinterest=input("Enter interest:")
		cursor = cnDB.files_data.find({"interest.name":{"$regex":searchinterest}})
		cursorsize = cnDB.files_data.find({"interest.name":{"$regex":searchinterest}}).count()
		for document in cursor:
			print(document)
		printpiegraph=input("Do you want to print pie graph y/n: ")
		if printpiegraph.strip()=="y":
			size1 = cnDB.files_data.find({"interest.name":{"$regex":searchinterest},"interest.level":1}).count()
			size2 = cnDB.files_data.find({"interest.name":{"$regex":searchinterest},"interest.level":2}).count()
			size3 = cnDB.files_data.find({"interest.name":{"$regex":searchinterest},"interest.level":3}).count()
			size4 = cnDB.files_data.find({"interest.name":{"$regex":searchinterest},"interest.level":4}).count()
			size5 = cnDB.files_data.find({"interest.name":{"$regex":searchinterest},"interest.level":5}).count()
			size6 = cnDB.files_data.find({"interest.name":{"$regex":searchinterest},"interest.level":6}).count()
			size7 = cnDB.files_data.find({"interest.name":{"$regex":searchinterest},"interest.level":7}).count()
			size8 = cnDB.files_data.find({"interest.name":{"$regex":searchinterest},"interest.level":8}).count()
			size9 = cnDB.files_data.find({"interest.name":{"$regex":searchinterest},"interest.level":9}).count()
			size10 = cnDB.files_data.find({"interest.name":{"$regex":searchinterest},"interest.level":10}).count()
			collabgraphs.printlevelgraph(cursorsize,size1,size2,size3,size4,size5,size6,size7,size8,size9,size10,totalcnDBsize)
			print("piegraph")		
	elif inputqueryCommands.strip()=="sksearch":
		searchskill=input("Enter skill:")
		cursor = cnDB.files_data.find({"skill.name":{"$regex":searchskill}})
		cursorsize = cnDB.files_data.find({"skill.name":{"$regex":searchskill}}).count()
		for document in cursor:
			print(document)
		printpiegraph=input("Do you want to print pie graph y/n: ")
		if printpiegraph.strip()=="y":
			size1 = cnDB.files_data.find({"skill.name":{"$regex":searchskill},"skill.level":1}).count()
			size2 = cnDB.files_data.find({"skill.name":{"$regex":searchskill},"skill.level":2}).count()
			size3 = cnDB.files_data.find({"skill.name":{"$regex":searchskill},"skill.level":3}).count()
			size4 = cnDB.files_data.find({"skill.name":{"$regex":searchskill},"skill.level":4}).count()
			size5 = cnDB.files_data.find({"skill.name":{"$regex":searchskill},"skill.level":5}).count()
			size6 = cnDB.files_data.find({"skill.name":{"$regex":searchskill},"skill.level":6}).count()
			size7 = cnDB.files_data.find({"skill.name":{"$regex":searchskill},"skill.level":7}).count()
			size8 = cnDB.files_data.find({"skill.name":{"$regex":searchskill},"skill.level":8}).count()
			size9 = cnDB.files_data.find({"skill.name":{"$regex":searchskill},"skill.level":9}).count()
			size10 = cnDB.files_data.find({"skill.name":{"$regex":searchskill},"skill.level":10}).count()
			collabgraphs.printlevelgraph(cursorsize,size1,size2,size3,size4,size5,size6,size7,size8,size9,size10,totalcnDBsize)
			print("piegraph")
	elif inputqueryCommands.strip()=="fnsearch":
		searchfirstname=input("Enter first name:")
		cursor = cnDB.files_data.find({"first_name":{"$regex":searchfirstname}})
		for document in cursor:
			print(document)
	elif inputqueryCommands.strip()=="lnsearch":
		searchlastname=input("Enter last name:")
		cursor = cnDB.files_data.find({"last_name":{"$regex":searchlastname}})
		for document in cursor:
			print(document)
	elif inputqueryCommands.strip()=="pnsearch":
		searchphonenumber=input("Enter phone number:")
		cursor = cnDB.files_data.find({"phonenumber":{"$regex":searchphonenumber}})
		for document in cursor:
			print(document)
	elif inputqueryCommands.strip()=="unsearch":
		searchusername=input("Enter user name:")
		cursor = cnDB.files_data.find({"username":{"$regex":searchusername}})
		for document in cursor:
			print(document)
	elif inputqueryCommands.strip()=="asearch":
		searchaddress=input("Enter address:")
		cursor = cnDB.files_data.find({"address":{"$regex":searchaddress}})
		for document in cursor:
			print(document)
	elif inputqueryCommands.strip()=="help":
		print(allpossibilities)
	elif inputqueryCommands.strip()=="exit":
		break
	elif inputqueryCommands.strip()=="clear and exit":
		clearneoserver = cypher.execute("MATCH n DETACH DELETE n")
		break