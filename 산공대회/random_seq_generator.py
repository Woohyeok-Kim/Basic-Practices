# hat_label maker
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import ast
import random
import torch
import copy

def format_into_pt(data):
    ret_pt = []
    for element in data:
        ret_pt.append(list(element))
    return ret_pt


def queue_sequence_generator(box_list, q_num):
    # cycle = len(box_list)//q_num
    rem = len(box_list) % q_num
    loc = 0
    queue_list = []
    slide = len(box_list) // q_num
    for cycle in range(q_num):
        queue_list.append(box_list[loc:loc+slide])
        if rem>0:
            queue_list[cycle].append(box_list[loc+slide])
            loc = loc+slide+1
            rem -= 1
        else :
            loc += slide
    #queue_list = rand_sequence_generator(queue_list, 1, len(queue_list))
    queue_list_copy = copy.deepcopy(queue_list)
    random.shuffle(queue_list_copy)
    return [item for sublist in queue_list_copy for item in sublist]
        
    

# def rand_sequence_generator(box_list, iter_num, pick_num):
#     # iter_num = 10
#     for _ in range(iter_num):
#         # pick_num = 2
#         sendBack_index = random.sample(range(len(box_list)), pick_num)
#         for i in range(pick_num):
#             send_back(box_list, box_list[sendBack_index[i]])
#         return box_list

# def top_n_indices(arr, n):
#     sorted_indices = sorted(range(len(arr)), key=lambda i: arr[i], reverse=True)
#     return sorted_indices[:n]

# def bottom_n_indices(arr, n):
#     sorted_indices = sorted(range(len(arr)), key=lambda i: arr[i], reverse=True)
#     return sorted_indices[-n:]


# def size_sequence_generator(box_list, pick_num, option):
#     # Make a copy of box_list to avoid modifying the original list
#     temp_box_list = box_list.copy()
    
#     vol_list = [dim[0]*dim[1]*dim[2] for dim in temp_box_list]
    
#     if option == 'top':
#         sendBack_index = top_n_indices(vol_list, pick_num)
#     elif option == 'bottom':
#         sendBack_index = bottom_n_indices(vol_list, pick_num)
    
#     for i in range(pick_num):
#         send_back(temp_box_list, temp_box_list[sendBack_index[i]])
    
#     return temp_box_list


# def send_back(full_list, box_to_send):
#     full_list.remove(box_to_send)
#     full_list.append(box_to_send)
#     return full_list

def top_n_indices(arr, n):
    sorted_indices = sorted(range(len(arr)), key=lambda i: arr[i], reverse=True)
    return sorted_indices[:n]

def bottom_n_indices(arr, n):
    sorted_indices = sorted(range(len(arr)), key=lambda i: arr[i], reverse=False)
    return sorted_indices[:n]

def size_sequence_generator(box_list, pick_num, option):
    temp_box_list = box_list.copy()
    vol_list = [dim[0] * dim[1] * dim[2] for dim in temp_box_list]

    if option == 'top':
        sendBack_index = top_n_indices(vol_list, pick_num)
    elif option == 'bottom':
        sendBack_index = bottom_n_indices(vol_list, pick_num)
    
    elements_to_move = [temp_box_list[i] for i in sendBack_index]
    temp_box_list = [box for i, box in enumerate(temp_box_list) if i not in sendBack_index]
    temp_box_list.extend(elements_to_move)
    
    return temp_box_list






def add_z_coordinate_to_boxes(items):
    bin_width = 10
    bin_length = 10
    bin_height = 10

    height_map = np.zeros((bin_width, bin_length))

    def find_max_height(flb_x, flb_y, width, length, height_map):
        max_height = 0
        for x in range(flb_x, flb_x + width):
            for y in range(flb_y, flb_y + length):
                max_height = max(max_height, height_map[x, y])
        return max_height

    def update_height_map(flb_x, flb_y, width, length, new_height, height_map):
        for x in range(flb_x, flb_x + width):
            for y in range(flb_y, flb_y + length):
                height_map[x, y] = new_height

    updated_items = []
    for item in items:
        # Unpack dimensions and FLB coordinates
        dimensions = item[0]
        flb_coordinates = item[1]

        # Extract width, length, and height
        width, length, height = dimensions
        
        # Extract x and y coordinates
        flb_x, flb_y = flb_coordinates

        # Calculate the z-coordinate using the height map
        max_height = find_max_height(flb_x, flb_y, width, length, height_map)
        z = max_height

        # Update the height map with the new height after placing the item
        new_height = z + height
        update_height_map(flb_x, flb_y, width, length, new_height, height_map)

        # Append the new item with the calculated z-coordinate
        updated_item = [dimensions, (flb_x, flb_y, z)]
        updated_items.append(updated_item)

    return updated_items


def process_chunks(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    chunks = []
    chunk = ""
    
    for line in lines:
        if line.strip() == "":  # Assuming empty line is the delimiter between chunks
            if chunk:
                chunks.append(chunk.strip())
                chunk = ""
        else:
            chunk += line
    
    # Add the last chunk if the file doesn't end with a blank line
    if chunk:
        chunks.append(chunk.strip())
    
    return chunks



def chunk_to_formatted_list(input_string):
    # Split the input string by newline to handle each sequence individually
    sequences = input_string.strip().split('\n')
    
    result = []
    for seq in sequences:
        # Use ast.literal_eval to safely evaluate the string representation of the tuple
        evaluated_seq = ast.literal_eval(seq)
        
        # Unpack the inner list and the integer, then combine them into one list
        combined_list = evaluated_seq[0][0] + [evaluated_seq[0][1]]
        
        # Append the combined list to the result
        result.append(combined_list)
    
    return result

def inference_to_cube(filepath_of_inference_txt):
    #file_path = filepath_of_inference_txt
    file_path = 'record.txt'
    chunks_list = process_chunks(file_path)

    formatted_nested_list = []
    for chunk in chunks_list:
        formatted_nested_list.append(chunk_to_formatted_list(chunk))


    divisor = 10
    modified_list = []
    for formatted_list in formatted_nested_list:
        modified_el = []
        for sublist in formatted_list:
            act_value = sublist[-1]  # Extract the last element (ACT value)
            quotient = act_value // divisor  # Integer division (quotient)
            remainder = act_value % divisor  # Remainder
            modified_sublist = []
            modified_sublist.append(tuple(sublist[:-1]))
            modified_sublist.append(tuple([quotient, remainder]))
            modified_el.append(modified_sublist)
        del modified_el[-1]
        modified_list.append(modified_el)

    return modified_list
    



def main():

    xcut_data = torch.load('xcut_2.pt')
    # print('length : ', len(xcut_data))
    # print('xcut : ', xcut_data[0])   # xcut is the same format as dim_only
    # print()


    # 0, 11, 29, 50, 159, 589, 1200
    seed = 1200
    xcut_sample = xcut_data[seed]
    print(f'current seed = {seed}')
    print()
    print(f"seed length : {len(xcut_sample)}")
    print()
    dim_only = xcut_sample
    print('original : ', dim_only)
    original = dim_only
    # print('0 : ', original)
    # print() 
    top_volume_stacked = size_sequence_generator(dim_only, 2, 'top')
    mode = 'bottom'
    #print(f'current mode = {mode}')
    print('current mode : queue')
    print()

# stack generator ------------------------------------------------------------------
    # stack = [original]
    # for i in range(len(dim_only)):
    #     stack.append(size_sequence_generator(dim_only, i+1, mode))

    # stack.append(top_volume_stacked) # for padding at the end
    # #print('stack : ', stack)

    # torch.save(stack, 'bottom_volume_1200.pt')
    #torch.save([original, stack_1, stack_2, stack_3, stack_4, stack_5, stack_6, stack_7, stack_8, stack_9, stack_10, top_volume_stacked], 'top_volume_29.pt')
    #print(f'{original}\n{stack_1}\n{stack_2}\n{stack_3}\n{stack_4}\n{stack_5}\n{stack_6}\n{stack_7}\n{stack_8}\n{stack_9}\n{stack_10}')
    

# conveyor belt part -----------------------------------------------
    queue_rand_save = []
    dim_only = xcut_sample
    for i in range(31):
        queue_1 = queue_sequence_generator(dim_only, 10)
        queue_rand_save.append(queue_1)
        # print(queue_1)
        # print()

    torch.save(queue_rand_save, 'queue_1200_10.pt')


    print('done')

if __name__ == "__main__":
    main()





