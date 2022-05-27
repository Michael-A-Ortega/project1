from cmath import e
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import json
import requests as re
client = MongoClient()
db = client['project1']
collection_movies = db.movies
api_key = "YOUR_API_KEY_HERE"
#search for movie in db if found movie detials are returned else None is returned

def search_movie():
    movie = str(input('Search Movie: '))
    data = collection_movies.find_one({'Title' : {'$regex': movie, '$options': 'i'}})
    if not data == None:
        print("\n***FOUND {}***\n".format(movie))
        print('Title: ' + data['Title'])
        print('Year: ' + data['Year'] )
        print('Rated: ' + data['Rated'] )
        print('Duration: ' + data['Runtime'] )
        print('Plot: ' + data['Plot'] )
        print("***********\n")
        return data['Title']
    return None
#inserts movies from json file to db
def add_movies_db(filename):
    try:
        with open('json/'+filename+'.json') as file:
            file_data = json.load(file)
            res = collection_movies.insert_many(file_data)
            print('\n{} documents were inserted\n'.format(len(res.inserted_ids)))
    except BulkWriteError as e:
        print('Oops some records already exist')
        print('\n{} documents were inserted\n'.format(e.details['nInserted']))

#delete movies from db reading from json file
def del_movies_db(filename):
    try:
        with open('json/'+filename+'.json') as file:
            file_data = json.load(file)
            lst_del = []
            query = {'Title': {'$in': lst_del}}
            for title in file_data:
               lst_del.append(title['Title'])
            res = collection_movies.delete_many(query)
            print('\n{} documents were deleted\n'.format(res.deleted_count))

    except e:
        print(e)
        print('Oops something went wrong')
#get random movie from db and return details of the movie       
def get_random_movie():
    query = [{'$sample': {'size': 1}}]
    res = collection_movies.aggregate(query)
    movie = list(res)[0]
    print("Title:{}\n".format(movie['Title']) +
        "Year:{}\n".format(movie['Year'])+
        "Runtime:{}\n".format(movie['Runtime'])+
        "Plot:{}".format(movie['Plot']))

#request movie from api and return results
def movie_search_api():
    query = input("Search movie: ")
    url = f"http://www.omdbapi.com/?apikey={api_key}="+query
    req = re.get(url)
    movie = req.json()

    return movie
#create json file of movies from api results
def create_movie_db():
    lst = []
    file_name = str(input('Name of new file: '))
    
    while True:
        u_action = input('Do you want to add to file {} yes/no: '.format(file_name))
        if u_action.lower() == 'no':
            break
        movie = movie_search_api()
        if movie['Response'] == 'True':
            print("Movie found!")
            lst.append(movie)
        else:
            print('Sorry no matches found')
        
    with open('json/'+file_name+'.json', 'w') as json_file:
        json.dump(lst, json_file, indent=4)
        json_file.close()