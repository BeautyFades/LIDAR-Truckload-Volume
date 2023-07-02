import math
import matplotlib.pyplot as plt

def rotate_points(points, angle_degrees, pivot):
    angle_radians = math.radians(angle_degrees)
    pivot_x, pivot_y = pivot
    rotated_points = []
    for x, y in points:
        translated_x = x - pivot_x
        translated_y = y - pivot_y
        new_x = translated_x * math.cos(angle_radians) - translated_y * math.sin(angle_radians)
        new_y = translated_x * math.sin(angle_radians) + translated_y * math.cos(angle_radians)
        rotated_x = new_x + pivot_x
        rotated_y = new_y + pivot_y
        rotated_points.append((rotated_x, rotated_y))
    return rotated_points

# Example usage
points = [(1.0, 2.0), (3.0, 4.0), (5.0, 6.0)]
angle = 45.0
pivot = (2.0, 3.0)
rotated_points = rotate_points(points, angle, pivot)

# Extract x and y coordinates for plotting
x_original = [point[0] for point in points]
y_original = [point[1] for point in points]
x_rotated = [point[0] for point in rotated_points]
y_rotated = [point[1] for point in rotated_points]

# Plot the original and rotated points
plt.figure(figsize=(8, 4))
plt.subplot(121)
plt.scatter(x_original, y_original, color='blue', label='Original')
plt.scatter(pivot[0], pivot[1], color='red', label='Pivot')
plt.title('Original Points')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.legend()

plt.subplot(122)
plt.scatter(x_rotated, y_rotated, color='red', label='Rotated')
plt.scatter(pivot[0], pivot[1], color='blue', label='Pivot')
plt.title('Rotated Points')
plt.xlabel('X')
plt.ylabel('Y')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
