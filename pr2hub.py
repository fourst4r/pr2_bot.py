from nap.url import Url

pr2hub = Url("https://pr2hub.com")
levels = pr2hub.join("levels")
files = pr2hub.join("files")

def __error_check(response):
    if response.content.startswith("error="):
        raise PR2HubError(response.content[6:])
    elif response.content.startswith("{error:\""):
        raise PR2HubError(response.content[8:2])

def get_player_info(player_name : str):
    """returns a Player class instance"""
    resp = pr2hub.get("get_player_info_2.php", params={
        "name" : player_name
    })
    __error_check(resp)
    return Player(resp.json())

def get_guild_info(guild_name : str, get_members : bool):
    """returns a Guild class instance"""
    if get_members:
        get_members = "yes"
    else:
        get_members = "no"

    resp = pr2hub.get("guild_info.php", params={
        "name" : guild_name,
        "getMembers" : get_members
    })
    __error_check(resp)
    return resp.content

def get_servers_info():
    """returns a list of Server class instances"""
    resp = files.get("server_status_2.txt")
    __error_check(resp)

    servers = []
    for server_info in resp.json()["servers"]:
        servers.append(Server(server_info))

    return servers

class Server:
    def __init__(self, json):
        self.id = json["server_id"]
        self.name = json["server_name"]
        self.address = json["address"]
        self.port = json["port"]
        self.population = json["population"]
        self.status = json["status"]
        self.guild_id = json["guild_id"]
        self.is_tournament = json["tournament"]
        self.is_happy_hour = json["happy_hour"]

        if self.is_tournament == "0":
            self.is_tournament = False
        else:
            self.is_tournament = True

        if self.is_happy_hour == "0":
            self.is_happy_hour = False
        else:
            self.is_happy_hour = True


# class Guild:
#     def __init__(self, json):
#         self.name = 

class Player:
    def __init__(self, json):
        self.id = json["userId"]
        self.name = json["name"]
        self.rank = json["rank"]
        self.hats = json["hats"]
        self.status = json["status"]
        self.login_date = json["loginDate"]
        self.register_date = json["registerDate"]
        self.group = json["group"]
        self.guild_id = json["guildId"]
        self.guild_name = json["guildName"]
        
        self.hat = self.Part(json["hat"], json["hatColor"], json["hatColor2"])
        self.head = self.Part(json["head"], json["headColor"], json["headColor2"])
        self.body = self.Part(json["body"], json["bodyColor"], json["bodyColor2"])
        self.feet = self.Part(json["feet"], json["feetColor"], json["feetColor2"])

        if self.register_date == "1/Jan/1970":
            self.register_date = "Age of Heroes"

        if self.group == "0":
            self.group = "Guest"
        elif self.group == "1":
            self.group = "Member"
        elif self.group == "2":
            self.group = "Moderator"
        else:
            self.group = "Admin"

    class Part:
        def __init__(self, id, color_1, color_2):
            self.id = id
            self.color_1 = color_1
            self.color_2 = color_2

class PR2HubError(Exception):
    pass