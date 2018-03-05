from uber_rides.session import Session
session = Session(server_token='qZLzWGMbxgTW4uZIlE0zZ7OA2oQRwV88qyVIyi3a')
from uber_rides.client import UberRidesClient
client = UberRidesClient(session)

response = client.get_price_estimates(
    start_latitude=-22.894925, 
    start_longitude=-43.294089,
    end_latitude=-22.941335,  
    end_longitude=-43.202743,
    seat_count=2
)
estimate = response.json.get('prices')
print (estimate)
print (estimate[0]['display_name'], estimate[0]['estimate'])
