class HumanService:

    def __init__(self, human_list):
        self.human_list = human_list

    def append_human_list(self, human):
        self.human_list.append(human)

    def process_human_list(self):
        score_1 = 0
        score_2 = 0
        u = 0
        l_v_1 = []
        l_v_2 = []
        l_v_3 = []
        l_v_4 = []

        if len(self.human_list) >= 4:
            human_01 = [x for x in self.human_list if x['isAttack'] is True and x['user'] == 1]
            human_1 = human_01[0]
            for i in human_1.values():
                l_v_1.append(i)
            human_02 = [x for x in self.human_list if x['isAttack'] is False and x['user'] == 2]
            human_2 = human_02[0]
            for i in human_2.values():
                l_v_2.append(i)
            print(l_v_1)
            print(l_v_2)
            for i in range(0, 6):
                if l_v_1[i] == l_v_2[i]:
                    u += 1
                    continue
                elif l_v_1[i] and not l_v_2[i]:
                    if u == 0:
                        score_1 += 10
                        u += 1
                    elif u == 1:
                        score_1 += 7
                        u += 1
                    else:
                        score_1 += 5
                u += 1
            print('total damage' + ' ' + str(score_1) + '\n')

            human_03 = [x for x in self.human_list if x['isAttack'] is False and x['user'] == 1]
            human_3 = human_03[0]
            for i in human_3.values():
                l_v_3.append(i)
            human_04 = [x for x in self.human_list if x['isAttack'] is True and x['user'] == 2]
            human_4 = human_04[0]
            for i in human_4.values():
                l_v_4.append(i)
            print(l_v_3)
            print(l_v_4)
            for i in range(0, 6):
                if l_v_3[i] == l_v_4[i]:
                    u += 1
                    continue
                elif l_v_3[i] and not l_v_4[i]:
                    if u == 0:
                        score_2 += 10
                        u += 1
                    elif u == 1:
                        score_2 += 7
                        u += 1
                    else:
                        score_2 += 5
                u += 1
            print('total damage second' + ' ' + str(score_2) + '\n')
            self.human_list.clear()

