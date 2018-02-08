from nap.url import Url

pr2hub = Url("https://pr2hub.com/")
levels = pr2hub.join("levels/")
files = pr2hub.join("files/")

def __error_check(response):
    """checks if a pr2hub response is an error"""
    if response.content.startswith(b"error="):
        raise PR2HubError(str(response.content)[6:])
    elif response.content.startswith(b"{\"error\":\""):
        raise PR2HubError(response.json()["error"])

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
    return Guild(resp.json())

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
        self.population = int(json["population"])
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

class Guild:
    def __init__(self, json):
        guild_json = json["guild"]
        members_json = json["members"]

        self.name = guild_json["guild_name"]
        self.id = guild_json["guild_id"]
        self.creation_date = guild_json["creation_date"]
        self.active_date = guild_json["active_date"]
        self.member_count = int(guild_json["member_count"])
        self.active_count = int(guild_json["active_count"])
        self.emblem = guild_json["emblem"]
        self.gp_today = guild_json["gp_today"]
        self.gp_total = int(guild_json["gp_total"])
        self.owner_id = guild_json["owner_id"]
        self.note = guild_json["note"]
        self.members = []

        if self.gp_today == None:
            self.gp_today = 0
        else:
            self.gp_today = int(self.gp_today)

        for member_json in members_json:
            self.members.append(self.Member(member_json))

    class Member:
        def __init__(self, json2):
            self.id = json2["user_id"]
            self.name = json2["name"]
            self.group = json2["power"]
            self.rank = int(json2["rank"])
            self.gp_today = json2["gp_today"]
            self.gp_total = json2["gp_total"]

            if self.gp_today == None:
                self.gp_today = 0
            else:
                self.gp_today = int(self.gp_today)

            if self.gp_total == None:
                self.gp_total = 0
            else:
                self.gp_total = int(self.gp_total)

class Player:
    def __init__(self, json):
        self.id = json["userId"]
        self.name = json["name"]
        self.rank = int(json["rank"])
        self.hats = int(json["hats"])
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