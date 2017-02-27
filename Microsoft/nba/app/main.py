#  -*- coding: utf-8 -*-
import data_processed
import nba_predict
import sys
TEST_YEAR = [86, 89, 92, 95, 98, 1, 4, 7, 10, 13, 16]
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv[1]) > 2:
            print len(sys.argv[1])
            print "Please enter the last two bits of the year"
        else:
            year = int(sys.argv[1])
            east_training_set_1st, east_training_label_1st, east_training_set_2nd, east_training_label_2nd, \
                east_training_set_3rd, east_training_label_3rd,\
                west_training_set_1st, west_training_label_1st, west_training_set_2nd, west_training_label_2nd, \
                west_training_set_3rd, west_training_label_3rd,\
                training_set_final, training_label_final = nba_predict.init_training_set_rank(year)
            year = data_processed.year2str(year)
            east_data_rank = data_processed.data2digit(data_processed.read_data("data_processed_rank/" + year + "E"))
            west_data_rank = data_processed.data2digit(data_processed.read_data("data_processed_rank/" + year + "W"))

            year = int(year)
            east_training_set, east_training_label, west_training_set, west_training_label = nba_predict.init_training_set_diff(year)
            year = data_processed.year2str(year)
            east_data = data_processed.data2digit(data_processed.read_data("data_processed_diff/" + year + "E"))
            west_data = data_processed.data2digit(data_processed.read_data("data_processed_diff/" + year + "W"))


            east_winner_1st_res, east_winner_2nd_res, east_winner_3rd_res, west_winner_1st_res, west_winner_2nd_res, \
                       west_winner_3rd_res, final_res = nba_predict.predict(east_training_set, east_training_label, east_data,
                                                                            west_training_set, west_training_label, west_data,
                                                                            east_training_set_3rd, east_training_label_3rd,
                                                                            west_training_set_3rd, west_training_label_3rd,
                                                                            training_set_final, training_label_final, east_data_rank,
                                                                            west_data_rank)
            print "[" + year + "]"
            nba_predict.predict_output(east_data, west_data, east_winner_1st_res, east_winner_2nd_res, east_winner_3rd_res, west_winner_1st_res, west_winner_2nd_res, \
                       west_winner_3rd_res, final_res)
    else:
        for year in TEST_YEAR:

            east_training_set_1st, east_training_label_1st, east_training_set_2nd, east_training_label_2nd, \
                east_training_set_3rd, east_training_label_3rd,\
                west_training_set_1st, west_training_label_1st, west_training_set_2nd, west_training_label_2nd, \
                west_training_set_3rd, west_training_label_3rd,\
                training_set_final, training_label_final = nba_predict.init_training_set_rank(year)
            year = data_processed.year2str(year)
            east_data_rank = data_processed.data2digit(data_processed.read_data("data_processed_rank/" + year + "E"))
            west_data_rank = data_processed.data2digit(data_processed.read_data("data_processed_rank/" + year + "W"))

            year = int(year)
            east_training_set, east_training_label, west_training_set, west_training_label = nba_predict.init_training_set_diff(year)
            year = data_processed.year2str(year)
            east_data = data_processed.data2digit(data_processed.read_data("data_processed_diff/" + year + "E"))
            west_data = data_processed.data2digit(data_processed.read_data("data_processed_diff/" + year + "W"))


            east_winner_1st_res, east_winner_2nd_res, east_winner_3rd_res, west_winner_1st_res, west_winner_2nd_res, \
                       west_winner_3rd_res, final_res = nba_predict.predict(east_training_set, east_training_label, east_data,
                                                                            west_training_set, west_training_label, west_data,
                                                                            east_training_set_3rd, east_training_label_3rd,
                                                                            west_training_set_3rd, west_training_label_3rd,
                                                                            training_set_final, training_label_final, east_data_rank,
                                                                            west_data_rank)
            print "[" + year + "]"
            nba_predict.predict_output(east_data, west_data, east_winner_1st_res, east_winner_2nd_res, east_winner_3rd_res, west_winner_1st_res, west_winner_2nd_res, \
                       west_winner_3rd_res, final_res)
