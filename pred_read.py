import re

file_name = "test_output"

file = open(file_name, "r")
lines = file.readlines()

labels = []
for i in range(len(lines)):
    line = lines[-i-1]
    if "%\t" in line:
        labels.append(line)

# dict structure: {"label_name": [confidence_percent, left_x, top_y, width, height]}
labels_dict = {}
for label in labels:
    name = label.split(":")[0]

    num_list = [int(s) for s in re.findall("-?\d+\.?\d*", label)]
    if len(num_list) > 5:
        num_list = num_list[-5:]
    
    labels_dict[name] = num_list

print(labels_dict)
