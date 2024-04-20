import streamlit as st

# st.sidebar.title('Utility App')
st.title(':blue[Utility App]')
st.subheader(":orange[Select an option]", divider='orange')
st.page_link("Home.py", label="Home", icon="🏠")
st.page_link("pages/Check-Weather.py", label="Check Weather", icon="☁️")
st.page_link("pages/Download-Youtube-Videos.py", label="Download Youtube Videos", icon="📽️")
st.page_link("pages/Edit-PDFs.py", label="PDF Editor", icon="📄")
st.page_link("pages/QR-Code-Generator.py", label="Generate QR Code", icon="🎲")
st.page_link("pages/Translater.py", label="Translate", icon="⌨️")