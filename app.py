import streamlit as st
import pandas as pd

# Load book data
@st.cache_data
def load_data():
    return pd.read_excel("library_books_real.xlsx")

df = load_data()

def display_books():
    st.markdown("## 📚 Welcome to Your Smart Library System")
    st.markdown("Manage your library like a pro! 🤓 Use the sidebar to:")
    st.markdown("- 🔍 Search for books")
    st.markdown("- 📕 Borrow a book")
    st.markdown("- 📗 Return a book")

    # Book statistics
    total = len(df)
    available = len(df[df["Status"] == "Available"])
    borrowed = len(df[df["Status"] == "Borrowed"])

    col1, col2, col3 = st.columns(3)
    col1.metric("📘 Total Books", total)
    col2.metric("✅ Available", available)
    col3.metric("📕 Borrowed", borrowed)

    st.markdown("### 📖 Book List")
    st.dataframe(df, use_container_width=True)



def search_books(query):
    query = query.lower()
    filtered = df[
        df["Title"].str.lower().str.contains(query) |
        df["Author"].str.lower().str.contains(query) |
        df["ISBN"].astype(str).str.contains(query)
    ]
    return filtered

def borrow_book(isbn, user_name):
    if isbn in df["ISBN"].values:
        book = df[df["ISBN"] == isbn]
        if book["Status"].iloc[0] == "Available":
            df.loc[df["ISBN"] == isbn, "Status"] = "Borrowed"
            st.success(f"✅ {user_name} borrowed '{book['Title'].iloc[0]}'")
        else:
            st.warning("⚠️ Book is already borrowed.")
    else:
        st.error("❌ ISBN not found.")

def return_book(isbn, user_name):
    if isbn in df["ISBN"].values:
        book = df[df["ISBN"] == isbn]
        if book["Status"].iloc[0] == "Borrowed":
            df.loc[df["ISBN"] == isbn, "Status"] = "Available"
            st.success(f"✅ {user_name} returned '{book['Title'].iloc[0]}'")
        else:
            st.warning("⚠️ Book was not borrowed.")
    else:
        st.error("❌ ISBN not found.")

# Streamlit interface
st.title("📖 Library Management System")

menu = ["Home", "Search Books", "Borrow Book", "Return Book"]
choice = st.sidebar.selectbox("Choose an Option", menu)

if choice == "Home":
    display_books()

elif choice == "Search Books":
    st.subheader("🔍 Search for a Book")
    st.markdown("Type a **Book Title**, **Author Name**, or **ISBN** to search:")
    query = st.text_input("Search here...")
    if query:
        results = search_books(query)
        if not results.empty:
            st.success(f"🔎 Found {len(results)} book(s):")
            st.dataframe(results)
        else:
            st.warning("❌ No matching books found.")

elif choice == "Borrow Book":
    st.subheader("📕 Borrow a Book")
    isbn = st.text_input("Enter ISBN of the book you want to borrow")
    user = st.text_input("Enter Your Name")
    if st.button("Borrow"):
        borrow_book(isbn, user)

elif choice == "Return Book":
    st.subheader("📗 Return a Book")
    isbn = st.text_input("Enter ISBN of the book you want to return")
    user = st.text_input("Enter Your Name")
    if st.button("Return"):
        return_book(isbn, user)

