from fileinput import filename
import users
import movies

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
                print('\t***Goodbye ' + user.user_name +'***')
                break

            elif selection == 1:
                lst = user.get_user_watchlist()
               
                if not lst:
                    print('\n\n\tOops no watchlist found! Create one.\n')

            elif selection == 2:
                print("\n\t**Creating a new watchlist**")
                listname = str(input('Name of the list: '))
                user.create_user_watchlist(listname)

            elif selection == 3:
                
                while True:
                    
                    watchlists = user.get_user_watchlist()
                    if not watchlists:
                        print('\n\n\tOops no watchlist found! Create one.\n')
                        break
                    edit_list = str(input('Name of list to edit: '))
                    if not edit_list in watchlists:
                        print('Invalid list name! Try again')
                    else:

                        print("\t    ***"+edit_list+"***")
                        for film in watchlists[edit_list]:
                            print('  * '+ film)

                        while True:
                            action = str(input('\nModify list add or delete or quit: '))
                            if action in ['add', 'delete', 'del', 'quit', 'q']:
                                if action.lower() == 'add':
                                    movie = movies.search_movie()
                                    a = input('Do you want to add {} yes/no? >>'.format(movie))
                                    if a == 'yes':
                                        user.edit_watchlist('add', movie, edit_list)
                                elif action.lower() == 'delete' or action.lower() == 'del':
                                    movie = input('Movie: ')
                                    user.edit_watchlist('delete', movie, edit_list)

                                elif action.lower() == 'quit' or action.lower() == 'q':
                                    break
                            else:
                                print('Oops invalid input!!!!')
                        break
            elif selection == 4:
                watchlists = user.get_user_watchlist()
                del_list = str(input('Name of list to edit: '))
                if not del_list in watchlists:
                    print('Invalid list name! Try again')
                else:
                    user.delete_list(del_list)
        except ValueError:
            print ('\nInvalid Input!!! Choose 1 - 5\n')

def admin_menu(user):
    print('\n***{}***'.format(user.user_name))
    print('Add movies (1)')
    print('Delete movies (2)')
    print('Create new movie file (3)')
    selection = int(input(">>>"))

    if selection == 1:
        filename = str(input('Filename: '))
        movies.add_movies_db(filename)
    elif selection == 2:
        filename = str(input('Filename: '))
        movies.del_movies_db(filename)
    else:
        movies.create_movie_db()
def main():

    print('**Welcome to Movie Watchlist**')
    selection = 0
    while True:
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
    
    if selection == 1:
        #user = ''
        while True:
            username = input('Enter a username: ')
            password = input('Enter password: ')
            user = users.Users(username, password)

            res = user.log_in('u')

            if res == None:
                print('\nInvalid credentials!!!! Try Again\n')
            else:
                break
        print('\n\t**WELCOME {}**\n'.format(user.user_name))
        menu(user)
  
    elif selection == 2:
        user = ''
        while True:
            username = input('Enter a username: ')
            password = input('Enter password: ')
            user = users.Users(username, password)
            if user.create_user():
                break
        menu(user)

    elif selection == 3:
        while True:
            username = input('Enter a username: ')
            password = input('Enter password: ')
            user = users.Users(username, password)
            res = user.log_in('admin')
            if res == None:
                print('\nInvalid credentials!!!! Try Again\n')
            else:
                break
        admin_menu(user)
    else:
        movies.get_random_movie()
        
if __name__ == '__main__':
    main()