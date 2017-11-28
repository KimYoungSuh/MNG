from Data.C_RoomData import RoomData
from  Data.C_PlayerData import PlayerData

class GameSysMain:


    def __init__(self):
        self.is_game_over = False
        self.rooms_data= [RoomData() for i in range(5)]
        self.maxroomcount = 4
        self.player_count = 0
        self.players_data = []

    def init_game_sys(self):
        self.is_game_over = False

    def exist_room_count(self):
        count = 0
        for room in self.rooms_data:
            if room.is_room_exist():
                count += 1
        return count
    def join_player(self):
        self.player_count+=1
        print(self.player_count)
