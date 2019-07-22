# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.4'
#       jupytext_version: 1.2.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

print(1+2)

# This is a comment for this code.

# +
# %matplotlib inline
import matplotlib.pyplot as plt

price = [100, 250, 380, 500, 700]
number = [1, 2, 3, 4, 5]

# グラフを書く
plt.plot(price, number)

# グラフのタイトル
plt.title("price / number")

# x軸のラベル
plt.xlabel("price")

# y軸のラベル
plt.ylabel("number")

# 表示する
plt.show()
# -

1+2

7/5

type(7/5)

x = 10
print(x)

import numpy as np
x = np.array([1, 2, 3])
type(x)

# +
import numpy as np
import matplotlib.pyplot as plt

x = np.arange(0, 6, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, label="sin")
plt.plot(x, y2, linestyle="--", label="cos")
plt.xlabel("x")
plt.ylabel("y")
plt.title('sin & cos')
plt.legend()
plt.show()
# -


