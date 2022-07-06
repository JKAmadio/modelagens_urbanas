import numpy as np
import matplotlib.pyplot as plt
import cv2
import os

def count_access(matrix, coordinates):
    number_of_access = 0
    row_index = coordinates[0]
    column_index = coordinates[1]
    # compute 4-neighbour (up, down, left, right)
    # diagonal not available
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    for index in range(len(dx)):
        neighbour_x_index = row_index + dx[index]
        neighbour_y_index = column_index + dy[index]
        if ((neighbour_x_index >= 0 and neighbour_x_index < matrix.shape[0])
                and (neighbour_y_index >= 0 and neighbour_y_index < matrix.shape[1])
                and (matrix[neighbour_x_index][neighbour_y_index] == 0)):
            number_of_access += 1
    return number_of_access

def count_distance_to_unit(matrix, coordinates, visited):
    units = 0
    queue = []
    nodes_left_in_layer = 1
    nodes_in_next_layer = 0
    move_count = 0

    queue.insert(0, coordinates)
    visited[coordinates[0]][coordinates[1]] = True
    while len(queue) > 0:
        current = queue.pop()
        visited, queue, nodes_in_next_layer = explore_neighbours(matrix, current[0], current[1], visited, queue, nodes_in_next_layer)
        nodes_left_in_layer -= 1
        if (matrix[current[0]][current[1]] == 1):
            units += 1
        if (nodes_left_in_layer == 0
                and units == 0):
            nodes_left_in_layer = nodes_in_next_layer
            nodes_in_next_layer = 0
            move_count += 1
        elif (nodes_left_in_layer == 0
                and units != 0):
            break
    return [move_count, units]

def explore_neighbours(matrix, row_index, column_index, visited, queue, nodes_in_next_layer):
    dx = [-1, 1, 0, 0]
    dy = [0, 0, 1, -1]
    for index in range(len(dx)):
        neighbour_x_index = row_index + dx[index]
        neighbour_y_index = column_index + dy[index]
        # não é vizinho válido se for out of bound do array
        if ((neighbour_x_index < 0 or neighbour_x_index >= matrix.shape[0])
                or (neighbour_y_index < 0 or neighbour_y_index >= matrix.shape[1])):
            continue
        if visited[neighbour_x_index][neighbour_y_index] == True:
            continue
        queue.insert(0, [neighbour_x_index, neighbour_y_index])
        visited[neighbour_x_index][neighbour_y_index] = True
        nodes_in_next_layer += 1
    return [visited, queue, nodes_in_next_layer]

def update_cell_state(cell_state, number_of_access, distance_to_unit, number_of_units):
    if (number_of_access == 0
            or (number_of_access == 1 and distance_to_unit == 1 and number_of_units == 1)
            or (number_of_access == 2 and distance_to_unit == 2 and number_of_units == 2)
            or (number_of_access == 3 and distance_to_unit == 2 and number_of_units == 2)
            or (number_of_access == 2 and distance_to_unit == 2 and number_of_units == 1)
            or (number_of_access == 2 and distance_to_unit == 2 and number_of_units == 1)
            or (number_of_access == 3 and distance_to_unit == 2 and number_of_units == 4)):
        cell_state = 0
    else:
        cell_state = 1
    return cell_state

def walk_through_city(city):
    new_generation = city.copy()
    for row in range(city.shape[0]):
        for column in range(city.shape[1]):
            visited = np.full((city.shape[0], city.shape[1]), False)
            number_of_access = count_access(city, [row, column])
            distance_to_unit, number_of_units = count_distance_to_unit(city, [row, column], visited)
            # print(f'[{row}][{column}] -> {number_of_access} saidas')
            # print(f'{distance_to_unit} passos -> {number_of_units} unidades')
            new_generation[row][column] = update_cell_state(
                city[row][column],
                number_of_access,
                distance_to_unit,
                number_of_units
            )
    return new_generation

def print_grid(matrix, count_generations):
    fig, ax = plt.subplots()
    ax.imshow(matrix, cmap='gray')
    fig.set_facecolor('black')
    # plt.show()
    plt.savefig(f"./images/morphogenese_{format(count_generations, '04d')}")

def record_grid_changes():
    # image_list = [img for img in os.listdir('./images/') if img.startswith('morphogenese_)') and img.endswith('.png')]
    image_list = []
    for file in os.listdir('./images/'):
        if (file.startswith('morphogenese_') and file.endswith('.png')):
            image_list.append(file)
    image_list.sort()
    frame = cv2.imread(f'./images/{image_list[0]}')
    height, width, layers = frame.shape
    video = cv2.VideoWriter('./images/morphogenese_video.avi', 0, 3, (width, height))
    for image in image_list:
        video.write(cv2.imread(f"./images/{image}"))
    cv2.destroyAllWindows()
    video.release()

if __name__ == '__main__':
    matrix = np.random.binomial(n=1, p=0.5, size=[10, 10])
    count_generations = 0
    for i in range(20):
        print_grid(matrix, count_generations)
        matrix = walk_through_city(matrix)
        count_generations += 1
    record_grid_changes()
