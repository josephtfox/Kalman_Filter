import matplotlib.pyplot as plt
import numpy as np

def plot_results(true_states, measurements, estimated_states):
    plt.figure(figsize=(12, 6))
    plt.plot(true_states[:, 0], true_states[:, 1], label='True Path')
    plt.scatter(measurements[:, 0], measurements[:, 1], color='r', s=10, label='Measurements')
    plt.plot(estimated_states[:, 0], estimated_states[:, 1], label='Estimated Path')
    plt.legend()
    plt.title('Object Tracking with Kalman Filter')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.grid(True)
    plt.show()

def plot_error(true_states, estimated_states):
    error = np.sqrt(np.sum((true_states[:, :2] - estimated_states)**2, axis=1))
    plt.figure(figsize=(12, 6))
    plt.plot(error)
    plt.title('Estimation Error over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Error')
    plt.grid(True)
    plt.show()
     