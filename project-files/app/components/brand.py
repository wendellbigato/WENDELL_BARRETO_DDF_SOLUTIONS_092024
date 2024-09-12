# Import the streamlit library
import streamlit as st

# Cache the results of the function for 300 seconds
st.cache_data(ttl=300)

# Define a function called "put"
def put():
    # Create a container for the streamlit app
    with st.container():
        # Use HTML/CSS to adjust the image width to 20% and align it to the left
        st.markdown(
            """
            <div style='text-align: left;'>
                <img src="https://app.dadosfera.ai/en-US/assets/images/identity/dadosfera-login.svg" style="width: 20%;">
            </div>
            """, 
            unsafe_allow_html=True
        )
        # Display the specified text as Markdown
        st.markdown("**Data app** templates")
