import numpy as np
import pandas as pd

def generate_data(num_steps, initial_state, noise_std, dt=1):
    true_states = []
    measurements = []
    
    current_state = initial_state.copy()
    
    for _ in range(num_steps):
        # Record true state
        true_states.append(current_state.copy())
        
        # Generate noisy measurement
        measurement = current_state[:2] + np.random.normal(0, noise_std, 2)
        measurements.append(measurement)
        
        # Update true state (constant velocity model)
        current_state[0] += current_state[2] * dt
        current_state[1] += current_state[3] * dt
        
        # Add some random acceleration
        current_state[2] += np.random.normal(0, 0.1)
        current_state[3] += np.random.normal(0, 0.1)
    
    # Convert to DataFrames
    true_df = pd.DataFrame(true_states, columns=['px', 'py', 'vx', 'vy'])
    meas_df = pd.DataFrame(measurements, columns=['mx', 'my'])
    
    return true_df, meas_df

def save_data(true_df, meas_df, true_file='true_states.csv', meas_file='measurements.csv'):
    true_df.to_csv(true_file, index=False)
    meas_df.to_csv(meas_file, index=False)

def load_data(true_file='true_states.csv', meas_file='measurements.csv'):
    true_df = pd.read_csv(true_file)
    meas_df = pd.read_csv(meas_file)
    return true_df, meas_df