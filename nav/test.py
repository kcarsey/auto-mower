from geopy.distance import geodesic
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Using Vincenty (geodesic method) from geopy to calculate distances
def vincenty_distance(lat1, lon1, lat2, lon2):
    # Calculate distance between two lat/lon points in meters
    return geodesic((lat1, lon1), (lat2, lon2)).meters

# Define a function to generate a dense 3D mesh based on input corners and a given distance between points
def generate_dense_3d_mesh(corner1, corner2, corner3, corner4, pass_distance, point_distance):
    # Ensure the corners form a valid rectangular shape in the x-y plane
    if (corner1[1] != corner2[1] or corner3[1] != corner4[1]) or \
       (corner1[0] != corner4[0] or corner2[0] != corner3[0]):
        raise ValueError("The four coordinates must form a rectangle in the x-y plane.")
    
    # Extract x, y, and z ranges
    min_x = min(corner1[0], corner2[0])
    max_x = max(corner3[0], corner4[0])
    min_y = min(corner1[1], corner4[1])
    max_y = max(corner2[1], corner3[1])
    
    # Z interpolation between points to create the sloped plane
    def interpolate_z(x, y):
        # Bilinear interpolation between z values of corners
        z1 = corner1[2]
        z2 = corner2[2]
        z3 = corner3[2]
        z4 = corner4[2]
        
        # Interpolation weights
        tx = (x - min_x) / (max_x - min_x)
        ty = (y - min_y) / (max_y - min_y)
        
        # Bilinear interpolation formula
        z_bottom = (1 - tx) * z1 + tx * z2
        z_top = (1 - tx) * z4 + tx * z3
        return (1 - ty) * z_bottom + ty * z_top

    # Function to sample points along the path with a given resolution
    def sample_path(start_x, end_x, y, direction, point_distance):
        path_points = []
        x = start_x
        step = point_distance if direction == 1 else -point_distance
        
        while (direction == 1 and x <= end_x) or (direction == -1 and x >= end_x):
            z = interpolate_z(x, y)
            path_points.append((x, y, z))
            x += step
        
        return path_points
    
    # Generate the 3D mesh points
    current_y = min_y
    direction = 1  # Start moving left to right (1 for right, -1 for left)
    path = []
    
    while current_y <= max_y:
        if direction == 1:  # Move right
            path.extend(sample_path(min_x, max_x, current_y, direction, point_distance))
        else:  # Move left
            path.extend(sample_path(max_x, min_x, current_y, direction, point_distance))
        
        current_y += pass_distance
        direction *= -1  # Switch direction for the next pass
    
    return path

# Example coordinates (decimal lat/lon) of four corner points
corner1_latlon = (34.0, -118.0)  # Bottom-left corner (lat, lon)
corner2_latlon = (34.0, -117.99)  # Bottom-right corner (lat, lon)
corner3_latlon = (34.01, -117.99)  # Top-right corner (lat, lon)
corner4_latlon = (34.01, -118.0)  # Top-left corner (lat, lon)

# Altitudes at each corner (in meters)
corner1_alt = 50   # Altitude at corner1 in meters
corner2_alt = 60   # Altitude at corner2 in meters
corner3_alt = 100  # Altitude at corner3 in meters
corner4_alt = 90   # Altitude at corner4 in meters

# Convert the corner lat/lon into x, y distances in meters using the Vincenty (geodesic) method
corner1 = (0, 0, corner1_alt)  # Reference point (0, 0) for bottom-left
corner2_x = vincenty_distance(corner1_latlon[0], corner1_latlon[1], corner2_latlon[0], corner2_latlon[1])
corner3_y = vincenty_distance(corner2_latlon[0], corner2_latlon[1], corner3_latlon[0], corner3_latlon[1])

corner2 = (corner2_x, 0, corner2_alt)  # Bottom-right corner in meters
corner3 = (corner2_x, corner3_y, corner3_alt)  # Top-right corner in meters
corner4 = (0, corner3_y, corner4_alt)  # Top-left corner in meters

# Use the distance-based points to create the 3D mesh
pass_distance = 50  # Distance between each pass in meters
point_distance = 20  # Distance between points along the path in meters

# Generate the dense 3D mesh using the coordinates in meters
dense_3d_mesh_meters_vincenty = generate_dense_3d_mesh(corner1, corner2, corner3, corner4, pass_distance, point_distance)

# Extract the X, Y, Z coordinates
X_meters_vincenty, Y_meters_vincenty, Z_meters_vincenty = zip(*dense_3d_mesh_meters_vincenty)

# Plotting the 3D path with real-world lat/lon to meters converted (using Vincenty)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the points in meters
ax.scatter(X_meters_vincenty, Y_meters_vincenty, Z_meters_vincenty, c=Z_meters_vincenty, cmap='viridis')

# Labeling axes with distance in meters
ax.set_xlabel('X distance (m)')
ax.set_ylabel('Y distance (m)')
ax.set_zlabel('Altitude (m)')

plt.title('3D Mesh Plot of Zigzag Path (Vincenty Distance)')
plt.show()
