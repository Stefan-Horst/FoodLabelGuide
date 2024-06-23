import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
img_paths = os.listdir(f"{current_dir}/images")

with open(f"{current_dir}/label_descriptions.json", "r", encoding="utf-8") as fp:
    text_dict = json.load(fp)

dict = {}

for img_path in img_paths:
    label_name = os.path.splitext(img_path)[0]

    dict[label_name] = {
        "img_path": img_path,
        "description": text_dict[label_name]["text"],
    }

with open(f"{current_dir}/final_dict.json", "w", encoding="utf-8") as fp:
    json.dump(dict, fp, ensure_ascii=False)

# with open(f"test.txt", "w") as fp:
#     for img_path in img_paths:
#         fp.write(f"{os.path.splitext(img_path)[0]}, ")
