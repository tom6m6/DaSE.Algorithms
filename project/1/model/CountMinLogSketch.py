from array import array
from math import log, e, ceil, pow
import hashlib
import random


class CountMinLogSketch(object):
    def __init__(self, w=None, d=None, delta=None, epsilon=None, exp=1.00026):
        if w is not None and d is not None:
            self.w = w
            self.d = d
        elif delta is not None and epsilon is not None:
            self.w = int(ceil(e / epsilon))
            self.d = int(ceil(log(1. / delta)))
        else:
            raise Exception("Incomplete parameters. Please provide w&d or delta&epsilon.")

        self.exp = exp
        # 数组元素的类型是long
        self.table = [array('l', (0 for _ in range(self.w))) for _ in range(self.d)]

    def increaseDecision(self, c):
        return random.random() * pow(self.exp, float(c)) < 1

    def pointValue(self, c):
        if c == 0:
            return 0
        return pow(self.exp, float(c-1))

    def value(self, c):
        if c <= 1:
            return self.pointValue(c)
        else:
            v = self.pointValue(c + 1)
            return (1 - v) / (1 - self.exp)
    def _hash(self, x):
        md5 = hashlib.md5(str(hash(x)).encode())
        for i in range(self.d):
            md5.update(str(i).encode())
            yield int(md5.hexdigest(), 16) % self.w

    def add(self, x, v=1):
        # 元素x出现了v次
        for _ in range(1, v+1):
            c = min(table[i] for table, i in zip(self.table, self._hash(x)))
            if self.increaseDecision(c):
                for table, i in zip(self.table, self._hash(x)):
                    if table[i] == c:
                        table[i] += 1
        """
        c = min(table[i] for table, i in zip(self.table, self._hash(x)))
        if self.increaseDecision(c):
            for table, i in zip(self.table, self._hash(x)):
                if table[i] == c:
                    table[i] += v
        """

    def query(self, x):
        # 元素x的估计出现次数
        c = min(table[i] for table, i in zip(self.table, self._hash(x)))
        return int(self.value(c))

    def __getitem__(self, x):
        return self.query(x)


if __name__ == '__main__':
    # 以下内容仅用于测试
    cmls = CountMinLogSketch(delta=1e-6, epsilon=(e / 1000) )
    cmls.add(1)
    cmls.add(2)
    cmls.add(1)
    cmls.add(3)
    cmls.add(1)
    cmls.add(1)
    cmls.add(1,100)
    print(int(cmls.query(1)))
    print(int(cmls.query(2)))
    print(int(cmls.query(3)))