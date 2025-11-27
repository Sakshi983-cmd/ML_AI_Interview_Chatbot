import streamlit as st

def voice_input():
    st.write("Voice mode अभी active है – बोलो:")
    # हम बाद में full voice डाल देंगे, अभी placeholder
    return st.text_input("या यहाँ टाइप करके test करो:")
