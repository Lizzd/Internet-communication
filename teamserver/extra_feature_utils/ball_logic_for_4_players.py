import math

import numpy as np


class Ball_Logic_For_4_Players():
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
        self.score = [0 for _ in range(4)]  # [Player_left, Player_right]

        self.pause = 10
        self.max_score = 20
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

        # add one point to each player, later subtract one point from the loser
        if not self.ball_inside_field():
            for id in range(4):
                self.score[id] += 1
            if self.position[0] < 0:  # Player left
                self.score[0] -= 1
                self.ballAngle = math.radians(180)
            elif self.position[0] > self.field_size[0]:  # Player right
                self.score[1] -= 1
                self.ballAngle = math.radians(0)
            elif self.position[1] < 0:  # Player top
                self.score[2] -= 1
                self.ballAngle = math.radians(90)
            elif self.position[1] > self.field_size[1]:  # Player bottom
                self.score[3] -= 1
                self.ballAngle = math.radians(-90)
            self.reset_to_inital_value()

            first_max_score = sorted(self.score, reverse=True)[0]
            second_max_score = sorted(self.score, reverse=True)[1]

            if first_max_score >= self.max_score and first_max_score - second_max_score >= 2:
                # TODO looks somehow wrong
                return self.score[self.score == first_max_score]

        if self.gravity:
            self.apply_acceleration_effect()
        self.ballAngle = math.atan2(-self.ballSpeed[1], self.ballSpeed[0])
        self.speed = np.linalg.norm(self.ballSpeed)
        self.collision_detector(players_states, players_velocity_states)
        self.ballSpeed = self.speed * np.array(
            [math.cos(self.ballAngle), -math.sin(self.ballAngle)])
        return None

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
        if r_value < 3:
            r_value = 3
        r_norm = r / r_value ** 2
        acceleration = r_norm * 2
        self.ballSpeed += acceleration

    # ===============
    # 4 Player Modus

    def ball_inside_field(self):
        return 0 <= self.position[0] <= self.field_size[0] and 0 <= self.position[1] <= \
               self.field_size[1]

    def collision_detector(self, players_states, players_velocity_states):
        """ players_states: [player_left, player_right]"""

        def is_collision_with_player_0(player_states):
            is_x_position_in_collision = False
            is_y_position_in_collision = False
            for position in [self.position, self.position + self.ballSpeed // 2]:
                is_x_position_in_collision |= player_states[0] >= position[0] >= player_states[
                    0] - self.player_thickness
                is_y_position_in_collision |= player_states[1] + self.player_half_width > position[
                    1] > player_states[
                                                  1] - self.player_half_width
            return is_x_position_in_collision and is_y_position_in_collision

        def is_collision_with_player_1(player_states):
            is_x_position_in_collision = False
            is_y_position_in_collision = False
            for position in [self.position, self.position + self.ballSpeed // 2]:
                is_x_position_in_collision |= player_states[0] <= position[0] <= player_states[
                    0] + self.player_thickness
                is_y_position_in_collision |= player_states[1] + self.player_half_width > position[
                    1] > player_states[
                                                  1] - self.player_half_width
            return is_x_position_in_collision and is_y_position_in_collision

        def is_collision_with_player_2(player_states):
            is_x_position_in_collision = False
            is_y_position_in_collision = False
            for position in [self.position, self.position + self.ballSpeed // 2]:
                is_x_position_in_collision |= player_states[0] - self.player_half_width <= position[
                    0] <= player_states[
                                                  0] + self.player_half_width
                is_y_position_in_collision |= player_states[1] > position[1] > player_states[
                    1] - self.player_thickness
            return is_x_position_in_collision and is_y_position_in_collision

        def is_collision_with_player_3(player_states):
            is_x_position_in_collision = False
            is_y_position_in_collision = False
            for position in [self.position, self.position + self.ballSpeed // 2]:
                is_x_position_in_collision |= player_states[0] - self.player_half_width <= position[
                    0] <= player_states[
                                                  0] + self.player_half_width
                is_y_position_in_collision |= player_states[1] <= position[1] <= player_states[
                    1] + self.player_thickness
            return is_x_position_in_collision and is_y_position_in_collision

        def update_collision_speed(players_velocity_states, player_id):
            self.ballSpeed = self.speed * np.array(
                [math.cos(self.ballAngle), -math.sin(self.ballAngle)])
            self.ballSpeed += players_velocity_states[player_id]
            self.ballAngle = math.atan2(-self.ballSpeed[1], self.ballSpeed[0])
            self.speed = np.linalg.norm(self.ballSpeed)

        alpha = 1

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

        if is_collision_with_player_2(players_states[2]) and self.last_collision != 2:
            self.last_collision = 2
            self.ballAngle = - self.ballAngle - math.radians(
                int((players_states[2][0] - self.position[0]) * alpha))
            update_collision_speed(players_velocity_states, 2)

        if is_collision_with_player_3(players_states[3]) and self.last_collision != 3:
            self.last_collision = 3
            self.ballAngle = - self.ballAngle + math.radians(
                int((players_states[3][0] - self.position[0]) * alpha))
            update_collision_speed(players_velocity_states, 3)

        if not is_collision_with_player_0(players_states[0]) and not is_collision_with_player_1(
                players_states[1]) and not is_collision_with_player_2(
                players_states[2]) and not is_collision_with_player_3(players_states[3]):
            self.last_collision = -1
