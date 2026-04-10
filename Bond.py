import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

st.set_page_config(page_title="Bond Interest Calculator", layout="wide")

st.title("📊 Bond Interest & Coupon Schedule Calculator")

# Function to generate coupon schedule
def generate_coupon_schedule(face_value, coupon_rate, issue_date, maturity_date, frequency):
    periods_per_year = {
        "Annual": 1,
        "Semi-Annual": 2,
        "Quarterly": 4,
        "Monthly": 12
    }

    n = periods_per_year[frequency]
    coupon_payment = (face_value * coupon_rate) / n

    schedule = []
    current_date = issue_date
    total_interest = 0

    while current_date < maturity_date:
        current_date += relativedelta(months=int(12 / n))
        if current_date > maturity_date:
            current_date = maturity_date

        schedule.append({
            "Payment Date": current_date,
            "Coupon Payment": round(coupon_payment, 2)
        })

        total_interest += coupon_payment

        if current_date == maturity_date:
            break

    df = pd.DataFrame(schedule)
    return df, round(total_interest, 2), round(coupon_payment, 2)

# Sidebar inputs
st.sidebar.header("➕ Add Bond Details")

bond_name = st.sidebar.text_input("Bond Name", "Bond A")
face_value = st.sidebar.number_input("Face Value", value=1000.0)
coupon_rate = st.sidebar.number_input("Coupon Rate (%)", value=5.0) / 100

issue_date = st.sidebar.date_input("Issue Date", datetime.today())
maturity_date = st.sidebar.date_input("Maturity Date", datetime(2030, 1, 1))

frequency = st.sidebar.selectbox(
    "Payment Frequency",
    ["Annual", "Semi-Annual", "Quarterly", "Monthly"]
)

if "bonds" not in st.session_state:
    st.session_state.bonds = []

if st.sidebar.button("Add Bond"):
    st.session_state.bonds.append({
        "name": bond_name,
        "face_value": face_value,
        "coupon_rate": coupon_rate,
        "issue_date": issue_date,
        "maturity_date": maturity_date,
        "frequency": frequency
    })

# Display bonds
if st.session_state.bonds:
    for i, bond in enumerate(st.session_state.bonds):
        st.subheader(f"📌 {bond['name']}")

        schedule_df, total_interest, coupon_payment = generate_coupon_schedule(
            bond["face_value"],
            bond["coupon_rate"],
            bond["issue_date"],
            bond["maturity_date"],
            bond["frequency"]
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Coupon Payment", f"{coupon_payment}")
        col2.metric("Total Expected Interest", f"{total_interest}")
        col3.metric("Payments Count", len(schedule_df))

        st.dataframe(schedule_df, use_container_width=True)

        # Download CSV
        csv = schedule_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Schedule",
            data=csv,
            file_name=f"{bond['name']}_schedule.csv",
            mime='text/csv'
        )

        st.divider()
else:
    st.info("👈 Add a bond from the sidebar to begin.")
