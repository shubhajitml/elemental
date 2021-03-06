# Autograd function is two functions that operate on Tensors,
# the Forward function computes the o/p Tensors from i/p Tensors and
# the Backwrd function receives the gradient of o/p Tensors WRT. some scalar value,
# and computes the gradient of i/p Tensors WRT. that scalar value

# In this implementation we implement our own custom autograd function to perform the ReLU function.

# coding: utf-8
import time
import torch

class MyRelu(torch.autograd.Function):
    """
    We can implement our own custom autograd Functions by subclassing
    torch.autograd.Function and implementing the forward and backward passes
    which operate on Tensors.
    """
    @staticmethod
    def forward(ctx, input):
        """
        In the forward pass we receive a Tensor containing the input and return
        a Tensor containing the output. ctx is a context object that can be used
        to stash information for backward computation. You can cache arbitrary
        objects for use in the backward pass using the ctx.save_for_backward method.
        """
        ctx.save_for_backward(input)
        return input.clamp(min=0)

    @staticmethod
    def backward(ctx, grad_output):
        """
        In the backward pass we receive a Tensor containing the gradient of the loss
        with respect to the output, and we need to compute the gradient of the loss
        with respect to the input.
        """
        input, = ctx.saved_tensors
        grad_input = grad_output.clone()
        grad_input[input < 0] = 0
        return grad_input

dtype = torch.float
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    
# N : batch size, D_in : input dimension,
# H : hidden dimension, D_out : output dimension
N, D_in, H, D_out = 64, 1000, 100, 10

# Create random Tensors to hold input and outputs.
x = torch.randn(N, D_in, device=device, dtype=dtype)
y = torch.randn(N, D_out, device=device, dtype=dtype)

# Create random Tensors for weights.
w1 = torch.randn(D_in, H, device=device, dtype=dtype, requires_grad=True)
w2 = torch.randn(H, D_out, device=device, dtype=dtype, requires_grad=True)

learning_rate = 1e-6
start_time = time.time()
for t in range(500):
    # To apply our Function, we use Function.apply method. We alias this as 'relu'.
    relu = MyRelu.apply
    
    # Forward pass: compute predicted y using operations;
    # we compute ReLU using our custom autograd operation.
    y_pred = relu(x.mm(w1)).mm(w2)

    # compute loss and print
    loss = (y_pred - y).pow(2).sum()
    print(t, loss.item())

    # using autograd to compute the backward pass 
    loss.backward()

    # update weights using gradient descent
    with torch.no_grad():
        w1 -= learning_rate * w1.grad
        w2 -= learning_rate * w2.grad

        # manually zero the gradients after updating weights
        w1.grad.zero_()
        w2.grad.zero_()

finish_time = time.time()
print(f'time of execution: ', finish_time - start_time)  # in my first run 2.2270095348358154 s