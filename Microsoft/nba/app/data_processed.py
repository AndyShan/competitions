#  -*- coding: utf-8 -*-
import pyExcelerator
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8")


# 东部训练数据（不能被三整除）
EAST_WINNER = {87: [[1, 4, 2, 3], [1, 3], [1]], 88: [[1, 4, 2, 3], [1, 2], [2]],
               90: [[1, 5, 2, 3], [1, 2], [1]], 91: [[1, 5, 2, 3], [1, 3], [1]],
               93: [[1, 5, 2, 3], [1, 2], [2]], 94: [[1, 5, 2, 3], [5, 2], [2]],
               96: [[1, 4, 2, 6], [1, 2], [1]], 97: [[1, 4, 2, 3], [1, 2], [1]],
               0: [[1, 4, 2, 3], [1, 3], [1]], 2: [[1, 4, 2, 3], [1, 3], [1]],
               3: [[1, 4, 2, 6], [1, 2], [2]], 5: [[1, 5, 2, 6], [1, 2], [2]],
               6: [[1, 4, 2, 3], [1, 2], [2]], 8: [[1, 4, 2, 3], [1, 2], [1]],
               9: [[1, 4, 2, 3], [1, 3], [3]], 11: [[1, 5, 2, 3], [1, 2], [2]],
               14: [[1, 5, 2, 6], [1, 2], [2]], 15: [[1, 5, 2, 3], [1, 2], [2]]}


# 西部训练数据（不能被三整除）
WEST_WINNER = {87: [[1, 5, 7, 6], [1, 7], [1]],88: [[1, 5, 2, 3], [1, 3], [1]],
               90: [[1, 5, 2, 3], [5, 2], [2]], 91: [[1, 5, 2, 6], [1, 2], [2]],
               93: [[1, 5, 2, 3], [1, 3], [1]], 94: [[8, 5, 2, 3], [5, 2], [2]],
               96: [[1, 5, 2, 3], [1, 3], [1]], 97: [[1, 4, 2, 3], [1, 2], [1]],
               0: [[1, 4, 2, 3], [1, 2], [1]], 2: [[1, 4, 2, 3], [1, 3], [3]],
               3: [[1, 5, 2, 3], [1, 2], [1]], 5: [[1, 4, 2, 3], [1, 2], [2]],
               6: [[1, 4, 2, 3], [4, 2], [4]], 8: [[1, 5, 2, 3], [1, 3], [1]],
               9: [[1, 5, 2, 6], [1, 2], [1]], 11: [[8, 4, 2, 3], [4, 3], [3]],
               14: [[1, 4, 2, 3], [1, 2], [1]], 15: [[1, 4, 2, 3], [1, 2], [1]]}

# 总决赛训练数据（不能被三整除）
FINAL_WINNER = {87: "W|1",88: "W|1", 90: "E|1", 91: "E|1", 93: "E|2", 94: "W|2", 96: "E|1", 97: "E|1", 0: "W|1",
                2: "W|3", 3: "W|1", 5: "W|2", 6: "E|2", 8: "E|1", 9: "W|1", 11: "W|3", 14: "W|1", 15:"W|1"}

TRAINING_YEAR_TMP = EAST_WINNER.keys()
TRAINING_YEAR = []
for y in TRAINING_YEAR_TMP:
    if y < 16:
        TRAINING_YEAR.append(2000 + y)
    else:
        TRAINING_YEAR.append(1900 + y)
TRAINING_YEAR.sort()


def year2str(year):
    if year < 10:
        year = "0" + str(year)
    else:
        year = str(year)
    return year


def xls2text_rank():
    """
    rank模型从excel读取队伍数据
    """
    if os.listdir("data_processed_rank/"):
        return
    year = 86
    part = ["W", "E"]
    for p in part:
        while True:
            if year < 10:
                sheets = pyExcelerator.parse_xls("data/0" + str(year) + p + ".xls", "utf-8")
                f = open("data_processed_rank/0" + str(year) + p, "a+")
            else:
                sheets = pyExcelerator.parse_xls("data/" + str(year) + p + ".xls", "utf-8")
                f = open("data_processed_rank/" + str(year) + p, "a+")
            data = ""
            for line in sheets:
                for i in range(1, 9):
                    for j in range(1, 24):
                        if j in [2, 23, 22]:
                            continue
                        data += str(line[1][(i, j)]) + "\t"
                    data += "\n"
            f.write(data)
            f.close()
            year += 1
            if year == 100:
                year = 0
            if year == 17:
                year = 86
                break


def xls2text_diff():
    """
    diff模型从excel读取队伍数据
    """
    if os.listdir("data_processed_diff/"):
        return
    year = 86
    part = ["W", "E"]
    for p in part:
        while True:
            if year < 10:
                sheets = pyExcelerator.parse_xls("data/0" + str(year) + p + ".xls", "utf-8")
                f = open("data_processed_diff/0" + str(year) + p, "a+")
            else:
                sheets = pyExcelerator.parse_xls("data/" + str(year) + p + ".xls", "utf-8")
                f = open("data_processed_diff/" + str(year) + p, "a+")
            data = ""
            for line in sheets:
                for i in range(1, 9):
                    for j in range(1, 24):
                        if j in [2, 23, 4, 5, 7, 8, 10, 11, 13, 14, 19]:
                            continue
                        # if j == 20:
                            # data += str(float(line[1][(i, j)]) - float(line[1][(i, j + 1)])) + "\t"
                            # continue
                        if j == 21:
                            data += str(-float(line[1][(i, j)])) + "\t"
                            continue
                        if j == 18:
                            data += str(-float(line[1][(i, j)])) + "\t"
                            continue
                        data += str(line[1][(i, j)]) + "\t"
                    data += "\n"
            f.write(data)
            f.close()
            year += 1
            if year == 100:
                year = 0
            if year == 17:
                year = 86
                break


def read_data(filename):
    """
    从格式化数据文件读取数据到内存
    :param filename:
    :return:
    """
    f = open(filename)
    data = []
    for line in f:
        arr = line.strip().split("\t")
        if len(data) < 8:
            data.append(arr)
        else:
            break
    return data


def data2digit(data):
    """
    将内存的数据中的字符串转为需要的浮点型
    """
    res = []
    for d in data:
        tmp = [d[0]]
        for i in range(1, len(d)):
            try:
                tmp.append(float(d[i]))
            except:
                tmp_str = str(d[i]).replace("%", "").replace(".","")
                tmp.append(float("0." + tmp_str))
        res.append(tmp)
    return res


def get_training_year(year):
    tmp = year
    if tmp <= 16:
        year += 2000
    else:
        year += 1900
    training_year_tmp = []
    pos = -1
    for i in range(len(TRAINING_YEAR)):
        if TRAINING_YEAR[i] > year:
            pos = i
            break
    if pos >= 12 or pos < 0:
        training_year_tmp = TRAINING_YEAR[-9:]
    elif pos < 6:
        training_year_tmp = TRAINING_YEAR[:9]
    else:
        for i in range(pos - 4, pos):
            training_year_tmp.append(TRAINING_YEAR[i])
        for i in range(pos, pos + 5):
            training_year_tmp.append(TRAINING_YEAR[i])
    training_year = []
    for i in training_year_tmp:
        if i < 2000:
            training_year.append(i - 1900)
        else:
            training_year.append(i - 2000)
    # print training_year
    return training_year


def training_set_construct_part_rank(winners_dict, part, training_year):
    training_set_1st = []
    training_label_1st = []
    training_set_2nd = []
    training_label_2nd = []
    training_set_3rd = []
    training_label_3rd = []

    for key in training_year:
        if key < 10:
            key = "0" + str(key)
        data = data2digit(read_data("data_processed_rank/" + str(key) + part))
        sort_data = []
        for i in range(1, len(data[0])):
            tmp_data = []
            for j in range(8):
                tmp_data.append(data[j][i])
            if i == 16 or i == 17 or i == 19:
                tmp_data.sort()
            else:
                tmp_data.sort(reverse=True)
            sort_data.append(tmp_data)
        winners = winners_dict[int(key)]
        for play_round in range(len(winners)):
            if play_round == 0:
                for t in winners[play_round]:
                    winner_data = []
                    for i in range(len(data[0]) - 1):
                        winner_data.append(sort_data[i].index(data[t - 1][i + 1]) + 1)
                    training_set_1st.append(winner_data)
                    training_label_1st.append(1)
                    loser_data = []
                    for i in range(len(data[0]) - 1):
                        loser_data.append(sort_data[i].index(data[8 - t][i + 1]) + 1)
                    training_set_1st.append(loser_data)
                    training_label_1st.append(0)
            elif play_round == 1:
                current_winner = []
                for i in winners[play_round]:
                    current_winner.append(i)
                current_loser = []
                for i in winners[play_round - 1]:
                    current_loser.append(i)
                for i in current_winner:
                    current_loser.remove(i)
                for t in current_winner:
                    winner_data = []
                    for i in range(len(data[0]) - 1):
                        winner_data.append(sort_data[i].index(data[t - 1][i + 1]) + 1)
                    training_set_2nd.append(winner_data)
                    training_label_2nd.append(1)
                for t in current_loser:
                    loser_data = []
                    for i in range(len(data[0]) - 1):
                        loser_data.append(sort_data[i].index(data[t - 1][i + 1]) + 1)
                    training_set_2nd.append(loser_data)
                    training_label_2nd.append(0)
            else:
                current_winner = []
                for i in winners[play_round]:
                    current_winner.append(i)
                current_loser = []
                for i in winners[play_round - 1]:
                    current_loser.append(i)
                for i in current_winner:
                    current_loser.remove(i)
                for t in current_winner:
                    winner_data = []
                    for i in range(len(data[0]) - 1):
                        winner_data.append(sort_data[i].index(data[t - 1][i + 1]) + 1)
                    training_set_3rd.append(winner_data)
                    training_label_3rd.append(1)
                for t in current_loser:
                    loser_data = []
                    for i in range(len(data[0]) - 1):
                        loser_data.append(sort_data[i].index(data[t - 1][i + 1]) + 1)
                    training_set_3rd.append(loser_data)
                    training_label_3rd.append(0)
    return training_set_1st, training_label_1st, training_set_2nd, training_label_2nd, training_set_3rd, \
           training_label_3rd


def training_set_construct_part_final_rank(training_year):
    training_set = []
    training_label = []
    for key in training_year:
        winner_str = FINAL_WINNER[key]
        winner_arr = winner_str.split("|")
        winner_part = winner_arr[0]
        part = ["W","E"]
        part.remove(winner_part)
        loser_part = part[0]
        if winner_part == "W":
            winner = WEST_WINNER[key][2][0]
            loser = EAST_WINNER[key][2][0]
        else:
            winner = EAST_WINNER[key][2][0]
            loser = WEST_WINNER[key][2][0]
        if key < 10:
            key = "0" + str(key)
        else:
            key = str(key)
        winner_data = data2digit(read_data("data_processed_rank/" + str(key) + winner_part))
        loser_data= data2digit(read_data("data_processed_rank/" + str(key) + loser_part))
        winner_data_sort = []
        for i in range(1, len(winner_data[0])):
            tmp_data = []
            for j in range(8):
                tmp_data.append(winner_data[j][i])
            if i == 16 or i == 17 or i == 19:
                tmp_data.sort()
            else:
                tmp_data.sort(reverse=True)
            winner_data_sort.append(tmp_data)

        loser_data_sort = []
        for i in range(1, len(loser_data[0])):
            tmp_data = []
            for j in range(8):
                tmp_data.append(loser_data[j][i])
            if i == 16 or i == 17 or i == 19:
                tmp_data.sort()
            else:
                tmp_data.sort(reverse=True)
            loser_data_sort.append(tmp_data)
        tmp_training_data = []
        for i in range(len(winner_data[0]) - 1):
            tmp_training_data.append(winner_data_sort[i].index(winner_data[winner - 1][i + 1]) + 1)
        training_set.append(tmp_training_data)
        training_label.append(1)

        tmp_training_data = []
        for i in range(len(loser_data[0]) - 1):
            tmp_training_data.append(loser_data_sort[i].index(loser_data[loser - 1][i + 1]) + 1)
        training_set.append(tmp_training_data)
        training_label.append(0)

    return training_set, training_label


def training_set_construct_rank(year):
    training_year = get_training_year(year)
    east_training_set_1st, east_training_label_1st, east_training_set_2nd, east_training_label_2nd, \
    east_training_set_3rd, east_training_label_3rd= training_set_construct_part_rank(EAST_WINNER, "E", training_year)
    west_training_set_1st, west_training_label_1st, west_training_set_2nd, west_training_label_2nd, \
    west_training_set_3rd, west_training_label_3rd = training_set_construct_part_rank(WEST_WINNER, "W", training_year)
    training_set_final, training_label_final = training_set_construct_part_final_rank(training_year)
    return east_training_set_1st, east_training_label_1st, east_training_set_2nd, east_training_label_2nd, \
    east_training_set_3rd, east_training_label_3rd,\
    west_training_set_1st, west_training_label_1st, west_training_set_2nd, west_training_label_2nd, \
    west_training_set_3rd, west_training_label_3rd,\
    training_set_final, training_label_final


def training_set_construct_part_diff(winners_dict, part, training_year):
    training_set = {}
    training_label = {}

    for key in training_year:
        if key < 10:
            key = "0" + str(key)
        data = data2digit(read_data("data_processed_diff/" + str(key) + part))
        winners = winners_dict[int(key)]
        key = str(key)
        training_set[key] = []
        training_label[key] = []
        is_win = 0
        is_lose = 0

        for playoff_round in range(len(winners)):
            if playoff_round == 0:
                for game_result in winners[playoff_round]:
                    if game_result <= 4:
                        winner_data = data[game_result - 1][1:]
                        loser_data = data[9 - game_result - 1][1:]
                        if is_win < 3:
                            training_data = list(map(lambda x: x[0] - x[1], zip(winner_data, loser_data))) + [1]
                            training_label[key].append(1)
                            training_set[key].append(training_data)
                            is_win += 1
                        else:
                            training_data = list(map(lambda x: x[1] - x[0], zip(winner_data, loser_data))) + [0]
                            training_label[key].append(0)
                            training_set[key].append(training_data)
                            is_lose += 1
                    if game_result > 4:
                        winner_data = data[game_result - 1][1:]
                        loser_data = data[9 - game_result - 1][1:]
                        if is_win < 3:
                            training_data = list(map(lambda  x: x[0] - x[1], zip(winner_data, loser_data))) + [0]
                            training_label[key].append(1)
                            training_set[key].append(training_data)
                            is_win += 1
                        else:
                            training_data = list(map(lambda x: x[1] - x[0], zip(winner_data, loser_data))) + [1]
                            training_label[key].append(0)
                            training_set[key].append(training_data)
                            is_lose += 1
            else:
                for game_result in winners[playoff_round]:
                    if winners[playoff_round - 1].index(game_result) % 2 == 0:
                        winner_data = data[game_result - 1][1:]
                        loser_data = data[winners[playoff_round - 1][winners[playoff_round - 1].index(game_result) + 1]
                                          - 1][1:]
                        if is_win < 3:
                            training_data = list(map(lambda x: x[0] - x[1], zip(winner_data, loser_data))) + [1]
                            training_label[key].append(1)
                            training_set[key].append(training_data)
                            is_win += 1
                        else:
                            training_data = list(map(lambda x: x[1] - x[0], zip(winner_data, loser_data))) + [0]
                            training_label[key].append(0)
                            training_set[key].append(training_data)
                            is_lose += 1
                    else:
                        winner_data = data[game_result - 1][1:]
                        loser_data = data[winners[playoff_round - 1][winners[playoff_round - 1].index(game_result) - 1]
                                          - 1][1:]
                        if is_win < 3:
                            training_data = list(map(lambda x: x[0] - x[1], zip(winner_data, loser_data))) + [0]
                            training_label[key].append(1)
                            training_set[key].append(training_data)
                            is_win += 1
                        else:
                            training_data = list(map(lambda x: x[1] - x[0], zip(winner_data, loser_data))) + [1]
                            training_label[key].append(0)
                            training_set[key].append(training_data)
                            is_lose += 1
    return training_set, training_label


def training_set_construct_part_final_diff(training_set, training_label, training_year):
    for key in training_year:
        winner_str = FINAL_WINNER[key]
        winner_arr = winner_str.split("|")
        winner_part = winner_arr[0]
        part = ["W","E"]
        part.remove(winner_part)
        loser_part = part[0]
        if winner_part == "W":
            winner = WEST_WINNER[key][2][0]
            loser = EAST_WINNER[key][2][0]
        else:
            winner = EAST_WINNER[key][2][0]
            loser = WEST_WINNER[key][2][0]
        if key < 10:
            key = "0" + str(key)
        else:
            key = str(key)
        winner_data = data2digit(read_data("data_processed_diff/" + str(key) + winner_part))[winner - 1][1:]
        loser_data= data2digit(read_data("data_processed_diff/" + str(key) + loser_part))[loser - 1][1:]
        if winner_data[10] > loser_data[10]:
            training_data = list(map(lambda x: x[0] - x[1], zip(winner_data, loser_data))) + [1]
            training_label[key].append(1)
            training_set[key].append(training_data)
        else:
            training_data = list(map(lambda x: x[0] - x[1], zip(winner_data, loser_data))) + [0]
            training_label[key].append(1)
            training_set[key].append(training_data)


def training_set_construct_diff(year):
    training_year = get_training_year(year)
    east_training_set, east_training_label = training_set_construct_part_diff(EAST_WINNER, "E", training_year)
    training_set_construct_part_final_diff(east_training_set, east_training_label, training_year)
    west_training_set, west_training_label = training_set_construct_part_diff(WEST_WINNER, "W", training_year)
    training_set_construct_part_final_diff(west_training_set, west_training_label, training_year)
    return east_training_set, east_training_label, west_training_set, west_training_label

