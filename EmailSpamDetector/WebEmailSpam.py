import streamlit as st
import pickle

with open('spam_detect', 'rb') as file:
    clf = pickle.load(file)

st.title("Email Spam Cheaker")
emails = st.text_area("Enter an email")
if st.button('Check'):
    if clf.predict([emails])[0] == 1:
        st.warning('The email is a Spam email')
    else:
        st.success('The email is not a Spam email')