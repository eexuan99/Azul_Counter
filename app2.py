from flask import Flask, render_template, request, jsonify
from game import Game


app = Flask(__name__)
game = Game()


@app.route('/')
def index():

    return render_template('index2.html', button_array=game.button_array)

@app.route('/update_array', methods=['POST'])
def update_array():
    button_index = int(request.form['button_index'])
    row_number = game.button_array[button_index].row
    game.row_checker(row_number, button_index)
    game.button_array[button_index].toggleClicked()
    return jsonify(success=True, buttons=[button.__dict__ for button in game.button_array])

@app.route('/next_round', methods=['POST'])
def next_round():
    game.lock_buttons_and_count()
    return jsonify(success=True, count=game.score, lock_buttons=game.get_locked_buttons(), message="Round completed")

@app.route('/reset_game', methods=['POST'])
def reset_game():
    game.reset_game()
    return jsonify(success=True, buttons=[button.__dict__ for button in game.button_array])

@app.route('/get_button_state', methods=['GET'])
def get_button_state():
    return jsonify(success=True, buttons=[button.__dict__ for button in game.button_array])

@app.route('/get_index_locked_buttons', methods=['GET'])
def get_index_locked_buttons():
    locked_buttons = game.get_locked_buttons()
    locked_buttons_list = [locked_buttons[i:i + 5] for i in range(0, len(locked_buttons), 5)]
    print("over hereS")
    print(locked_buttons)
    print(locked_buttons_list)

    return jsonify(success=True, index=locked_buttons_list)

    # def next_rount(self):
    #     # get indexes
    #     new_indexes = self.get_indexes_of_ones(self.button_array) - self.get_indexes_of_ones(self.array_duplicate)
    #
    #     for i in new_indexes:
    #         row = i // 5  # Calculate the row index
    #         col = i % 5  # Calculate the column
    #         index_tracker = i
    #         if self.counter_matrix[index_tracker] != 1:
    #             count = count + self.button_array[index_tracker]
    #             self.counter_matrix[index_tracker] = 1
    #
    #         while row > 0:  # TODO: Need to check if button_array doesnt get reset
    #             index_tracker = index_tracker - 5
    #             if self.button_array[index_tracker] != 0 and self.counter_matrix[index_tracker] != 1:
    #                 self.counter_matrix[index_tracker] = 1
    #                 count = count + 1
    #                 row = row - 1
    #             else:
    #                 break
    #
    #         index_tracker = i
    #         while row < 4:  # TODO: Need to check if button_array doesnt get reset
    #             index_tracker = index_tracker + 5
    #
    #             if self.button_array[index_tracker] != 0 and self.counter_matrix[index_tracker] != 1:
    #                 self.counter_matrix[index_tracker] = 1
    #                 count = count + 1
    #                 row = row + 1
    #             else:
    #                 break
    #
    #         index_tracker = i
    #         while col > 0:  # TODO: Need to check if button_array doesnt get reset
    #             index_tracker = index_tracker - 1
    #             if self.button_array[index_tracker] != 0 and self.counter_matrix[index_tracker] != 1:
    #                 self.counter_matrix[index_tracker] = 1
    #                 count = count + 1
    #                 col = col - 1
    #             else:
    #                 break
    #
    #         index_tracker = i
    #         while col < 4:  # TODO: Need to check if button_array doesnt get reset
    #             index_tracker = index_tracker + 1
    #             if self.button_array[index_tracker] != 0 and self.counter_matrix[index_tracker] != 1:
    #                 self.counter_matrix[index_tracker] = 1
    #                 count = count + 1
    #                 col = col + 1
    #             else:
    #                 break
    #
    #     self.counter_matrix = [0] * 25
    #     return count
    #
    # # Function to calculate the sum of values in a row
    # def sum_of_row(self, row):
    #     start_index = row * 5
    #     end_index = start_index + 5
    #     print(button_array[start_index])
    #     row_values = self.button_array[start_index:end_index]
    #     print(row_values)
    #     return sum(row_values)
    #
    # # Function to calculate the sum of values in a row
    # def sum_of_remaining_row(self, indexes):
    #     count = 0
    #     for i in indexes:
    #         count = count + button_array[i]
    #     print("count ", count)
    #     if count > 0:
    #         return True
    #     return False
    #
    # # Function to calculate the sum of columns in a col
    # def sum_of_col(self, col):
    #     # TODO test
    #     start_index = col % 5
    #     col_values = []
    #     for i in 5:
    #         col_values.append(button_array[start_index])
    #         start_index = start_index * 5
    #     return sum(col_values)


if __name__ == '__main__':
    app.run(debug=True)