#Required Libraries
import csv
import sys
from pymongo import MongoClient, ASCENDING
from py2neo import Graph, authenticate

graph = Graph()
graphformat = {"User" : "user_id" , "Skill" : "name" , "Interest" : "name" , "Organization" : "name" , "Project" : "name"}
totalcnDBsize = 0
allpossibilities = "Possible commands:\nfunc1\nfunc2\nosearch\notypesearch\nisearch\nsksearch\nfnsearch\nlnsearch\npnsearch\nunsearch\nasearch\nhelp\nexit\nclear and exit"

def initialize_input_file():
	if len(sys.argv) == 1:
		file_1=input("Enter file with users with their full names: ")
		file_2=input("Enter file with the users and their projects: ")
		file_3=input("Enter file with the users and their organizations: ")
		file_4=input("Enter file with user and their skills: ")
		file_5=input("Enter file with user and their interests: ")
		file_6=input("Enter file with organizations and their distances: ")
	elif len(sys.argv) == 7:
		file_1=sys.argv[1]
		file_2=sys.argv[2]
		file_3=sys.argv[3]
		file_4=sys.argv[4]
		file_5=sys.argv[5]
		file_6=sys.argv[6]
	else:
		if sys.argv[1] == "help":
			print("You need to enter six files through command line enter files through program:")
		else:
			print("Enter Filenames not enough provided.")
			file_1=input("Enter file with users with their full names: ")
			file_2=input("Enter file with the users and their projects: ")
			file_3=input("Enter file with the users and their organizations: ")
			file_4=input("Enter file with user and their skills: ")
			file_5=input("Enter file with user and their interests: ")
			file_6=input("Enter file with organizations and their distances: ")
	return file_1, file_2, file_3, file_4, file_5, file_6

def initialize_mongo():
	client = MongoClient()
	return client

def initalize_neo():
	authenticate("localhost:7474","neo4j","gael")
	graph = Graph("http://localhost:7474/db/data")

def schema_initialiation(format):
	for each in format:
		try:
			graph.schema.create_uniqueness_constraint(each, graphformat[each])
		except:
			pass

def enter_user(mongo_db,neo_db,user_file):
	cypher = neo_db.cypher
	theUserFile = open(user_file,"r")
	theUserReader = csv.DictReader(theUserFile, fieldnames=['user_id','first_name','last_name','phonenumber','username','address'])
	for each in theUserReader:
		try:
			user_id = mongo_db.files_data.insert_one(each).inserted_id
		except:
			pass
		try:
			create = cypher.execute("MERGE (user:User {user_id:{a}, first_name:{b}, last_name:{c}, phonenumber:{d}, username:{e}, address:{f}}) RETURN user",a=each['user_id'],b=each['first_name'],c=each['last_name'],d=each['phonenumber'],e=each['username'],f=each['address'])
		except:
			print("User Data Not Merged...")

def enter_org(mongo_db,neo_db,org_file):
	cypher = neo_db.cypher
	theOrgFile = open(org_file,"r")
	theOrganizationReader = csv.DictReader(theOrgFile, fieldnames=['user_id','organization','organization_type'])
	for each in theOrganizationReader:
		try:
			org_insert = mongo_db.files_data.update({'user_id':each['user_id']},{'$set':{'organization':{'name': each['organization'], 'type':each['organization_type']}}})
		except:
			pass
		try:
			create = cypher.execute("MATCH (user {user_id:{a}}) SET user.organization.name={b},user.organization.type={c} RETURN user", a=each['user_id'],b=each['organization'],c=each['organization_type'])
		except:
			print("User not linked to Organization...")
		try:
			create = cypher.execute("MERGE (org:Org {name:{a}, type:{b}})", a=each['organization'],b=each['organization_type'])
		except:
			print("Organization Data Not Merged...")
		try:
			create = cypher.execute("MATCH (org:Org {name:{b}}), (user:User {user_id:{a}})"+"MERGE (user)-[rel:workedat]->(org)",a=each['user_id'],b=each['organization'])
		except:
			print("Worked At relationship not linked...")

def enter_proj(mongo_db,neo_db,proj_file):
	cypher = neo_db.cypher
	theProjectfile = open(proj_file,"r")
	theProjectReader = csv.DictReader(theProjectfile, fieldnames=['user_id','project'])
	cypher=graph.cypher
	for each in theProjectReader:
		try:
			project_insert = mongo_db.files_data.update({'user_id':each['user_id']},{'$set':{'projects': {'name':each['project']}}})
		except:
			pass
		try:
			create = cypher.execute("MERGE (project:Project {name:{a}})", a=each['project'])
		except:
			print("Project Data Not Merged...")
		try:
			create = cypher.execute("MATCH (project:Project {name:{b}}), (user:User {user_id:{a}})"+"MERGE (user)-[rel:workedon]->(project)",a=each['user_id'],b=each['project'])
		except:
			print("Worked On relationship not linked...")

def enter_skills(mongo_db,neo_db,skill_file):
	cypher = neo_db.cypher
	theSkillfile = open(skill_file,"r")
	theSkillReader = csv.DictReader(theSkillfile, fieldnames=['user_id','skill','skill level'])
	for each in theSkillReader:
		try:
			each['skill level']=int(each['skill level'])
		except ValueError:
			continue
		try:
			skill_insert = mongo_db.files_data.update({'user_id':each['user_id']},{'$set':{'skill':{'name':each['skill'], 'level':each['skill level']}}})
		except:
			pass
		try:
			create = cypher.execute("MERGE (skill:Skill {name:{a},level:{b}})",a=each['skill'],b=each['skill level'])
		except:
			print("Skill Data Not Merged...")
		try:
			create = cypher.execute("MATCH (skill:Skill {name:{a}}),(user:User {user_id:{c}})"+"MERGE (user)-[rel:skilledin {weight: {b}}]->(skill)", a=each['skill'],b=each['skill level'],c=each['user_id'])
		except:
			print("Skilled in relationship not linked...")

def enter_interest(mongo_db,neo_db,interest_file):
	cypher = neo_db.cypher
	theInterestfile = open(interest_file,"r")
	theInterestReader= csv.DictReader(theInterestfile, fieldnames=['user_id','interest','interest level'])
	cypher=graph.cypher
	for each in theInterestReader:
		try:
			each['interest level']=int(each['interest level'])
		except ValueError:
			continue
		try:
			interest_insert = cnDB.files_data.update({'user_id':each['user_id']},{'$set':{'interest':{'name':each['interest'], 'level':each['interest level']}}})
		except:
			pass
		try:
			create = cypher.execute("MERGE (interest:Interest {name:{a}, level:{b}})",a=each['interest'],b=each['interest level'])
		except:
			print("Interest Data Not Merged...")
		try:
			create = cypher.execute("MATCH (interest:Interest {name:{a}}), (user:User {user_id:{c}})"+"MERGE (user)-[r:interestedin {level: {b}}]->(interest)",a=each['interest'],b=each['interest level'],c=each['user_id'])
		except:
			print("Interested In relationship not linked...")

def enter_distance(mongo_db,neo_db,distance_file):
	cypher = neo_db.cypher
	theDistancefile = open(distance_file,"r")
	theDistanceReader = csv.DictReader(theDistancefile, fieldnames=['organization_1','organization_2','distance'])
	cypher=graph.cypher
	for each in theDistanceReader:
		try:
			each['distance'] = float(each['distance'])
		except ValueError:
			continue
		try:
			create=cypher.execute("MATCH (org1:Org {name:{a}}),(org2:Org {name:{b}})"+"CREATE (org1)-[rel:distance {miles: {c}}]->(org2)",a=each['organization_1'],b=each['organization_2'],c=each['distance'])
		except:
			print("Distance relationship not linked...")

def report_database_size(mongo_db):
	total_database_size = mongo_db.files_data.find().count()
	totalcnDBsize = total_database_size
	print("Total Database Size: ",total_database_size)

def retrieve_int_in_data(neo_db):
	cypher = neo_db.cypher
	userinput = input("Enter Username: ")
	gettheuser = cypher.execute("MATCH (user:User {username:{a}})-[:interestedin]->(interest)<-[getvalue:interestedin]-(otheruser:User) MATCH (otheruser:User)-[:workedat]->(org:Org) MATCH (anotheruser:User)-[:workedat]->(b:Org) MATCH (org:Org)<-[r:distance]->(b:Org) WHERE r.miles <= 10 MATCH (b:Org)<-[:workedat]-(user:User) WITH user,otheruser,collect(distinct b.name) as organization,collect(distinct interest.name) as matchedinterest,collect(distinct r.miles) as distance,collect(distinct getvalue.level) as interestlevel RETURN DISTINCT otheruser.username, matchedinterest, distance, organization, interestlevel ORDER BY otheruser.username DESCENDING", a=userinput)
	return gettheuser

def retrieve_trusted_colleagues(neo_db):
	cypher = neo_db.cypher
	userinput = input("Enter username to return trusted colleagues: ")
	gettrustedcolleagues = cypher.execute("match (user:User {username:{usersinput}}),(thecollabuser:User)-[:workedon]->(project)<-[:workedon]-(theothercollabuser:User),(thecollabuser)-[:interestedin]-(interest) WITH user,thecollabuser,project, collect(user.username) as originaluser, collect(thecollabuser.phonenumber) as phonenumber, theothercollabuser, collect (project.name) as collabproject, collect(interest.name) as particularinterests WHERE thecollabuser.user_id<>user.user_id AND theothercollabuser.user_id<>user.user_id AND thecollabuser<>theothercollabuser RETURN DISTINCT originaluser,thecollabuser.username,collabproject,phonenumber, particularinterests ORDER BY thecollabuser.username DESCENDING",usersinput = userinput)
	return gettrustedcolleagues

def retrieve_user_data(mongo_db):
	idnumber=input("Enter user id or username:")
	cursor = mongo_db.files_data.find({"username":idnumber},{"first_name":1,"last_name":1,"phonenumber":1,"address":1,"organization":1})
	for document in cursor:
		print(document)

def org_search(mongo_db):
	searchcorps=input("Enter organization: ")
	cursor = mongo_db.files_data.find({"organization.name":{"$regex":searchcorps}})
	databasesize= mongo_db.files_data.find().count()
	cursorsize = mongo_db.files_data.find({"organization.name":{"$regex":searchcorps}}).count()
	for document in cursor:
		print(document)
	orglabel = searchcorps

def org_type_search(mongo_db):
	searchcorpstype=input("Enter organization type:")
	cursor = mongo_db.files_data.find({"organization.type":{"$regex":searchcorpstype}})
	cursorsize = mongo_db.files_data.find({"organization.type":{"$regex":searchcorpstype}}).count()
	for document in cursor:
		print(document)
	orglabel=searchcorpstype

def interest_search(mongo_db):
	searchinterest=input("Enter interest:")
	cursor = mongo_db.files_data.find({"interest.name":{"$regex":searchinterest}})
	cursorsize = mongo_db.files_data.find({"interest.name":{"$regex":searchinterest}}).count()
	for document in cursor:
		print(document)

def skill_search(mongo_db):
	searchskill=input("Enter skill: ")
	cursor = mongo_db.files_data.find({"skill.name":{"$regex":searchskill}})
	cursorsize = mongo_db.files_data.find({"skill.name":{"$regex":searchskill}}).count()
	for document in cursor:
		print(document)

def first_name_search(mongo_db):
	searchfirstname = input("Enter first name:")
	cursor = mongo_db.files_data.find({"first_name":{"$regex":searchfirstname}})
	for document in cursor:
		print(document)

def last_name_search(mongo_db):
	searchlastname=input("Enter last name:")
	cursor = mongo_db.files_data.find({"last_name":{"$regex":searchlastname}})
	for document in cursor:
		print(document)

def phone_search(mongo_db):
	searchphonenumber=input("Enter phone number:")
	cursor = mongo_db.files_data.find({"phonenumber":{"$regex":searchphonenumber}})
	for document in cursor:
		print(document)

def user_name_search(mongo_db):
	searchusername=input("Enter user name:")
	cursor = mongo_db.files_data.find({"username":{"$regex":searchusername}})
	for document in cursor:
		print(document)

def address_search(mongo_db):
	searchaddress=input("Enter address:")
	cursor = mongo_db.files_data.find({"address":{"$regex":searchaddress}})
	for document in cursor:
		print(document)

def helpmessage():
	print("func1 --- For a university user find users with same interests and skills within a 10 mile distance\n")
	print("func2 --- For a user find the trusted collegaues of colleages")
	print("func3 --- For a user return personal information")
	print("fnsearch - Given first name return all users")
	print("lnsearch - Given last name return all users")
	print("unsearch - Given user name return all users")
	print("asearch - Given user name return all users")
	print("pnsearch - Given phone number return all users")
	print("osearch - For an organization return all affiliated users")
	print("otypesearch - For an organization type return all affiliated users")
	print("dsearch - For a degree return a list of users with that degree")
	print("sksearch- For a skill return all users that have it")
	print("isearch - For an interests return all users that have it")
	print("help ---- Print this message and return to option prompt")

file_1, file_2, file_3, file_4, file_5, file_6 = initialize_input_file()
cnDB = initialize_mongo().primerodos
initalize_neo()
schema_initialiation(graphformat)
#create index based off user id in the mongoDB
cnDB.files_data.create_index([('user_id', ASCENDING)], unique=True)
enter_user(cnDB,graph,file_1)
enter_org(cnDB,graph,file_3)
enter_proj(cnDB,graph,file_2)
enter_skills(cnDB,graph,file_4)
enter_interest(cnDB,graph,file_5)
enter_distance(cnDB, graph, file_6)
report_database_size(cnDB)
#Our Interface
while True:
	inputqueryCommands = input("Enter a command to execute:")
	if inputqueryCommands.strip()=="func1":
		interested_distance_data = retrieve_int_in_data(graph)
		print(interested_distance_data)
	elif inputqueryCommands.strip()=="func2":
		trusted_colleague_data = retrieve_trusted_colleagues(graph)
		print(trusted_colleague_data)
	elif inputqueryCommands.strip()=="func3":
		retrieve_user_data(cnDB)
	elif inputqueryCommands.strip()=="osearch":
		org_search(cnDB)
	elif inputqueryCommands.strip()=="otypesearch":
		org_type_search(cnDB)
	elif inputqueryCommands.strip()=="isearch":
		interest_search(cnDB)
	elif inputqueryCommands.strip()=="sksearch":
		skill_search(cnDB)
	elif inputqueryCommands.strip()=="fnsearch":
		first_name_search(cnDB)
	elif inputqueryCommands.strip()=="lnsearch":
		last_name_search(cnDB)
	elif inputqueryCommands.strip()=="pnsearch":
		phone_search(cnDB)
	elif inputqueryCommands.strip()=="unsearch":
		user_name_search(cnDB)
	elif inputqueryCommands.strip()=="asearch":
		address_search(cnDB)
	elif inputqueryCommands.strip()=="help":
		helpmessage()
	elif inputqueryCommands.strip()=="exit":
		break