from flask import Flask, render_template, request, jsonify
import copy

app = Flask(__name__)

# Initialize the array
button_array = [0] * 25
array_duplicate = [0] * 25
counter_matrix = [0] * 25
count = 0

@app.route('/')
def index():
    return render_template('index.html', button_array=button_array)

@app.route('/update_array', methods=['POST'])
def update_array():
    button_index = int(request.form['button_index'])
    indexes = list(get_unclicked_row_indices(button_index))
    print(indexes)
    if button_array[button_index] == 1 and array_duplicate[button_index] != 1:
        button_array[button_index] = 0
    else:
        # Check if any other button is already clicked on the same row
        # indexes = get_indexes_of_ones(array_duplicate)
        if sum_of_remaining_row(indexes):
            reset_row(indexes)
        button_array[button_index] = 1

    print(button_array)
    disabled_buttons = list(get_indexes_of_ones(button_array))
    return jsonify(success=True, disabled_buttons=disabled_buttons)

@app.route('/next_round', methods=['POST'])
def next_round_route():
    curr_count = next_round()
    disabled_buttons = list(get_indexes_of_ones(button_array))
    return jsonify(count=curr_count, disabled_buttons=disabled_buttons)


def next_round():
    # Need to count rows and columns
    global array_duplicate
    global counter_matrix
    global count
    new_indexes = get_indexes_of_ones(button_array) - get_indexes_of_ones(array_duplicate)

    for i in new_indexes:
        row = i // 5  # Calculate the row index
        col = i % 5  # Calculate the column
        index_tracker = i
        if counter_matrix[index_tracker] != 1:
            count = count + button_array[index_tracker]
            counter_matrix[index_tracker] = 1

        while row > 0: #TODO: Need to check if button_array doesnt get reset
            index_tracker = index_tracker - 5
            if button_array[index_tracker] != 0 and counter_matrix[index_tracker] != 1:
                counter_matrix[index_tracker] = 1
                count = count + 1
                row = row - 1

            else:
                break

        index_tracker = i
        while row < 4: #TODO: Need to check if button_array doesnt get reset
            index_tracker = index_tracker + 5

            if button_array[index_tracker] != 0 and counter_matrix[index_tracker] != 1:
                counter_matrix[index_tracker] = 1
                count = count + 1
                row = row + 1
            else:
                break

        index_tracker = i
        while col > 0: #TODO: Need to check if button_array doesnt get reset
            index_tracker = index_tracker - 1
            if button_array[index_tracker] != 0 and counter_matrix[index_tracker] != 1:
                counter_matrix[index_tracker] = 1
                count = count + 1
                col = col - 1
            else:
                break

        index_tracker = i
        while col < 4: #TODO: Need to check if button_array doesnt get reset
            index_tracker = index_tracker + 1
            if button_array[index_tracker] != 0 and counter_matrix[index_tracker] != 1:
                counter_matrix[index_tracker] = 1
                count = count + 1
                col = col + 1
            else:
                break
    counter_matrix = [0] * 25
    return count

    # # for i in range(0, 21, 5):
    #     new_indexes = get_indexes_of_ones(button_array) - get_indexes_of_ones(array_duplicate)
    #     #TODO: NEed to account for those from previous rows
    #     row = i // 5  # Calculate the row index
    #
    #     row_count = sum_of_row(row)
    #     col_count = sum_of_col(col)
    #     count = count + row_count + col_count
    #
    # array_duplicate = copy.deepcopy(button_array)
    # # return count

# Function to calculate the sum of values in a row
def sum_of_row(row):
    start_index = row * 5
    end_index = start_index + 5
    print(button_array[start_index])
    row_values = button_array[start_index:end_index]
    print(row_values)
    return sum(row_values)


# Function to calculate the sum of values in a row
def sum_of_remaining_row(indexes):
    count = 0
    for i in indexes:
        count = count + button_array[i]
    print("count ", count)
    if count > 0:
        return True
    return False


# Function to calculate the sum of columns in a col
def sum_of_col(col):
    #TODO test
    start_index = col % 5
    col_values = []
    for i in 5:
        col_values.append(button_array[start_index])
        start_index = start_index * 5
    return sum(col_values)

def get_unclicked_row_indices(index):
    num_cols = 5
    row_index = index // num_cols  # Integer division to find the row index
    start_index = row_index * num_cols
    end_index = start_index + num_cols - 1
    res = []
    for i in range(start_index, end_index):
        if array_duplicate[i] == 0:
            res.append(i)
    return res

def reset_row(indexes):
    for i in indexes:
        button_array[i] = 0

def get_indexes_of_ones(A):
    indexes = set()
    for i in range(len(A)):
        if A[i] == 1:
            indexes.add(i)
    return indexes

def get_remaining_indexes(known_indexes):
    all_indexes = set(range(25))
    remaining_indexes = all_indexes - known_indexes
    return remaining_indexes

if __name__ == '__main__':
    app.run(debug=True)
