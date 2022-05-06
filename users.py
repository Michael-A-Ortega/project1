from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

client = MongoClient()
db = client['project1']
users_collection = db.users

#querey users credentials 
def log_in (credentials, typ_acct):
        if typ_acct == 'u':
            res = users_collection.find_one({'username': credentials[0], 'password': credentials[1]})
        else:
            res = users_collection.find_one({'username': credentials[0], 'password':credentials[1], 'admin' : True})
        return res
#if username doesnt exist a new documents is inserted in users colletion
def create_user(username, password):
    created = False
    try:
        res = users_collection.insert_one({'username' : username, 'password' : password})
        created = res.acknowledged
    except DuplicateKeyError:
        print('\n\nThat username already exist!! Try a different username\n')
    return created 
#get and print all users watchlist
def get_user_watchlist(username):
        res = users_collection.find_one({'username': username})
        
        if 'watchlist' in list(res):
            if len(res['watchlist']):
                usersList = {}
                print('\t***** WATCHLIST *****\n')
                for watchlists in res['watchlist']:
                    print(' \t  * '+watchlists['name'])
                    usersList[watchlists['name']] = watchlists['list']
                print('\n\t******* END *******\n')
                return usersList    
        return 0
#new watchlist is inserted into users accounts
def create_user_watchlist(username, listname):
    notExist = True
    res = users_collection.find_one({'username': username}, {'watchlist': 1})
    if 'watchlist' in res:
        for i in res['watchlist']:
            if listname in i:
                print('List Already Exist')
                notExist = False
                break
        if notExist:
                res = users_collection.update_one({'username': username}, {'$push': {'watchlist': {'name' : listname, 'list': []}}})
    else:
        res = users_collection.update_one({'username': username}, {'$push': {'watchlist': {'name' : listname, 'list': []}}})
#update users watchlist, add or delete from list
def edit_watchlist(username, action, movie, lst_name):
    filterDb = {'username': username, 'watchlist' : { '$elemMatch': {'name': lst_name}}}

    if action == 'add':
        res = users_collection.update_one(filterDb,{'$push': {'watchlist.$.list': movie}})
        if not res == None:
            print(movie + ' was added to '+lst_name)
    elif action == 'delete':
        res = users_collection.update_one(filterDb,{'$pull': {'watchlist.$.list': {'$regex': movie, '$options': 'i'}}})
        print(movie + ' was deleted to '+lst_name)
#drop a complete list from watchlist
def delete_list(username, lst_name):
    filterDb = {'username': username, 'watchlist' : { '$elemMatch': {'name': lst_name}}}
    res = users_collection.update_one(filterDb, {'$pull': {'watchlist': {'name': lst_name}}})
    print(res.modified_count)
   
        
        
    
        
