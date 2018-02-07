class Guild:
    def __init__(self, json):
        guild_json = json["guild"]
        members_json = json["members"]

        self.name = guild_json["guild_name"]
        self.id = guild_json["guild_id"]
        self.creation_date = guild_json["creation_date"]
        self.active_date = guild_json["active_date"]
        self.member_count = guild_json["member_count"]
        self.active_count = guild_json["active_count"]
        self.emblem = guild_json["emblem"]
        self.gp_today = guild_json["gp_today"]
        self.gp_total = guild_json["gp_total"]
        self.owner_id = guild_json["owner_id"]
        self.note = guild_json["note"]
        self.members = []

        for member_json in members_json:
            self.members.append(self.Member(member_json))

    class Member:
        def __init__(self, json2):
            self.id = json2["user_id"]
            self.name = json2["name"]
            self.group = json2["power"]
            self.rank = json2["rank"]
            self.gp_today = json2["gp_today"]
            self.gp_total = json2["gp_total"]

            if self.gp_today == None:
                self.gp_today = 0

            if self.gp_total == None:
                self.gp_total = 0

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