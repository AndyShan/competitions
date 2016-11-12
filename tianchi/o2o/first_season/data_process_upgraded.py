#  -*- coding: utf-8 -*-
import model
import file_data
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from numpy import *
from imblearn.over_sampling import SMOTE

MOUTH = [31, 29, 31, 30, 31, 30]
UCB = 0.478872089763
UCBID = 0.426788396311
UB = 2.54035823625
UUR = 0.066368408765
UUB = 0.0840314715117
OUU = 0.0598824189205
OUUID = 0.0572482723917
OUB = 4.10497885384
OUUR = 0.2122912522
OUUB = 0.0134535724562
OUF = 0.0799693467163
DISR = 0.844331107968
DIST = 2.92454221741


def get_rate(a, b):
    """
    获取满减形式的折扣率
    :param a:
    :param b:
    :return:
    """
    ratio = 100 / a
    return (100 - (ratio * b)) / 100


def load_data2object(filename):
    """
    读取数据存入对象供特征提取方法使用
    :param filename:
    :return:
    """
    file = open(filename)
    offline_users = []
    # offline_merchants = []
    # offline_coupons = []
    for line in file:
        arr = line.replace("\n", "").split(",")
        if len(arr) == 7:
            user = model.OfflineUser(arr[0], arr[1], arr[2], arr[5], arr[6])
            offline_users.append(user)
            # merchant = model.OfflineMerchant(arr[1], arr[2], arr[5], arr[6])
            # offline_merchants.append(merchant)
            # coupon = model.OfflineCoupon(arr[2], arr[5], arr[6])
            # offline_coupons.append(coupon)
        elif len(arr) == 6:
            user = model.OfflineUser(arr[0], arr[1], arr[2], arr[5], "null")
            offline_users.append(user)
            # merchant = model.OfflineMerchant(arr[1], arr[2], arr[5], "null")
            # offline_merchants.append(merchant)
            # coupon = model.OfflineCoupon(arr[2], arr[5], "null")
            # offline_coupons.append(coupon)
    file.close()

    online_file = open(file_data.ONLINE_TRAIN)
    online_users = []
    for line in online_file:
        arr = line.replace("\n","").split(",")
        user = model.OnlineUser(arr[0], arr[3], arr[5], arr[6])
        online_users.append(user)
    online_file.close()

    return offline_users, online_users


def date2num(date):
    """
    日期转数字
    :param date:
    :return:
    """
    num = 0
    m = int(date[4] + date[5]) - 1
    for i in range(m):
        num += MOUTH[i]
    num += int(date[6] + date[7])
    return num


def data_stats():
    """
    数据统计
    :return:
    """
    f = open(file_data.OFFLINE_TRAINING_SET)
    index = 0
    ucb = 0.0
    ucbid = 0.0
    ub = 0.0
    uur = 0.0
    uub = 0.0
    ouu = 0.0
    ouuid = 0.0
    oub = 0.0
    ouur = 0.0
    ouub = 0.0
    ouf = 0.0
    disr = 0.0
    dist = 0.0

    for line in f:
        arr = line.replace("\n","").split("\t")
        index += 1
        if arr[0] != "null":
            ucb += float(arr[0])
        if arr[1] != "null":
            ucbid += float(arr[1])
        if arr[2] != "null":
            ub += float(arr[2])
        if arr[3] != "null":
            uur += float(arr[3])
        if arr[4] != "null":
            uub += float(arr[4])
        if arr[5] != "null":
            ouu += float(arr[5])
        if arr[6] != "null":
            ouuid += float(arr[6])
        if arr[7] != "null":
            oub += float(arr[7])
        if arr[8] != "null":
            ouur += float(arr[8])
        if arr[9] != "null":
            ouub += float(arr[9])
        if arr[10] != "null":
            ouf += float(arr[10])
        if arr[11] != "null":
            disr += float(arr[11])
        if arr[12] != "null":
            dist += float(arr[12])
    print ucb / index
    print ucbid / index
    print ub / index
    print uur / index
    print uub / index
    print ouu / index
    print ouuid / index
    print oub / index
    print ouur / index
    print ouub / index
    print ouf / index
    print disr / index
    print dist / index
    f.close()


def offline_user_feature(offline_users):
    """
    离线用户特征提取
    :param offline_users:
    :return:
    """
    offline_user_coupon_buy = {}  # 用券数
    offline_user_coupon_buy_in_date = {}  # 用券有效数
    offline_user_buy = {}  # 正常购买数
    offline_user_receive = {}  # 领取数
    offline_user_use_receive = {}  # 用券 / 领取
    offline_user_use_buy = {}  # 用券 / 正常买
    for user in offline_users:
        if user.uid in offline_user_coupon_buy:
            if user.is_positive():
                offline_user_coupon_buy[user.uid] += 1
            if user.is_buy():
                offline_user_buy[user.uid] += 1
            if user.is_receive():
                offline_user_receive[user.uid] += 1
            if user.is_use_in_date():
                offline_user_coupon_buy_in_date[user.uid] += 1
        else:
            if user.is_positive():
                offline_user_coupon_buy[user.uid] = 1
            else:
                offline_user_coupon_buy[user.uid] = 0
            if user.is_buy():
                offline_user_buy[user.uid] = 1
            else:
                offline_user_buy[user.uid] = 0
            if user.is_receive():
                offline_user_receive[user.uid] = 1
            else:
                offline_user_receive[user.uid] = 0
            if user.is_use_in_date():
                offline_user_coupon_buy_in_date[user.uid] = 1
            else:
                offline_user_coupon_buy_in_date[user.uid] = 0

    for k, v in offline_user_coupon_buy.items():
        if int(offline_user_receive[k]) == 0:
            offline_user_use_receive[k] = 0
        else:
            offline_user_use_receive[k] = float(v) / (offline_user_receive[k])
        if int(offline_user_buy[k]) == 0:
            offline_user_use_buy[k] = 0
        else:
            offline_user_use_buy[k] = float(v) / (offline_user_buy[k])

    return offline_user_coupon_buy, offline_user_coupon_buy_in_date, offline_user_buy, offline_user_use_receive, \
           offline_user_use_buy


def online_user_feature(online_users):
    online_user_use = {}  # 在线用户使用优惠券数目
    online_user_use_in_date = {}  # 在线用户使用优惠券有效数
    online_user_buy = {}  # 在线用户购买数
    online_user_receive = {}  # 在线用户领券数
    online_user_use_receive = {}  # 在线用户使用 / 领券
    online_user_use_buy = {}  # 在线用户使用 / 正常购买
    online_user_fixed = {}  # 在线用户参加限时优惠的数目
    for u in online_users:
        if u.uid in online_user_use:
            if u.is_use():
                online_user_use[u.uid] += 1
            if u.is_buy():
                online_user_buy[u.uid] += 1
            if u.is_receive():
                online_user_receive[u.uid] += 1
            if u.is_fixed():
                online_user_fixed[u.uid] += 1
            if u.is_use_in_date():
                online_user_use_in_date[u.uid] += 1
        else:
            if u.is_use():
                online_user_use[u.uid] = 1
            else:
                online_user_use[u.uid] = 0
            if u.is_buy():
                online_user_buy[u.uid] = 1
            else:
                online_user_buy[u.uid] = 0
            if u.is_receive():
                online_user_receive[u.uid] = 1
            else:
                online_user_receive[u.uid] = 0
            if u.is_fixed():
                online_user_fixed[u.uid] = 1
            else:
                online_user_fixed[u.uid] = 0
            if u.is_use_in_date():
                online_user_use_in_date[u.uid] = 1
            else:
                online_user_use_in_date[u.uid] = 0
    for k, v in online_user_use.items():
        if int(online_user_receive[k]) == 0:
            online_user_use_receive[k] = 0
        else:
            online_user_use_receive[k] = float(v) / online_user_receive[k] + 1
        if int(online_user_buy[k] == 0):
            online_user_use_buy[k] = 0
        else:
            online_user_use_buy[k] = float(v) / online_user_buy[k]

    return online_user_use, online_user_use_in_date, online_user_buy, online_user_use_receive, online_user_use_buy, \
            online_user_fixed


def offline_train_data(flag, offline_user_coupon_buy, offline_user_coupon_buy_in_date, offline_user_buy, \
            offline_user_use_receive, offline_user_use_buy, online_user_use, online_user_use_in_date, online_user_buy,
            online_user_use_receive, online_user_use_buy, online_user_fixed):
    f = open(file_data.OFFLINE_TRAINING_SET, "a+")
    pre_x = []
    if flag == 0:
        ff = open(file_data.OFFLINE_TRAIN)
    elif flag == 1:
        ff = open(file_data.TEST_DATA)
    for line in ff:
        ucb = UCB
        ucbid = UCBID
        ub = UB
        uur = UUR
        uub = UUB
        ouu = OUU
        ouuid = OUUID
        oub = OUB
        ouur = OUUR
        ouub = OUUB
        ouf = OUF
        disr = DISR
        dist = DIST
        arr = line.replace("\n","").split(",")
        if arr[0] in offline_user_coupon_buy:
            ucb = str(offline_user_coupon_buy[arr[0]])
            ucbid = str(offline_user_coupon_buy_in_date[arr[0]])
            ub = str(offline_user_buy[arr[0]])
            uur = str(offline_user_use_receive[arr[0]])
            uub = str(offline_user_use_buy[arr[0]])
        if arr[0] in online_user_use:
            ouu = str(online_user_use[arr[0]])
            ouuid = str(online_user_use_in_date[arr[0]])
            oub = str(online_user_buy[arr[0]])
            ouur = str(online_user_use_receive[arr[0]])
            ouub = str(online_user_use_buy[arr[0]])
            ouf = str(online_user_fixed[arr[0]])
        if arr[3] != "null":
            if ":" in arr[3]:
                rates = arr[3].split(":")
                disr = str(get_rate(float(rates[0]), float(rates[1])))
            else:
                disr = str(arr[3])
        if arr[4] != "null":
            dist = str(arr[4])
        if flag == 0:
            if arr[2] != "null" and arr[6] != "null" and (date2num(arr[6]) - date2num(arr[5]) <= 15):
                f.write(str(ucb) + "\t" + str(ucbid) + "\t" + str(ub) + "\t" + str(uur) + "\t" + str(uub) + "\t" +
                        str(ouu) + "\t" + str(ouuid) + "\t" + str(oub) +
                        "\t" + str(ouur) + "\t" + str(ouub) + "\t" + str(ouf) + "\t" +
                        str(disr) + "\t" + str(dist) +
                        "\t" + "1" + "\n")
            elif arr[2] != "null" and arr[6] != "null" and (date2num(arr[6]) - date2num(arr[5]) > 15):
                f.write(str(ucb) + "\t" + str(ucbid) + "\t" + str(ub) + "\t" + str(uur) + "\t" + str(uub) + "\t" +
                        str(ouu) + "\t" + str(ouuid) + "\t" + str(oub) +
                        "\t" + str(ouur) + "\t" + str(ouub) + "\t" + str(ouf) + "\t" +
                        str(disr) + "\t" + str(dist) +
                        "\t" + "2" + "\n")
            elif arr[2] != "null" and arr[6] == "null":
                f.write(str(ucb) + "\t" + str(ucbid) + "\t" + str(ub) + "\t" + str(uur) + "\t" + str(uub) + "\t" +
                        str(ouu) + "\t" + str(ouuid) + "\t" + str(oub) +
                        "\t" + str(ouur) + "\t" + str(ouub) + "\t" + str(ouf) + "\t" +
                        str(disr) + "\t" + str(dist) +
                        "\t" + "0" + "\n")
        elif flag == 1:
            pre_x.append([float(ucb), float(ucbid), float(ub), float(uur), float(uub),
                          float(ouu), float(ouuid), float(oub),
                          float(ouur), float(ouub), float(ouf),
                          float(disr), float(dist)])
    ff.close()
    f.close()
    return pre_x


def init_dict():
    """
    初始化提取特征后的训练数据字典
    :return:
    """
    users, online_users = load_data2object(file_data.OFFLINE_TRAIN)
    offline_user_coupon_buy, offline_user_coupon_buy_in_date, offline_user_buy, offline_user_use_receive, \
    offline_user_use_buy= offline_user_feature(users)
    online_user_use, online_user_use_in_date, online_user_buy, online_user_use_receive, online_user_use_buy, \
    online_user_fixed = online_user_feature(online_users)
    return offline_user_coupon_buy, offline_user_coupon_buy_in_date, offline_user_buy, offline_user_use_receive, \
           offline_user_use_buy, online_user_use, online_user_use_in_date, online_user_buy, online_user_use_receive, \
           online_user_use_buy, online_user_fixed


def load_data():
    """
    读取提取特征后的训练数据
    :return:
    """
    data_mat = []
    label_mat = []
    fr = open(file_data.BALANCED_TRAINING_SET)
    for line in fr.readlines():
        line_arr = line.strip().replace("\n","").split("\t")
        data_mat.append([float(line_arr[0]), float(line_arr[1]) , float(line_arr[2]), float(line_arr[3]),
                         float(line_arr[4]), float(line_arr[5]), float(line_arr[6]), float(line_arr[7]),
                         float(line_arr[8]), float(line_arr[9]), float(line_arr[10]), float(line_arr[11]),
                         float(line_arr[12])])
        label_mat.append(int(line_arr[13]))
    return data_mat, label_mat


def fit(d, l, pre_x):
    """
    训练和预测
    :param d:
    :param l:
    :param pre_x:
    :return:
    """
    lr = GradientBoostingClassifier(n_estimators=200, max_features="sqrt")
    lr.fit(array(d), array(l))
    print lr.feature_importances_
    f = open("newresult.txt", "a+")
    for x in pre_x:
        f.write(str(float(lr.predict_proba(array(x).reshape(1, -1))[0][1])) + "\n")


def main():
    offline_user_coupon_buy, offline_user_coupon_buy_in_date, offline_user_buy, offline_user_use_receive, \
    offline_user_use_buy, online_user_use, online_user_use_in_date, online_user_buy, online_user_use_receive, \
           online_user_use_buy, online_user_fixed = init_dict()

    offline_train_data(0, offline_user_coupon_buy, offline_user_coupon_buy_in_date, offline_user_buy, offline_user_use_receive, \
           offline_user_use_buy, online_user_use, online_user_use_in_date, online_user_buy, online_user_use_receive, \
           online_user_use_buy, online_user_fixed
                       )
    # data_stats()
    print "offline_training_set ok!"
    pre_x = offline_train_data(1, offline_user_coupon_buy, offline_user_coupon_buy_in_date, offline_user_buy, offline_user_use_receive, \
           offline_user_use_buy, online_user_use, online_user_use_in_date, online_user_buy, online_user_use_receive, \
           online_user_use_buy, online_user_fixed)

    over_sampling()
    d, l = load_data()
    print "data load ok!"
    fit(d, l, pre_x)
    print "train ok!"


def generate_results(method):
    """
    合成比赛要求格式的结果文件
    :param method:
    :return:
    """
    if method == "train":
        test_file = open(file_data.TEST_DATA)
    elif method == "test":
        test_file = open(file_data.CROSS_TEST)
    pro_file = open("newresult.txt")
    result_file = open("result2.txt", "a+")
    lines = test_file.readlines()
    lines2 = pro_file.readlines()
    if method == "train":
        for i in range(len(lines)):
            arr = str(lines[i]).replace("\n","").split(",")
            result_file.write(arr[0] + "," + arr[2] + "," + arr[5] + "," + '%.10f' % float(lines2[i]) + "\n")
    elif method == "test":
        for i in range(len(lines)):
            arr = str(lines[i]).replace("\n","").split(",")
            if arr[2] != "null" and arr[6] != "null":
                result_file.write(arr[2] + "\t" + "1" + "\t" + lines2[i])
            elif arr[2] != "null" and arr[6] == "null":
                result_file.write(arr[2] + "\t" + "0" + "\t" + lines2[i])
    test_file.close()
    pro_file.close()
    result_file.close()


def cross():
    """
    为交叉验证划分训练集
    :return:
    """
    f = open(file_data.CROSS_TRAIN, "a+")
    ff = open(file_data.CROSS_TEST, "a+")
    fff = open(file_data.OFFLINE_TRAIN)

    random_index = random.randint(0, 20)
    index = 0
    for line in fff:
        if index == random_index:
            arr = line.replace("\n","").split(",")
            if arr[2] != "null":
                ff.write(line)
                index = 0
                random_index = random.randint(0, 20)
        else:
            index += 1
            f.write(line)


def auc():
    """
    auc 模型评价
    :return:
    """
    f = open("result.txt")
    cid_pre = {}
    cid_true = {}
    for line in f:
        arr = line.replace("\n","").split("\t")
        if arr[0] in cid_pre:
            cid_pre[arr[0]].append(float(arr[2]))
        else:
            cid_pre[arr[0]] = [float(arr[2])]
        if arr[0] in cid_true:
            cid_true[arr[0]].append(int(arr[1]))
        else:
            cid_true[arr[0]] = [int(arr[1])]
    sco_sum = 0.0
    sco_index = 0
    for k,v in cid_true.items():
        if 1 in v and 0 in v:
            y_true = array(v)
            y_pre = array(cid_pre[k])
            sco = roc_auc_score(y_true, y_pre)
            sco_index += 1
            sco_sum += sco
    print sco_sum / sco_index


def over_sampling():
    """
    使用smote的over sampling
    :return:
    """
    ff = open(file_data.BALANCED_TRAINING_SET, "a+")
    data_mat = []
    label_mat = []
    fr = open(file_data.OFFLINE_TRAINING_SET)
    for line in fr.readlines():
        line_arr = line.strip().replace("\n","").split("\t")
        data_mat.append([float(line_arr[0]), float(line_arr[1]) , float(line_arr[2]), float(line_arr[3]),
                         float(line_arr[4]), float(line_arr[5]), float(line_arr[6]), float(line_arr[6]),
                         float(line_arr[7]), float(line_arr[8]), float(line_arr[9]), float(line_arr[10]), float(line_arr[11]), float(line_arr[12])])
        label_mat.append(int(line_arr[13]))
    sm = SMOTE(random_state=42)
    data_mat_res, label_mat_res = sm.fit_sample(data_mat, label_mat)
    for i in range(len(data_mat_res)):
        ff.write(str(data_mat_res[i][0]) + "\t" + str(data_mat_res[i][1]) + "\t" + str(data_mat_res[i][2]) + "\t" +
                 str(data_mat_res[i][3]) + "\t" + str(data_mat_res[i][4]) + "\t" + str(data_mat_res[i][5]) + "\t" +
                 str(data_mat_res[i][6]) + "\t" + str(data_mat_res[i][7]) + "\t" + str(data_mat_res[i][8]) + "\t" +
                 str(data_mat_res[i][9]) + "\t" + str(data_mat_res[i][10]) + "\t"+str(data_mat_res[i][11]) + "\t" +
                 str(data_mat_res[i][12]) + "\t" + str(label_mat_res[i]) + "\n")
    ff.close()
    fr.close()


if __name__ == "__main__":
    # cross()
    main()
    generate_results("train")
    # auc()

