from instagrapi import Client
import re
from sql import add_user
import random

############# SETTINGS #############   שם משתמש וסיסמה 
# Instagram account login
email = "agitatormicha@gmail.com"
password = "72217221Mike8295301"

# Hashtag to search for     האשטאג הרצוי לחיפוש
hashtag = "zamna"

# Number of new users to find   סבב של כמה חיפושים במכה
required_new_users = random.randint(30, 52)

# Recent / Top / Reels posts (options: recent, top, reels)   איפה לחפש בפוסטים אחרונים או בטופ פוסטים או ברילס 
mode = "reels"
###################################

try:
    client = Client()
    client.login(email, password)
except Exception as e:
    print(f"An error occurred: {e}")

#######################################################################

def find_posts_by_hashtag(hashtag: str, num = 3) -> list:
    try:
        # Get the hashtag feed
        if mode == "reels":
            hashtag_feed = client.hashtag_medias_reels_v1(hashtag, num)
        elif mode == "recent":
            hashtag_feed = client.hashtag_medias_recent(hashtag, num)
        else:
            hashtag_feed = client.hashtag_medias_top(hashtag, num)
        return hashtag_feed

    except Exception as e:
        print(f"An error occurred: {e}")

#######################################################################

def get_usernames_from_posts(posts: list) -> list:
    usernames = []
    for post in posts:
        username = post.user.username
        if username not in usernames:
            usernames.append(username)
    return usernames
    
#######################################################################

def get_user_info_from_username(username: str) -> str:
    try:
        # Get the user info
        user_info = client.user_info_by_username(username)

        # Find the email in the bio
        email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", user_info.biography)

        return [user_info.username, user_info.full_name, user_info.follower_count, user_info.biography, user_info.public_email, user_info.contact_phone_number, user_info.bio_links, email]
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
#######################################################################

if __name__ == "__main__":
    # step 1: find posts by hashtag
    posts = find_posts_by_hashtag(hashtag, required_new_users)

    # step 2: get usernames from posts
    users = get_usernames_from_posts(posts)

    # step 3: get user info from username
    user_infos = []
    for user in users:
        print(f"Getting info for user: {user}")
        user_info = get_user_info_from_username(user)
        if user_info:
            user_infos.append(user_info)
        add_user(user_info)