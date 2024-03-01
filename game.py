from button import Button


class Game:

    def __init__(self):
        self.button_array = [Button(i // 5 + 1) for i in range(25)]
        self.set_button_images()
        self.counter_matrix = [0] * 25
        self.score = 0
        # self.locked_buttons = []


    def row_checker(self, row_number, button_index):
        start_index = (row_number - 1) * 5
        end_index = row_number * 5

        for i, button in enumerate(self.button_array[start_index:end_index]):
            if button.clicked and i is not button_index:
                button.toggleClicked()

    def calculate_longest_chain(self, score, index, stepsize, ogindex):
        # row_index = ((ogindex // 5) + 1) * 5
        # row_index = (index // 5) -1
        col_index = (index) % 5
        # print(ogindex, " INDEX")
        # print(row_index, " ROW INDEX")
        print(col_index, " COL INDEX")
        ### TODO: THIS HERE or (col_index == 0 and stepsize > 0) or (col_index == 4 and stepsize < 0)
        if col_index < -1 or col_index > 4 or index > 24 or index < 0 or (ogindex % 5 == 4 and stepsize == 1) or (ogindex % 5 == 0 and stepsize == -1):
            print("OUT OF BOUNDS: ", index)
            return score
        # if ogindex % 5 == 4 and stepsize == 1:
        # if index < row_index-5 or index > row_index - 1 or col_index < -1 or col_index > 4:
        #     print("Huh: ", index)
        #     return score
        if not self.button_array[index].clicked:
            print("NOT CLICKED ", index)
            return score
        if self.button_array[index].clicked:
            self.button_array[index].lockButton()
            print("SCORE ADDED 1 at ", index)
            return self.calculate_longest_chain(score + 1, index + stepsize, stepsize, ogindex)




    ### TODO: One problem is that if 2 next to each other are selected same col then we get +2 2*
    def lock_buttons_and_count(self):
        col = -1
        for i, buttons in enumerate(self.button_array):
            # col_checker = i % 5 == col
            # print("####################### LINE BREAK ##########")
            # print(i, " index")
            # print(col, " col")
            # print(col_checker, " Col checker")
            # print("####################### LINE BREAK ##########")

            if buttons.clicked and not buttons.locked: # and not col_checker:
                # col = i % 5
                buttons.lockButton()
                print("RIGHT ")
                left = self.calculate_longest_chain(0, i+1, 1, i)
                print("LEFT ")
                right = self.calculate_longest_chain(0, i-1, -1, i)
                print("UP ")
                up = self.calculate_longest_chain(0, i+5, 5, i)
                print("DOWN ")
                down = self.calculate_longest_chain(0, i-5, -5, i)
                flag = False
                if left or right >= 1:
                    print("WE added 1 cuz no left or right >=1 ")
                    flag = True
                    self.score += 1 + left + right
                if up or down >= 1:
                    print("WE added 1 cuz no up or down >=1 ")
                    flag = True
                    self.score += 1 + up + down
                if not flag:
                    self.score += 1

    def get_locked_buttons(self):
        locked_buttons_index = []
        for i, buttons in enumerate(self.button_array):
            if buttons.locked:
                locked_buttons_index.append(i)
        return locked_buttons_index

    def reset_game(self):
        self.button_array = [Button(i // 5 + 1) for i in range(25)]
        self.counter_matrix = [0] * 25
        self.score = 0

    def set_button_images(self):
        azul_board_1d = [1, 2, 3, 4, 5, 5, 1, 2, 3, 4, 4, 5, 1, 2, 3, 3, 4, 5, 1, 2, 2, 3, 4, 5, 1]
        for i, button in enumerate(self.button_array):
            image_index = azul_board_1d[i]
            if image_index == 1:
                button.image = 'blue_unclicked.png'
                button.clicked_image = 'blue_clicked.png'
            elif image_index == 2:
                button.image = 'yellow_unclicked.png'
                button.clicked_image = 'yellow_clicked.png'
            elif image_index == 3:
                button.image = 'red_unclicked.png'
                button.clicked_image = 'red_clicked.png'
            elif image_index == 4:
                button.image = 'black_unclicked.png'
                button.clicked_image = 'black_clicked.png'
            elif image_index == 5:
                button.image = 'light_blue_unclicked.png'
                button.clicked_image = 'light_blue_clicked.png'

    # def update_locked_buttons(self):
    #     for index, button in self.button_array:
    #         if button.locked:
    #             self.button_array.append(index)
    #
    # def get_locked_buttons(self):
    #     return self.locked_buttons
