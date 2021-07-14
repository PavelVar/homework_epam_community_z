"""
added some checks to ver1
"""

data_file_address: str = 'C:\\Users\\100nout.by\\Desktop\\'  # necessary to add correct data_file address
data_file_name: str = 'INPUT.txt'  # necessary to add correct data_file name

output_file_address: str = 'C:\\Users\\100nout.by\\Desktop\\'  # necessary to add correct output file address
output_file_name: str = 'OUTPUT.txt'  # necessary to add correct output file name

# get data from file
data = [int(line.strip()) for line in open(f'{data_file_address}{data_file_name}') if line.strip().isdigit()]

if len(data) != 3:  # create messages if not enough digits in file
    print('Please check the amount of data in your file. You are to have 3 digits in it.')
    with open(f'{output_file_address}{output_file_name}', 'w') as output_file:
        output_file.write('Please check the amount of data in your file. You are to have 3 digit in it.')
else:
    N, M, H = data

    items_from_one_tree = H // N  # stakes possible to make from 1 tree

    trees_to_cut = M / items_from_one_tree  # necessary amount of trees

    if int(trees_to_cut) == trees_to_cut:  # check if result is integer
        result = int(trees_to_cut)  # if yes, it's our result
    else:
        result = int(trees_to_cut) + 1  # if no, we need one more tree

    with open(f'{output_file_address}{output_file_name}', 'w') as output_file:
        output_file.write(f'{result}')
