import math

import numpy as np


class Ball_Logic():
    def __init__(self, field_size, feature_list):

        self.higher_ballSpeed = False
        self.invisibility = False
        self.multiple_balls = False
        self.half_racket = False
        self.gravity = False

        self.gravity_center = np.array(field_size) / 2
        self.blackhole_mass = 10

        if "higher_ballSpeed" in feature_list:
            self.higher_ballSpeed = True
        if "invisibility" in feature_list:
            self.invisibility = True
        if "multiple_balls" in feature_list:
            self.multiple_balls = True
        if "half_racket" in feature_list:
            self.half_racket = True
        if "gravity" in feature_list:
            self.gravity = True

        self.field_size = field_size
        self.player_thickness = 10
        if self.half_racket:
            self.player_half_width = 30
        else:
            self.player_half_width = 60
        # ========== size_offset = 4
        self.player_half_width += 4

        # self.playerRects = [player_left,player_right]

        # self.ball = pygame.Rect(400, 300, 5, 5)
        self.position = (np.array(field_size) / 2)
        # self.position = [self.position[0], self.position[1]

        self.ballAngle = math.radians(0)
        if self.higher_ballSpeed:
            self.speed = 16
        else:
            self.speed = 6
        self.ballSpeed = self.speed * np.array(
            [math.cos(self.ballAngle), -math.sin(self.ballAngle)])

        self.ball_no = 1
        self.score = [0, 0]  # [Player_left, Player_right]

        self.pause = 10
        self.max_score = 5
        self.last_collision = None

    def reset_to_inital_value(self):
        if self.higher_ballSpeed:
            self.speed = 16
        else:
            self.speed = 6
        self.ballSpeed = self.speed * np.array(
            [math.cos(self.ballAngle), -math.sin(self.ballAngle)])
        self.position = (np.array(self.field_size) / 2)
        self.last_collision = None

    def update_ball(self, players_states, players_velocity_states):
        self.position += self.ballSpeed

        if self.position[1] <= 0:
            self.ballSpeed[1] = abs(self.ballSpeed[1])
        if self.position[1] > self.field_size[1]:
            self.ballSpeed[1] = -abs(self.ballSpeed[1])

        if self.position[0] > self.field_size[0] or self.position[0] < 0:
            if self.position[0] > self.field_size[0]:
                self.score[0] += 1
                self.ballAngle = math.radians(180)
            elif self.position[0] < 0:
                self.score[1] += 1
                self.ballAngle = math.radians(0)
            self.reset_to_inital_value()

            if self.score[0] >= self.max_score and self.score[0] - self.score[1] >= 2:
                self.score = [0, 0]
                return 1
            if self.score[1] >= self.max_score and self.score[1] - self.score[0] >= 2:
                self.score = [0, 0]
                return 2
        if self.gravity:
            self.apply_acceleration_effect()
        self.ballAngle = math.atan2(-self.ballSpeed[1], self.ballSpeed[0])
        self.speed = np.linalg.norm(self.ballSpeed)
        self.collision_detector(players_states, players_velocity_states)
        self.ballSpeed = self.speed * np.array(
            [math.cos(self.ballAngle), -math.sin(self.ballAngle)])
        return None

    def collision_detector(self, players_states, players_velocity_states):
        """ players_states: [player_left, player_right]"""

        def is_collision_with_player_0(player_states):
            is_x_position_in_collision = False
            is_y_position_in_collision = False
            for position in [self.position, self.position + self.ballSpeed // 2]:
                is_x_position_in_collision |= player_states[0] + self.player_thickness // 2 >= \
                                              position[0] >= \
                                              player_states[
                                                  0] - self.player_thickness // 2
                is_y_position_in_collision |= player_states[1] + self.player_half_width > position[
                    1] > player_states[
                                                  1] - self.player_half_width
            return is_x_position_in_collision and is_y_position_in_collision

        def is_collision_with_player_1(player_states):
            is_x_position_in_collision = False
            is_y_position_in_collision = False
            for position in [self.position, self.position + self.ballSpeed // 2]:
                is_x_position_in_collision |= player_states[0] - self.player_thickness // 2 <= \
                                              position[0] <= \
                                              player_states[
                                                  0] + self.player_thickness
                is_y_position_in_collision |= player_states[1] + self.player_half_width > position[
                    1] > player_states[
                                                  1] - self.player_half_width
            return is_x_position_in_collision and is_y_position_in_collision

        def update_collision_speed(players_velocity_states, player_id):
            self.ballSpeed = self.speed * np.array(
                [math.cos(self.ballAngle), -math.sin(self.ballAngle)])
            self.ballSpeed += players_velocity_states[player_id]
            self.ballAngle = math.atan2(-self.ballSpeed[1], self.ballSpeed[0])
            self.speed = np.linalg.norm(self.ballSpeed)

        alpha = 0.8
        if is_collision_with_player_0(players_states[0]) and self.last_collision != 0:
            self.last_collision = 0
            self.ballAngle = math.pi - self.ballAngle + math.radians(
                int((players_states[0][1] - self.position[1]) * alpha))

            update_collision_speed(players_velocity_states, 0)

        if is_collision_with_player_1(players_states[1]) and self.last_collision != 1:
            self.last_collision = 1
            self.ballAngle = math.pi - self.ballAngle - math.radians(
                int((players_states[1][1] - self.position[1]) * alpha))

            update_collision_speed(players_velocity_states, 1)

        if not is_collision_with_player_0(players_states[0]) and not is_collision_with_player_1(
                players_states[1]):
            self.last_collision = -1

    def get_ball_info(self):
        info_list = [self.ball_no] + list(self.position.astype(int)) + list(
            self.ballSpeed.astype(int))
        if self.invisibility and self.field_size[0] * 2 / 5 < self.position[0] < self.field_size[
            0] * 3 / 5:
            info_list = [self.ball_no] + [0, 0] + list(self.ballSpeed)
        return [int(x) for x in info_list]

    def apply_acceleration_effect(self):
        r = self.gravity_center - self.position
        r_value = np.linalg.norm(r)
        if r_value < 5:
            r_value = 5
        r_norm = r / r_value ** 2
        acceleration = r_norm * 2
        self.ballSpeed += acceleration
