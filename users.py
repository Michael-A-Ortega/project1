from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
class Users:

    def __init__(self, user_name, password):
        self.user_name = user_name 
        self.password = password
        self.client = MongoClient()
        self.db = self.client['project1']
        self.collection = self.db.users
        
    def log_in (self, typ_acct):
        if typ_acct == 'u':
            res = self.collection.find_one({'username': self.user_name, 'password': self.password})
        else:
            res = self.collection.find_one({'username': self.user_name, 'password': self.password, 'admin' : True})

        return res

    def create_user(self):
       

        try:
            res = self.collection.insert_one({'username' : self.user_name, 'password' : self.password})
            return 1
        except DuplicateKeyError:
            print('\n\nThat username already exist!! Try a different username\n')
            return 0
       
    def get_user_watchlist(self):
        res = self.collection.find_one({'username': self.user_name})
        
        if 'watchlist' in list(res):
            if len(res['watchlist']):
                usersList = {}
                print('*****WATCHLIST*****\n')
                for watchlists in res['watchlist']:
                    print(' * '+watchlists['name'])
                    usersList[watchlists['name']] = watchlists['list']
                print('*****END*****\n')
                return usersList    
        return 0
    def create_user_watchlist(self, listname):
        notExist = True
        res = self.collection.find_one({'username': self.user_name}, {'watchlist': 1})
        if 'watchlist' in res:
            for i in res['watchlist']:
                if listname in i:
                    print('List Already Exist')
                    notExist = False
                    break
            if notExist:
                res = self.collection.update_one({'username': self.user_name}, {'$push': {'watchlist': {'name' : listname, 'list': []}}})
        else:
           res = self.collection.update_one({'username': self.user_name}, {'$push': {'watchlist': {'name' : listname, 'list': []}}})
      
        """if listname in :
            print('List already exist')"""
        #res = self.collection.update_one({'username': self.user_name}, {'$push': {'watchlist': {listname : []}}})
    def edit_watchlist(self, action, movie, lst_name):
        filterDb = {'username': self.user_name, 'watchlist' : { '$elemMatch': {'name': lst_name}}}

        if action == 'add':
            res = self.collection.update_one(filterDb,{'$push': {'watchlist.$.list': movie}})
            if not res == None:
                print(movie + ' was added to '+lst_name)
        elif action == 'delete':
            res = self.collection.update_one(filterDb,{'$pull': {'watchlist.$.list': {'$regex': movie, '$options': 'i'}}})
            print(movie + ' was deleted to '+lst_name)
    
    def delete_list(self, lst_name):
        filterDb = {'username': self.user_name, 'watchlist' : { '$elemMatch': {'name': lst_name}}}
        res = self.collection.update_one(filterDb, {'$pull': {'watchlist': {'name': lst_name}}})
        
        
    
        
