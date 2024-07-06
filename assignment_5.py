# -*- coding: utf-8 -*-
"""Assignment_5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1o7CRgOT-wIdxTFTtfcNBGmKkf9skER_O
"""

import numpy as np
import random

number_people = 400
conflict_matrix = np.zeros((number_people, number_people))
conflict_pairs = random.sample([(i, j) for i in range(number_people) for j in range(i+1, number_people)], 600)
for i, j in conflict_pairs:
    conflict_matrix[i][j] = 1
    conflict_matrix[j][i] = 1

group_size = 5
num_groups = number_people // group_size

import torch
import torch.nn as nn
import torch.optim as optim


class SeatingArrangementNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SeatingArrangementNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return self.softmax(x)

# Step 3: Custom loss function
def custom_loss(pred, conflict_matrix, group_size):
    pred = pred.argmax(dim=1)
    num_people = pred.shape[0]
    num_groups = num_people // group_size

    # Initialize loss components
    loss_conflict = torch.tensor(0.0, requires_grad=True)
    loss_group = torch.tensor(0.0, requires_grad=True)

    # Penalize conflicts
    for i in range(num_people):
        for j in range(i + 1, num_people):
            if conflict_matrix[i][j] == 1 and pred[i] == pred[j]:
                loss_conflict = loss_conflict + 1

    # Reward group cohesion
    for g in range(num_groups):
        group_indices = pred[g * group_size:(g + 1) * group_size]
        for i in range(group_size):
            for j in range(i + 1, group_size):
                if group_indices[i] // group_size == group_indices[j] // group_size:
                    loss_group = loss_group + 1

    return loss_conflict - loss_group

# Hyperparameters
input_size = number_people
hidden_size = 128
output_size = number_people

# Instantiate the network
net = SeatingArrangementNN(input_size, hidden_size, output_size)

# Optimizer
optimizer = optim.Adam(net.parameters(), lr=0.001)

# Training data (random initialization)
# Each person is initially assigned a random group
initial_seating = torch.eye(number_people)

# Training loop
num_epochs = 1000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    output = net(initial_seating)
    loss = custom_loss(output, conflict_matrix, group_size)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}')

# The output of the network is the final seating arrangement
final_seating = net(initial_seating).argmax(dim=1).numpy()

print("Final seating arrangement:", final_seating)

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

# Step 1: Create conflict matrix
num_people = 400
group_size = 5
num_groups = num_people // group_size
conflict_matrix = np.zeros((num_people, num_people))

# Randomly create 600 conflicts
conflict_pairs = random.sample([(i, j) for i in range(num_people) for j in range(i+1, num_people)], 600)
for i, j in conflict_pairs:
    conflict_matrix[i][j] = 1
    conflict_matrix[j][i] = 1

conflict_matrix = torch.tensor(conflict_matrix, dtype=torch.float32)

# Step 2: Neural network design
class SeatingArrangementNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SeatingArrangementNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return self.softmax(x)

# Step 3: Custom loss function
def custom_loss(pred, conflict_matrix, group_size):
    pred = pred.argmax(dim=1)
    num_people = pred.shape[0]
    num_groups = num_people // group_size

    # Initialize loss components
    loss_conflict = torch.tensor(0.0, requires_grad=True)
    loss_group = torch.tensor(0.0, requires_grad=True)

    # Penalize conflicts
    for i in range(num_people):
        for j in range(i + 1, num_people):
            if conflict_matrix[i][j] == 1 and pred[i] == pred[j]:
                loss_conflict = loss_conflict + 1

    # Reward group cohesion
    for g in range(num_groups):
        group_indices = pred[g * group_size:(g + 1) * group_size]
        for i in range(group_size):
            for j in range(i + 1, group_size):
                if group_indices[i] // group_size == group_indices[j] // group_size:
                    loss_group = loss_group + 1

    return loss_conflict - loss_group

# Hyperparameters
input_size = num_people
hidden_size = 128
output_size = num_people

# Instantiate the network
net = SeatingArrangementNN(input_size, hidden_size, output_size)

# Optimizer
optimizer = optim.Adam(net.parameters(), lr=0.001)

# Training data (random initialization)
# Each person is initially assigned a random group
initial_seating = torch.eye(num_people)

# Training loop
num_epochs = 1000
for epoch in range(num_epochs):
    optimizer.zero_grad()
    output = net(initial_seating)
    loss = custom_loss(output, conflict_matrix, group_size)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}')

# The output of the network is the final seating arrangement
final_seating = net(initial_seating).argmax(dim=1).numpy()

print("Final seating arrangement:", final_seating)

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random

# Step 1: Create conflict matrix
num_people = 400
group_size = 5
num_groups = num_people // group_size
conflict_matrix = np.zeros((num_people, num_people))

# Randomly create 600 conflicts
conflict_pairs = random.sample([(i, j) for i in range(num_people) for j in range(i+1, num_people)], 600)
for i, j in conflict_pairs:
    conflict_matrix[i][j] = 1
    conflict_matrix[j][i] = 1

conflict_matrix = torch.tensor(conflict_matrix, dtype=torch.float32)

# Step 2: Neural network design
class SeatingArrangementNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SeatingArrangementNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.softmax = nn.Softmax(dim=1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return self.softmax(x)

# Step 3: Custom loss function
def custom_loss(pred, conflict_matrix, group_size, correlation_coefficient=0.5):
    pred = pred.argmax(dim=1)
    num_people = pred.shape[0]
    num_groups = num_people // group_size

    # Initialize loss components
    loss_conflict = torch.tensor(0.0, requires_grad=True)
    loss_group = torch.tensor(0.0, requires_grad=True)

    # Penalize conflicts
    for i in range(num_people):
        for j in range(i + 1, num_people):
            if conflict_matrix[i][j] == 1 and pred[i] == pred[j]:
                loss_conflict = loss_conflict + 1

    # Reward group cohesion
    for g in range(num_groups):
        group_indices = pred[g * group_size:(g + 1) * group_size]
        for i in range(group_size):
            for j in range(i + 1, group_size):
                if group_indices[i] // group_size == group_indices[j] // group_size:
                    loss_group = loss_group + 1

    # Balance the loss using the correlation coefficient
    return correlation_coefficient * loss_conflict - (1 - correlation_coefficient) * loss_group

# Hyperparameters
input_size = num_people
hidden_size = 128
output_size = num_people

# Instantiate the network
net = SeatingArrangementNN(input_size, hidden_size, output_size)

# Optimizer
optimizer = optim.Adam(net.parameters(), lr=0.001)

# Training data (random initialization)
# Each person is initially assigned a random group
initial_seating = torch.eye(num_people)

# Training loop
num_epochs = 1000
correlation_coefficient = 0.5
for epoch in range(num_epochs):
    optimizer.zero_grad()
    output = net(initial_seating)
    loss = custom_loss(output, conflict_matrix, group_size, correlation_coefficient)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item()}')

# The output of the network is the final seating arrangement
final_seating = net(initial_seating).argmax(dim=1).numpy()

print("Final seating arrangement:", final_seating)