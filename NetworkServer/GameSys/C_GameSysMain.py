from Data.C_RoomData import RoomData
from  Data.C_PlayerData import PlayerData
<<<<<<< HEAD
from Data.C_WaittingRoomData import WaittingRoomData
=======
>>>>>>> bc72cd4972b68522bc2fedeaa997813eba48b0ab

class GameSysMain:


    def __init__(self):
        self.is_game_over = False
<<<<<<< HEAD
        self.players_data = []
        self.waitting_room_data = WaittingRoomData().waitting_room_data
        #self.rooms_data= [RoomData() for RoomData() in range(1,5)]
=======
        self.rooms_data= [RoomData() for i in range(5)]
        self.maxroomcount = 4
        self.player_count = 0
        self.players_data = []
>>>>>>> bc72cd4972b68522bc2fedeaa997813eba48b0ab

    def init_game_sys(self):
        self.is_game_over = False

    def exist_room_count(self):
        count = 0
        for room in self.rooms_data:
            if room.is_room_exist():
                count += 1
        return count

    def join_player(self,player_data):
        self.players_data.append(player_data)
        (self.waitting_room_data)['player_count']+=1
        print((self.waitting_room_data)['player_count'])
