import streamlit as st


img = "/resources/images/bio_hexagon.svg"


st.write("""
# AISS CV
This is a demo window.
""")

st.divider()


col1, col2 = st.columns(2)

col1.write("""
## Image:
""")

col1.image(img)


for i in range(2):
    with col2.expander("Label Name", expanded=True):
        scol1, scol2 = st.columns(2)

        scol1.image(img)

        scol2.write("""
        ## Label
        This is text.
        This is even more text.
        This is a description.
        """)
