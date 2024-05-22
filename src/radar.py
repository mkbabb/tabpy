import numpy as np
import pandas as pd


def calculate_radar_coordinates(
    data: list[str],
    calc_amplitude_data: list[str],
    threads: list[str],
    node_types: list[str],
    dimension: str,
) -> list[str]:
    dimension = dimension.lower()

    # Create a DataFrame from the input lists
    df = pd.DataFrame(
        {
            'Data': data,
            'Amplitude': calc_amplitude_data,
            'Thread': threads,
            'NodeType': node_types,
        }
    )

    # Group by 'Data' column and count occurrences (amplitudes)
    grouped = df.groupby('Data').size().reset_index(name='AmplitudeCount')

    # Normalize amplitude counts to be between 0 and 1
    grouped['NormalizedAmplitude'] = (
        grouped['AmplitudeCount'] - grouped['AmplitudeCount'].min()
    ) / (grouped['AmplitudeCount'].max() - grouped['AmplitudeCount'].min())

    # Calculate the radar coordinates
    distinct_values = grouped['Data'].unique()
    num_values = len(distinct_values)

    # Create angle mappings for each data value
    angles = {distinct_values[i]: i * 2 * np.pi / num_values for i in range(num_values)}

    grouped['Angle'] = grouped['Data'].map(angles)

    # Add random noise to each distinct point
    np.random.seed(0)  # Ensure reproducibility
    noise = np.random.normal(0, 0.1, size=num_values)
    grouped['Noise'] = noise

    grouped['x'] = grouped['NormalizedAmplitude'] * np.cos(grouped['Angle']) + grouped['Noise']
    grouped['y'] = grouped['NormalizedAmplitude'] * np.sin(grouped['Angle']) + grouped['Noise']

    # Join the original data with the calculated coordinates
    result = df.merge(
        grouped[['Data', 'x', 'y', 'AmplitudeCount']], on='Data', how='left'
    )

    # Mirror nodes by 180 degrees
    result['x_mirror'] = result['x'] * -1
    result['y_mirror'] = result['y'] * -1

    # Apply mirrored coordinates to 'mirrored' node types
    result.loc[result['NodeType'] == 'mirrored', 'x'] = result['x_mirror']
    result.loc[result['NodeType'] == 'mirrored', 'y'] = result['y_mirror']

    # Ensure dimension matches column names correctly
    if dimension not in ['x', 'y', 'size']:
        raise ValueError('Dimension must be x, y, or size')

    if dimension == 'size':
        return result['AmplitudeCount'].values.flatten().tolist()
    else:
        return result[dimension].values.flatten().tolist()


data = _arg1
calc_amplitude_data = _arg2
threads = _arg3
node_types = _arg4
dimension = _arg5

if isinstance(dimension, list):
    dimension = str(dimension[0])

return calculate_radar_coordinates(
    data=data,
    calc_amplitude_data=calc_amplitude_data,
    threads=threads,
    node_types=node_types,
    dimension=dimension,
)
