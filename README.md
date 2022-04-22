# Serendipity AI
Interview task for serendipityai about topics (Flask and Neo4j)

----
### Neo4j - Sandbox database: 
- https://sandbox.neo4j.com/
- Expires: 1st May
----

### Flask API:

/topics/ - GET

- list all the topics
- option parameter: '/name' to filter the Topics

/topics/id/ - GET

- return a single Topic based on the id

/topics/ - POST

- based on the JSON date (name, desc.) create the Topic connected to the User
- unique id generated based on UUID

/topics/id/ - POST

- update the Topic with the given id

/topics/id/ - DELETE

- delete the the Topic and all the relationship

-------

## Security

- Create, Update, Delete only allowed for a Topic if the it is owned by the User

