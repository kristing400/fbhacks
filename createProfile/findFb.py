import facebook
import requests

# graph = facebook.GraphAPI(access_token="EAAE8JiSHqYkBAFneWY3hiTHeZBEtPszCbZB3ugCz7cSpewjZCyGstnkVWbsnGJfVZA5MlfFMkRUj6ZCZBDmzl2rKRFZAv6ILocPZAZCxJzPtCQS39xyK0kOM7fpFPaz0ZCHdDsJy7byWy1QJwVRpnwdowZAASidj1yrxC7UbVVZAEnjG4wZDZD", version="2.12")

# Retrieve the number of people who say that they are attending or
# declining  to attend a specific event.
# event = graph.get_object(id='199899257565788',
#                          fields='interested')
# print(event['interested'])

token = 'EAAE8JiSHqYkBAMrSCOAZAneGfGEJUnGMDe5piD2aoDf8KDHqoqWmArEw70pCEkIZBLIrLEK1uZAGZAdMrWZCXZA6A5dHmTIdrQnZBlq63xvGkxr02U6GjOl0tfR2ZAwfBrv7fBMLoltZBGS67acvzWqjFcsHrGUOf4ZCPCtD54dLXNgvsbFrMKZAPcXktf28ZCRq7zHi1yoOWrrfwrSgZAFuLylGZCIPKTZA5e6q0wZD'
event_id = '199899257565788'
interested = requests.get("https://graph.facebook.com/v3.1/"+place+"/interested?access_token="+token)
interested_json = interested.json()
print(interested_json)

# interested = requests.get(“https://graph.facebook.com/v2.7/199899257565788/interested?access_token=EAAE8JiSHqYkBAFneWY3hiTHeZBEtPszCbZB3ugCz7cSpewjZCyGstnkVWbsnGJfVZA5MlfFMkRUj6ZCZBDmzl2rKRFZAv6ILocPZAZCxJzPtCQS39xyK0kOM7fpFPaz0ZCHdDsJy7byWy1QJwVRpnwdowZAASidj1yrxC7UbVVZAEnjG4wZDZD)
# interested_json = interested.json()
# print(interested_json)
