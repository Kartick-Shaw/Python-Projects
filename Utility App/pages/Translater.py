import streamlit as st
from googletrans import Translator, LANGUAGES

st.title(':blue[Translator]')

# languageDict = {
#     'Hindi': 'hi',
#     'English': 'en',
#     'Bengali': 'bn',
#     'Kannada': 'kn',
#     'Malayalam': 'ml',
#     'Marathi': 'mr',
#     'Russian': 'ru',
#     'Tamil': 'ta',
#     'Telugu': 'te',
#     'Urdu': 'ur',
#     'French': 'fr',
#     'Japanese': 'ja',
#     'Italian': 'it',
# }
languageDict = {v:k for k, v in LANGUAGES.items()}
translator = Translator()
text = st.text_area("Enter an Text: ")
# translator_lang_option = st.selectbox(
#     'Select language in which you want to translate:',
#     ('Hindi', 'English', 'Bengali', 'Kannada', 'Malayalam', 'Marathi', 'Tamil', 'Telugu', 'Urdu', 'French', 'Russian', 'Japanese', 'Italian'))
translator_lang_option = st.selectbox(
    'Select language in which you want to translate:',
    languageDict.keys()
)
if st.button('Translate') and text and translator_lang_option:
    translated_text = translator.translate(text, src='auto', dest=languageDict[translator_lang_option]).text
    st.header(":violet[Translated Text:]", divider='violet')
    st.markdown(f'<h3>{translated_text}</h3>', unsafe_allow_html=True)
