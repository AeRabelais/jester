import streamlit as st

# Function to display the applicant info table
def display_applicants():
    st.subheader("Applicant Table")
    # Example data - you might replace this with a call to your database
    applicant_data = {
        "Name": ["John Doe", "Jane Smith", "Alice Johnson"],
        "Position Applied": ["Software Engineer", "Data Analyst", "Product Manager"],
        "Status": ["Reviewed", "Pending", "Interview"]
    }
    st.write(applicant_data)

# Function to edit outreach templates
def edit_templates():
    st.subheader("Edit Outreach Templates")
    template = st.text_area("Edit your email template here:", "Hello [Name],\nThank you for applying to [Position]. We would...")
    if st.button("Save Template"):
        st.success("Template saved successfully!")

# Function to manage hiring roles
def manage_roles():
    st.subheader("Role Management")
    with st.form(key='role_form'):
        role_name = st.text_input("Role Name")
        description = st.text_area("Role Description")
        submit_button = st.form_submit_button("Submit")
        if submit_button:
            st.success(f"Role '{role_name}' updated successfully!")

def main():
    st.sidebar.title("Jester")

    JESTER_LOGO = "/Users/ae_rabelais/Documents/jester/assets/jester_logo.jpg"
    st.logo(JESTER_LOGO) #    st.logo(JESTER_LOGO, icon_image=main_body_logo)

    admin_name = st.sidebar.selectbox("Select Admin", ["Ashia", "Michael", "Tiffany"])
    
    st.sidebar.write(f"Logged in as: {admin_name}")
    
    # Navigation
    page = st.sidebar.radio("Go to", ("Applicant Info", "Edit Templates", "Manage Roles"))
    
    if page == "Applicant Info":
        display_applicants()
    elif page == "Edit Templates":
        edit_templates()
    elif page == "Manage Roles":
        manage_roles()

if __name__ == "__main__":
    main()
