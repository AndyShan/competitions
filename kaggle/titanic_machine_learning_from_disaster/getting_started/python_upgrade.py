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

# 设置费用的上限
fare_ceiling = 40

# 将乘客的fare大于等于fare_ceiling将其设置为fare_ceiling - 1.0
data[data[0::, 9].astype(np.float) >= fare_ceiling, 9] = fare_ceiling - 1.0

# 得到按照fare分类的个数
fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size

# 得到按照pclass分类的个数
number_of_class = len(np.unique(data[0::, 2]))

# 幸存表
survival_table = np.zeros((2, number_of_class, number_of_price_brackets))

# 获取不同pclass的人不同fare的存活率
for i in xrange(number_of_class):
    for j in xrange(number_of_price_brackets):
        women_only_stats = data[(data[0::, 4] == "female") & (data[0::, 2].astype(np.float) == i + 1)
                                & (data[0:, 9].astype(np.float) >= j * fare_bracket_size)
                                & (data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size)
        , 1]

        men_only_stats = data[(data[0::, 4] != "female") & (data[0::, 2].astype(np.float) == i + 1)
                                & (data[0:, 9].astype(np.float) >= j * fare_bracket_size)
                                & (data[0:, 9].astype(np.float) < (j + 1) * fare_bracket_size)
        , 1]
        survival_table[0, i, j] = np.mean(women_only_stats.astype(np.float))
        survival_table[1, i, j] = np.mean(men_only_stats.astype(np.float))
        survival_table[survival_table != survival_table] = 0. # 若为nan则置为 0

# 若存活率大于0.5 则置位1
survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1

test_file = open('C:/Users/AD/PycharmProjects/titanic_machine_learning_from_disaster/data/test.csv', 'rb')
test_file_object = csv.reader(test_file)
header = test_file_object.next()
predictions_file = open("gender_class_model.csv", "wb")
p = csv.writer(predictions_file)
p.writerow(["PassengerId", "Survived"])

for row in test_file_object:
    for j in xrange(number_of_price_brackets):
        try:
            row[8] = float(row[8])
        except:
            bin_fare = 3 - float(row[1])
            break
        if row[8] > fare_ceiling:
            bin_fare = number_of_price_brackets - 1
            break
        if (j + 1) * fare_bracket_size > row[8] >= j * fare_bracket_size:
            bin_fare = j
            break
    if row[3] == 'female':
        p.writerow([row[0], "%d" % int(survival_table[0, float(row[1]) - 1, bin_fare])])
    else:
        p.writerow([row[0], "%d" % int(survival_table[1, float(row[1]) - 1, bin_fare])])

test_file.close()
predictions_file.close()