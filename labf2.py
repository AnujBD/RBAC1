import streamlit as st
import pandas as pd

# --- STREAMLIT CONFIG ---
st.set_page_config(
    page_title="RBAC Accelerator | Boolean Data Systems",
    page_icon="boolean logo.jpg",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CSS Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Montserrat', sans-serif !important; }
.stApp { background: linear-gradient(120deg, #f5f7fa 0%, #c3cfe2 100%) fixed; }

/* Role Badge */
.role-badge {
    display:inline-block; padding:5px 16px; font-size:15px;
    background: linear-gradient(90deg,#27488f,#2394ec);
    color: white; border-radius:18px; font-weight:600;
    margin-left:6px; letter-spacing:0.7px;
    font-family: Montserrat, sans-serif;
    box-shadow: 0 1px 5px #1A386B33;
}

/* Gradient Buttons */
.stButton > button {
    border-radius: 8px !important;
    background: linear-gradient(90deg,#27488f,#2394ec) !important;
    color: white !important;
    font-weight: 600;
    font-family: Montserrat, sans-serif;
    border: none;
    margin: 2px 0;
    transition: background 0.15s;
}
.stButton > button:hover {
    background: linear-gradient(90deg,#2394ec,#27488f) !important;
}
.stButton > button[disabled] {
    background: #AAC7FF !important;
    color: #eaf4ff !important;
}

/* Tags */
.data-tags span {
    background: #E6EEF5; color: #004A77; margin-right:5px; padding: 2px 10px;
    font-size:13px; border-radius:12px; font-weight:500; display:inline-block;
}

/* DataFrame Box */
.stDataFrame { background: white !important; border-radius:8px !important; }

/* Sidebar Styling */
.sidebar-img { width:110px; margin-bottom:12px; border-radius:50%; box-shadow:0 2px 6px rgba(0,0,0,0.05);}
.stSidebar { background: #f4f6f8 !important;}
.sidebar-title {font-size: 22px; font-weight:700; color:#004A77; letter-spacing:0.5px;}
.access-inbox { background:#f9f9fb; border-radius:10px; padding:15px 20px; margin:10px 0; }

hr { border:0; height:1px; background: #d8e0ea; margin:20px 0; }
</style>
""", unsafe_allow_html=True)

# --- IMAGE PATHS ---
BANNER_PATH = "Boolean Cover Photo.png"
LOGO_PATH = "boolean logo.jpg"
boo = "Boolean Full photo image.png"

# --- SESSION STATE INIT ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# --- USERS & ROLES ---
USERS_CREDS = {
    "Anuj": "admin@1",
    "Srihitha": "hr@1",
    "Siddharth": "fin@1",
    "Dara": "pub@1",
}
ROLES = ["Admin", "HR", "Finance", "Public"]
ADMIN_USER = "Anuj"
USERS = {
    "Anuj": {"Admin"},
    "Srihitha": {"HR"},
    "Siddharth": {"Finance"},
    "Dara": {"Public"},
}

# --- TABLE DATA ---
df_tables = {
    "HR data": pd.DataFrame([
        [101, "Arjun Rao", "HR data", "Recruiter", "2020-03-01"],
        [102, "Mira Jain", "HR data", "Manager", "2018-07-14"],
        [103, "Tanu Gupta", "HR data", "Analyst", "2019-02-22"],
        [104, "Adil Khan", "HR data", "Executive", "2022-01-12"],
        [105, "Ruhi Saini", "HR data", "Recruiter", "2021-09-10"],
    ], columns=["Employee ID", "Name", "Department", "Position", "Join Date"]),
    "User Salary": pd.DataFrame([
        [101, "Arjun Rao", 70000],
        [102, "Mira Jain", 85000],
        [103, "Tanu Gupta", 60000],
        [104, "Adil Khan", 55000],
        [105, "Ruhi Saini", 65000],
    ], columns=["Employee ID", "Name", "Annual Salary"]),
    "Finance Data": pd.DataFrame([
        ["F201", "Rohit Sharma", "Finance", "Accountant", "2020-01-10"],
        ["F202", "Tina Dey", "Finance", "Analyst", "2020-05-17"],
        ["F203", "John Mathew", "Finance", "Treasurer", "2021-06-30"],
        ["F204", "Simran Chawla", "Finance", "Finance Mgr.", "2019-09-05"],
        ["F205", "Alok Naik", "Finance", "Controller", "2018-03-22"],
    ], columns=["Finance ID", "Name", "Department", "Designation", "Join Date"]),
    "Financial Reports": pd.DataFrame([
        ["Q1", 500000, 400000, 100000],
        ["Q2", 550000, 420000, 130000],
        ["Q3", 600000, 450000, 150000],
        ["Q4", 620000, 460000, 160000],
        ["Year", 2270000, 1730000, 540000],
    ], columns=["Period", "Revenue", "Expense", "Profit"]),
    "Admin Data": pd.DataFrame([
        ["A301", "Suresh Panth", "Admin", "Head", "2017-10-09"],
        ["A302", "Meena Paul", "Admin", "Coordinator", "2019-11-22"],
        ["A303", "Farhan Naik", "Admin", "Supervisor", "2021-03-10"],
        ["A304", "Shiv Rathi", "Admin", "Officer", "2022-09-24"],
        ["A305", "Sara Dutta", "Admin", "Junior Admin", "2020-06-01"],
    ], columns=["Admin ID", "Name", "Department", "Title", "Join Date"]),
    "Admin Logs": pd.DataFrame([
        ["2024-08-01", "User Anuj updated role permissions."],
        ["2024-08-02", "User Dara requested access to Finance Data."],
        ["2024-08-03", "Access request approved for Srihitha on User Salary."],
        ["2024-08-04", "User Siddharth revoked Finance Report access for Dara."],
        ["2024-08-05", "Password updated for user Srihitha."],
    ], columns=["Date", "Activity"]),
    "Public Data": pd.DataFrame([
        ["P001", "Karan G.", "Mumbai", "Student", "2024-06-12"],
        ["P002", "Rupa S.", "Bengaluru", "Teacher", "2023-12-23"],
        ["P003", "Aman L.", "Pune", "Engineer", "2025-01-19"],
        ["P004", "Sneha P.", "Hyderabad", "Designer", "2023-09-10"],
        ["P005", "Devansh R.", "Kolkata", "Executive", "2024-10-02"],
    ], columns=["ID", "Name", "City", "Occupation", "Joined"]),
    "Public Events": pd.DataFrame([
        ["2024-08-10", "Community meetup", "Mumbai"],
        ["2024-09-15", "Charity run", "Bengaluru"],
        ["2024-10-01", "Tech conference", "Pune"],
        ["2024-11-05", "Art exhibition", "Hyderabad"],
        ["2024-12-12", "Book fair", "Kolkata"],
    ], columns=["Date", "Event", "Location"]),
}

TABLES = list(df_tables.keys())
DEFAULT_ROLE_PERMS = {
    "Admin": TABLES,
    "HR": ["HR data", "User Salary"],
    "Finance": ["Finance Data", "Financial Reports"],
    "Public": ["Public Data", "Public Events"],
}
AVAILABLE_TAGS = ["PII", "Confidential", "Public", "Financial", "HR"]

# --- SESSION STATE for app data ---
if "role_permissions" not in st.session_state:
    st.session_state.role_permissions = {role: set(tabs) for role, tabs in DEFAULT_ROLE_PERMS.items()}
if "access_requests" not in st.session_state:
    st.session_state.access_requests = []
if "user_roles" not in st.session_state:
    st.session_state.user_roles = {user: set(roles) for user, roles in USERS.items()}
if "show_table" not in st.session_state:
    st.session_state.show_table = None
if "table_tags" not in st.session_state:
    st.session_state.table_tags = {
        "HR data": {"PII", "Confidential"},
        "User Salary": {"Confidential"},
        "Finance Data": {"Financial", "Confidential"},
        "Financial Reports": {"Financial"},
        "Admin Data": {"Confidential"},
        "Admin Logs": {"Confidential"},
        "Public Data": {"Public"},
        "Public Events": {"Public"},
    }

# --- Helper Functions ---
def get_role_for_table(table):
    if table in ["HR data", "User Salary"]:
        return "HR"
    elif table in ["Finance Data", "Financial Reports"]:
        return "Finance"
    elif table in ["Admin Data", "Admin Logs"]:
        return "Admin"
    elif table in ["Public Data", "Public Events"]:
        return "Public"
    return "Public"

def is_admin_table(table):
    return table in ["Admin Data", "Admin Logs"]

def table_has_tags(table, selected_tags):
    return not selected_tags or any(t in st.session_state.table_tags.get(table, set()) for t in selected_tags)

# --- LOGIN PAGE ---
if not st.session_state.logged_in:
    st.image(boo)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS_CREDS and USERS_CREDS[username] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("Login successful. Welcome!")
            st.rerun()
        else:
            st.error("Invalid username or password. Try again.")
    st.stop()

# --- SIDEBAR (only after login) ---
with st.sidebar:
    st.image(LOGO_PATH, use_container_width=False, width=110)
    st.markdown('<div class="sidebar-title">BOOLEAN<br>DATA SYSTEMS</div>', unsafe_allow_html=True)
    st.markdown("---")

# --- MAIN DASHBOARD ---
st.image(BANNER_PATH, use_container_width=True)
current_user = st.session_state.current_user

# Impersonation for Admin
if current_user == ADMIN_USER:
    user = st.sidebar.selectbox(
        "🔎 Impersonate User",
        list(st.session_state.user_roles.keys()),
        index=list(st.session_state.user_roles.keys()).index(current_user),
    )
else:
    user = current_user

user_roles = st.session_state.user_roles[user]
st.success(f"Welcome, **{user}**!", icon="✅")

st.sidebar.header("🔖 Filter Tables by Tags")
selected_tags = st.sidebar.multiselect("Select Tags", AVAILABLE_TAGS)

# Filter and permissions
filtered_tables = [
    t for t in TABLES
    if table_has_tags(t, selected_tags) and (("Admin" in user_roles) or not is_admin_table(t))
]
allowed_tables = set()
for role in user_roles:
    allowed_tables |= st.session_state.role_permissions.get(role, set())

st.write("---")
st.header("📊 Available Data Tables")
for table in filtered_tables:
    tags = st.session_state.table_tags.get(table, set())
    tags_spans = ''.join([f"<span>{t}</span>" for t in sorted(tags)]) if tags else "<i>No tags</i>"
    c1, c2, c3 = st.columns([3,1,2])
    c1.markdown(f"**{table}**")
    c3.markdown(f'<div class="data-tags">{tags_spans}</div>', unsafe_allow_html=True)
    if table in allowed_tables:
        if c2.button("View Table", key=f"view_{table}_{user}"):
            st.session_state.show_table = table
    else:
        if "Admin" not in user_roles:
            if (user, table) in st.session_state.access_requests:
                c2.button("Request Sent", disabled=True, key=f"req_{table}_{user}")
            else:
                if c2.button("Request Access", key=f"req_{table}_{user}"):
                    st.session_state.access_requests.append((user, table))
                    st.rerun()

st.write("---")

# Show Data Table
if st.session_state.show_table:
    tbl = st.session_state.show_table
    if tbl in allowed_tables:
        st.subheader(f"{tbl} Table")
        st.dataframe(df_tables[tbl], use_container_width=True, hide_index=True)
    else:
        st.warning("You do not have permission to view this table.")

# Admin Controls
if user == ADMIN_USER:
    st.write("---")
    st.header("🔔 Access Requests Inbox")
    if st.session_state.access_requests:
        for req_user, req_table in list(st.session_state.access_requests):
            target_role = get_role_for_table(req_table)
            c1, c2, c3 = st.columns([3, 1, 1])
            info = (f"<span style='font-weight:500;color:#234;'>User <b>{req_user}</b> "
                    f"(Roles: <b>{', '.join(sorted(st.session_state.user_roles[req_user]))}</b>) "
                    f"requests <b>{req_table}</b> (adds role: <b>{target_role}</b>)</span>")
            c1.markdown(info, unsafe_allow_html=True)
            if c2.button("Approve", key=f"approve_{req_user}_{req_table}"):
                st.session_state.role_permissions[target_role].add(req_table)
                st.session_state.user_roles[req_user].add(target_role)
                st.session_state.access_requests.remove((req_user, req_table))
                st.rerun()
            if c3.button("Deny", key=f"deny_{req_user}_{req_table}"):
                st.session_state.access_requests.remove((req_user, req_table))
                st.rerun()
    else:
        st.info("No pending access requests.")

    # --- NEW FEATURE: Direct Role Access Assignment ---
    st.write("---")
    st.header("⚡ Direct Role Access Assignment")
    target_user = st.selectbox(
        "Select User",
        [u for u in st.session_state.user_roles if u != ADMIN_USER]
    )
    target_table = st.selectbox(
        "Select Table",
        TABLES
    )
    if st.button("Grant Access"):
        target_role = get_role_for_table(target_table)
        if target_role not in st.session_state.user_roles[target_user]:
            st.session_state.user_roles[target_user].add(target_role)
            st.success(f"✅ Role '{target_role}' added to user '{target_user}'")
        if target_table not in st.session_state.role_permissions[target_role]:
            st.session_state.role_permissions[target_role].add(target_table)
            st.success(f"✅ Table '{target_table}' added to role '{target_role}' permissions")
        st.rerun()

    st.write("---")
    st.header("👥 Roles & Assigned Users")
    for role in ROLES:
        members = [u for u, roles in st.session_state.user_roles.items() if role in roles]
        st.markdown(f"<b>{role}:</b> {', '.join(members) if members else '_None_'}", unsafe_allow_html=True)

    st.write("---")
    st.header("🔒 Manage Role Permissions")
    for role in ROLES:
        if role == "Admin":
            continue
        st.subheader(role)
        for tab in list(st.session_state.role_permissions[role]):
            c1, c2 = st.columns([3, 1])
            c1.write(f"Access to table: **{tab}**")
            if c2.button("Revoke", key=f"revoke_{role}_{tab}"):
                st.session_state.role_permissions[role].remove(tab)
                st.rerun()

    st.write("---")
    st.header("🏷️ Table Tag Management")
    for table in TABLES:
        if not ("Admin" in user_roles or not is_admin_table(table)):
            continue
        st.subheader(table)
        current_tags = st.session_state.table_tags.get(table, set())
        c1, c2 = st.columns([3,2])
        with c1:
            if current_tags:
                for tag in sorted(current_tags):
                    if st.button(f"Remove {tag}", key=f"remove_tag_{table}_{tag}"):
                        current_tags.remove(tag)
                        st.session_state.table_tags[table] = current_tags
                        st.rerun()
            else:
                st.markdown("_No tags assigned_")
        with c2:
            available_to_add = [t for t in AVAILABLE_TAGS if t not in current_tags]
            new_tag = st.selectbox(f"Add tag to {table}", [""] + available_to_add, key=f"add_tag_{table}")
            if new_tag:
                current_tags.add(new_tag)
                st.session_state.table_tags[table] = current_tags
                st.rerun()

# Logout
st.sidebar.markdown("---")
if st.sidebar.button("Log out", key="logout-btn"):
    for k in ("logged_in", "current_user", "show_table"):
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

st.sidebar.markdown("""
<p style='text-align:center;font-size:12px;color:#789;'>© Boolean Data Systems Inc.<br>
</p>""", unsafe_allow_html=True)
