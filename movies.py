from cmath import e
from pymongo import MongoClient
from pymongo.errors import BulkWriteError
import json
import requests as re
client = MongoClient()
db = client['project1']
collection_movies = db.movies

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

def add_movies_db(filename):
    try:
        with open('json/'+filename) as file:
            file_data = json.load(file)
            collection_movies.insert_many(file_data) 
    except BulkWriteError:
        print('Oops some records already exist')

def del_movies_db(filename):
    try:
        with open('json/'+filename) as file:
            file_data = json.load(file)
            lst_del = []
            query = {'Title': {'$in': lst_del}}
            for title in file_data:
               lst_del.append(title['Title'])
            res = collection_movies.delete_many(query)

    except e:
        print(e)
        print('Oops something went wrong')
def get_random_movie():
    query = [{'$sample': {'size': 1}}]
    res = collection_movies.aggregate(query)
    movie = list(res)[0]
    print("Title:{}\n".format(movie['Title']) +
        "Year:{}\n".format(movie['Year'])+
        "Runtime:{}\n".format(movie['Runtime'])+
        "Plot:{}".format(movie['Plot']))

def movie_search_api():
    query = input("Search movie: ")
    url = "http://www.omdbapi.com/?apikey=6e1729d3&t="+query
    req = re.get(url)
    movie = req.json()

    return movie

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