import time
import streamlit as st
from utils.globals import *
import utils.util as util


label_dict = util.read_label_dict("label_dict.json")

st.set_page_config(page_title="Food Label Recognition", 
                   page_icon="🧃",
                   layout="wide") 

## HEADER

st.write("""
# Food Label Recognition
Take picture of food products and get information on the labels their packaging might have.
""")
st.divider()

## BODY - 2 COLUMNS

col1, col2 = st.columns(2)

## LEFT COLUMN

col1.write("""
## Image Placeholder:
""")
col1.image(str(DIR_IMG / "bio_hexagon.svg")) # placeholder

## RIGHT COLUMN

model_output = util.get_newest_file_in_dir(DIR_MODEL_RESULTS)
while model_output == "": # wait until file exists in directory
    model_output = util.get_newest_file_in_dir(DIR_MODEL_RESULTS)
    time.sleep(0.2)
model_labels = util.read_yolo_output(model_output)

for label_name in model_labels.keys():
    img_path, label_description = util.get_label_data(label_name, label_dict)

    with col2.expander(f"**{label_name}**", expanded=True):
        scol1, scol2 = st.columns(2, vertical_alignment="center")

        scol1.image(str(img_path), width=200)

        scol2.write(f"""
        ## {label_name}
        {label_description}
        """)
