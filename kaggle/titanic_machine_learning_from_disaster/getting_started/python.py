#  -*- coding: utf-8 -*-
import numpy as np
import csv as csv

# 读取数据
csv_file_object = csv.reader(open("C:/Users/AD/PycharmProjects/titanic_machine_learning_from_disaster/data"
                                  "/train.csv", "rb"))
# 跳过列名
header = csv_file_object.next()

# 读取数据
data = []
for row in csv_file_object:
    data.append(row)
data = np.array(data)

# 使用numpy统计存活率
number_passengers = np.size(data[0::, 1].astype(np.float))
number_survived = np.sum(data[0::, 1].astype(np.float))
proportion_survivors = number_survived / number_passengers

# 统计船上的每位乘客是否为女性
women_only_stats = data[0::, 4] == "female"
men_only_stats = data[0::, 4] != "female"

# 按性别统计存活数
women_onboard = data[women_only_stats, 1].astype(np.float)
men_onboard = data[men_only_stats, 1].astype(np.float)

# 分别统计男女存活率
proportion_women_survived = np.sum(women_onboard) / np.size(women_onboard)
proportion_men_survived = np.sum(men_onboard) / np.size(men_onboard)

# proportion_women_survived = 0.742038216561
# proportion_men_survived = 0.188908145581
# 由简单统计得出女性乘客存活率更高，决定规则，如果是女性乘客就预测为存活

# 读取测试文件
test_file = open("C:/Users/AD/PycharmProjects/titanic_machine_learning_from_disaster/data/test.csv", "rb")
test_file_object = csv.reader(test_file)
header = test_file_object.next()

# 创建测试结果文件
prediction_file = open("gender_based_model.csv", "wb")
prediction_file_object = csv.writer(prediction_file)

# 写入列名并判断预测数据的性别是否为女性，基于规则预测是否存活
prediction_file_object.writerow(["PassengerId", "Survived"])
for row in test_file_object:
    if row[3] == 'female':
        prediction_file_object.writerow([row[0], 1])
    else:
        prediction_file_object.writerow([row[0], 0])
test_file.close()
prediction_file.close()