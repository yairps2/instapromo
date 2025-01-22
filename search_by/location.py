from instagrapi import Client
from geopy.geocoders import Nominatim

class Location:
    
    def __init__(self, client: Client, location_query: str, mode: str, num: int = 10):
        self.geolocator = Nominatim(user_agent="instapromo")
        self.client = client
        self.location_query = location_query

        self.mode = mode
        if mode not in ["recent", "top"]:
            raise ValueError("Invalid mode. Options: recent, top")
        
        self.location_pk = None

        location = self.geolocator.geocode(self.location_query)
        if location:
            lat = location.latitude
            lon = location.longitude
            locations = self.client.location_search(lat, lon)
            if locations:
                self.location_pk = locations[0].pk
            else:
                raise ValueError("Instagrapi: Location not found")
        else:
            raise ValueError("Geopy: Location not found")
        
        self.num = num

    def find_posts(self) -> list:
        try:
            if self.mode == "recent":
                location_feed = self.client.location_medias_recent(self.location_pk, self.num)
            else:
                location_feed = self.client.location_medias_top(self.location_pk, self.num)
                
            return location_feed

        except Exception as e:
            print(f"An error occurred: {e}")