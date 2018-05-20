# Employee Graph Database

Contributor(s): Gael Blanchard(https://github.com/gaelblanchard), Lloyd Massiah(https://github.com/lmassiah)

Other Version(s):

Requirements: Neo4j, MongoDB, pymongo, py2neo, csv

Installation Instructions:

# Objective(s):
Given csv files that represent organizations, projects, employees and skills initialize 2 databases.
One database is MongoDb and the other is Neo4j. Create a function to find a user and all of their related information. Create functions that can group users by a specific skill, degree,
organization or location. Implement a function to determine users with same interests and skills within a 10 mile distance.
Implement a function to determine a trusted colleague of colleagues. 

# Our Data:
6 seperate csv files that have been provided. Therefore cleanup is not necessary. However if cleanup was necessary we could incorporate seperate procedures on every csv file following these stipulations:

User Csv file: Ensure no repetitions in user_id, and proper formats for all columns

Distance Csv file: Ensure there is no duplicate data and all distance values are non-negative

Interest Csv file: Ensure that Interest Level is a positive integer on the 1-10 scale. Ensure that all user_ids are valid and that all interests are valid

Organization Csv file: Ensure Organization type is either U,C,G. And if another type is added make sure that it is valid.

Project Csv file: Ensure that all columns have the proper format

Skill Csv file: Ensure that Skill Level is a positive integer on the 1-10 scale. Ensure that all user_ids are valid and that all skills are valid

Our data is primarily qualitative with our only quantitative values being the distance between organizations.

# How it Works:
By seperating our objectivs into two categories we can use Neo4j and mongoDB effectively. Leveraging Neo4j's capabilties we are able to return users based on shared interests and skills as well as trusted colleagues of colleagues. Using MongoDB we can use simple queries to return data based on Organzation, Skill and so forth.

# Going Further:
Testing more complex data sets we can infer more diverse relationships. We can also utilize more complex data sets to develop insights based on those complex relationships.
