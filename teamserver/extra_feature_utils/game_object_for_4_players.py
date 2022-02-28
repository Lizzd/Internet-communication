class Game_Object_For_4_Player():
    def __init__(self, id, color=[127, 127, 127], field_size=[800, 800]):
        offset_from_edge = 50
        self.move_field_width = 200
        self.field_size = field_size

        if id == 1:
            self.position = [offset_from_edge, field_size[1] // 2]  # West player
            self.move_field_x_range = [0, self.move_field_width]
            self.move_field_y_range = [0, self.field_size[1]]
        elif id == 2:
            self.position = [field_size[0] - offset_from_edge, field_size[1] // 2]  # East player
            self.move_field_x_range = [self.field_size[0] - self.move_field_width,
                                       self.field_size[0]]
            self.move_field_y_range = [0, self.field_size[1]]
        elif id == 3:
            self.position = [field_size[0] // 2, offset_from_edge]  # Nord player
            self.move_field_x_range = [0, self.field_size[0]]
            self.move_field_y_range = [0, self.move_field_width]
        elif id == 4:
            self.position = [field_size[0] // 2, field_size[1] - offset_from_edge]  # South player
            self.move_field_x_range = [0, self.field_size[0]]
            self.move_field_y_range = [self.field_size[1] - self.move_field_width,
                                       self.field_size[1]]
        else:
            print("Wrong Player ID")

        self.velocity = [0, 0]

        self.max_acceleration = 0.2
        self.max_velocity = 4
        self.color = color
        self.id = id

        self.player_info = None
        self.key_list = []  # UP, DOWN, LEFT, RIGHT, SPACE
        self.ready = False

    def update_player_features(self, color, id):
        self.color = color
        self.id = id

    def update_connection_info(self, addr):
        self.addr = addr

    def update_playerstates(self):

        if self.move_field_y_range[0] < self.position[1] < self.move_field_y_range[1]:
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
            if self.position[1] > self.move_field_y_range[1]:
                self.velocity[1] = -1 * abs(self.velocity[1])
            if self.position[1] < self.move_field_y_range[0]:
                self.velocity[1] = abs(self.velocity[1])
        self.position[1] += self.velocity[1]

        if self.move_field_x_range[0] < self.position[0] < self.move_field_x_range[1]:
            for key in self.key_list:
                if key is None or key == "SPACE":
                    pass
                elif key == "LEFT":
                    if self.velocity[0] >= -self.max_velocity:
                        self.velocity[0] += -self.max_acceleration
                    else:
                        self.velocity[0] += 0.1
                elif key == "RIGHT":
                    if self.velocity[0] <= self.max_velocity:
                        self.velocity[0] += self.max_acceleration
                    else:
                        self.velocity[0] += -0.1
        else:
            if self.position[0] > self.move_field_x_range[1]:
                self.velocity[0] = -1 * abs(self.velocity[0])
            if self.position[0] < self.move_field_x_range[0]:
                self.velocity[0] = abs(self.velocity[0])
        self.position[0] += self.velocity[0]

    def get_player_info(self):
        player_info = self.position + self.velocity
        player_info = [int(x) for x in player_info]
        return self.id, player_info
