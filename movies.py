from pymongo import MongoClient

client = MongoClient()
db = client['project1']
collection_movies = db.movies

def search_movie():
    movie = input('Search Movie: ')
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