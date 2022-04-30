
from urllib import response
import requests as re
import json

def movie_search():
    query = input("Search movie: ")
    url = "http://www.omdbapi.com/?apikey=6e1729d3&t="+query
    req = re.get(url)
    movie = req.json()

    return movie

'''with open('json/movies.json') as json_file:
    data = json.load(json_file)
    data.append(movie)

nf = open('json/movies.json', 'w')
json.dump(data, nf, indent=4)
nf.close()'''

def create_movie_db():
    lst = []
    file_name = str(input('Name of new file: '))
    
    while True:
        u_action = input('Do you want to add to file {} yes/no: '.format(file_name))
        if u_action.lower() == 'no':
            break
        movie = movie_search()
        if movie['Response'] == 'True':
            print("Movie found!")
            lst.append(movie)
        else:
            print('Sorry no matches found')
        
    with open('json/'+file_name+'.json', 'w') as json_file:
        json.dump(lst, json_file, indent=4)
        json_file.close()
        
    

create_movie_db()