import streamlit as st
import base64
import plotly.express as px
import streamlit_authenticator as stauth
import sqlite3
import yaml
from yaml.loader import SafeLoader
with open(r'C:\Users\Abhishek\Desktop\credentials.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Set the page configuration
st.set_page_config(
    page_title="Ayurvedic Practitioner's Portal",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded",
)

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
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data


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
st.sidebar.header("Configuration")

def main():
    st.title("Ayurvedic Practitioner's Portal")

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")

    elif choice == "Login":
        st.subheader("Login Section")
        name, authentication_status, username = authenticator.login('Login', 'main')
        if authentication_status:
            authenticator.logout('Logout', 'main')
        if username == 'tswift':
            st.write(f'Welcome *{name}*')
            authenticator.logout('Logout', 'main')
            st.title('Application 1')

        elif username == 'weeknd':
            st.write(f'Welcome *{name}*')
            authenticator.logout('Logout', 'main')
            st.title('Application 2')
            
        elif authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status == None:
            st.warning('Please enter your username and password')


    elif choice == "SignUp":
        st.subheader("Create a New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        if st.button("Signup"):
            # Implement your account creation logic here
            st.success("You have successfully created an account")
            
if __name__ == "__main__":
    main()
