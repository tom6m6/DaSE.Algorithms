class MinHeap:
    def __init__(self, maxsize):
        self.heap = []
        self.maxsize = maxsize
        self.index_map = {}

    def swap(self, i, j):
        self.index_map[self.heap[i][0]] = j
        self.index_map[self.heap[j][0]] = i
        self.heap[i][0], self.heap[j][0] = self.heap[j][0], self.heap[i][0]
        self.heap[i][1], self.heap[j][1] = self.heap[j][1], self.heap[i][1]

    def adjust_up(self, i):
        while i > 0 and self.heap[(i - 1) // 2][1] > self.heap[i][1]:
            self.swap(i, (i - 1) // 2)
            i = (i - 1) // 2

    def adjust_down(self, i):
        min_index = i
        if ((2 * i + 1) < len(self.heap)) and self.heap[(2 * i + 1)][1] < self.heap[min_index][1]:
            min_index = (2 * i + 1)
        if ((2 * i + 2) < len(self.heap)) and self.heap[(2 * i + 2)][1] < self.heap[min_index][1]:
            min_index = (2 * i + 2)
        if i != min_index:
            self.swap(i, min_index)
            self.adjust_down(min_index)

    def insert(self, p):
        if p[0] in self.index_map:
            i = self.index_map[p[0]]
            self.heap[i] = [p[0], (p[1] + self.heap[i][1])]
            self.adjust_up(i)
            self.adjust_down(i)
        else:
            self.heap.append(p)
            self.index_map[p[0]] = len(self.heap) - 1
            self.adjust_up(len(self.heap) - 1)

    def pop(self):
        root = self.heap[0]
        if len(self.heap) > 1:
            self.heap[0] = self.heap.pop(-1)
            self.index_map[self.heap[0][0]] = 0
            self.adjust_down(0)
        else:
            self.heap.pop()
        del self.index_map[root[0]]
        return root

    def getmin(self):
        if len(self.heap) == 0:
            return None
        else:
            return self.heap[0][1]

