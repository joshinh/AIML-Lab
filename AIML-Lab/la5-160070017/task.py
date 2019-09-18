import numpy as np
from utils import *

def preprocess(X, Y):
	''' TASK 0
	X = input feature matrix [N X D] 
	Y = output values [N X 1]
	Convert data X, Y obtained from read_data() to a usable format by gradient descent function
	Return the processed X, Y that can be directly passed to grad_descent function
	NOTE: X has first column denote index of data point. Ignore that column 
	and add constant 1 instead (for bias part of feature set)
	'''
	X_new = np.ones((X.shape[0],1), dtype=np.float32)
	for i in range(1,X.shape[1]):
		if type(X[0][i]) is str:
			labels = list(set(X[:,i]))
			one_hot_temp = one_hot_encode(X[:,i],labels) 
			for j in range(len(labels)):
				X_new = np.concatenate([X_new,np.expand_dims(one_hot_temp[:,j],-1)],axis=-1)
				
		else:
			mean = np.mean(X[:,i])
			std = np.std(X[:,i])
			X_norm = (X[:,i] - mean)/std
			X_norm = X_norm
			X_new = np.concatenate([X_new, np.expand_dims(X_norm,-1)], axis=-1)

	return X_new.astype(float), Y.astype(float)

	#pass

def grad_ridge(W, X, Y, _lambda):
	'''  TASK 2
	W = weight vector [D X 1]
	X = input feature matrix [N X D]
	Y = output values [N X 1]
	_lambda = scalar parameter lambda
	Return the gradient of ridge objective function (||Y - X W||^2  + lambda*||w||^2 )

	'''
	
	diff = Y - np.matmul(X,W)
	W_grad = 2 * (-np.matmul(np.transpose(X),diff) + _lambda * W)

	return W_grad

	#pass

def ridge_grad_descent(X, Y, _lambda, max_iter=20000, lr=0.00001, epsilon = 1e-4):
	''' TASK 2
	X 			= input feature matrix [N X D]
	Y 			= output values [N X 1]
	_lambda 	= scalar parameter lambda
	max_iter 	= maximum number of iterations of gradient descent to run in case of no convergence
	lr 			= learning rate
	epsilon 	= gradient norm below which we can say that the algorithm has converged 
	Return the trained weight vector [D X 1] after performing gradient descent using Ridge Loss Function 
	NOTE: You may precompure some values to make computation faster
	'''
	W = np.ones((X.shape[1],1), dtype=np.float32)
	for i in range(max_iter):
		W_grad = grad_ridge(W,X,Y,_lambda)
		if np.linalg.norm(W_grad) < epsilon:
			break
		W = W - (lr * W_grad)
	
	return W
	#pass

def k_fold_cross_validation(X, Y, k, lambdas, algo):
	''' TASK 3
	X 			= input feature matrix [N X D]
	Y 			= output values [N X 1]
	k 			= number of splits to perform while doing kfold cross validation
	lambdas 	= list of scalar parameter lambda
	algo 		= one of {coord_grad_descent, ridge_grad_descent}
	Return a list of average SSE values (on validation set) across various datasets obtained from k equal splits in X, Y 
	on each of the lambdas given 
	'''

	Z = np.asarray(list(zip(X,Y)))
	Z_new = np.split(Z,k)
	Z_new = [list(zip(*t)) for t in Z_new]
	
	average_sse = []

	for i in range(len(lambdas)):
		sse_current = 0.0
		for j in range(k):
			X_val = np.asarray(list(Z_new[j][0]))
			Y_val = np.asarray(list(Z_new[j][1]))
			X_list = [np.asarray(list(x[0])) for l,x in enumerate(Z_new) if l!=j]
			Y_list = [np.asarray(list(x[1])) for l,x in enumerate(Z_new) if l!=j]
			X_train = np.concatenate(X_list,0)
			Y_train = np.concatenate(Y_list,0)
			W_op = algo(X_train,Y_train,lambdas[i])
			sse_current += sse(X_val,Y_val,W_op)

		average_sse.append(sse_current/k)

	return average_sse


	#pass

def coord_grad_descent(X, Y, _lambda, max_iter=1000):
	''' TASK 4
	X 			= input feature matrix [N X D]
	Y 			= output values [N X 1]
	_lambda 	= scalar parameter lambda
	max_iter 	= maximum number of iterations of gradient descent to run in case of no convergence
	Return the trained weight vector [D X 1] after performing gradient descent using Ridge Loss Function 
	'''
	
	dot_list = []
	xy_temp = np.matmul(np.transpose(X),Y)
	xx_temp = np.matmul(np.transpose(X), X)
	for j in range(X.shape[1]):
		X_new = X[:,j]
		dot_list.append(np.dot(X_new,X_new))
	
	W = np.random.rand(X.shape[1],1)
	for i in range(max_iter):
		for j in range(X.shape[1]):
			if dot_list[j] == 0:
				continue
			W_rem = np.copy(W)
			W_rem[j] = 0
			temp = 2 * (xy_temp[j,0] - np.dot(xx_temp[j,:], W_rem))

			if temp > _lambda:
				W[j] = (temp - _lambda)/(2 * dot_list[j])
			elif temp > -_lambda:
				W[j] = 0
			else:
				W[j] = (temp + _lambda)/(2 * dot_list[j])

	return W			


if __name__ == "__main__":
	# Do your testing for Kfold Cross Validation in by experimenting with the code below 
	X, Y = read_data("./dataset/train.csv")
	X, Y = preprocess(X, Y)
	trainX, trainY, testX, testY = separate_data(X, Y)
	
	lambdas = [1e5, 2e5,3e5,4e5, 5e5, 6e5, 7e5, 8e5] # Assign a suitable list Task 5 need best SSE on test data so tune lambda accordingly
	scores = k_fold_cross_validation(trainX, trainY, 6, lambdas, coord_grad_descent)
	print(scores)
	plot_kfold(lambdas, scores)
	# W_op = coord_grad_descent(trainX, trainY, 4e5)
	# c = 0
	# for i in range(W_op.shape[0]):
	# 	if W_op[i,0] == 0:
	# 		c += 1
	# print(sse(testX, testY, W_op))
	# print(c)