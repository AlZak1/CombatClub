class HumanService:

    def __init__(self, human_list, room_list):
        self.human_list = human_list
        self.room_list = room_list

    def append_human_list(self, human):
        self.human_list.append(human)

    def append_room_list(self, room):
        self.room_list.append(room)

    def process_human_list(self):
        obj = {}
        user1_attack = []
        user1_defense = []
        user2_attack = []
        user2_defense = []
        counter_1 = 0
        counter_2 = 0
        damage_by_user_1 = 0
        damage_by_user_2 = 0
        print('room', self.room_list)

        if len(self.human_list) >= 4:
            room = self.room_list[0]
            for i in self.human_list:
                if i['isAttack'] is True and i['user'] == room.user_1.id:
                    for k in i.values():
                        user1_attack.append(k)
                elif i['isAttack'] is False and i['user'] == room.user_2.id:
                    for k in i.values():
                        user2_defense.append(k)
                elif i['isAttack'] is True and i['user'] == room.user_2.id:
                    for k in i.values():
                        user2_attack.append(k)
                elif i['isAttack'] is False and i['user'] == room.user_1.id:
                    for k in i.values():
                        user1_defense.append(k)

            print('user1attack', user1_attack)
            print('user2defense', user2_defense)
            print('user2attack', user2_attack)
            print('user1defense', user1_defense)

            for i in range(2, 8):
                if user1_attack[i] == user2_defense[i]:
                    counter_1 += 1
                    continue
                elif user1_attack[i] and not user2_defense[i]:
                    if counter_1 == 0:
                        damage_by_user_1 += 10
                        counter_1 += 1
                    elif counter_1 == 1:
                        damage_by_user_1 += 7
                        counter_1 += 1
                    else:
                        damage_by_user_1 += 5
                counter_1 += 1
            print('total damage by 1st user' + ' ' + str(damage_by_user_1) + '\n')

            # for i in self.human_list:
            #     if i['user'] == 1:
            #         i['total_damage'] = damage_by_user_1
            #         i['enemy_damage'] = damage_by_user_2
            #         i['current_damage'] = damage_by_user_1

            for i in range(2, 8):
                if user2_attack[i] == user1_defense[i]:
                    counter_2 += 1
                    continue
                elif user2_attack[i] and not user1_defense[i]:
                    if counter_2 == 0:
                        damage_by_user_2 += 10
                        counter_2 += 1
                    elif counter_2 == 1:
                        damage_by_user_2 += 7
                        counter_2 += 1
                    else:
                        damage_by_user_2 += 5
                counter_2 += 1
            print('total damage by 2st user' + ' ' + str(damage_by_user_2) + '\n')

            # for i in self.human_list:
            #     if i['user'] == 2:
            #         i['total_damage'] = damage_by_user_2
            #         i['enemy_damage'] = damage_by_user_1
            #         i['current_damage'] = damage_by_user_2

            obj = {'damage1': damage_by_user_1,
                   'damage2': damage_by_user_2}

        # print('human_list', self.human_list)
        # print('human_list_copy', human_list_copy)

        return obj
