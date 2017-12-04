# Employee-Data-Project
Populate and utilize a datase to return requested data graphically


Gael Blanchard
Lloyd Massiah


Required libraries

Import csv for csv file manipulation

Import pandas as pd

Import sys,getopt,pprint 

Import matplotlib.pyplot as plt  for pie graphs

Import collabheader  defined the help function call in the main Python file

Import collabgraphs  holds code for the pie graph returning functions

From pymongo import MongoClient, ASCENDING  to initialize mongoDB

pymongo.ASCENDING deprecated 

From py2neo import G,a,import cyphererror  To authorize neo4j database and utilize it cypher error allows us to detect errors during the runtime of giving data to the neo4j


Used queries:
Mongodb primary query
cnDB.files_data.find({"address":{"$regex":searchaddress}})
Using the standard query syntax along with regex we can access the address in the database and therefore return it. Just by replacing the address field with interest.name we can access even su document fields




The preceding query is the query designed to answer the first function. We basically reaccess each relation from one user to the other user using a relation chain. This is the standard syntax. The most unique we do in this query is add the get value to define the weight of the interest. The collect statements were used for readability 
