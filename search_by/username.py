from instagrapi import Client

class Username:
    
    def __init__(self, client: Client, username: str, num: int = 10):
        self.client = client
        self.username = username
        self.num = num

    def find_users(self) -> list:
        try:
            user_feed = self.client.user
            return user_feed

        except Exception as e:
            print(f"An error occurred: {e}")