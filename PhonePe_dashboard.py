import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# -- App Config
st.set_page_config(
    layout="wide",
    page_title="PhonePe Data Dashboard",
    page_icon=":chart_with_upwards_trend:"
)

# -- Custom Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
            
        * {
            font-family: 'Poppins', sans-serif !important;
        }
        
        [data-testid="stHeader"],
        [data-testid="stSidebarCollapsedControl"], 
        [data-testid="stSidebarCollapseButton"], 
        [data-testid="stHeaderActionElements"] { 
            display: none !important; 
        }
        .stMainBlockContainer {
            padding: 1rem 1rem 3rem;
            padding-left: 5rem;
        }
        .scroll-box::-webkit-scrollbar {
            display: none;
        }
        .scroll-box {
            overflow-y: auto;
            max-height: 70vh;
        }
    </style>
""", unsafe_allow_html=True)

# -- Session State Init
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'category' not in st.session_state:
    st.session_state.category = None
if 'subcategory' not in st.session_state:
    st.session_state.subcategory = "Aggregated"
if 'view' not in st.session_state:
    st.session_state.view = "Country"

# -- Callback
def update_category():
    cat = st.session_state["category_select"]
    st.session_state.category = None if cat == "Home" else cat
    if cat == "Home":
        st.session_state.page = "home"
    else:
        st.session_state.page = f"{cat.lower()}_{st.session_state.subcategory.lower()}"
    st.session_state.view = "Country"


# Insurance:

# -- Insurance Aggregated Country Chart
def insurance_aggregated_country_chart():
    df1 = pd.read_csv("dataset/insurance/aggregated_insurance_country.csv")
    df1['from_date'] = pd.to_datetime(df1['from_date'], errors='coerce')  
    with st.container(height=520,border=False):
        # --- Chart 1: Line Chart
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Insurance Amount Over Time (Country Level)")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(df1['from_date'], df1['amount'], marker='o', color='cyan')
            ax.set_xlabel("From Date")
            plt.setp(ax.get_xticklabels(), rotation=90)
            ax.set_ylabel("Amount")
            ax.set_title("Insurance Purchase Trends (Time Series)")
            ax.grid()
            st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.subheader("Insights Summary")
            st.markdown("""
            - Shows **total insurance amount** bought across India from 2020–2024.
            - Steady growth implies increasing trust in PhonePe’s insurance offerings.
            - Peaks often align with campaign periods or year-end pushes.
            """)

        # --- Chart 2: Bar Chart (Average Amount per Transaction by Year)
        df1['average_transaction_amount'] = df1['amount'] / df1['count']
        df1['year'] = df1['from_date'].dt.year
        yearly_avg = df1.groupby('year')['average_transaction_amount'].mean().reset_index()
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Avg Amount per Insurance Transaction by Year")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(yearly_avg['year'], yearly_avg['average_transaction_amount'], color='green')
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Avg Amount per Transaction")
            ax2.set_title("Average Insurance Transaction Value (Year-wise)")
            ax2.grid(axis='y')
            st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
            st.pyplot(fig2)
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            st.subheader("Insights: Average Amount per Transaction")
            st.markdown("""
            * Shows the **average insurance transaction value** from 2020 to 2024.
            * It increased steadily from just below ₹400 to nearly ₹1600.
            * Indicates growing **user trust** and **larger policies** being bought.
            """)

# -- Insurance Aggregated State Chart
def insurance_aggregated_state_chart():
    df2 = pd.read_csv("dataset/insurance/aggregated_insurance_state.csv")

    with st.container(height=520, border=False):
        # --- Chart 1: Total Amount by State
        state_total_amount = df2.groupby('state')['amount'].mean().reset_index()

        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Total Insurance Transaction Amount (State Level)")
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.bar(state_total_amount['state'], state_total_amount['amount'], color='green')
            ax.set_xlabel("State")
            ax.set_ylabel("Total Amount (₹)")
            ax.set_title("State-wise Insurance Amount Distribution")
            plt.setp(ax.get_xticklabels(), rotation=90)
            ax.grid(axis='y')
            st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.subheader("Insights: Amount by State")
            st.markdown("""
            - **Karnataka** and **Maharashtra** had the highest average insurance amounts.
            - Indicates a preference for **larger insurance plans** in these regions.
            - **Ladakh**, **Mizoram**, and **Nagaland** saw minimal usage comparatively.
            """)

        # --- Chart 2: Total Count by State
        state_total_count = df2.groupby('state')['count'].mean().reset_index()

        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Total Number of Insurance Transactions by State (2020–2024)")
            fig2, ax2 = plt.subplots(figsize=(12, 5))
            ax2.bar(state_total_count['state'], state_total_count['count'], color='orange')
            ax2.set_xlabel("State")
            ax2.set_ylabel("Total Transaction Count")
            ax2.set_title("State-wise Insurance Transaction Count")
            plt.setp(ax2.get_xticklabels(), rotation=90)
            ax2.grid(axis='y')
            st.markdown('<div class="scroll-box">', unsafe_allow_html=True)
            st.pyplot(fig2)
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            st.subheader("Insights: Transaction Count by State")
            st.markdown("""
            - **Karnataka** and **Maharashtra** again lead with the **most transactions**.
            - Shows higher **user adoption** in these states.
            - **Tamil Nadu** and **Uttar Pradesh** show moderate use.
            - **Ladakh** and **Sikkim** saw **very limited activity**.
            """)
    
# -- Insurance Map Country Chart
def insurance_map_country_chart():
    import pandas as pd
    df3 = pd.read_csv("dataset/insurance/map_insurance_hover_country.csv")
    df3['year'] = df3['year'].astype(str)

    idx_max = df3.groupby('year')['amount'].idxmax()
    top_states = df3.loc[idx_max].reset_index(drop=True)

    idx_min = df3.groupby('year')['amount'].idxmin()
    bottom_states = df3.loc[idx_min].reset_index(drop=True)

    with st.container(height=500, border=False):
        # --- Chart 1: Highest Insurance Amount by Year
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Highest Insurance Amount by Year")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(top_states['year'], top_states['amount'], color='green')
            for i, (state, amount) in enumerate(zip(top_states['state'], top_states['amount'])):
                ax1.text(i, amount, state, ha='center', va='bottom', fontsize=10)
            ax1.set_xlabel("Year")
            ax1.set_ylabel("Amount (₹)")
            ax1.set_title("Top State by Insurance Amount Each Year")
            ax1.grid(axis='y')
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: Highest Amount")
            st.markdown("""
            - **Karnataka** and **Maharashtra** led in total insurance amount.
            - **Karnataka** started rising in 2022 and **overtook Maharashtra** in the later years.
            """)

        # --- Chart 2: Lowest Insurance Amount by Year
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Lowest Insurance Amount by Year")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(bottom_states['year'], bottom_states['amount'], color='red')
            for i, (state, amount) in enumerate(zip(bottom_states['state'], bottom_states['amount'])):
                ax2.text(i, amount, state, ha='center', va='bottom', fontsize=10)
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Amount (₹)")
            ax2.set_title("Bottom State by Insurance Amount Each Year")
            ax2.grid(axis='y')
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Lowest Amount")
            st.markdown("""
            - **Lakshadweep** had the lowest insurance amount every year from 2020 to 2024.
            - It peaked in **2022** just above ₹25K and stayed **low afterward**.
            """)

# -- Insurance Map State Chart
def insurance_map_state_chart():
    import pandas as pd
    df4 = pd.read_csv("dataset/insurance/map_insurance_hover_state.csv")
    df4['year'] = df4['year'].astype(str)

    # --- Highest Amount District
    year_district_amount = df4.groupby(['year', 'district'])['amount'].sum().reset_index()
    idx_max = year_district_amount.groupby('year')['amount'].idxmax()
    top_districts = year_district_amount.loc[idx_max].reset_index(drop=True)

    # --- Lowest Amount District
    idx_min = year_district_amount.groupby('year')['amount'].idxmin()
    bottom_districts = year_district_amount.loc[idx_min].reset_index(drop=True)

    with st.container(height=500, border=False):
        # --- Chart 1: Highest District by Year
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("District with Highest Insurance Amount by Year")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(top_districts['year'], top_districts['amount'], color='blue')
            for i, (district, amount) in enumerate(zip(top_districts['district'], top_districts['amount'])):
                ax1.text(i, amount, district, ha='center', va='bottom', fontsize=10)
            ax1.set_xlabel("Year")
            ax1.set_ylabel("Amount (₹)")
            ax1.set_title("Top District by Insurance Amount Each Year")
            ax1.grid(axis='y')
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: Highest Amount")
            st.markdown("""
            - **Bengaluru Urban** consistently ranked **#1** for insurance amount every year.
            - It’s the **most dominant district** in insurance usage on PhonePe from 2020–2024.
            """)

        # --- Chart 2: Lowest District by Year
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("District with Lowest Insurance Amount by Year")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(bottom_districts['year'], bottom_districts['amount'], color='blue')
            for i, (district, amount) in enumerate(zip(bottom_districts['district'], bottom_districts['amount'])):
                ax2.text(i, amount, district, ha='center', va='bottom', fontsize=10)
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Amount (₹)")
            ax2.set_title("Bottom District by Insurance Amount Each Year")
            ax2.grid(axis='y')
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Lowest Amount")
            st.markdown("""
            - **Pherzawl district** appears most often as the **lowest**.
            - **Shi Yomi** peaked briefly in **2022** among the bottom districts.
            - The **lowest values peaked in 2022**, then declined again.
            """)

# -- Insurance Top Country Chart
def insurance_top_country_chart():
    import pandas as pd
    df5 = pd.read_csv("dataset/insurance/top_insurance_country.csv")

    # Chart Data
    top_states = df5[df5['level'] == 'state']
    top_districts = df5[df5['level'] == 'district']

    with st.container(height=520, border=False):
        # --- Chart 1: Top States
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Top States by Total Insurance Amount")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(top_states['entity_name'], top_states['amount'], color='green')
            ax1.set_xlabel("State")
            ax1.set_ylabel("Amount (₹)")
            ax1.set_title("Total Insurance Amount by State")
            ax1.grid(axis='y')
            plt.setp(ax1.get_xticklabels(), rotation=45)
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: State-Level")
            st.markdown("""
            - **Karnataka** & **Maharashtra** have nearly equal insurance amounts.
            - **UP** & **Tamil Nadu** are mid-range performers.
            - **Odisha** & **Madhya Pradesh** rank lowest in top 10 states.
            """)

        # --- Chart 2: Top Districts
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Top Districts by Total Insurance Amount")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(top_districts['entity_name'], top_districts['amount'], color='blue')
            ax2.set_xlabel("District")
            ax2.set_ylabel("Amount (₹)")
            ax2.set_title("Total Insurance Amount by District")
            ax2.grid(axis='y')
            plt.setp(ax2.get_xticklabels(), rotation=90)
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: District-Level")
            st.markdown("""
            - **Bengaluru Urban** clearly leads with a massive margin.
            - **Pune** is second but has less than half the value.
            - Other districts are closely clustered with smaller values.
            """)


# Transaction:

# -- Transaction Aggregated Country Chart
def transaction_aggregated_country_chart():
    df1 = pd.read_csv("dataset/transaction/aggregated_transaction_country.csv")

    # Prepare chart data
    transaction_total_amount = df1.groupby('transaction_name')['amount'].sum().reset_index()
    transaction_total_count = df1.groupby('transaction_name')['count'].sum().reset_index()

    with st.container(height=520, border=False):
        # --- Chart 1: Amount by Transaction Type
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Total Amount by Transaction Type")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(transaction_total_amount['transaction_name'], transaction_total_amount['amount'], color='green')
            ax1.set_title("Total Transaction Amount by Type (2020–2024)")
            ax1.set_xlabel("Transaction Type")
            ax1.set_ylabel("Total Amount (₹)")
            ax1.grid(axis='y')
            plt.setp(ax1.get_xticklabels(), rotation=45)
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: Amount")
            st.markdown("""
            - **Peer-to-peer payments** lead in terms of total transferred amount.
            - **Merchant payments** are less than half of peer-to-peer.
            - Indicates people transfer **more money to individuals** than to merchants.
            """)

        # --- Chart 2: Count by Transaction Type
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Total Count by Transaction Type")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(transaction_total_count['transaction_name'], transaction_total_count['count'], color='orange')
            ax2.set_title("Total Transaction Count by Type (2018–2024)")
            ax2.set_xlabel("Transaction Type")
            ax2.set_ylabel("Transaction Count")
            ax2.grid(axis='y')
            plt.setp(ax2.get_xticklabels(), rotation=45)
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Count")
            st.markdown("""
            - **Merchant payments** occur much more frequently than peer-to-peer.
            - However, they involve **smaller amounts per transaction**.
            - Shows **UPI merchant payments adoption** is widespread.
            """)

# -- Transaction Aggregated State Chart
def transaction_aggregated_state_chart():
    df2 = pd.read_csv("dataset/transaction/aggregated_transaction_state.csv")

    state_total_amount = df2.groupby('state')['amount'].mean().reset_index()
    state_total_count = df2.groupby('state')['count'].mean().reset_index()

    with st.container(height=520, border=False):
        # --- Chart 1: Total Amount by State
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Total Transaction Amount by State")
            fig1, ax1 = plt.subplots(figsize=(14, 6))
            ax1.bar(state_total_amount['state'], state_total_amount['amount'], color='teal')
            ax1.set_title("State-wise Average Transaction Amount (2020–2024)")
            ax1.set_xlabel("State")
            ax1.set_ylabel("Amount (₹)")
            ax1.grid(axis='y')
            plt.setp(ax1.get_xticklabels(), rotation=90)
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: Transaction Amount")
            st.markdown("""
            - **Telangana** & **Andhra Pradesh** top the chart in average transaction amount.
            - These states performed **low in insurance**, revealing spending priority differences.
            - **Maharashtra** and **Karnataka** stayed high in both transactions and insurance.
            - **Kerala** performed well in insurance but **low in transactions**.
            """)

        # --- Chart 2: Total Count by State
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Total Transaction Count by State")
            fig2, ax2 = plt.subplots(figsize=(14, 6))
            ax2.bar(state_total_count['state'], state_total_count['count'], color='orange')
            ax2.set_title("State-wise Average Transaction Count (2020–2024)")
            ax2.set_xlabel("State")
            ax2.set_ylabel("Transaction Count")
            ax2.grid(axis='y')
            plt.setp(ax2.get_xticklabels(), rotation=90)
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Transaction Count")
            st.markdown("""
            - **Maharashtra** and **Karnataka** lead in total number of transactions.
            - **Telangana** and **AP** follow closely with both high count and amount.
            - Smaller states have visibly lower usage on PhonePe for transactions.
            """)

# -- Transaction Map Country Chart
def transaction_map_country_chart():
    df3 = pd.read_csv("dataset/transaction/map_transaction_country.csv")
    df3['year'] = df3['year'].astype(str)

    # Chart 1: Highest Amount by State
    idx_max_amt = df3.groupby('year')['amount'].idxmax()
    top_states_amt = df3.loc[idx_max_amt].reset_index(drop=True)

    # Chart 2: Highest Count by State
    idx_max_count = df3.groupby('year')['count'].idxmax()
    top_states_count = df3.loc[idx_max_count].reset_index(drop=True)

    with st.container(height=520, border=False):
        # --- Chart 1: Top Transaction Amount States
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("State with Highest Transaction Amount (Year-wise)")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(top_states_amt['year'], top_states_amt['amount'], color='green')
            for i, (state, amount) in enumerate(zip(top_states_amt['state'], top_states_amt['amount'])):
                ax1.text(i, amount, state, ha='center', va='bottom', fontsize=10)
            ax1.set_title("Top States by Transaction Amount")
            ax1.set_xlabel("Year")
            ax1.set_ylabel("Amount (₹)")
            ax1.grid(axis='y')
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: Transaction Amount")
            st.markdown("""
            - **Maharashtra** led initially (2018–2021).
            - **Telangana** peaked during 2020 and 2022.
            - **Karnataka** overtook all in 2023 and 2024.
            """)

        # --- Chart 2: Top Transaction Count States
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("State with Highest Transaction Count (Year-wise)")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(top_states_count['year'], top_states_count['count'], color='orange')
            for i, (state, count) in enumerate(zip(top_states_count['state'], top_states_count['count'])):
                ax2.text(i, count, state, ha='center', va='bottom', fontsize=10)
            ax2.set_title("Top States by Transaction Count")
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Transaction Count")
            ax2.grid(axis='y')
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Transaction Count")
            st.markdown("""
            - **Maharashtra** had the highest overall transaction count.
            - **Karnataka** overtook in value but not always in count.
            - **West Bengal** appeared in 2018, **Telangana** peaked in 2022.
            """)

# -- Transaction Map State Chart
def transaction_map_state_chart():
    df4 = pd.read_csv("dataset/transaction/map_transaction_state.csv")
    df4['year'] = df4['year'].astype(str)

    # Chart 1: Highest District by Amount
    idx_max_amt = df4.groupby('year')['amount'].idxmax()
    top_districts_amt = df4.loc[idx_max_amt].reset_index(drop=True)

    # Chart 2: Highest District by Count
    idx_max_count = df4.groupby('year')['count'].idxmax()
    top_districts_count = df4.loc[idx_max_count].reset_index(drop=True)

    with st.container(height=520, border=False):
        # --- Chart 1: Top Transaction Amount Districts
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("District with Highest Transaction Amount (Year-wise)")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(top_districts_amt['year'], top_districts_amt['amount'], color='green')
            for i, (district, amount) in enumerate(zip(top_districts_amt['district'], top_districts_amt['amount'])):
                ax1.text(i, amount, district, ha='center', va='bottom', fontsize=9)
            ax1.set_title("Top Districts by Transaction Amount")
            ax1.set_xlabel("Year")
            ax1.set_ylabel("Amount (₹)")
            ax1.grid(axis='y')
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: Transaction Amount")
            st.markdown("""
            - **Bengaluru Urban** held the highest transaction amount since 2018.
            - **Hyderabad** surpassed it only in **2022**, matching Bengaluru’s 2024 peak.
            """)

        # --- Chart 2: Top Transaction Count Districts
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("District with Highest Transaction Count (Year-wise)")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(top_districts_count['year'], top_districts_count['count'], color='orange')
            for i, (district, count) in enumerate(zip(top_districts_count['district'], top_districts_count['count'])):
                ax2.text(i, count, district, ha='center', va='bottom', fontsize=9)
            ax2.set_title("Top Districts by Transaction Count")
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Transaction Count")
            ax2.grid(axis='y')
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Transaction Count")
            st.markdown("""
            - **Bengaluru Urban** consistently led transaction count except in **2022**.
            - That year, **Hyderabad** briefly overtook before Bengaluru reclaimed the lead.
            """)

# -- Transaction Top Country Chart
def transaction_top_country_chart():
    df5 = pd.read_csv("dataset/transaction/top_transaction_country.csv")

    states = df5[df5['level'] == 'state']
    districts = df5[df5['level'] == 'district']
    pincodes = df5[df5['level'] == 'pincode']

    # --- Chart 1: Top States
    with st.container(height=520, border=False):
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Top States by Transaction Amount (2018)")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(states['entity'], states['amount'], color='green')
            ax1.set_xlabel("State")
            ax1.set_ylabel("Amount (₹)")
            ax1.set_title("Top Performing States")
            ax1.tick_params(axis='x', rotation=45)
            ax1.grid(axis='y')
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: States")
            st.markdown("""
            - **Maharashtra** and **Karnataka** are neck-and-neck at the top.
            - **Telangana** is just behind them.
            - **Delhi** and **Tamil Nadu** are at the bottom of this top list.
            """)

    # --- Chart 2: Top Districts
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Top Districts by Transaction Amount (2018)")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(districts['entity'], districts['amount'], color='blue')
            ax2.set_xlabel("District")
            ax2.set_ylabel("Amount (₹)")
            ax2.set_title("Top Performing Districts")
            ax2.tick_params(axis='x', rotation=90)
            ax2.grid(axis='y')
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Districts")
            st.markdown("""
            - **Bengaluru Urban** and **Hyderabad** dominate district-level transactions.
            - The rest don’t even reach **half** of their values.
            """)

    # --- Chart 3: Top Pincodes
        col5, col6 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col5:
            st.subheader("Top Pincodes by Transaction Amount (2018)")
            fig3, ax3 = plt.subplots(figsize=(10, 5))
            ax3.bar(pincodes['entity'].astype(str), pincodes['amount'], color='orange')
            ax3.set_xlabel("Pincode")
            ax3.set_ylabel("Amount (₹)")
            ax3.set_title("Top Performing Pincodes")
            ax3.tick_params(axis='x', rotation=90)
            ax3.grid(axis='y')
            st.pyplot(fig3)
        with col6:
            st.subheader("Insights: Pincodes")
            st.markdown("""
            - **500034** had the highest transaction total by far.
            - **500001** was second but not even half of 500034’s value.
            """)


# User:

# -- User Aggregated Country Chart
def user_aggregated_country_chart():
    df1 = pd.read_csv("dataset/user/aggregated_user_country.csv")
    df1['year'] = df1['year'].astype(str)

    # --- Chart 1: Total Registered Users by Year
    yearly_registers = df1[df1['brand'] == 'all'].groupby('year')['registered_users'].sum().reset_index()

    # --- Chart 2: Top Brand by Year
    brands_only = df1[df1['brand'] != 'all']
    idx = brands_only.groupby('year')['registered_users'].idxmax()
    top_brands = brands_only.loc[idx].reset_index(drop=True)

    with st.container(height=520, border=False):
        # --- Chart 1: Total Registered Users
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Total Registered Users by Year")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(yearly_registers['year'], yearly_registers['registered_users'], color='green')
            ax1.set_title("Total Registered Users (2018–2024)")
            ax1.set_xlabel("Year")
            ax1.set_ylabel("Registered Users")
            ax1.grid(axis='y')
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: Registration Growth")
            st.markdown("""
            - Registered users increased steadily from **2018** to **2024**.
            - Growth from **~8 lakh** in 2018 to over **586 million** by 2024.
            - Indicates massive nationwide PhonePe adoption over years.
            """)

        # --- Chart 2: Top Brand by Year
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Top Mobile Brand per Year")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(top_brands['year'], top_brands['registered_users'], color='teal')
            for i, (brand, users) in enumerate(zip(top_brands['brand'], top_brands['registered_users'])):
                ax2.text(i, users, brand, ha='center', va='bottom', fontsize=11)
            ax2.set_title("Top Brand by Registered Users")
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Registered Users")
            ax2.grid(axis='y')
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Top Brand Trend")
            st.markdown("""
            - **Xiaomi** consistently topped user registrations every year till **2022**.
            - No other brand appeared in top chart at country level during that time.
            - Brand data is **not available after 2022** in the dataset.
            """)

# -- User Aggregated State Chart
def user_aggregated_state_chart():
    df2 = pd.read_csv("dataset/user/aggregated_user_state.csv")

    brands_only = df2[df2['brand'] != 'all']
    state_brand_totals = brands_only.groupby(['state', 'brand'])['registered_users'].sum().reset_index()
    idx = state_brand_totals.groupby('state')['registered_users'].idxmax()
    top_brands = state_brand_totals.loc[idx].reset_index(drop=True)

    with st.container(height=520, border=False):
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Brand with Highest Registered Users per State")
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.bar(top_brands['state'], top_brands['registered_users'], color='orange')
            for i, (brand, users) in enumerate(zip(top_brands['brand'], top_brands['registered_users'])):
                ax.text(i, users, brand, ha='center', va='bottom', fontsize=8, rotation=90)
            ax.set_title("Brand with Highest Total Registered Users per State")
            ax.set_xlabel("State")
            ax.set_ylabel("Total Registered Users")
            ax.tick_params(axis='x', rotation=90)
            ax.grid(axis='y')
            plt.tight_layout()
            st.pyplot(fig)
        with col2:
            st.subheader("Insights")
            st.markdown("""
            - **Xiaomi** is the biggest brand in user registrations across India.
            - **Vivo** appears as the top brand in only **4 states**.
            - **Samsung** appears just **once**, in **Sikkim**.
            """)

# -- User Map Country Chart
def user_map_country_chart():
    df3 = pd.read_csv("dataset/user/map_user_country.csv")
    df3['year'] = df3['year'].astype(str)

    idx_max = df3.groupby('year')['registered_users'].idxmax()
    top_states = df3.loc[idx_max].reset_index(drop=True)

    idx_min = df3.groupby('year')['registered_users'].idxmin()
    bottom_states = df3.loc[idx_min].reset_index(drop=True)

    with st.container(height=520, border=False):
        # --- Top States
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Top States by Registered Users (Per Year)")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(top_states['year'], top_states['registered_users'], color='green')
            for i, (state, users) in enumerate(zip(top_states['state'], top_states['registered_users'])):
                ax1.text(i, users, state, ha='center', va='bottom', fontsize=11)
            ax1.set_title("State with Highest Registered Users")
            ax1.set_xlabel("Year")
            ax1.set_ylabel("Registered Users")
            ax1.grid(axis='y')
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: Highest Registration")
            st.markdown("""
            - **Maharashtra** consistently had the **highest registrations every year**.
            - Other major states didn’t appear even once in the top list.
            """)

        # --- Bottom States
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Bottom States by Registered Users (Per Year)")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(bottom_states['year'], bottom_states['registered_users'], color='green')
            for i, (state, users) in enumerate(zip(bottom_states['state'], bottom_states['registered_users'])):
                ax2.text(i, users, state, ha='center', va='bottom', fontsize=11)
            ax2.set_title("State with Lowest Registered Users")
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Registered Users")
            ax2.grid(axis='y')
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Lowest Registration")
            st.markdown("""
            - **Lakshadweep** was the **lowest every single year**.
            - No other states appeared in the bottom list.
            """)

# -- User Map State Chart
def user_map_state_chart():
    df4 = pd.read_csv("dataset/user/map_user_state.csv")
    df4['year'] = df4['year'].astype(str)

    idx_max = df4.groupby('year')['registered_users'].idxmax()
    top_districts = df4.loc[idx_max].reset_index(drop=True)

    idx_min = df4.groupby('year')['registered_users'].idxmin()
    bottom_districts = df4.loc[idx_min].reset_index(drop=True)

    with st.container(height=520, border=False):
        # --- Top Districts
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Top Districts by Registered Users (Per Year)")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(top_districts['year'], top_districts['registered_users'], color='green')
            for i, (district, users) in enumerate(zip(top_districts['district'], top_districts['registered_users'])):
                ax1.text(i, users, district, ha='center', va='bottom', fontsize=9)
            ax1.set_title("District with Highest Registered Users")
            ax1.set_xlabel("Year")
            ax1.set_ylabel("Registered Users")
            ax1.grid(axis='y')
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: Highest Districts")
            st.markdown("""
            - **Bengaluru Urban** has been the **consistent leader** since 2018.
            - No other district appeared in the top across all years.
            """)

        # --- Bottom Districts
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Bottom Districts by Registered Users (Per Year)")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(bottom_districts['year'], bottom_districts['registered_users'], color='green')
            for i, (district, users) in enumerate(zip(bottom_districts['district'], bottom_districts['registered_users'])):
                ax2.text(i, users, district, ha='center', va='bottom', fontsize=9)
            ax2.set_title("District with Lowest Registered Users")
            ax2.set_xlabel("Year")
            ax2.set_ylabel("Registered Users")
            ax2.grid(axis='y')
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Lowest Districts")
            st.markdown("""
            - **Muzaffarabad** occurred most often as the lowest.
            - **Kamle (2018)** and **Niuland (2024)** also had the **lowest values**.
            - All three had **similar user counts** despite different years.
            """)

# -- User Top Country Chart
def user_top_country_chart():
    df5 = pd.read_csv("dataset/user/top_user_country.csv")

    states = df5[df5['level'] == 'state']
    districts = df5[df5['level'] == 'district']
    pincodes = df5[df5['level'] == 'pincode']

    # --- Chart 1: Top States
    with st.container(height=520, border=False):
        col1, col2 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col1:
            st.subheader("Top States by Registered Users")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(states['name'], states['registered_users'], color='teal')
            ax1.set_title("Top States by Registered Users")
            ax1.set_xlabel("State")
            ax1.set_ylabel("Registered Users")
            ax1.tick_params(axis='x', rotation=45)
            ax1.grid(axis='y')
            st.pyplot(fig1)
        with col2:
            st.subheader("Insights: States")
            st.markdown("""
            - **Maharashtra** and **Uttar Pradesh** are the top contributors.
            - Surprisingly, **Karnataka** is not at the top this time.
            - The rest of the top states match national average distribution.
            """)

        # --- Chart 2: Top Districts
        col3, col4 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col3:
            st.subheader("Top Districts by Registered Users")
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            ax2.bar(districts['name'], districts['registered_users'], color='orange')
            ax2.set_title("Top Districts by Registered Users")
            ax2.set_xlabel("District")
            ax2.set_ylabel("Registered Users")
            ax2.tick_params(axis='x', rotation=90)
            ax2.grid(axis='y')
            st.pyplot(fig2)
        with col4:
            st.subheader("Insights: Districts")
            st.markdown("""
            - **Bengaluru Urban** leads by a significant margin.
            - **Pune** holds the second spot.
            - **Visakhapatnam** appears at the lowest end.
            - Others show similar mid-level performance.
            """)

        # --- Chart 3: Top Pincodes
        col5, col6 = st.columns([2, 1], gap="medium", vertical_alignment="center")
        with col5:
            st.subheader("Top Pincodes by Registered Users")
            fig3, ax3 = plt.subplots(figsize=(10, 5))
            ax3.bar(pincodes['name'], pincodes['registered_users'], color='purple')
            ax3.set_title("Top Pincodes by Registered Users")
            ax3.set_xlabel("Pincode")
            ax3.set_ylabel("Registered Users")
            ax3.tick_params(axis='x', rotation=90)
            ax3.grid(axis='y')
            st.pyplot(fig3)
        with col6:
            st.subheader("Insights: Pincodes")
            st.markdown("""
            - **201301** is the most registered pincode.
            - **560037**, **302012**, and **11085** are among the lowest.
            - **11086** seems just above average despite **11085** being low.
            """)

# -- Sidebar
def render_sidebar():
    with st.sidebar:
        st.title("Navigation")
        st.selectbox(
            "Select Page",
            ["Home", "Insurance", "Transaction", "User"],
            index=0 if not st.session_state.category else
            ["Insurance", "Transaction", "User"].index(st.session_state.category) + 1,
            key="category_select",
            on_change=update_category
        )

        category = st.session_state.get("category")
        if category == "Insurance":
            sub = st.radio("Insurance Subcategory", ["Aggregated", "Map", "Top"], key="ins_radio")
            st.session_state.page = f"insurance_{sub.lower()}"
            st.session_state.subcategory = sub
        elif category == "Transaction":
            sub = st.radio("Transaction Subcategory", ["Aggregated", "Map", "Top"], key="trans_radio")
            st.session_state.page = f"transaction_{sub.lower()}"
            st.session_state.subcategory = sub
        elif category == "User":
            sub = st.radio("User Subcategory", ["Aggregated", "Map", "Top"], key="user_radio")
            st.session_state.page = f"user_{sub.lower()}"
            st.session_state.subcategory = sub

# -- Home Page
def render_home():
    st.title("PhonePe Data Dashboard")

    st.markdown("""
    Welcome to the **PhonePe India Dashboard** — a visual exploration of PhonePe's digital journey across India from **2018 to 2024**.  
    Dive into data-driven insights that reflect how digital payments and insurance adoption have evolved across regions, users, and time.

    Whether you're a data enthusiast, analyst, or simply curious about how India transacts, this dashboard offers an intuitive way to explore trends that shaped the country’s digital finance landscape.

    The dashboard showcases three main categories:
    - 👥 **Users**: Growth trends, brand preferences, and user distribution across states and districts.
    - 💸 **Transactions**: Volume and value patterns by region, year, and category.
    - 🛡️ **Insurance**: Insurance adoption by location, including average premiums and transaction amounts.

    📂 All data was originally sourced from JSON folders and converted into structured CSVs for analysis.  
                
    📊 Visuals are categorized under **Aggregated**, **Map**, and **Top** sub-sections for both country and state levels.

    👉 Click **Get Started** to begin your interactive journey through India's evolving digital economy with PhonePe.
    """)

    if st.button("🚀 Get Started"):
        st.session_state.category = "Insurance"
        st.session_state.page = "insurance_aggregated"
        st.session_state.subcategory = "Aggregated"
        st.session_state.view = "Country"
        st.rerun()

# -- Layout Helper
def render_category_page(title_str):
    title, _, btn1, btn2 = st.columns([6, 2, 1, 1], vertical_alignment="bottom")
    title.title(title_str)
    if btn1.button("Country", use_container_width=True):
        st.session_state.view = "Country"
    if btn2.button("State", use_container_width=True):
        st.session_state.view = "State"
    return st.session_state.view

# -- Insurance Page
def render_insurance_page():
    view = render_category_page("📄 Insurance Analysis")
    sub = st.session_state.subcategory
    if sub == "Aggregated" and view == "Country":
        insurance_aggregated_country_chart()
    elif sub == "Aggregated" and view == "State":
        insurance_aggregated_state_chart()
    elif sub == "Map" and view == "Country":
        insurance_map_country_chart()
    elif sub == "Map" and view == "State":
        insurance_map_state_chart()
    elif sub == "Top" and view == "Country":
        insurance_top_country_chart()
    elif sub == "Top" and view == "State":
        insurance_top_country_chart()

# -- Transaction Page
def render_transaction_page():
    view = render_category_page("💸 Transaction Analysis")
    sub = st.session_state.subcategory
    if sub == "Aggregated" and view == "Country":
        transaction_aggregated_country_chart()
    elif sub == "Aggregated" and view == "State":
        transaction_aggregated_state_chart()
    elif sub == "Map" and view == "Country":
        transaction_map_country_chart()
    elif sub == "Map" and view == "State":
        transaction_map_state_chart()
    elif sub == "Top" and view == "Country":
        transaction_top_country_chart()
    elif sub == "Top" and view == "State":
        transaction_top_country_chart()

# -- User Page
def render_user_page():
    view = render_category_page("👥 User Analysis")
    sub = st.session_state.subcategory
    if sub == "Aggregated" and view == "Country":
        user_aggregated_country_chart()
    elif sub == "Aggregated" and view == "State":
        user_aggregated_state_chart()
    elif sub == "Map" and view == "Country":
        user_map_country_chart()
    elif sub == "Map" and view == "State":
        user_map_state_chart()
    elif sub == "Top" and view == "Country":
        user_top_country_chart()
    elif sub == "Top" and view == "State":
        user_top_country_chart()

# -- App Router
render_sidebar()

if st.session_state.page == "home":
    render_home()
elif st.session_state.page.startswith("insurance"):
    render_insurance_page()
elif st.session_state.page.startswith("transaction"):
    render_transaction_page()
elif st.session_state.page.startswith("user"):
    render_user_page()