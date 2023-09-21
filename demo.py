import streamlit as st
import base64
import plotly.express as px
import streamlit_authenticator as stauth
import sqlite3
import yaml
import os
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration 
from dotenv import load_dotenv
from yaml.loader import SafeLoader
with open(r'C:\Users\Abhishek\Desktop\Herbalise\credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Set the page configuration
st.set_page_config(
    page_title="Ayurvedic Practitioner's Portal",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded",
)

load_dotenv()  # Load environment variables from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Get API key from environment variable
tokenizer = RagTokenizer.from_pretrained("facebook/rag-token-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-token-nq", index_name="exact", use_dummy_dataset=True)
model = RagTokenForGeneration.from_pretrained("facebook/rag-token-nq", retriever=retriever)

conn = sqlite3.connect('data.db')
c = conn.cursor()
def create_usertable(): 
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
def add_userdata(username,password):
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username,password))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username,password))
    data = c.fetchall()
    return data

def view_all_users():
    c.execute('SELECT * FROM usertable')
    data = c.fetchall()
    return data

def application():
    authenticator.logout('Logout','main')
    user_input = st.text_input("Enter your query:")
    if st.button("Generate"):
        inputs = tokenizer.prepare_seq2seq_batch([user_input], return_tensors="pt")
        generated = model.generate(inputs["input_ids"])
        st.write(tokenizer.batch_decode(generated, skip_special_tokens=True))



authenticator = stauth.Authenticate (
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


df = px.data.iris()
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64(r"C:\Users\Abhishek\OneDrive\Desktop\pexels-nataliya-vaitkevich-7615574.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: 100%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("https://wallpapercave.com/wp/wp6845532.jpg"); 
background-repeat: no-repeat;
background-size: 100%;
background-attachment: fixed;
background-position: right;
font-color:Black;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}


[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
st.sidebar.title("Configuration")

def main():
    st.title("Ayurvedic Practitioner's Portal")

    menu = ["Home", "Login", "SignUp","Application"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type='password')
        if st.button("Login"):
            data=login_user(username_input, password_input)
            print("Data from the database:", data)
            if data:
                st.write(f'Welcome *{data[0][0]}*')
                application()
            else:
                st.error('username/password is incorrect')

    elif choice == "SignUp":
        st.subheader("Create an Account")
        username = st.text_input('Username')
        password = st.text_input('Password',type='password')
        if st.button('SignUp'):
            create_usertable()
            add_userdata(username,password)
            st.success("You have successfully created an account. Go to the Login Menu to login")
            view_all_users
    
            
if __name__ == "__main__":
    main()
