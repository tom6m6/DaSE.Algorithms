from array import array
from math import log, e, ceil
import hashlib


class CountMinSketch(object):
    def __init__(self, w=None, d=None, delta=None, epsilon=None, is_conservative_update=False):
        """
        w: hash表的大小(映射区间); d: hash表的数量
        如果w和d设置了delta和epsilon就没必要设置了
        delta: 查询错误的最大概率 epsilon: 查询错误的最大偏离值
        w = ceil(e/epsilon)
        d = ceil(ln(1.0/delta))
        "An improved data stream summary: the count-min sketch and its applications" by Cormode and Muthukrishnan, 2004.
        """

        if w is not None and d is not None:
            self.w = w
            self.d = d
        elif delta is not None and epsilon is not None:
            self.w = int(ceil(e / epsilon))
            self.d = int(ceil(log(1. / delta)))
        else:
            raise Exception("Incomplete parameters. Please provide w&d or delta&epsilon.")

        # 数组元素的类型是long
        self.table = [array('l', (0 for _ in range(self.w))) for _ in range(self.d)]
        self.is_conservative_update = is_conservative_update

    def _hash(self, x):
        md5 = hashlib.md5(str(hash(x)).encode())
        for i in range(self.d):
            md5.update(str(i).encode())
            yield int(md5.hexdigest(), 16) % self.w

    def add(self, x, v=1):
        # 元素x出现了v次
        if self.is_conservative_update:
            min_count = self.query(x)
            for table, i in zip(self.table, self._hash(x)):
                if table[i] == min_count:
                    table[i] += v
        else:
            for table, i in zip(self.table, self._hash(x)):
                table[i] += v

    def query(self, x):
        # 元素x的估计出现次数
        return min(table[i] for table, i in zip(self.table, self._hash(x)))

    def __getitem__(self, x):
        return self.query(x)

    def __setitem__(self, x, v):
        for table, i in zip(self.table, self._hash(x)):
            table[i] = v
