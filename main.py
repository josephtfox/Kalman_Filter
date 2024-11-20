import pandas as pd
import numpy as np
import kalman_filter
import create_data
import visualize_results

def run_kalman_filter(kf, measurements):
    estimated_states = []
    for measurement in measurements:
        kf.predict()
        kf.update(measurement)
        estimated_states.append(kf.x.flatten()[:2])  # Only store position estimates
    return np.array(estimated_states)

def calculate_rmse(true_states, estimated_states):
    return np.sqrt(np.mean((true_states - estimated_states)**2, axis=0))

def calculate_accuracy(true_states, estimated_states, threshold=0.5):
    errors = np.abs(true_states[:, :2] - estimated_states)
    within_threshold = np.all(errors <= threshold, axis=1)
    accuracy = np.mean(within_threshold) * 100
    return accuracy

if __name__ == "__main__":
    # Generate or load data
    generate_new_data = True  # Set to False to load existing data
    
    if generate_new_data:
        num_steps = 100
        initial_state = np.array([0, 0, 1, 1])  # [px, py, vx, vy]
        noise_std = 0.1
        true_df, meas_df = create_data.generate_data(num_steps, initial_state, noise_std)
        create_data.save_data(true_df, meas_df)
    else:
        true_df, meas_df = create_data.load_data()

    # Extract numpy arrays
    true_states = true_df.values
    measurements = meas_df.values

    # Initialize Kalman Filter
    dt = 1.0
    init_x_std = 0.1
    init_y_std = 0.1
    measure_std = 0.1
    kf = kalman_filter.KalmanFilter(dt, init_x_std, init_y_std, measure_std)

    # Run Kalman Filter
    estimated_states = run_kalman_filter(kf, measurements)

    # Plot results
    visualize_results.plot_results(true_states, measurements, estimated_states)
    visualize_results.plot_error(true_states, estimated_states)

    # Calculate RMSE
    rmse = calculate_rmse(true_states[:, :2], estimated_states)
    print(f"RMSE: X={rmse[0]:.4f}, Y={rmse[1]:.4f}")

    # Calculate accuracy
    accuracy = calculate_accuracy(true_states, estimated_states, threshold=0.5)
    print(f"Model Accuracy: {accuracy:.2f}%")

    # Print final state estimate
    print("Final estimated state:")
    print(f"Position: ({estimated_states[-1, 0]:.2f}, {estimated_states[-1, 1]:.2f})")

    # Check the shape of kf.x and print accordingly
    if kf.x.shape[0] == 4:
        print(f"Velocity: ({kf.x[2, 0]:.2f}, {kf.x[3, 0]:.2f})")
    elif kf.x.shape[1] == 4:
        print(f"Velocity: ({kf.x[0, 2]:.2f}, {kf.x[0, 3]:.2f})")
    else:
        print("Velocity: Unable to retrieve (unexpected state vector shape)")

    # Consistency check
    error = true_states[-1, :2] - estimated_states[-1, :]
    estimated_cov = kf.P[:2, :2]
    mahalanobis_distance = np.sqrt(error @ np.linalg.inv(estimated_cov) @ error.T)
    print(f"Mahalanobis distance: {mahalanobis_distance:.4f}")