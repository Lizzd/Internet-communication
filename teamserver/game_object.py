class Game_Object():
    def __init__(self, player_id, color=[127, 127, 127], field_size=[800, 600]):
        offset_from_edge = 50
        """
        Player 0: West player
        Player 1: East player
        Player 2: North player
        Player 3: South player
        
        """
        if player_id == 1:
            self.position = [offset_from_edge, field_size[1] // 2]
        elif player_id == 2:
            self.position = [field_size[0] - offset_from_edge, field_size[1] // 2]
        elif player_id == 3:
            self.position = [field_size[0] // 2, offset_from_edge]
        elif player_id == 4:
            self.position = [field_size[0] // 2, field_size[1] - offset_from_edge]
        else:
            print("Wrong Player ID")

        self.velocity = [0, 0]
        self.field_size = field_size

        self.max_acceleration = 0.5
        self.max_velocity = 6
        self.color = color
        self.id = player_id

        self.player_info = None
        self.key_list = []  # UP, DONW, RIGHT, LEFT,  SPACE
        self.ready = False

    def update_player_features(self, color, id):
        self.color = color
        self.id = id

    def update_connection_info(self, addr):
        self.addr = addr

    def update_playerstates(self):
        if self.field_size[1] > self.position[1] > 0:
            for key in self.key_list:
                if key is None or key == "SPACE":
                    pass
                elif key == "UP":
                    if self.velocity[1] >= -self.max_velocity:
                        self.velocity[1] += -self.max_acceleration
                    else:
                        self.velocity[1] += 0.1
                elif key == "DOWN":
                    if self.velocity[1] <= self.max_velocity:
                        self.velocity[1] += self.max_acceleration
                    else:
                        self.velocity[1] += -0.1
        else:
            if self.position[1] > self.field_size[1]:
                self.velocity[1] = -1 * abs(self.velocity[1])
            if self.position[1] < 0:
                self.velocity[1] = abs(self.velocity[1])
        self.position[1] += self.velocity[1]
        self.key_list = []

    def get_player_info(self):
        player_info = self.position + self.velocity
        player_info = [int(x) for x in player_info]
        return self.id, player_info
