import time
import streamlit as st
from utils.globals import *
import utils.util as util


label_dict = util.read_label_dict("label_dict.json")

st.set_page_config(page_title="Food Label Recognition", 
                   page_icon="🧃",
                   layout="wide")

# Make sure page renders from a clean slate on state changes (otherwise deleted elements will stay greyed-out in backgorund)
def get_clean_rendering_container():
    slot_in_use = st.session_state.slot_in_use = st.session_state.get("slot_in_use", "a")
    if slot_in_use == "a":
        slot_in_use = st.session_state.slot_in_use = "b"
    else:
        slot_in_use = st.session_state.slot_in_use = "a"

    slot = {
        "a": st.empty(),
        "b": st.empty(),
    }[slot_in_use]

    return slot.container()


## HEADER

st.write("""
# Food Label Recognition
Take picture of food products and get information on the labels their packaging might have.
""")
st.divider()

## BODY - 2 COLUMNS

cont = get_clean_rendering_container()
col1, col2 = cont.columns(2)

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

for label in model_labels.keys():
    img_path, label_name, label_description = util.get_label_data(label, label_dict)

    with col2.expander(f"**{label_name}**", expanded=True):
        scol1, scol2 = st.columns(2, vertical_alignment="center")

        scol1.image(str(img_path), width=200)

        scol2.write(f"""
        ## {label_name}
        {label_description}
        """)

## REFRESH SCRIPT

while True: # wait until new file (with new labels) exists in directory, then refresh page
    # might be enough to just check for new file, not if labels are also equal
    model_output = util.get_newest_file_in_dir(DIR_MODEL_RESULTS)
    model_labels_new = util.read_yolo_output(model_output)

    if model_labels_new != model_labels:
        st.rerun()

    time.sleep(0.2)
