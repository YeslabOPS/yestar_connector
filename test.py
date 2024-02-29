import os
back_path = 'ConfigBack'
ctime = os.path.getctime(back_path+'/1_1_1_1_15_12_13.txt')
print(ctime)