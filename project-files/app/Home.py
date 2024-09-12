import streamlit as st
import numpy as np
from components import brand

brand.put()


# Non-interactive elements return a placeholder to their location
# in the app. Here we're storing progress_bar to update it later.
progress_bar = st.sidebar.progress(0)

# These two elements will be filled in later, so we create a placeholder
# for them using st.empty()
frame_text = st.sidebar.empty()
image = st.empty()


# We clear elements by calling empty on them.
progress_bar.empty()
frame_text.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")
