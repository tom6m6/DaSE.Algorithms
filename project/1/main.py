from model.CountMinSketch import CountMinSketch
from model.MinHeap import MinHeap
from model.SpaceSaving import SpaceSaving
from model.CountMinLogSketch import CountMinLogSketch
import math as math
import argparse
import pandas as pd
import random
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', default=25, type=int, help='Max query k value in Top-K')
    parser.add_argument('--p', default=1e-3, type=float, help='query probability')
    parser.add_argument('--filepath', default='data/data.csv', type=str, help='input file path')
    parser.add_argument('--delta', default=1e-6, type=float, help='delta')
    parser.add_argument('--eps', default=(math.e / 10000), type=float, help='epsilon')
    parser.add_argument('--ssk', default=10000, type=int, help='k value of SpaceSaving')
    parser.add_argument('--is_conservative_update', default=True, type=bool, help='Conservative Update')
    parser.add_argument('--logexp', default=1.00026, type=float, help='CountMinLogSketch exp value')
    parser.add_argument('--head', default=0, type=int, help='how much lines do you want to read from the file?')
    args = parser.parse_args()

    df = pd.read_csv(args.filepath)
    if args.head != 0:
        df = df.head(args.head)

    ans_count = {}  # 用于记录各电影在此之前真实出现的次数
    cms = CountMinSketch(delta=args.delta, epsilon=args.eps, is_conservative_update=args.is_conservative_update)
    cmls = CountMinLogSketch(delta=args.delta, epsilon=args.eps, exp=args.logexp)
    ss = SpaceSaving(args.ssk)
    hp = MinHeap(args.k)
    hp_log = MinHeap(args.k)

    is_query = False
    k = args.k
    query_times12, query_times3 = 0, 0
    sum_error_task1, sum_error_task2, sum_error_task3 = 0, 0, 0
    sum_error_task1_log, sum_error_task2_log, sum_error_task3_log = 0, 0, 0
    sum_error_task1_ss, sum_error_task2_ss, sum_error_task3_ss = 0, 0, 0

    start_time = time.time()
    for index, (timestamp, group_data) in enumerate(df.groupby('timestamp')):
        is_query = False
        # print("Timestamp:", timestamp)
        random_num = random.randint(1, 1000000)
        if random_num <= int(1000000 * args.p):
            is_query = True

        for _, row in group_data.iterrows():
            movie_id = row['movieId']
            cms.add(movie_id)
            cmls.add(movie_id)
            ss.add(movie_id)
            ans_count[movie_id] = ans_count.get(movie_id, 0) + 1

            if movie_id in hp.index_map:
                hp.insert([movie_id, 1])
            else:
                frequent_hat = cms.query(movie_id)
                if len(hp.heap) < args.k:
                    hp.insert([movie_id, frequent_hat])
                elif frequent_hat > hp.getmin():
                    root = hp.heap[0]
                    hp.heap[0] = [movie_id, frequent_hat]
                    hp.index_map[movie_id] = 0
                    hp.adjust_down(0)
                    del hp.index_map[root[0]]

            if movie_id in hp_log.index_map:
                hp_log.insert([movie_id, 1])
            else:
                frequent_hat_log = cmls.query(movie_id)
                if len(hp_log.heap) < args.k:
                    hp_log.insert([movie_id, frequent_hat_log])
                elif frequent_hat_log > hp_log.getmin():
                    root = hp_log.heap[0]
                    hp_log.heap[0] = [movie_id, frequent_hat_log]
                    hp_log.index_map[movie_id] = 0
                    hp_log.adjust_down(0)
                    del hp_log.index_map[root[0]]

        if is_query:
            for _, row in group_data.iterrows():
                query_times12 += 1
                movie_id = row['movieId']
                frequent_hat = cms.query(movie_id)
                frequent_hat_log = cmls.query(movie_id)
                if movie_id in ss.counters:
                    frequent_hat_ss = ss.counters[movie_id]
                else:
                    frequent_hat_ss = 0

                # task1: 成员查询：对给定查询时间戳和电影id，查询该电影在该时间戳及之前是否曾被评分过
                if frequent_hat > 0 and ans_count[movie_id] == 0:
                    # 此时算法认为该电影在该时间戳及之前被评分过
                    # 并且假设该电影此前并没有被评分过(预测失败)
                    sum_error_task1 += 1

                # 根据CMS算法的原理，不可能出现算法认为该电影在该时间戳及之前未被评分过但实际被评分过的情况

                if frequent_hat_log > 0 and ans_count[movie_id] == 0:
                    sum_error_task1_log += 1

                if frequent_hat_ss > 0 and ans_count[movie_id] == 0:
                    sum_error_task1_ss += 1

                # task2: 频度查询：对于给定查询时间戳和电影id，查询该电影在该时间戳及之前被评分的总次数
                sum_error_task2 += (frequent_hat - ans_count[movie_id]) ** 2
                sum_error_task2_log += (frequent_hat_log - ans_count[movie_id]) ** 2
                sum_error_task2_ss += (frequent_hat_ss - ans_count[movie_id]) ** 2

            # task3: Top-k查询：对给定正整数k和查询时间戳，查询在该时间戳及之前被评分次数最多的前k个电影。
            query_times3 += 1

            sum_error_task3_tmp = 0
            sum_error_task3_tmp_log = 0
            sum_error_task3_tmp_ss = 0

            k = random.randint(1, args.k)

            topk_ans_true = sorted(ans_count.items(), key=lambda x: x[1], reverse=True)[:k]
            topk_ans_true = [[x[0], x[1]] for x in topk_ans_true]

            topk_ans_hat = sorted(hp.heap, key=lambda x: x[1], reverse=True)[:k]
            topk_ans_hat_log = sorted(hp_log.heap, key=lambda x: x[1], reverse=True)[:k]

            topk_ans_hat_ss = sorted(ss.counters.items(), key=lambda x: x[1], reverse=True)[:k]
            topk_ans_hat_ss = [[x[0], x[1]] for x in topk_ans_hat_ss]

            for p, q in zip(topk_ans_true, topk_ans_hat):
                sum_error_task3_tmp += (p[1] - q[1]) ** 2

            for p, q in zip(topk_ans_true, topk_ans_hat_log):
                sum_error_task3_tmp_log += (p[1] - q[1]) ** 2

            for p, q in zip(topk_ans_true, topk_ans_hat_ss):
                sum_error_task3_tmp_ss += (p[1] - q[1]) ** 2

            sum_error_task3_tmp = sum_error_task3_tmp / k
            sum_error_task3_tmp_log = sum_error_task3_tmp_log / k
            sum_error_task3_tmp_ss = sum_error_task3_tmp_ss / k

            sum_error_task3 += sum_error_task3_tmp
            sum_error_task3_log += sum_error_task3_tmp_log
            sum_error_task3_ss += sum_error_task3_tmp_ss

            if query_times3 % 100 == 0:
                # 每100次查询显示一下结果
                print("timestamp:{},query_times:{}".format(timestamp, query_times3))

                print("CMS:")
                mean_error_task1, mean_error_task2, mean_error_task3 = (sum_error_task1 / query_times12), (
                        sum_error_task2 / query_times12), (sum_error_task3 / query_times3)
                print("task1 MSE:{} task2 MSE:{} task3 MSE:{}".format(mean_error_task1, mean_error_task2,
                                                                      mean_error_task3))
                print("CMLS:")
                mean_error_task1_log, mean_error_task2_log, mean_error_task3_log = (
                            sum_error_task1_log / query_times12), (
                        sum_error_task2_log / query_times12), (sum_error_task3_log / query_times3)

                print("task1 MSE:{} task2 MSE:{} task3 MSE:{}".format(mean_error_task1_log, mean_error_task2_log,
                                                                      mean_error_task3_log))
                print("SpaceSaving:")
                mean_error_task1_ss, mean_error_task2_ss, mean_error_task3_ss = (sum_error_task1_ss / query_times12), (
                        sum_error_task2_ss / query_times12), (sum_error_task3_ss / query_times3)
                print("task1 MSE:{} task2 MSE:{} task3 MSE:{}".format(mean_error_task1_ss, mean_error_task2_ss,
                                                                      mean_error_task3_ss))

            '''
            print(topk_ans_true)
            print(topk_ans_hat)
            '''
    end_time = time.time()
    if query_times12 == 0:
        mean_error_task1 = 0
        mean_error_task2 = 0
        mean_error_task3 = 0
        print("Because query_times12 == 0, result == 0")
        execution_time = end_time - start_time
        print("Execution time: ", execution_time, "seconds")
    else:
        print("CMS:")
        mean_error_task1, mean_error_task2, mean_error_task3 = (sum_error_task1 / query_times12), (
                sum_error_task2 / query_times12), (sum_error_task3 / query_times3)
        print("task1 MSE:{} task2 MSE:{} task3 MSE:{}".format(mean_error_task1, mean_error_task2,
                                                              mean_error_task3))
        print("CMLS:")
        mean_error_task1_log, mean_error_task2_log, mean_error_task3_log = (
                sum_error_task1_log / query_times12), (
                sum_error_task2_log / query_times12), (sum_error_task3_log / query_times3)

        print("task1 MSE:{} task2 MSE:{} task3 MSE:{}".format(mean_error_task1_log, mean_error_task2_log,
                                                              mean_error_task3_log))
        print("SpaceSaving:")
        mean_error_task1_ss, mean_error_task2_ss, mean_error_task3_ss = (sum_error_task1_ss / query_times12), (
                sum_error_task2_ss / query_times12), (sum_error_task3_ss / query_times3)
        print("task1 MSE:{} task2 MSE:{} task3 MSE:{}".format(mean_error_task1_ss, mean_error_task2_ss,
                                                              mean_error_task3_ss))
        execution_time = end_time - start_time
        print("Execution time: ", execution_time, "seconds")
