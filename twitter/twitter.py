from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
        quit()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        valid = False
        while valid == False:
            valid = True
            handle = input("What will your twitter handle be?\n")
            password = input("Enter a password:\n")
            password2 = input("Re-enter your password:\n")
            users = db_session.query(User).all()
            if password != password2:
                print("Those passwords don't match. Try again.\n")
                valid = False
            for user in users:
                if user.username == handle:
                    print("That username is already taken. Try again.\n")
                    valid = False

        new_user = User(username=handle, password=password)
        db_session.add(new_user)
        db_session.commit()

        print(f"Welcome {handle}!")


    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        correct = False
        while correct == False:
            username = input("Username: ")
            password = input("Password: ")
            users = db_session.query(User).all()
            for user in users:
                if (username == user.username) & (password == user.password):
                    print(f"Welcome {user.username}!\n")
                    correct = True
            if correct == False:
                print("Invalid username or password")

    
    def logout(self):
        print("You've been logged out successfully.")

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        while True:
            print("Please select a menu option:")
            print("1. Login")
            print("2. Register User")
            print("0. Exit\n")
            option = input()
            if option == "1":
                self.login()
                break
            elif option == "2":
                self.register_user()
                break
            elif option == "0":
                self.end()
                break
            else:
                print("That's not an option!")
                


    def follow(self):
        pass

    def unfollow(self):
        pass

    def tweet(self):
        pass
    
    def view_my_tweets(self):
        pass
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

        self.print_menu()
        option = int(input(""))

        if option == 1:
            self.view_feed()
        elif option == 2:
            self.view_my_tweets()
        elif option == 3:
            self.search_by_tag()
        elif option == 4:
            self.search_by_user()
        elif option == 5:
            self.tweet()
        elif option == 6:
            self.follow()
        elif option == 7:
            self.unfollow()
        else:
            self.logout()
        
        self.end()
