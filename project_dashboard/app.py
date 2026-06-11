import streamlit as st
import sqlite3

# Database Connection
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ---------------- LOGIN PAGE ---------------- #

if not st.session_state.logged_in:

    st.markdown("""
    <style>
    .stApp {
        background-color: #2196F3;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>Login</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):

            if email and password:

                st.session_state.logged_in = True
                st.session_state.user_email = email

                st.rerun()

            else:
                st.error("Enter Email and Password")

# ---------------- DASHBOARD ---------------- #

else:

    top1, top2 = st.columns([9,1])

    with top2:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.rerun()

    st.title("Dashboard")

    st.success(f"Logged in as: {st.session_state.user_email}")

    st.markdown("---")

    st.subheader("All Added Users")

    c.execute("SELECT name,email,password FROM users")
    users = c.fetchall()

    if users:
        for user in users:

            st.markdown(
                f"""
                <div style="
                    border:1px solid #ccc;
                    padding:15px;
                    border-radius:10px;
                    margin-bottom:10px;
                ">
                <b>Name:</b> {user[0]}<br>
                <b>Email:</b> {user[1]}<br>
                <b>Password:</b> {user[2]}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No users added yet.")

    st.markdown("---")

    st.subheader("Add User")

    with st.form("add_user_form"):

        name = st.text_input("Name")
        new_email = st.text_input("Email")
        new_password = st.text_input("Password")

        submit = st.form_submit_button("Add User")

        if submit:

            if name and new_email and new_password:

                try:

                    c.execute(
                        """
                        INSERT INTO users(name,email,password)
                        VALUES(?,?,?)
                        """,
                        (name, new_email, new_password)
                    )

                    conn.commit()

                    st.success("User Added Successfully")
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("Email Already Exists")

            else:
                st.warning("Fill all fields")