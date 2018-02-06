import requests
from nap.url import Url

#pr2hub = 

# name
GET_PLAYER_INFO = "https://pr2hub.com/get_player_info_2.php"

# name|id, getMembers
GET_GUILD_INFO = "https://pr2hub.com/guild_info.php"

async def get_info(player_name, get_members):
    if get_members:
        get_members = "yes"
    else:
        get_members = "no"
    body = {
        "name" : player_name,
        "getMembers" : get_members
    }
    requests.get(GET_PLAYER_INFO, body)