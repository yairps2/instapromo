from instagrapi import Client

class Hashtag:

    def __init__(self, client: Client, hashtag: str, mode: str, num: int = 10):
        if mode not in ["recent", "top", "reels"]:
            raise ValueError("Invalid mode. Options: recent, top, reels")
        self.client = client
        self.hashtag = hashtag
        self.mode = mode
        self.num = num

    def find_posts(self) -> list:
        try:
            if self.mode == "reels":
                hashtag_feed = self.client.hashtag_medias_reels_v1(self.hashtag, self.num)
            elif self.mode == "recent":
                hashtag_feed = self.client.hashtag_medias_recent_a1(self.hashtag, self.num)
            elif self.mode == "top":
                hashtag_feed = self.client.hashtag_medias_top_a1(self.hashtag, self.num)
            else:
                raise ValueError("Invalid mode. Options: recent, top, reels")
            return hashtag_feed

        except Exception as e:
            print(f"An error occurred: {e}")