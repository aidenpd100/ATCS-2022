from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    active_user = None

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
        self.active_user = new_user


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
                    self.active_user = user
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
        users = db_session.query(User).all()
        following = self.active_user.following
        follow = input("\nWho would you like to follow?\n")
        exists = False
        new = True
        for user in users:
            if follow == user.username:
                exists = True
                followed_user = user
                for u in following:
                    if follow == u.username:
                        print("You already follow " + follow)
                        new = False
        if exists == False:
            print("That user doesn't exist!")
        elif exists == True & new == True:
            self.active_user.following.append(followed_user)
            db_session.commit()
            print("You are now following " + follow)


    def unfollow(self):
        users = db_session.query(User).all()
        following = self.active_user.following
        exists = False
        is_following = False
        unfollow = input("\nWho would you like to unfollow?\n")
        for user in users:
            if unfollow == user.username:
                exists = True
                unfollowed_user = user
                for u in following:
                    if unfollow == u.username:
                        is_following = True
        if exists == False:
            print("That user doesn't exist!")
        elif is_following == False:
            print("You don't follow " + unfollow)
        elif exists == True & is_following == True:
            self.active_user.following.remove(unfollowed_user)
            db_session.commit()
            print("You no longer follow " + unfollow)


    def tweet(self):
        content = input("Create Tweet: ")
        tags = input("Enter your tags separated by spaces: ")
        timestamp = datetime.now()
        tweet = Tweet(content=content, timestamp=timestamp, username=self.active_user.username)

        for t in tags.split():
            existing_tag = db_session.query(Tag).where(Tag.content == t).first()
            if not existing_tag:
                new_tag = Tag(content=t)
                tweet.tags.append(new_tag)
            else:
                tweet.tags.append(existing_tag)
        db_session.add(tweet)
        db_session.commit()




    
    def view_my_tweets(self):
        self.print_tweets(self.active_user.tweets)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        following = self.active_user.following
        followed_tweets = db_session.query(Tweet).where(Tweet.username.in_([u.username for u in following])).order_by(Tweet.id.desc()).all()[:5]
        self.print_tweets(followed_tweets)

    def search_by_user(self):
        username = input("Username: ")
        users = db_session.query(User).all()
        for u in users:
            if username == u.username:
                tweets = db_session.query(Tweet).where(Tweet.username == username).order_by(Tweet.id.desc()).all()
                self.print_tweets(tweets)
                return 
        print("There is no user by that name")
        
        

    def search_by_tag(self):
        tag_name = input("Tag: ")
        tag = db_session.query(Tag).where(Tag.content == tag_name).first()
        if not tag:
            print("There are no tweets with this tag")
        else:
            tweets = db_session.query(Tweet).where((Tweet.id == TweetTag.tweet_id) & (TweetTag.tag_id == Tag.id) & (Tag.id == tag.id)).all()
            self.print_tweets(tweets)

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

        while True:
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
            

