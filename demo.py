import streamlit as st
from PIL import Image

# Load the background image
background = Image.open(r'C:\Users\Abhishek\OneDrive\Desktop\pexels-nataliya-vaitkevich-7615574.jpg')

# Set the page configuration
st.set_page_config(
    page_title="Ayurvedic Practitioner's Portal",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="expanded",
)

def main():
    st.title("Ayurvedic Practitioner's Portal")

    menu = ["Home", "Login", "SignUp"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.image(background)

    elif choice == "Login":
        st.subheader("Login Section")
        username = st.sidebar.text_input("User Name")
        password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.checkbox("Login"):
            # Implement your authentication logic here
            st.success("Logged In as {}".format(username))

    elif choice == "SignUp":
        st.subheader("Create a New Account")
        new_user = st.text_input("Username")
        new_password = st.text_input("Password", type='password')
        if st.button("Signup"):
            # Implement your account creation logic here
            st.success("You have successfully created an account")

if __name__ == "__main__":
    main()
