from PIL import Image
import random, shutil
class Visual:
    def arrange_fruits_on_shelves(altered, file1, file2, level):
        shelves_img = Image.open(r'assets\shelves.png').convert('RGBA')
        fruits = {
            'apple': Image.open(r'assets\apple.png').convert('RGBA'),
            'banana': Image.open(r'assets\banana.png').convert('RGBA'),
            'orange': Image.open(r'assets\orange.png').convert('RGBA'),
            'grapes': Image.open(r'assets\grapes.png').convert('RGBA'),
            'watermelon': Image.open(r'assets\watermelon.png').convert('RGBA'),
            'goldenapple': Image.open(r'assets\goldenapple.png').convert('RGBA')
        }
        resize_factor = 0.5
        for fruit_name, fruit_img in fruits.items():
            width, height = fruit_img.size
            new_size = (int(width * resize_factor), int(height * resize_factor))
            fruits[fruit_name] = fruit_img.resize(new_size, Image.LANCZOS)
        if level <= 2: fruit_options = ['apple', 'banana', 'empty', 'empty', 'empty', 'empty']
        if 3 <= level <= 5: fruit_options = ['apple', 'banana', 'orange', 'empty']
        if 6 <= level <= 11: fruit_options = ['apple', 'banana', 'orange', 'empty', 'grapes']
        if 12 <= level <= 19: fruit_options = ['apple', 'banana', 'orange', 'empty', 'grapes', 'watermelon']
        if 20 <= level: fruit_options = ['apple', 'banana', 'orange', 'empty', 'grapes', 'watermelon', 'goldenapple']
        fruit_order = [random.choice(fruit_options) for _ in range(12)]
        final_img = shelves_img.copy()
        width, height = final_img.size
        shelf_area = (0, 0, width, height)
        def place_fruits_on_shelf(shelf_area, fruit_order):
            x1, y1, x2, y2 = shelf_area
            shelf_width = x2 - x1
            shelf_height = y2 - y1
            fruit_width, fruit_height = fruits['apple'].size
            x_spacing = (shelf_width - 4 * fruit_width) // (4 + 1)
            y_spacing = (shelf_height - 3 * fruit_height) // (3 + 1)
            x_spacing = max(10, x_spacing)
            y_spacing = max(10, y_spacing)
            row_offsets = [45, 33, 5]
            for row in range(3):
                for col in range(4):
                    x = x1 + x_spacing + col * (fruit_width + x_spacing)
                    y = y1 + y_spacing + row * (fruit_height + y_spacing) + row_offsets[row]
                    fruit_name = fruit_order[row * 4 + col]
                    if fruit_name != 'empty':
                        fruit_img = fruits[fruit_name]
                        final_img.paste(fruit_img, (x, y), fruit_img)
        place_fruits_on_shelf(shelf_area, fruit_order)
        final_img.save(file1)
        if altered:
            altered_order = fruit_order.copy()
            if fruit_order != ['empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty', 'empty']: 
                alteration = random.choice(['remove', 'change'])
                final_img = shelves_img.copy()
                if alteration == 'remove':
                    fruit_index = random.choice([i for i in range(12) if altered_order[i] != 'empty'])
                    altered_order[fruit_index] = 'empty'
                elif alteration == 'change':
                    fruit_index = random.choice([i for i in range(12) if altered_order[i] != 'empty'])
                    altered_order[fruit_index] = random.choice([x for x in fruit_options if x != altered_order[fruit_index]])
            else: altered_order[random.randint(1,12)] = random.choice(fruit_options)
            place_fruits_on_shelf(shelf_area, altered_order)
            final_img.save(file2)
        else:
            shutil.copy(file1, file2)

