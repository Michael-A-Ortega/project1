from ast import While
from fileinput import filename
import users
import movies
import logging


logging.basicConfig(filename='watchlist.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
def menu(user):
    while True:
        try:
            print('\tShow watchlists (1)')
            print('    Create a new watchlist (2)')
            print('\tEdit watchlists (3)')
            print('\tRemove watchlist (4)')
            print('\t    Quit (5)')
            selection = int(input('Chose an option from above: '))
            if selection not in [1,2,3,4,5]:
                raise(ValueError)

            if selection == 5:
                print('\t***Goodbye ' + user[0] +'***')
                break

            elif selection == 1:
                #get_user_watchlist fetches from the database for users watchlist and prints list
                #if no list exit then int(0) is return
                lst = users.get_user_watchlist(user[0])
                #If no list exist then we prompt the users to create some
                if not lst:
                    print('\n\nOops no watchlist found! Create one.\n')

                else:
                    while True:
                        #users can choose to view items in a specific list
                        edit = input('View list in detail or quit: ')
                        #validate whether the user input is list 
                        if not edit in lst and not edit == 'quit':
                            print('{} is not a watchlist try again!'.format(edit))
                        elif edit == 'quit':
                            break
                        else:
                            #print each movies in the list specified
                            for movie in lst[edit]:
                                print("\t"+movie)
                            print('\n')
                            break
                    
            elif selection == 2:
                print("\n\t**Creating a new watchlist**")
                listname = str(input('Name of the list: '))
                #insert a new watchlist to database
                users.create_user_watchlist(user[0],listname)

            elif selection == 3:
                
                while True:
                    #print watchlist if any exist
                    watchlists = users.get_user_watchlist(user[0])
                    if not watchlists:
                        print('\n\nOops no watchlist found! Create one.\n')
                        break
                    edit_list = str(input('Name of list to edit: '))
                    #check if list exist in db
                    if not edit_list in watchlists:
                        print('Invalid list name! Try again')
                    else:
                        while True:
                            watchlists = users.get_user_watchlist(user[0])
                            #movies in list are shown
                            print("\t    ***"+edit_list+"***")
                            for film in watchlists[edit_list]:
                                print('  * '+ film)

                            action = str(input('\nModify list add or delete or quit: '))

                            if action in ['add', 'delete', 'del', 'quit', 'q']:
                                if action.lower() == 'add':
                                    #search for movie in db
                                    movie = movies.search_movie()
                                    if movie == None:
                                        print("\nOops!! We don't have to movie yet!")
                                        print("Try another search!")
                                    else:
                                        a = input('Do you want to add {} yes/no? >>'.format(movie))
                                        if a == 'yes':
                                            #add movies to watchlist
                                            users.edit_watchlist(user[0],'add', movie, edit_list)

                                elif action.lower() == 'delete' or action.lower() == 'del':
                                    movie = input('Movie: ')
                                    #delete movie from watchlist
                                    users.edit_watchlist(user[0],'delete', movie, edit_list)

                                elif action.lower() == 'quit' or action.lower() == 'q':
                                    break
                            else:
                                print('Oops invalid input!!!!')
                        break
            elif selection == 4:
                #delete list from db
                watchlists = users.get_user_watchlist(user[0])
                if not watchlists:
                    print('\n\n\tYou have no list!\n')
                else:
                    del_list = str(input('Name of list to edit: '))
                    if not del_list in watchlists:
                        print('Invalid list name! Try again')
                    else:
                        users.delete_list(user[0], del_list)
        except ValueError:
            print ('\nInvalid Input!!! Choose 1 - 5\n')

def admin_menu(user):
    print('\n***{}***'.format(user))
    #loop until admin quits
    while True:
        #try validates users input only 1-4 is valid
        try:
            print('Add movies (1)')
            print('Delete movies (2)')
            print('Create new movie file (3)')
            print('Quit (4)')
            selection = int(input(">>>"))
            if selection not in [1,2,3,4]:
                raise(ValueError)
            if selection == 1:
                filename = str(input('Filename: '))
                #add movies looks for file name in  /json directory
                #uses json file to insert into database
                movies.add_movies_db(filename)
            elif selection == 2:
                #del_movies takes json file and deletes movies from database
                filename = str(input('Filename: '))
                movies.del_movies_db(filename)
            elif selection == 3:
                #create_movie_db creates a json file into dir /json
                movies.create_movie_db()
            else:
                break

        except ValueError:
            print('\n\nInvalid input!!\n')


def main():

    print('**Welcome to  #TOWATCH**')
    selection = 0
    while True:
        #validate the user input make sure its one of the options
        try:
            print('\t   Log In (1)')
            print('\tCreate Account(2)')
            print('\t   Admin (3)')
            print('\tRandom Movie (4)')

            selection = int(input('Chose an option from above: '))
            if selection not in [1,2,3,4]:
                raise(ValueError)
            break
        except ValueError:
            print ('\nInvalid Input!!! Choose 1 - 3\n')

    # user input decides whether to login, create account, or get random movie
    if selection == 1:
        attempts = 3
        while True:
            username = input('Enter a username: ')
            password = input('Enter password: ')
            res = users.log_in([username, password], 'u')
            #if credentials are invalid the users has to resubmit new credtials
            #only gets 3 attempts after 3 unsuccessful attempts program ends
            if res == None:
                print('\nInvalid credentials!!!! Try Again\n')
                logging.info('USER: %s failed to login. Invalid credentials', username)
                attempts -=1
                if attempts < 1:
                    print('Sorry out of attemps! now ending program .....')
                    quit()
            else:
                break
        #user logged in successfuly and is promted with menu
        print('\n\t**WELCOME {}**\n'.format(username))
        menu([username, password])
    #user creates a new account, username has to be unique otherwise error will prompt
    elif selection == 2:
        
        while True:
            username = input('Enter a username: ')
            password = input('Enter password: ')
            res = users.create_user(username, password)
            if res:
                break
        menu([username, password])
    
    #3 option is for admin login, if login fails 3 times then program ends
    elif selection == 3:
        attempts = 3
        while True:
            username = input('Enter a username: ')
            password = input('Enter password: ')
           
            res = users.log_in([username, password], 'a')
            if res == None:
                attempts -=1
                logging.info("Users failed to loggin. Invalid credentials")
                print('\nInvalid credentials!!!! Try Again\n')
                if attempts < 1:
                    print('Sorry out of attemps! program ending.....')
                    quit()
            else:
                break
        #different menu for admin is called
        admin_menu(username)
    #Final options is get a random movie from database
    else:
        movies.get_random_movie()
        
if __name__ == '__main__':
    main()