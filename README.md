# Foundation project: TO:WATCHLIST
## Description

This program lets users create accounts in which they can create multiple lists that keep track of movies or shows. Users get movies from the database. Users are free to update their list or completely drop the list. Only the admin is allowed to add or delete movies to the database. The admin can use a movie API to search for movies to add to the database. 

## Technologies

 - Python 3
	 - Modules
		 - Pymongo, Json, Request
 - MongoDB
 - VsCode
 - GitHub
 
 ## Features
 
 - CLI application
 - Imports movies json files to database
 - Delete movies from database
 - Create accounts 
 - Update or delete lists
 - Create json file of movies 
 - Search movies from API http://www.omdbapi.com/
 

TODO

 - Add movie suggestions if movie is not found in the database
 - Refactor code
 - Finish documentation
 
 ## SETUP
 -  Follow these steps to setup mongoDB [guide install mongoDB](https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb#:~:text=To%20establish%20a%20connection%20to,you%20use%20the%20MongoClient%20class.&text=The%20%E2%80%9C,create%20your%20MongoDB%20connection%20string.)
 
 - git clone https://github.com/Michael-A-Ortega/project1.git
 - Get an API key from http://www.omdbapi.com/
 - Add api key to movie.py line 9
 - py driver.py
 
