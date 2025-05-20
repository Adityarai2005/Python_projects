import os
import streamlit as st
from  dotenv import load_dotenv
import google.generativeai as gen_ai
from streamlit_option_menu import option_menu
load_dotenv()

st.set_page_config(
    page_title="chat with Gemini",
    page_icon="brain",
    layout="centered"
)
api=os.getenv("api_key")
gen_ai.configure(api_key=api)


with st.sidebar:
   selected=option_menu(menu_title="Gemini AI",
                     options=   ["Chat Bot",
                        'Image Captioning'
                        ,"Embed text",
                        "Ask me Anything"],
                        menu_icon='robot',
                        icons=['chat-dots-fill','image-fill'
                               ,'textarea-t','patch-question-fill'],
                               default_index=0)
if selected=="Chat Bot":
     model=gen_ai.GenerativeModel('gemini-2.0-flash')
     def translate_role(user_role):
      if user_role=='model':
        return "assistant"
      else:
        return user_role
     if "chat_session" not in st.session_state:
         st.session_state.chat_session =model.start_chat(history=[])
        
     st.title("Chatbot")

     for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role(message.role)):
           st.markdown(message.part[0].text)

     prompt=st.chat_input("ask gemini")
     if prompt:
        st.chat_message("User").markdown(prompt)

        gemini_response=st.session_state.chat_session.send_message(prompt)

        with st.chat_message("assistant"):
           st.markdown(gemini_response.text)