import pandas as pd
import os

if __name__ == '__main__':
    print(os.getcwd())
    df1 = pd.read_csv('../data/ratings.csv')
    df1.sort_values(by='timestamp', inplace=True)
    df1 = df1[['timestamp', 'movieId']]
    df1.to_csv('../data/data.csv', index=False)

    df2 = pd.read_csv('../data/data.csv')
    data_mini = df2.head(100)
    data_mini.to_csv('../data/data_mini.csv', index=False)