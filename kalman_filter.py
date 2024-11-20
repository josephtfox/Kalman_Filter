import numpy as np
import pandas

class KalmanFilter:
    def __init__(self, dt, init_x_std, init_y_std, measure_std):
        self.dt = dt

        # State Vector 
        self.x = np.zeros((4, 1))

        # State Covariance Matrix
        self.P = np.array([
            [init_x_std ** 2, 0, 0, 0],
            [0, init_x_std ** 2, 0, 0],
            [0, 0, init_y_std ** 2, 0],
            [0, 0, 0, init_y_std ** 2]
        ])

        # State Transition Matrix
        self.F = np.array([
            [1, 0, self.dt, 0],
            [0, 1, 0, self.dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        # Measurment Matrix
        self.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])

        # Measurement Noise Covariance
        self.R = np.array([
            [measure_std ** 2, 0],
            [0, measure_std ** 2]
        ])
    
    """
    Where the Next State of the system is predicted given the previous measurements
    """
    def predict(self):
        self.x = np.dot(self.F, self.x)
        self.P = np.dot(self.F, np.dot(self.P, self.F.T))
        # Noise is not needed
        # self.P = np.dot(self.F, np.dot(self.P, self.F.T)) + self.Q
        return(self.x[0], self.x[1])

    """
    S = the covariance or predictive mean of Y
    K = The kalman Gain matrix    
    """
    def update(self, Z):
        self.Y = Z - np.dot(self.H, self.x)
        self.S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R
        self.K = np.dot(self.P, np.dot(self.H.T, np.linalg.inv(self.S)))

        # Identity Matrix
        I = np.eye(4)

        self.x = self.x + np.dot(self.K, self.Y)
        self.P = np.dot((I - np.dot(self.K, self.H)), self.P)
        return()
    