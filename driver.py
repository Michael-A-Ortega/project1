import users
import movies

def menu(user):
    while True:
        try:
            print('Show watchlists (1)')
            print('Create a new watchlist (2)')
            print('Edit watchlists (3)')
            print('Remove watchlist (4)')
            print('Quit (5)')
            selection = int(input('Chose an option from above: '))
            if selection not in [1,2,3,4,5]:
                raise(ValueError)

            if selection == 5:
                print('Goodbye ' + user.user_name)
                break

            elif selection == 1:
                lst = user.get_user_watchlist()
                if lst:
                    print(lst)
                else:
                    print('Oops not watchlist found! Create one.')

            elif selection == 2:
                print("\n **Creating a new watchlist**")
                listname = str(input('Name of the list: '))
                user.create_user_watchlist(listname)

            elif selection == 3:
                watchlists = user.get_user_watchlist()
                while True:
                    edit_list = str(input('Name of list to edit: '))
                    if not edit_list in watchlists:
                        print('Invalid list name! Try again')
                    else:
                        print(edit_list)
                        action = input('Modify list add or delete: ')
                        if action == 'add':
                             movie = movies.search_movie()
                             a = input('Do you want to add {} yes/no? >>'.format(movie))
                             user.edit_watchlist('add', movie, edit_list)
                        elif action == 'delete':
                            movie = input('Movie: ')
                            user.edit_watchlist('delete', movie, edit_list)
                        break
        except ValueError:
            print ('\nInvalid Input!!! Choose 1 - 3\n')

def main():

    print('**Welcome to Movie Watchlist**')
    selection = 0
    while True:
        try:
            print('\t   Log In (1)')
            print('\tCreate Account(2)') 
            print('\tRandom Movie (3)')

            selection = int(input('Chose an option from above: '))
            if selection not in [1,2,3]:
                raise(ValueError)
            break
        except ValueError:
            print ('\nInvalid Input!!! Choose 1 - 3\n')
    
    if selection == 1:
        user = ''
        while True:
            username = input('Enter a username: ')
            password = input('Enter password: ')
            user = users.Users(username, password)

            res = user.log_in()

            if res == None:
                print('\nInvalid credentials!!!! Try Again\n')
            else:
                break
        print('\tWELCOME {}'.format(user.user_name))
        menu(user)
  
    if selection == 2:
        user = ''
        while True:
            username = input('Enter a username: ')
            password = input('Enter password: ')
            user = users.Users(username, password)
            if user.create_user():
                break
        menu(user)
if __name__ == '__main__':
    main()