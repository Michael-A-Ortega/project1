import requests as re
import json

query = input("Search movie: ")
url = "http://www.omdbapi.com/?apikey=6e1729d3&t="+query
req = re.get(url)
movie = req.json()



with open('json/movies.json') as json_file:
    data = json.load(json_file)
    data.append(movie)
nf = open('json/movies.json', 'w')
json.dump(data, nf, indent=4)
nf.close()
