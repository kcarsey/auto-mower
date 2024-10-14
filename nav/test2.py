from scipy.spatial import ConvexHull
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to dynamically adjust point distance based on elevation change
def dynamic_point_spacing(elevation_change, base_distance):
    if abs(elevation_change) > 2:  # Significant elevation change, reduce spacing
        return base_distance * 0.5
    elif abs(elevation_change) < 0.5:  # Minimal elevation change, increase spacing
        return base_distance * 1.5
    else:
        return base_distance

# Generate Convex Hull of N points to form a polygon
def convex_hull_from_points(points):
    lat_lon_points = np.array([(p[0], p[1]) for p in points])
    hull = ConvexHull(lat_lon_points)
    return [points[i] for i in hull.vertices]

# Generate dense 3D mesh for an arbitrary polygon (N points) based on zigzag paths
def generate_dense_3d_mesh_N(points, pass_distance, base_point_distance):
    polygon = convex_hull_from_points(points)  # Get the convex hull for N points
    
    # Get min/max bounds in terms of lat/lon for defining the zigzag boundaries
    lats, lons, alts = zip(*polygon)
    min_lat, max_lat = min(lats), max(lats)
    min_lon, max_lon = min(lons), max(lons)

    # Generate the zigzag passes and adjust point spacing dynamically
    path = []
    current_lat = min_lat
    direction = 1  # Start moving left to right

    while current_lat <= max_lat:
        # Determine the x range for the current zigzag pass
        if direction == 1:
            path.extend(sample_path(min_lon, max_lon, current_lat, direction, base_point_distance, polygon))
        else:
            path.extend(sample_path(max_lon, min_lon, current_lat, direction, base_point_distance, polygon))

        current_lat += pass_distance
        direction *= -1  # Switch direction

    return path

# Function to sample points along the path with a given resolution and dynamic spacing
def sample_path(start_lon, end_lon, lat, direction, base_point_distance, polygon):
    path_points = []
    current_lon = start_lon
    step = base_point_distance if direction == 1 else -base_point_distance

    while (direction == 1 and current_lon <= end_lon) or (direction == -1 and current_lon >= end_lon):
        # Interpolate altitude based on the current lat/lon
        interpolated_alt = interpolate_altitude(lat, current_lon, polygon)
        
        # Adjust point spacing dynamically based on elevation changes
        if path_points:
            elevation_change = interpolated_alt - path_points[-1][2]
            adjusted_distance = dynamic_point_spacing(elevation_change, base_point_distance)
        else:
            adjusted_distance = base_point_distance
        
        path_points.append((lat, current_lon, interpolated_alt))
        current_lon += step

    return path_points

# Interpolate altitude between points for a given lat/lon (basic linear interpolation for now)
def interpolate_altitude(lat, lon, polygon):
    # Simple interpolation based on average altitudes of nearby points (for demo purposes)
    lats, lons, alts = zip(*polygon)
    avg_alt = np.mean(alts)
    return avg_alt  # Replace with more complex interpolation if needed

# Example of N corner points (5 points)
corner_points = [
    (38.928177, -81.726472, 185),  # Point A (lat, lon, altitude)
    (38.927968, -81.725935, 184),  # Point B
    (38.927755, -81.726096, 183),  # Point C
    (38.927887, -81.726492, 184),  # Point D
    (38.928132, -81.726607, 182)   # Point E (new point)
]

# Pass width of 1.35 meters with overlap, and base point distance of 1 meter
pass_distance = 1.35
base_point_distance = 1

# Generate the 3D zigzag path with dynamic point spacing for N points
dense_3d_mesh_N = generate_dense_3d_mesh_N(corner_points, pass_distance, base_point_distance)

# Extract X, Y, Z coordinates for plotting
lats, lons, alts = zip(*dense_3d_mesh_N)

# Plotting the 3D zigzag path with dynamic point spacing
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the points in meters
ax.scatter(lats, lons, alts, c=alts, cmap='viridis')

# Labeling axes with distance in meters
ax.set_xlabel('Latitude')
ax.set_ylabel('Longitude')
ax.set_zlabel('Altitude (m)')

plt.title('3D Mesh with Dynamic Point Spacing for N Points')
plt.show()
