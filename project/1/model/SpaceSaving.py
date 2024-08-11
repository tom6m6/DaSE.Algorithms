import pandas as pd
class SpaceSaving(object):
    def __init__(self, k):
        self.counters = {}
        self.k = k

    def add(self, x):
        if x in self.counters:
            self.counters[x] += 1
        else:
            if len(self.counters) + 1 > self.k:
                min_counter = min(self.counters, key=self.counters.get)
                self.counters[x] = self.counters.pop(min_counter) + 1
            else:
                self.counters[x] = 1

if __name__ == '__main__':
    # 以下内容仅用于测试
    ss = SpaceSaving(10000)
    df = pd.read_csv('../data/data_mini.csv')
    ans_count = {}  # 用于记录各电影在此之前真实出现的次数

    for index, (timestamp, group_data) in enumerate(df.head(50).groupby('timestamp')):
        # print("Timestamp:", timestamp)
        for _, row in group_data.iterrows():
            movie_id = row['movieId']
            ans_count[movie_id] = ans_count.get(movie_id, 0) + 1
            ss.add(movie_id)

    print(ss.counters)
    print(ans_count)
