import streamlit as st
import os
import json

# # Path to your SVG file
svg_file_path = "./images/bio_hexagon.svg"

# # Read the SVG file content
# with open(svg_file_path, "r") as file:
#     svg_content = file.read()

current_dir = os.path.dirname(os.path.abspath(__file__))

with open(f"{current_dir}/final_dict.json", "r", encoding="utf-8") as fp:
    final_dict = json.load(fp)


for key, val in final_dict.items():
    img_path = f'{current_dir}/images/{val['img_path']}'
    st.image(img_path, width = 200)
    st.text(val["description"])
    st.divider()
