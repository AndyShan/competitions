#  -*- coding: utf-8 -*-
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
import data_processed
import numpy as np
import sys
sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('UTF-8')
sys.getdefaultencoding()


def init_training_set_rank(year):
    data_processed.xls2text_rank()
    east_training_set_1st, east_training_label_1st, east_training_set_2nd, east_training_label_2nd, \
    east_training_set_3rd, east_training_label_3rd, \
    west_training_set_1st, west_training_label_1st, west_training_set_2nd, west_training_label_2nd, \
    west_training_set_3rd, west_training_label_3rd, \
    training_set_final, training_label_final = data_processed.training_set_construct_rank(year)

    return east_training_set_1st, east_training_label_1st, east_training_set_2nd, east_training_label_2nd, \
    east_training_set_3rd, east_training_label_3rd, \
    west_training_set_1st, west_training_label_1st, west_training_set_2nd, west_training_label_2nd, \
    west_training_set_3rd, west_training_label_3rd, \
    training_set_final, training_label_final


def predict_rank(training_set, training_label, test_data):
    gbdt = GradientBoostingClassifier()
    gbdt.fit(training_set, training_label)
    # important = rf.feature_importances_
    # for i in important:
    #     print i
    proba = gbdt.predict_proba(test_data)
    # print proba
    res = []
    for i in proba:
        res.append(i[1])
    return res


def predict_1st_rank(training_set, training_label, data, weight1 = 0 , weight2 = 0, weight3 = 0, weight4 = 0):
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

    test_data = []
    for i in range(8):
        tmp_test_data = []
        for j in range(len(data[0]) - 1):
            tmp_test_data.append(sort_data[j].index(data[i][j + 1]) + 1)
        test_data.append(tmp_test_data)
    result = predict_rank(training_set, training_label, test_data)
    winner = []
    if (1 - weight1) * result[0] > weight1 * result[7]:
        winner.append(1)
    else:
        winner.append(8)
    if  (1 - weight2) * result[3] > weight2 * result[4]:
        winner.append(4)
    else:
        winner.append(5)
    if (1 - weight3) * result[1] > weight3 * result[6]:
        winner.append(2)
    else:
        winner.append(7)
    if (1 - weight4) * result[2] > weight4 * result[5]:
        winner.append(3)
    else:
        winner.append(6)
    # for i in winner:
    #     print i , data[i - 1][0]
    return winner


def predict_2nd_rank(training_set, training_label, data, winner_1st, weight1 = 0, weight2 = 0.041):
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

    test_data = []
    for i in winner_1st:
        tmp_test_data = []
        for j in range(len(data[0]) - 1):
            tmp_test_data.append(sort_data[j].index(data[i - 1][j + 1]) + 1)
        test_data.append(tmp_test_data)

    result = predict_rank(training_set, training_label, test_data)
    winner = []
    if (1 - weight1) * result[0] > weight1 * result[1]:
        winner.append(winner_1st[0])
    else:
        winner.append(winner_1st[1])
    if weight2 * result[2] > weight2 * result[3]:
        winner.append(winner_1st[2])
    else:
        winner.append(winner_1st[3])
    for i in winner:
        print i ,data[i - 1][0]
    return winner


def predict_3rd_rank(training_set, training_label, data, winner_2nd, weight1=0.012):
    tmp_winner = winner_2nd
    winner_2nd = []
    for i in tmp_winner:
        winner_2nd.append(i + 1)
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

    test_data = []
    for i in winner_2nd:
        tmp_test_data = []
        for j in range(len(data[0]) - 1):
            tmp_test_data.append(sort_data[j].index(data[i - 1][j + 1]) + 1)
        test_data.append(tmp_test_data)

    result = predict_rank(training_set, training_label, test_data)
    if (1 - weight1) * result[0] > weight1 * result[1]:
        # print winner_2nd[0], data[winner_2nd[0] - 1][0]
        return winner_2nd[0]
    else:
        # print winner_2nd[1], data[winner_2nd[1] - 1][0]
        return winner_2nd[1]


def predict_final_rank(east_training_set_1st, east_training_label_1st, east_training_set_2nd, east_training_label_2nd, \
    east_training_set_3rd, east_training_label_3rd,\
    west_training_set_1st, west_training_label_1st, west_training_set_2nd, west_training_label_2nd, \
    west_training_set_3rd, west_training_label_3rd,\
    training_set_final, training_label_final, east_data, west_data):
    print "round1:"
    east_winner_1st = predict_1st_rank(east_training_set_1st, east_training_label_1st, east_data)
    print "---------"
    west_winner_1st = predict_1st_rank( west_training_set_1st, west_training_label_1st, west_data)

    print "round2:"
    east_winner_2nd = predict_2nd_rank(east_training_set_2nd, east_training_label_2nd, east_data, east_winner_1st)
    print "---------"
    west_winner_2nd = predict_2nd_rank(west_training_set_2nd, west_training_label_2nd, west_data, west_winner_1st)

    print "round3:"
    east_winner_3rd = predict_3rd_rank(east_training_set_3rd, east_training_label_3rd, east_data, east_winner_2nd)
    print "---------"
    west_winner_3rd = predict_3rd_rank(west_training_set_3rd, west_training_label_3rd, west_data, west_winner_2nd)

    east_sort_data = []
    for i in range(1, len(east_data[0])):
        tmp_data = []
        for j in range(8):
            tmp_data.append(east_data[j][i])
        if i == 16 or i == 17 or i == 19:
            tmp_data.sort()
        else:
            tmp_data.sort(reverse=True)
        east_sort_data.append(tmp_data)

    west_sort_data = []
    for i in range(1, len(west_data[0])):
        tmp_data = []
        for j in range(8):
            tmp_data.append(west_data[j][i])
        if i == 16 or i == 17 or i == 19:
            tmp_data.sort()
        else:
            tmp_data.sort(reverse=True)
        west_sort_data.append(tmp_data)

    test_data = []
    tmp_test_data = []
    for j in range(len(east_data[0]) - 1):
        tmp_test_data.append(east_sort_data[j].index(east_data[east_winner_3rd - 1][j + 1]) + 1)
    test_data.append(tmp_test_data)

    tmp_test_data = []
    for j in range(len(west_data[0]) - 1):
        tmp_test_data.append(west_sort_data[j].index(west_data[west_winner_3rd - 1][j + 1]) + 1)
    test_data.append(tmp_test_data)

    result = predict_rank(training_set_final, training_label_final, test_data)
    print "round4:"
    if result[0] > result[1]:
        print east_winner_3rd, east_data[east_winner_3rd - 1][0]
        return "E|" + str(east_winner_3rd)
    else:
        print west_winner_3rd, west_data[west_winner_3rd - 1][0]
        return "W|" + str(west_winner_3rd)


def init_training_set_diff(year):
    data_processed.xls2text_diff()
    east_training_dict, east_training_label_dict, west_training_dict, west_training_label_dict = \
        data_processed.training_set_construct_diff(year)
    east_training_set = []
    east_training_label = []
    west_training_set = []
    west_training_label = []
    for key in east_training_dict.keys():
        for d in east_training_dict[key]:
            east_training_set.append(d)
        for d in east_training_label_dict[key]:
            east_training_label.append(d)
    for key in west_training_dict.keys():
        for d in west_training_dict[key]:
            west_training_set.append(d)
        for d in west_training_label_dict[key]:
            west_training_label.append(d)
    return east_training_set, east_training_label, west_training_set, west_training_label


def predict_diff(training_set, training_label, test_data, weight, part, is_final):
    gbdt = GradientBoostingClassifier()
    gbdt.fit(training_set, training_label)
    col = ["投篮", "三分", "罚球", "篮板", "助攻", "抢断", "盖帽", "失误",
           "得", "失", "胜", "主客"]
    important = gbdt.feature_importances_
    # for i in range(len(col)):
    #     print i + 3, col[i], ":", important[i]
    # for i in test_data:
    #     print i
    # print rf.predict_proba(test_data)
    if len(test_data) == 4:
        proba = gbdt.predict_proba(test_data)
        res = []
        for i in range(len(proba)):
            if 0 * proba[i][0] > 1 * proba[i][1]:
                res.append(0)
            else:
                res.append(1)
    elif len(test_data) == 2:
        proba = gbdt.predict_proba(test_data)
        res = []
        if part == "E":
            for i in range(len(proba)):
                if 0.181 * proba[i][0] > (1 - 0.181) * proba[i][1]:
                    res.append(0)
                else:
                    res.append(1)
        else:
            for i in range(len(proba)):
                if 0.126 * proba[i][0] > (1 - 0.126) * proba[i][1]:
                    res.append(0)
                else:
                    res.append(1)
    elif not is_final:
        proba = gbdt.predict_proba(test_data)
        res = []
        if part == "E":
            for i in range(len(proba)):
                if 0.256 * proba[i][0] > (1 - 0.256) * proba[i][1]:
                    res.append(0)
                else:
                    res.append(1)
        else:
            for i in range(len(proba)):
                if 0.128 * proba[i][0] > (1 - 0.128) * proba[i][1]:
                    res.append(0)
                else:
                    res.append(1)
    else:
        proba = gbdt.predict_proba(test_data)
        res = []
        for i in range(len(proba)):
            if proba[i][0] > proba[i][1]:
                res.append(0)
            else:
                res.append(1)
    return res


def predict_1st_diff(training_set, training_label, data, weight, part):
    test_data = []
    test_data.append(list(map(lambda x: x[0] - x[1], zip(data[0][1:], data[7][1:]))) + [1])
    test_data.append(list(map(lambda x: x[0] - x[1], zip(data[1][1:], data[6][1:]))) + [1])
    test_data.append(list(map(lambda x: x[0] - x[1], zip(data[2][1:], data[5][1:]))) + [1])
    test_data.append(list(map(lambda x: x[0] - x[1], zip(data[3][1:], data[4][1:]))) + [1])
    result = predict_diff(training_set, training_label, test_data, weight, part, False)
    winner = []
    for i in range(4):
        if i == 3:
            if result[i] == 1:
                winner.insert(1, i)
            else:
                winner.insert(1, 7 - i)
        else:
            if result[i] == 1:
                winner.append(i)
            else:
                winner.append(7 - i)
    # for i in winner:
    #     print i + 1, data[i][0]
    return winner


def predict_2nd_diff(training_set, training_label, data, winner_1st, weight, part):
    test_data = []
    if winner_1st[0] < winner_1st[1]:
        test_data.append(list(map(lambda x: x[0] - x[1], zip(data[winner_1st[0]][1:], data[winner_1st[1]][1:]))) + [1])
    else:
        test_data.append(list(map(lambda x: x[0] - x[1], zip(data[winner_1st[0]][1:], data[winner_1st[1]][1:]))) + [0])
    if winner_1st[2] < winner_1st[3]:
        test_data.append(list(map(lambda x: x[0] - x[1], zip(data[winner_1st[2]][1:], data[winner_1st[3]][1:]))) + [1])
    else:
        test_data.append(list(map(lambda x: x[0] - x[1], zip(data[winner_1st[2]][1:], data[winner_1st[3]][1:]))) + [0])
    result = predict_diff(training_set, training_label, test_data, weight, part, False)
    winner = []
    if result[0] == 1:
        winner.append(winner_1st[0])
    else:
        winner.append(winner_1st[1])
    if result[1] == 1:
        winner.append(winner_1st[2])
    else:
        winner.append(winner_1st[3])
    # for i in winner:
    #     print i + 1,data[i][0]
    return winner


def predict_3rd_diff(training_set, training_label, data, winner_2nd, weight, part):
    test_data = []
    if winner_2nd[0] < winner_2nd[1]:
        test_data.append(list(map(lambda x: x[0] - x[1], zip(data[winner_2nd[0]][1:], data[winner_2nd[1]][1:]))) + [1])
    else:
        test_data.append(list(map(lambda x: x[0] - x[1], zip(data[winner_2nd[0]][1:], data[winner_2nd[1]][1:]))) + [0])
    result = predict_diff(training_set, training_label, test_data, weight, part, False)
    if result[0] == 1:
        winner = winner_2nd[0]
    else:
        winner = winner_2nd[1]
    # print winner + 1, data[winner][0]
    return winner


def predict_final_diff(east_training_set, east_training_label, east_data, west_training_set, west_training_label, west_data, weight = None):
    print "round1:"
    east_winner_1st = predict_1st_diff(east_training_set, east_training_label, east_data, weight, "E")
    print "---------"
    west_winner_1st = predict_1st_diff(west_training_set, west_training_label, west_data, weight, "W")

    print "round2:"
    east_winner_2nd = predict_2nd_diff(east_training_set, east_training_label, east_data, east_winner_1st, weight, "E")
    print "---------"
    west_winner_2nd = predict_2nd_diff(west_training_set, west_training_label, west_data, west_winner_1st, weight, "W")

    print "round3:"
    east_winner_3rd = predict_3rd_diff(east_training_set, east_training_label, east_data, east_winner_2nd,weight, "E")
    print "---------"
    west_winner_3rd = predict_3rd_diff(west_training_set, west_training_label, west_data, west_winner_2nd,weight, "W")
    if east_data[east_winner_3rd][11] > west_data[west_winner_3rd][11]:
        test_data = np.array(list(map(lambda x: x[0] - x[1], zip(east_data[east_winner_3rd][1:], west_data[west_winner_3rd][1:]))) + [1])
    else:
        test_data = np.array(list(map(lambda x: x[0] - x[1], zip(east_data[east_winner_3rd][1:], west_data[west_winner_3rd][1:]))) + [0])
    result = predict_diff(west_training_set, west_training_label, test_data.reshape(1, -1), weight, "W", True)
    print "round4:"
    if result == 1:
        print east_winner_3rd + 1, east_data[east_winner_3rd][0]
        return "E|" + str(east_winner_3rd + 1)
    else:
        print west_winner_3rd + 1, west_data[west_winner_3rd][0]
        return "W|" + str(west_winner_3rd + 1)


def predict_single(east_training_set, east_training_label, east_data, west_training_set, west_training_label, west_data,
                   rank_east_training_set, rank_east_training_label, rank_west_training_set, rank_west_training_label,
                   rank_training_set_final, rank_training_label_final, rank_east_data, rank_west_data,
                   weight = None):
    # print "round1:"
    east_winner_1st = predict_1st_diff(east_training_set, east_training_label, east_data, weight, "E")
    # print "---------"
    west_winner_1st = predict_1st_diff(west_training_set, west_training_label, west_data, weight, "W")

    # print "round2:"
    east_winner_2nd = predict_2nd_diff(east_training_set, east_training_label, east_data, east_winner_1st, weight, "E")
    # print "---------"
    west_winner_2nd = predict_2nd_diff(west_training_set, west_training_label, west_data, west_winner_1st, weight, "W")

    # print "round3:"
    east_winner_3rd = predict_3rd_diff(east_training_set, east_training_label, east_data, east_winner_2nd, weight, "E")
    # print "---------"
    west_winner_3rd = predict_3rd_diff(west_training_set, west_training_label, west_data, west_winner_2nd, weight, "W")


    east_sort_data = []
    for i in range(1, len(rank_east_data[0])):
        tmp_data = []
        for j in range(8):
            tmp_data.append(rank_east_data[j][i])
        if i == 16 or i == 17 or i == 19:
            tmp_data.sort()
        else:
            tmp_data.sort(reverse=True)
        east_sort_data.append(tmp_data)

    west_sort_data = []
    for i in range(1, len(rank_west_data[0])):
        tmp_data = []
        for j in range(8):
            tmp_data.append(rank_west_data[j][i])
        if i == 16 or i == 17 or i == 19:
            tmp_data.sort()
        else:
            tmp_data.sort(reverse=True)
        west_sort_data.append(tmp_data)

    test_data = []
    tmp_test_data = []
    for j in range(len(rank_east_data[0]) - 1):
        tmp_test_data.append(east_sort_data[j].index(rank_east_data[east_winner_3rd][j + 1]) + 1)
    test_data.append(tmp_test_data)

    tmp_test_data = []
    for j in range(len(rank_west_data[0]) - 1):
        tmp_test_data.append(west_sort_data[j].index(rank_west_data[west_winner_3rd][j + 1]) + 1)
    test_data.append(tmp_test_data)

    result = predict_rank(rank_training_set_final, rank_training_label_final, test_data)
    # print "round4:"
    if result[0] > 0.8 * result[1]:
        # print east_winner_3rd + 1, rank_east_data[east_winner_3rd][0]
        final = "E" + str(east_winner_3rd)
    else:
        # print west_winner_3rd + 1, rank_west_data[west_winner_3rd][0]
        final = "W" + str(west_winner_3rd)
    return east_winner_1st, east_winner_2nd, east_winner_3rd, west_winner_1st, west_winner_2nd, west_winner_3rd, final


def predict(east_training_set, east_training_label, east_data, west_training_set, west_training_label, west_data,
                   rank_east_training_set, rank_east_training_label, rank_west_training_set, rank_west_training_label,
                   rank_training_set_final, rank_training_label_final, rank_east_data, rank_west_data,
                   weight = None):
    east_winner_1st = []
    east_winner_2nd = []
    east_winner_3rd = []
    west_winner_1st = []
    west_winner_2nd = []
    west_winner_3rd = []
    final = []
    for i in range(10):
        east_winner_1st_tmp, east_winner_2nd_tmp, east_winner_3rd_tmp, west_winner_1st_tmp, west_winner_2nd_tmp, \
        west_winner_3rd_tmp, final_tmp = predict_single(east_training_set, east_training_label, east_data, west_training_set, west_training_label, west_data,
                   rank_east_training_set, rank_east_training_label, rank_west_training_set, rank_west_training_label,
                   rank_training_set_final, rank_training_label_final, rank_east_data, rank_west_data,
                   weight = None)
        east_winner_1st.append(east_winner_1st_tmp)
        east_winner_2nd.append(east_winner_2nd_tmp)
        east_winner_3rd.append(east_winner_3rd_tmp)
        west_winner_1st.append(west_winner_1st_tmp)
        west_winner_2nd.append(west_winner_2nd_tmp)
        west_winner_3rd.append(west_winner_3rd_tmp)
        final.append(final_tmp)
    east_winner_1st_res = []
    east_winner_2nd_res = []
    east_winner_3rd_res = -1
    west_winner_1st_res = []
    west_winner_2nd_res = []
    west_winner_3rd_res = -1
    final_res = ""
    if east_winner_1st.count(0) >= east_winner_1st.count(7):
        east_winner_1st_res.append(0)
    else:
        east_winner_1st_res.append(7)
    if east_winner_1st.count(3) >= east_winner_1st.count(4):
        east_winner_1st_res.append(3)
    else:
        east_winner_1st_res.append(4)
    if east_winner_1st.count(1) >= east_winner_1st.count(6):
        east_winner_1st_res.append(1)
    else:
        east_winner_1st_res.append(6)
    if east_winner_1st.count(2) >= east_winner_1st.count(5):
        east_winner_1st_res.append(2)
    else:
        east_winner_1st_res.append(5)

    if west_winner_1st.count(0) >= west_winner_1st.count(7):
        west_winner_1st_res.append(0)
    else:
        west_winner_1st_res.append(7)
    if west_winner_1st.count(3) >= west_winner_1st.count(4):
        west_winner_1st_res.append(3)
    else:
        west_winner_1st_res.append(4)
    if west_winner_1st.count(1) >= west_winner_1st.count(6):
        west_winner_1st_res.append(1)
    else:
        west_winner_1st_res.append(6)
    if west_winner_1st.count(2) >= west_winner_1st.count(5):
        west_winner_1st_res.append(2)
    else:
        west_winner_1st_res.append(5)

    if east_winner_2nd.count(east_winner_1st_res[0]) >= east_winner_2nd.count(east_winner_1st_res[1]):
        east_winner_2nd_res.append(east_winner_1st_res[0])
    else:
        east_winner_2nd_res.append(east_winner_1st_res[1])
    if east_winner_2nd.count(east_winner_1st_res[2]) >= east_winner_2nd.count(east_winner_1st_res[3]):
        east_winner_2nd_res.append(east_winner_1st_res[2])
    else:
        east_winner_2nd_res.append(east_winner_1st_res[3])

    if west_winner_2nd.count(west_winner_1st_res[0]) >= west_winner_2nd.count(west_winner_1st_res[1]):
        west_winner_2nd_res.append(west_winner_1st_res[0])
    else:
        west_winner_2nd_res.append(west_winner_1st_res[1])
    if west_winner_2nd.count(west_winner_1st_res[2]) >= west_winner_2nd.count(west_winner_1st_res[3]):
        west_winner_2nd_res.append(west_winner_1st_res[2])
    else:
        west_winner_2nd_res.append(west_winner_1st_res[3])

    if east_winner_3rd.count(east_winner_2nd_res[0]) >= east_winner_3rd.count(east_winner_2nd_res[1]):
        east_winner_3rd_res = east_winner_2nd_res[0]
    else:
        east_winner_3rd_res = east_winner_2nd_res[1]
    if west_winner_3rd.count(west_winner_2nd_res[0]) >= west_winner_3rd.count(west_winner_2nd_res[1]):
        west_winner_3rd_res = west_winner_2nd_res[0]
    else:
        west_winner_3rd_res = west_winner_2nd_res[1]
    if final.count("E" + str(east_winner_3rd_res)) > final.count("W" + str(west_winner_3rd_res)):
        final_res = "E" + str(east_winner_3rd_res)
    else:
        final_res = "W" + str(west_winner_3rd_res)

    return east_winner_1st_res, east_winner_2nd_res, east_winner_3rd_res, west_winner_1st_res, west_winner_2nd_res, \
           west_winner_3rd_res, final_res


def predict_output(east_data, west_data, east_winner_1st_res, east_winner_2nd_res, east_winner_3rd_res, west_winner_1st_res, west_winner_2nd_res, \
           west_winner_3rd_res, final_res):
    print "----------round1----------"
    for i in range(4):
        print str(east_winner_1st_res[i] + 1), "." + \
            (east_data[east_winner_1st_res[i]][0]).decode('utf-8').encode('gbk') + "\t".decode('utf-8').encode('gbk')\
            + str(west_winner_1st_res[i] + 1) +  "." + (west_data[west_winner_1st_res[i]][0]).decode('utf-8').encode('gbk')
    print "----------round2-----------"
    for i in range(2):
        print east_winner_2nd_res[i] + 1, ".", east_data[east_winner_2nd_res[i]][0].decode('utf-8').encode('gbk'), \
            "\t", west_winner_2nd_res[i] + 1, ".", west_data[west_winner_2nd_res[i]][0].decode('utf-8').encode('gbk')
    print "----------round3----------"
    print east_winner_3rd_res + 1, ".", east_data[east_winner_3rd_res][0].decode('utf-8').encode('gbk'), "\t", \
        west_winner_3rd_res + 1, ".", west_data[west_winner_3rd_res][0].decode('utf-8').encode('gbk')
    print "----------final----------"
    if final_res[0] == "E":
        final_res = int(final_res.replace("E",""))
        print final_res + 1, ".", east_data[final_res][0].decode('utf-8').encode('gbk')
    else:
        final_res = int(final_res.replace("W",""))
        print final_res + 1, ".", west_data[final_res][0].decode('utf-8').encode('gbk')

