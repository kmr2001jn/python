import pickle
import numpy as np
import matplotlib.pylab as plt
from mnist import load_mnist

def step_function(x):
	return np.array(x > 0, dtype=np.int)

def sigmoid(x):
	return 1 / (1 + np.exp(-x))

def relu(x):
	return np.maximum(0, x)

def softmax(x):
	c = np.max(x)
	exp_x = np.exp(x - c)
	sum_exp_x = np.sum(exp_x)
	return exp_x / sum_exp_x

def get_data():
	(x_train, t_train), (x_test, t_test) = \
		load_mnist(normalize=True, flatten=True, one_hot_label=False)
	return x_test, t_test

def init_network():
	with open("sample_weight.pkl", 'rb') as f:
		network = pickle.load(f)
	return network

def predict(network, x):
	W1, W2, W3 = network['W1'], network['W2'], network['W3']
	b1, b2, b3 = network['b1'], network['b2'], network['b3']
	
	a1 = np.dot(x, W1) + b1
	z1 = sigmoid(a1)
	a2 = np.dot(z1, W2) + b2
	z2 = sigmoid(a2)
	a3 = np.dot(z2, W3) + b3
	y = softmax(a3)
	
	return y

x, t = get_data()
network = init_network()

batchSize = 100
accuracyCnt = 0

for i in range(0, len(x), batchSize):
	x_batch = x[i: i + batchSize]
	y_batch = predict(network, x_batch)
	p = np.argmax(y_batch, axis = 1)
	accuracyCnt += np.sum(p == t[i: i + batchSize])

print(float(accuracyCnt) / len(x))

# x = np.arange(-1.0, 1.0, 0.1)
# y = relu(x)
# plt.plot(x, y)
# plt.ylim(-0.1, 1.1)
# plt.show()
