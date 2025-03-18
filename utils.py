def refactor_groups_from_excel():
    """
    This code will help you to convert copied goals from Excel to Python List format
    We have the names of the goals in the txt file, 1 line 1 goal
    :example: 1 line: car
            2 line: energy
            3 line: house

    :return: ['car', 'energy', 'house']
    After formatting, you can copy and paste into the groups folder,
    having previously specified the variable from the buttons in the buttons folder

    """
    with open("refactor_your_groups.txt", "r", encoding="utf-8") as file:
        lines_list = [line.strip() for line in file]
        return print(lines_list)

refactor_groups_from_excel()