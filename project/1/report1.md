report1

$ \phi $ ( $ \sigma $ ) 

( $ \epsilon $ , $ \delta $ ) 近似算法的定义如下所示

给定输入的流数据 $ \sigma $ 和精确输出 $ \varepsilon $ ( $ \sigma $ ),近似算法的输出记为A( $ \sigma $ )。该算法被称之为
( $ \epsilon $ , $ \delta $ )-近似算法,如果该算法的输出结果满足

Pr[|A( $ \sigma $ )- $ \varepsilon $ ( $ \sigma $ )|<c $ \varepsilon $ ( $ \sigma $ )]>1- $ \delta $ 



这里给出的是相对版( $ \epsilon $ , $ \delta $ )-近似算法, 一个( $ \epsilon $ , $ \delta $ )-近似算法输出的结果可能会出现|A( $ \sigma $ )- $ \varepsilon $ ( $ \sigma $ )|<c $ \varepsilon $ ( $ \sigma $ ),但是这种情况发生的概率不会超过 $ \delta $ 。通常偏差很大的概率上界 $ \delta $ 是很小的一个值,这意味着( $ \epsilon $ , $ \delta $ )-近似算法输出值以概率(1- $ \delta $ )成为一个比较好的近似值。





在数据流$ \sigma $ =< $ a_ {1} $ , $ a_ {2} $ , $ \cdots $ , $ a_ {m} $ >, $ a_ {i} $ $ \in [n] $ 中,定义一个频数向量$f= (f_ {1} $ , $ f_ {2} $ , $ \cdots $ , $ f_ {n} )$ ,
其中$n$中不同元素的个数,$ f_ {i} $ 为元素$a_i$的频数。

得到元素的频数后,可以找出满足需求的元素,比如频繁项。该问题分为两类:
 大多数问题:如果 $ \exists $ $ a_ {i} $ : $ f_ {i} $ > $ \frac {m}{2} $ ,则输出 $ a_ {i} $ ,否则输出 $ \varnothing $ 。
频繁项:给定一个参数k,输出频繁元素集合{ $ a_ {i} $ : $ f_ {i} $ > $ \frac {m}{k} $ };或者,给定一个参数$\psi$,
输出频繁元素集合 $ a_ {1} $ : $ f_ {i} $ >$\psi m$.

```
delta: 查询错误的最大概率 epsilon: 查询错误的最大偏离值
w = ceil(e/epsilon)
d = ceil(ln(1.0/delta))
```

$w=O(\frac{1}{\epsilon}),d = O(ln(\frac{1}{\delta}))$空间复杂度:$O(\frac{1}{\epsilon}ln(\frac{1}{\delta}))$

