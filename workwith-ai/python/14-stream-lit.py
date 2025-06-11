import streamlit as st
import pandas as pd
import numpy as np

# Set page title
st.title('My Streamlit App')

# Add a header
st.header('Welcome to this demo!')

# Add some text
st.write('This is a simple Streamlit app demonstration')

# Create a sample dataframe
df = pd.DataFrame({
    'Column 1': [1, 2, 3, 4, 5],
    'Column 2': [10, 20, 30, 40, 50]
})

# Display the dataframe
st.subheader('Sample DataFrame:')
st.dataframe(df)

# Add a chart
st.subheader('Line Chart:')
st.line_chart(df)

# Add a slider widget
value = st.slider('Select a value:', 0, 100, 50)
st.write(f'Selected value: {value}')

# Add a selectbox
option = st.selectbox(
    'What is your favorite color?',
    ['Red', 'Green', 'Blue', 'Yellow']
)
st.write(f'Your selected color is: {option}')

# Add a button
if st.button('Click me!'):
    st.balloons()
    st.write('🎉 You clicked the button!')

# Add sidebar elements
with st.sidebar:
    st.header('Sidebar')
    st.write('This is a sidebar element')
    user_input = st.text_input('Enter your name')
    if user_input:
        st.write(f'Hello, {user_input}!')
