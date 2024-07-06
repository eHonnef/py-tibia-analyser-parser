# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os
from datetime import datetime


class ParseJson:
    def __init__(self, json_folder, hunt_name, party_size):
        self.party_size = party_size
        self.hunt_name = hunt_name
        self.json_file = [f"{json_folder}/{file}" for file in os.listdir(json_folder) if file.endswith(".json")][0]

    def __get_party_size(self):
        if self.party_size == 1:
            return "solo"
        elif self.party_size == 2:
            return "duo"
        elif self.party_size == 3:
            return "trio"
        elif self.party_size == 4:
            return "full-party"
        else:
            return "too many people"

    def __parse(self):
        rtn_dict = {
            "time": "",
            "monsters": {},
            "balance": {},
            "balance_h": {},
            "raw_exp_h": 0,
            "exp_h": 0,
            "total_exp": 0,
        }

        parsed_json = json.load(open(self.json_file, "r"))
        # Parse the session time
        datetime_obj = datetime.strptime(parsed_json["Session length"].replace("h", ""), "%H:%M")
        session_float_time = datetime_obj.hour + datetime_obj.minute / 60
        rtn_dict["time"] = datetime_obj.strftime("%H:%M")

        # Parse the monsters
        main_key = "Killed Monsters"
        counter_key = "Count"
        name_key = "Name"
        for monster in parsed_json[main_key]:
            rtn_dict["monsters"][monster[name_key]] = monster[counter_key]

        # Parsing balance
        rtn_dict["balance"] = int(parsed_json["Balance"].replace(",", ""))
        rtn_dict["balance_h"] = round(rtn_dict["balance"] / session_float_time)

        # Parsing exp
        rtn_dict["total_exp"] = int(parsed_json["XP Gain"].replace(",", ""))
        if "Raw XP/h" in parsed_json:
            rtn_dict["raw_exp_h"] = rtn_dict["Raw XP/h"]
        else:
            rtn_dict["raw_exp_h"] = "n/a"

        rtn_dict["exp_h"] = round(rtn_dict["total_exp"] / session_float_time)

        return rtn_dict

    def pretty_print(self):
        d = self.__parse()
        str_monsters = "Monstros mortos:\n"
        for key, value in d["monsters"].items():
            str_monsters += f"  - {key}: {value}\n"

        str_monsters += "\n"

        header = f"\n{self.hunt_name}\n\n[{datetime.today().strftime('%d/%m/%Y')}] Hunt session {d['time']} ({self.__get_party_size()})\n\n"
        raw_exp = f"XP/h (with bonus): {'{:,}'.format(d['exp_h'])}\n"
        if isinstance(d['raw_exp_h'], int):
            raw_exp = f"Raw XP/h: {'{:,}'.format(d['raw_exp_h'])}\n"
        profit = f"Profit: {'{:,}'.format(d['balance'])}\n"

        return f"{header}{str_monsters}{raw_exp}{profit}"


if __name__ == "__main__":
    hunt_name = input("\nEnter the hunt name\n\n")
    party_size = input(
        "\nEnter the number of people (e.g. enter 1 = solo, 2 = duo, 3 = trio, 4 = full party, 5 = too many people to count\n\n")
    parsed = ParseJson("/home/bhonnef/.local/share/CipSoft GmbH/Tibia/packages/Tibia/log", hunt_name, party_size)
    print("\n==========================================")
    print(parsed.pretty_print())
