import numpy as np

class FullyConnectedLayer:
	def __init__(self, in_nodes, out_nodes):
		# Method to initialize a Fully Connected Layer
		# Parameters
		# in_nodes - number of input nodes of this layer
		# out_nodes - number of output nodes of this layer
		self.in_nodes = in_nodes
		self.out_nodes = out_nodes
		# Stores the outgoing summation of weights * feautres 
		self.data = None

		# Initializes the Weights and Biases using a Normal Distribution with Mean 0 and Standard Deviation 0.1
		self.weights = np.random.normal(0,0.1,(in_nodes, out_nodes))	
		self.biases = np.random.normal(0,0.1, (1, out_nodes))
		###############################################
		# NOTE: You must NOT change the above code but you can add extra variables if necessary 

	def forwardpass(self, X):
		# print('Forward FC ',self.weights.shape)
		# Input
		# activations : Activations from previous layer/input
		# Output
		# activations : Activations after one forward pass through this layer
		
		n = X.shape[0]  # batch size
		# INPUT activation matrix  		:[n X self.in_nodes]
		# OUTPUT activation matrix		:[n X self.out_nodes]

		###############################################
		# TASK 1 - YOUR CODE HERE
		self.data = np.matmul(X,self.weights) + self.biases 
		out = sigmoid(self.data)
		return out
		#raise NotImplementedError
		###############################################
		
	def backwardpass(self, lr, activation_prev, delta):
		# Input
		# lr : learning rate of the neural network
		# activation_prev : Activations from previous layer
		# delta : del_Error/ del_activation_curr
		# Output
		# new_delta : del_Error/ del_activation_prev
		
		# Update self.weights and self.biases for this layer by backpropagation
		n = activation_prev.shape[0] # batch size

		###############################################
		# TASK 2 - YOUR CODE HERE
		# print("Prev", activation_prev.shape)
		# print("delta", delta.shape)
		delta_prime = derivative_sigmoid(self.data) * delta #[batch_size, out_nodes]
		grad_w_matrix = np.einsum('ij,ik->ijk', activation_prev, delta_prime)
		grad_b = np.sum(delta_prime,0)
		grad_w = np.sum(grad_w_matrix, 0) #[in_noces,out_nodes]
		new_delta = np.matmul(delta_prime, np.transpose(self.weights))
		self.weights = self.weights - lr * grad_w
		self.biases = self.biases - lr * grad_b


		return new_delta
		
		#raise NotImplementedError
		###############################################

class ConvolutionLayer:
	def __init__(self, in_channels, filter_size, numfilters, stride):
		# Method to initialize a Convolution Layer
		# Parameters
		# in_channels - list of 3 elements denoting size of input for convolution layer
		# filter_size - list of 2 elements denoting size of kernel weights for convolution layer
		# numfilters  - number of feature maps (denoting output depth)
		# stride	  - stride to used during convolution forward pass
		self.in_depth, self.in_row, self.in_col = in_channels
		self.filter_row, self.filter_col = filter_size
		self.stride = stride

		self.out_depth = numfilters
		self.out_row = int((self.in_row - self.filter_row)/self.stride + 1)
		self.out_col = int((self.in_col - self.filter_col)/self.stride + 1)

		# Stores the outgoing summation of weights * feautres 
		self.data = None
		
		# Initializes the Weights and Biases using a Normal Distribution with Mean 0 and Standard Deviation 0.1
		self.weights = np.random.normal(0,0.1, (self.out_depth, self.in_depth, self.filter_row, self.filter_col))	
		self.biases = np.random.normal(0,0.1,self.out_depth)
		

	def forwardpass(self, X):
		# print('Forward CN ',self.weights.shape)
		# Input
		# X : Activations from previous layer/input
		# Output
		# activations : Activations after one forward pass through this layer
		n = X.shape[0]  # batch size
		# INPUT activation matrix  		:[n X self.in_channels[0] X self.in_channels[1] X self.in_channels[2]]
		# OUTPUT activation matrix		:[n X self.outputsize[0] X self.outputsize[1] X self.numfilters]

		###############################################
		# TASK 1 - YOUR CODE HERE
		out = np.zeros((n, self.out_depth, self.out_row, self.out_col))
		for i in range(self.out_row):
			for j in range(self.out_col):
				X_new = np.tile(np.expand_dims(X[:,:,(i*self.stride):(i*self.stride)+self.filter_row,
					(j*self.stride):(j*self.stride)+self.filter_col],1), (1,self.out_depth, 1,1,1))
				weight_new = np.tile(np.expand_dims(self.weights,0), (n,1,1,1,1))
				#print(weight_new.shape)
				out[:,:,i,j] = np.sum(X_new * weight_new, (2,3,4)) + np.expand_dims(self.biases,0)
		self.data = out
		out = sigmoid(out)
		return out
		#raise NotImplementedError
		###############################################

	def backwardpass(self, lr, activation_prev, delta):
		# Input
		# lr : learning rate of the neural network
		# activation_prev : Activations from previous layer
		# delta : del_Error/ del_activation_curr
		# Output
		# new_delta : del_Error/ del_activation_prev
		
		# Update self.weights and self.biases for this layer by backpropagation
		n = activation_prev.shape[0] # batch size

		###############################################
		# TASK 2 - YOUR CODE HERE
		#Size of delta [batch_size, out_depth, out_row, out_col]
		#Size of activation prev [batch_size, in_depth, in_row, in_col]
		delta_prime_orig = derivative_sigmoid(self.data) * delta
		out = np.zeros((n, self.in_depth, self.in_row, self.in_col)) #To store the new delta
		grad_w = np.zeros((self.out_depth, self.in_depth, self.filter_row, self.filter_col))
		grad_b = np.zeros((self.out_depth))
		
		#Compute new delta
		for i in range(self.out_row):
			for j in range(self.out_col):
				delta_patch = np.einsum('ij,jklm->iklm',delta_prime_orig[:,:,i,j], self.weights) #[batch_size, in_nodes, filter_row,filter_col]
				out[:,:,(i*self.stride):(i*self.stride)+self.filter_row,
				 (j*self.stride):(j*self.stride)+self.filter_col] += delta_patch
				activation_temp = activation_prev[:,:,(i*self.stride):(i*self.stride)+self.filter_row,
				(j*self.stride):(j*self.stride)+self.filter_col] #[batch_size,in_depth, filter_row, filter_col]
				delta_temp = np.transpose(delta_prime_orig[:,:,i,j], (1,0)) #[out_depth, batch_size]
				grad_w += np.einsum('ij,jklm->iklm',delta_temp, activation_temp)
				grad_b += np.sum(delta_temp,1)
		
		#Update
		self.weights = self.weights - lr * grad_w
		self.biases = self.biases - lr * grad_b
		return out
		
		#raise NotImplementedError
		###############################################
	
class AvgPoolingLayer:
	def __init__(self, in_channels, filter_size, stride):
		# Method to initialize a Convolution Layer
		# Parameters
		# in_channels - list of 3 elements denoting size of input for max_pooling layer
		# filter_size - list of 2 elements denoting size of kernel weights for convolution layer

		# NOTE: Here we assume filter_size = stride
		# And we will ensure self.filter_size[0] = self.filter_size[1]
		self.in_depth, self.in_row, self.in_col = in_channels
		self.filter_row, self.filter_col = filter_size
		self.stride = stride

		self.out_depth = self.in_depth
		self.out_row = int((self.in_row - self.filter_row)/self.stride + 1)
		self.out_col = int((self.in_col - self.filter_col)/self.stride + 1)

	def forwardpass(self, X):
		# print('Forward MP ')
		# Input
		# X : Activations from previous layer/input
		# Output
		# activations : Activations after one forward pass through this layer
		
		n = X.shape[0]  # batch size
		# INPUT activation matrix  		:[n X self.in_channels[0] X self.in_channels[1] X self.in_channels[2]]
		# OUTPUT activation matrix		:[n X self.outputsize[0] X self.outputsize[1] X self.in_channels[2]]

		###############################################
		# TASK 1 - YOUR CODE HERE
		out = np.zeros((n,self.out_depth,self.out_row, self.out_col))
		for i in range(self.out_row):
			for j in range(self.out_col):
				X_new = X[:,:,(i*self.stride):(i*self.stride)+self.filter_row,
				(j*self.stride):(j*self.stride)+self.filter_col]
				out[:,:,i,j] = np.mean(X_new,(2,3))
		return out
		#raise NotImplementedError
		###############################################


	def backwardpass(self, alpha, activation_prev, delta):
		# Input
		# lr : learning rate of the neural network
		# activation_prev : Activations from previous layer
		# activations_curr : Activations of current layer
		# delta : del_Error/ del_activation_curr
		# Output
		# new_delta : del_Error/ del_activation_prev
		
		n = activation_prev.shape[0] # batch size

		###############################################
		# TASK 2 - YOUR CODE HERE
		#Size of delta [batch_size, out_depth, out_row, out_col]
		out = np.zeros((n, self.in_depth, self.in_row, self.in_col))
		for i in range(self.out_row):
			for j in range(self.out_col):
				new_delta = np.tile(np.expand_dims(np.expand_dims(delta[:,:,i,j],-1), -1), (1,1,self.filter_row,self.filter_col))
				out[:,:,(i*self.stride):(i*self.stride)+self.filter_row,
				 (j*self.stride):(j*self.stride)+self.filter_col] += new_delta/(self.filter_row * self.filter_col)

		return out
		#raise NotImplementedError
		###############################################


# Helper layer to insert between convolution and fully connected layers
class FlattenLayer:
    def __init__(self):
        pass
    
    def forwardpass(self, X):
        self.in_batch, self.r, self.c, self.k = X.shape
        return X.reshape(self.in_batch, self.r * self.c * self.k)

    def backwardpass(self, lr, activation_prev, delta):
        return delta.reshape(self.in_batch, self.r, self.c, self.k)


# Helper Function for the activation and its derivative
def sigmoid(x):
	return 1 / (1 + np.exp(-x))

def derivative_sigmoid(x):
	return sigmoid(x) * (1 - sigmoid(x))
