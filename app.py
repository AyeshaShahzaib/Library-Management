import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("library_books_real.xlsx")

df = load_data()

# --- HOME PAGE ---
def home():
    st.title("📚 Personal Library Manager")
    st.markdown("Welcome, Ayesha! This is your personal book tracker. ✨")
    total = len(df)
    to_read = len(df[df["Status"] == "To Read"])
    reading = len(df[df["Status"] == "Reading"])
    completed = len(df[df["Status"] == "Completed"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📘 Total Books", total)
    col2.metric("📖 To Read", to_read)
    col3.metric("📚 Reading", reading)
    col4.metric("✅ Completed", completed)

    st.markdown("### 📖 Your Book Collection")
    st.dataframe(df, use_container_width=True)

# --- SEARCH BOOKS ---
def search_books(query):
    query = query.lower()
    filtered = df[
        df["Title"].str.lower().str.contains(query) |
        df["Author"].str.lower().str.contains(query) |
        df["ISBN"].astype(str).str.contains(query)
    ]
    return filtered

# --- UPDATE READING STATUS ---
def update_status():
    st.subheader("📗 Update Book Status")
    isbn = st.text_input("Enter ISBN")
    new_status = st.selectbox("New Status", ["To Read", "Reading", "Completed"])
    if st.button("Update"):
        if isbn in df["ISBN"].values:
            df.loc[df["ISBN"] == isbn, "Status"] = new_status
            st.success(f"✅ Updated status to '{new_status}'")
        else:
            st.error("❌ ISBN not found.")

# --- ADD NEW BOOK ---
def add_book():
    st.subheader("➕ Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    isbn = st.text_input("ISBN")
    status = st.selectbox("Status", ["To Read", "Reading", "Completed"])
    if st.button("Add Book"):
        if isbn in df["ISBN"].astype(str).values:
            st.warning("⚠️ This book already exists.")
        else:
            new_row = pd.DataFrame([[title, author, isbn, status]], columns=["Title", "Author", "ISBN", "Status"])
            df.loc[len(df)] = new_row.iloc[0]
            st.success(f"📘 '{title}' added to your library!")

# --- FILTER BOOKS ---
def filter_books():
    st.subheader("📂 Filter Books by Status")
    option = st.selectbox("Choose status", ["To Read", "Reading", "Completed"])
    filtered = df[df["Status"] == option]
    st.dataframe(filtered)

# --- STREAMLIT NAVIGATION ---
menu = ["Home", "Search Books", "Update Status", "Add Book", "Filter by Status"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Home":
    home()
elif choice == "Search Books":
    st.subheader("🔍 Search Books")
    query = st.text_input("Search by title, author, or ISBN")
    if query:
        result = search_books(query)
        st.dataframe(result if not result.empty else pd.DataFrame([{"Message": "No results found"}]))
elif choice == "Update Status":
    update_status()
elif choice == "Add Book":
    add_book()
elif choice == "Filter by Status":
    filter_books()

