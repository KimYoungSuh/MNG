from Data.C_RoomData import RoomData
from  Data.C_PlayerData import PlayerData

from Data.C_WaittingRoomData import WaittingRoomData


class GameSysMain:


    def __init__(self):
        self.is_game_over = False

        self.players_data = [PlayerData().playerdata for i in range(16)]

        self.waitting_room_data = [WaittingRoomData().waitting_room_data for i in range(4)]
        self.rooms_data= [RoomData().room_data for i in range(4)]

        self.maxroomcount = 4
        self.player_count = 0

        self.player_number_table = [False for i in range(16)]

    def empty_player_number(self):
        for i in range(16):
            if not self.player_number_table[i]:
                self.player_number_table[i] = True
                return i
        return False

    def empty_room_number(self):
        for i in range(4):
            empty_number = i
            for room in self.rooms_data:
                if i == room['room_number']:
                    empty_number = False
                    break
            if empty_number != False:
                break
        return empty_number

    def init_game_sys(self):
        self.is_game_over = False

    def exist_room_count(self):
        count = 0
        for room in self.rooms_data:
            if room['full_player'] != 0:
                count += 1
        return count

    def join_player(self,player_data):
        self.players_data.append(player_data)
        (self.waitting_room_data)['player_count']+=1
        print((self.waitting_room_data)['player_count'])
