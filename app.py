import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector
import plotly.express as px
import os
import json
import plotly.graph_objects as go
import requests
from PIL import Image
import base64


connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root",
    database = "phonepay"
)

cursor = connection.cursor()


st.set_page_config(
    page_title="PhonePe Pulse Data Visualization",
    layout="wide",
    menu_items={'About': "# PhonePe Pulse"}
)

# Floating menu container
menu_container = st.container()
with menu_container:
    selected = option_menu(
            menu_title=None,
            options=["Home", "Explore", "Insights","Business Case Study"],
            icons=["house", "search", "graph-up","lightning"],
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {
                    "padding": "0!important", 
                    "background-color": "transparent",
                    # "color": "purple",
                    "border": "none"
                },
                "nav-link": {
                    "font-size": "14px",
                    "padding": "8px 12px",
                    "margin": "0 2px",
                    # "background-color": "white"
                    # "color": "purple"
                },
                "nav-link-selected": {"background-color": "#6F36AD"},
            }
        )
        
st.markdown('</div>', unsafe_allow_html=True)

if selected == "Home":
    # st.title("PhonePe Pulse Dashboard")
    # image_path = "phonepe.png"
    with open("D:\\Sara\\New folder\\Saravana\\Phonepay\\phonepe.png", "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px;">
            <img src="data:image/png;base64,{encoded}" width="300"/>
        </div>
        """,
        unsafe_allow_html=True
    )


    with st.container():
        st.markdown("""
        <style>
            .growth-header {
                background: linear-gradient(135deg, #4a2c82, #8a2be2);
                color: white;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                text-align: center;
            }
            .metric-card {
                background-color: transparent;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                text-align: center;
            }
            .metric-value {
                font-size: 28px;
                font-weight: bold;
                color: white;
            }
            .metric-label {
                font-size: 14px;
                color: #666;
            }
        </style>
        
        <div class="growth-header">
            <h2>PhonePe Growth Story</h2>
            <p>India's leading digital payments platform</p>
        </div>
        """, unsafe_allow_html=True)

        cursor.execute("""
            SELECT 
                SUM(Transaction_Count) as total_transactions,
                SUM(Transaction_Amount) as total_amount,
                COUNT(DISTINCT State) as states_covered
            FROM map_transaction
        """)
        metrics = cursor.fetchone()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{metrics[0]:,}</div>
                    <div class="metric-label">Total Transactions</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">₹{metrics[1]/100000:.1f} L cr</div>
                    <div class="metric-label">Payment Volume</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{metrics[2]}/36</div>
                    <div class="metric-label">States & UTs Covered</div>
                </div>
            """, unsafe_allow_html=True)

    
    with st.container():
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4a2c82, #8a2be2); color: white; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center;'>
            <h3 style='color: white;'>Transaction Patterns Across India</h3>
            <p>Explore how digital payments are growing across states</p>
        </div>
        """, unsafe_allow_html=True)

        selected_year = st.slider("**YEAR**",min_value=2018, max_value=2024)

        cursor.execute(f"""
            SELECT State, SUM(Transaction_Count), SUM(Transaction_Amount) 
            FROM map_transaction 
            WHERE Year={selected_year}
            GROUP BY State
        """)
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','Total_Transaction','Total_Amount'])
        df2 = pd.read_csv('D:\\Sara\\New folder\\Saravana\\Phonepay\\Statenames.csv')
        df1.State = df2
        fig = px.choropleth(
            df1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Total_Amount',
            color_continuous_scale='purples',
            range_color=(df1['Total_Amount'].min(), df1['Total_Amount'].max()),
            labels={'Total_Amount': 'Transaction Amount (₹ cr)'},
            title=f"PhonePe Transactions in {selected_year}"
        )

        # fig.update_geos(fitbounds="locations", visible=False)
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            bgcolor='rgba(0,0,0,0)'
        )
        

        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)


# ---------- Interesting Facts ----------
    with st.container():
        st.markdown("""
        <style>
            .fact-container {
                background: linear-gradient(135deg, #6a3093, #4a2c82);
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 16px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                height: 180px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border: 1px solid rgba(255,255,255,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .fact-container:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 24px rgba(0,0,0,0.3);
            }
            .fact-header {
                color: white;
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 12px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            .fact-body {
                font-size: 16px;
                color: rgba(255,255,255,0.9);
                line-height: 1.4;
            }
            .emoji {
                font-size: 24px;
                margin-bottom: 8px;
            }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
                <div class="fact-container">
                    <div>
                        <div class="emoji">🚀</div>
                        <div class="fact-header">Fastest Growing UPI App</div>
                    </div>
                    <div class="fact-body">PhonePe dominates with 50%+ UPI market share, outpacing competitors by 2x growth</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
                <div class="fact-container">
                    <div>
                        <div class="emoji">📍</div>
                        <div class="fact-header">Widest Reach</div>
                    </div>
                    <div class="fact-body">Serving 30M+ merchants in 20+ languages across 99% of Indian pin codes</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
                <div class="fact-container">
                    <div>
                        <div class="emoji">💰</div>
                        <div class="fact-header">Billions in Transactions</div>
                    </div>
                    <div class="fact-body">Processed ₹50L+ crore in 2024 - that's ₹1.3L+ crore daily!</div>
                </div>
            """, unsafe_allow_html=True)
    
# Explore Page
    
elif selected == "Explore":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2024, value= 2024)
    Quater = st.sidebar.slider("**Quater**", min_value=1, max_value=4)
    Insights = st.sidebar.selectbox("**Insights**", {"Transaction", "Users", "Insurance"})
    # col1,col2= st.columns(2)

    if Insights == "Transaction":
        
        # India Map - Transaction Amount
        st.markdown("""
            <div style='background-color: rgba(255,255,255,0.04); 
                        border: 1px solid #6F36AD; 
                        padding: 16px; 
                        border-radius: 12px;
                        margin-bottom: 25px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h3 style='color: #9D4EDD;'>India States - Transaction Amount</h3>
        """, unsafe_allow_html=True)

        cursor.execute(f"SELECT State, SUM(Transaction_Count), SUM(Transaction_Amount) FROM map_transaction WHERE Year={Year} AND Quarter={Quater} GROUP BY State")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','Total_Transaction','Total_Amount'])
        df2 = pd.read_csv('D:\\Sara\\New folder\\Saravana\\Phonepay\\Statenames.csv')
        df1.State = df2 

        fig = px.choropleth(df1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Total_Amount',
            color_continuous_scale='sunset')

        # fig.update_geos(fitbounds="locations", visible=False)
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            bgcolor='rgba(0,0,0,0)'
        )
        

        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


        st.markdown("""
            <div style='background-color: rgba(255,255,255,0.04); 
                        border: 1px solid #6F36AD; 
                        padding: 16px; 
                        border-radius: 12px;
                        margin-bottom: 25px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h3 style='color: #9D4EDD;'>India States - Total Transaction</h3>
        """, unsafe_allow_html=True)

        cursor.execute(f"SELECT State, SUM(Transaction_Count) AS Total_Transaction, SUM(Transaction_Amount) AS Total_Amount FROM map_transaction WHERE Year= {Year} AND Quarter= {Quater} GROUP BY State ORDER BY State;")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transaction', 'Total_Amount'])
        df2 = pd.read_csv('D:\\Sara\\New folder\\Saravana\\Phonepay\\Statenames.csv')
        df1.Total_Transaction = df1.Total_Transaction.astype(int)
        df1.State = df2
        fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations = 'State',
                    color= 'Total_Transaction',
                    color_continuous_scale='sunset')

        # fig.update_geos(fitbounds="locations", visible=False)
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            bgcolor='rgba(0,0,0,0)'
        )
        

        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
      

        st.markdown("## :violet[Top Payment Type]")
        cursor.execute(f"SELECT Transaction_type,SUM(Transaction_Count) AS Total_Transactions, SUM(Transaction_Amount) AS  Total_amount FROM agg_transaction WHERE Year= {Year} AND Quarter= {Quater} GROUP BY Transaction_type ORDER BY Transaction_type;")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)


        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        cursor.execute(f"select State, District,Year,Quarter, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_transaction where Year = {Year} and Quarter = {Quater} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

    #Explore- Users

    if Insights == "Users":

        st.markdown("""
            <div style='background-color: rgba(255,255,255,0.04); 
                        border: 1px solid #6F36AD; 
                        padding: 16px; 
                        border-radius: 12px;
                        margin-bottom: 25px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h3 style='color: #9D4EDD;'>India States - Total Users</h3>
        """, unsafe_allow_html=True)

        cursor.execute(f"SELECT State, SUM(RegisteredUsers) AS Total_users FROM  map_user WHERE Year = {Year} AND Quarter = {Quater} GROUP BY State ORDER BY  State  ;")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','Total_users'])
        df1.Total_users = df1.Total_users.astype(int)
        df2 = pd.read_csv('D:\\Sara\\New folder\\Saravana\\Phonepay\\Statenames.csv')
        df1.State = df2  

        fig = px.choropleth(df1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Total_users',
            color_continuous_scale='sunset')

        # fig.update_geos(fitbounds="locations", visible=False)
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            bgcolor='rgba(0,0,0,0)'
        )
        

        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div style='background-color: rgba(255,255,255,0.04); 
                        border: 1px solid #6F36AD; 
                        padding: 16px; 
                        border-radius: 12px;
                        margin-bottom: 25px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h3 style='color: #9D4EDD;'>India States - User Engagement</h3>
        """, unsafe_allow_html=True)

        cursor.execute(f"SELECT State, SUM(AppOpens) AS User_engagement FROM  map_user WHERE Year = {Year} AND Quarter = {Quater} GROUP BY State ORDER BY  State  ;")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','User_engagement'])
        df1.User_engagement = df1.User_engagement.astype(int)
        df2 = pd.read_csv('D:\\Sara\\New folder\\Saravana\\Phonepay\\Statenames.csv')
        df1.State = df2 

        fig = px.choropleth(df1,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='User_engagement',
            color_continuous_scale='sunset')

        # fig.update_geos(fitbounds="locations", visible=False)
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            bgcolor='rgba(0,0,0,0)'
        )
        

        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)


        st.markdown("## :violet[Top Devices]")
        cursor.execute(f"SELECT Brand,SUM(RegisteredUsers) AS total_registered_users,SUM(AppOpens) AS total_app_opens FROM agg_user GROUP BY Brand ORDER BY total_registered_users DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['Brand', 'RegisteredUsers','total_app_opens'])

        fig = px.bar(df,
                     title='Device Brand vs Total Registered Users',
                     x="Brand",
                     y="RegisteredUsers",
                     orientation='v',
                     color='total_app_opens',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)


        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        cursor.execute(f"select State, District,Year,Quarter, sum(RegisteredUsers) as Total_users, sum(AppOpens) as User_engagement from map_user where Year = {Year} and Quarter = {Quater} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_users','User_engagement'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_users",
                     orientation='v',
                     color='User_engagement',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)

    # ** EXPLORE - Insurance **     

    if Insights == "Insurance":
        
        
        st.markdown("""
            <div style='background-color: rgba(255,255,255,0.04); 
                        border: 1px solid #6F36AD; 
                        padding: 16px; 
                        border-radius: 12px;
                        margin-bottom: 25px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h3 style='color: #9D4EDD;'>India States - Total Insurance Transaction</h3>
        """, unsafe_allow_html=True)

        cursor.execute(f"SELECT State, SUM(Transaction_count) AS Total_Transaction, SUM(Transaction_amount) AS Total_Amount FROM map_insurance WHERE Year= {Year} AND Quarter= {Quater} GROUP BY State ORDER BY State;")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transaction', 'Total_Amount'])
        df2 = pd.read_csv('D:\\Sara\\New folder\\Saravana\\Phonepay\\Statenames.csv')
        df1.Total_Transaction = df1.Total_Transaction.astype(int)
        df1.State = df2
        fig = px.choropleth(df1, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations = 'State',
                    color= 'Total_Transaction',
                    color_continuous_scale='sunset')

        # fig.update_geos(fitbounds="locations", visible=False)
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            bgcolor='rgba(0,0,0,0)'
        )
        

        fig.update_layout(
            margin={"r":0,"t":40,"l":0,"b":0},
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
      

        st.markdown("## :violet[Top 10 Insurance Transaction]")
        cursor.execute(f"SELECT State,SUM(Transaction_count) AS Total_Transactions, SUM(Transaction_amount) AS  Total_amount FROM agg_insurance WHERE Year= {Year} AND Quarter= {Quater} GROUP BY State ORDER BY Total_amount DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="State",
                     y="Total_amount",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=False)


        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        cursor.execute(f"select State, District,Year,Quarter, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_insurance where Year = {Year} and Quarter = {Quater} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)


# -------INSIGHTS-------

elif selected == "Insights":
    # st.title("Data Insights")
    # st.write("Key findings and trends will appear here")

    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    # colum1,colum2= st.columns([1,1.5],gap="large")
    Year = st.sidebar.selectbox(
            "**Year**",
            options=[2018, 2019, 2020, 2021, 2022, 2023, 2024],
            index=4,  
            
        )

    Quarter = st.sidebar.selectbox(
            "**Quarter**",
            options=[1, 2, 3, 4]
        )

    st.markdown("""
        <style>
            .fact-container {
                background: linear-gradient(135deg, #6a3093, #4a2c82);
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 16px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
                height: 180px;
                # width: 2500px;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                border: 1px solid rgba(255,255,255,0.1);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }
            .fact-container:hover {
                transform: translateY(-5px);
                box-shadow: 0 12px 24px rgba(0,0,0,0.3);
            }
            .fact-header {
                color: white;
                font-size: 18px;
                font-weight: 700;
                margin-bottom: 12px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
            .fact-body {
                font-size: 16px;
                color: rgba(255,255,255,0.9);
                line-height: 1.4;
            }
            .emoji {
                font-size: 24px;
                margin-bottom: 8px;
            }
        </style>
        """, unsafe_allow_html=True)    
    

    st.markdown("""
                <div class="fact-container">
                    <div>
                        <div class="emoji">
                        <i class="fa-regular fa-circle-info"></i>
                        </div>
                        <div class="fact-header">From this menu we can get insights like :</div>
                    </div>
                    <div class="fact-body">
                        <ol>
                        <li>Overall ranking based on a particular Year and Quarter.</li>
                        <li>Top 10 States, Districts, and Pincodes based on the total number of transactions and total amount spent on PhonePe.</li>
                        <li>Top 10 States, Districts, and Pincodes based on total PhonePe users and their app opening frequency.</li>
                        <li>Top 10 mobile brands and their percentage based on how many people use PhonePe.</li>
                        </ol>
                    </div>
                </div>
            """, unsafe_allow_html=True)


    
    if Type == "Transactions":
        # col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with st.container():
            # st.markdown(
            #     """
            #     <style>
            #         .glow-container {
            #             border: 2px solid #7F00FF;
            #             box-shadow: 0 0 20px #7F00FF;
            #             border-radius: 12px;
            #             padding: 20px;
            #             margin-bottom: 20px;
            #             background-color: rgba(255,255,255,0.03);
            #         }
            #     </style>
            #     <div class='glow-container'>
            #     """,
            #     unsafe_allow_html=True
            # )
            # st.markdown("<div class='glow-container'>", unsafe_allow_html=True)
            # st.markdown("### :violet[State]")
            st.markdown("""
            <div style='background-color: rgba(255,255,255,0.04); 
                        border: 1px solid #6F36AD; 
                        padding: 16px; 
                        border-radius: 12px;
                        margin-bottom: 25px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h3 style='color: #9D4EDD;'>TOP 10 STATES</h3>
        """, unsafe_allow_html=True)
            cursor.execute(f"SELECT  State ,SUM(Transaction_Count) as total_transaction,  SUM(Transaction_Amount) AS total FROM  agg_transaction WHERE Year={Year} AND Quarter={Quarter}  GROUP BY State ORDER BY total DESC LIMIT 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            # st.markdown("</div>", unsafe_allow_html=True)
            # st.bokeh_chart(fig)
        st.markdown("---")   

        left, right = st.columns(2,gap="large") 
        with left:
            # st.markdown("### :violet[District]")
            st.markdown("""
            <div style='background-color: rgba(255,255,255,0.04); 
                        border: 1px solid #6F36AD; 
                        padding: 16px; 
                        border-radius: 12px;
                        margin-bottom: 25px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h3 style='color: #9D4EDD;'>TOP 10 DISTRICTS</h3>
        """, unsafe_allow_html=True)
            cursor.execute(f"SELECT District, SUM(Transaction_Count)as total_transaction ,SUM(Transaction_Amount) AS total FROM  map_transaction WHERE Year={Year} AND Quarter={Quarter} GROUP BY District  ORDER BY total DESC LIMIT 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with right:
            # st.markdown("### :violet[Pincode]")
            st.markdown("""
            <div style='background-color: rgba(255,255,255,0.04); 
                        border: 1px solid #6F36AD; 
                        padding: 16px; 
                        border-radius: 12px;
                        margin-bottom: 25px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h3 style='color: #9D4EDD;'>TOP 10 PINCODES</h3>
        """, unsafe_allow_html=True)
            cursor.execute(f"SELECT pincodes, SUM(Transaction_Count)as total_transaction ,SUM(Transaction_Amount) AS total FROM  top_transaction WHERE Year={Year} AND Quarter={Quarter} GROUP BY pincodes  ORDER BY total DESC LIMIT 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['pincodes', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='pincodes',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

    if Type == "Users":
        # col1,col2,col3,col4 = st.columns([4,4,4,4],gap="large")
        st.markdown("""
            <div style='background-color: rgba(255,255,255,0.04); 
                        border: 1px solid #6F36AD; 
                        padding: 16px; 
                        border-radius: 12px;
                        margin-bottom: 25px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
                <h3 style='color: #9D4EDD;'>TOP BRANDS</h3>
        """, unsafe_allow_html=True)
        if Year == [2022, 2023, 2024] and Quarter in [2,3,4]:
                st.markdown(f"#### Sorry No Data to Display for {Year} Qtr {Quarter}")
        else:
            cursor.execute(f"SELECT Year, Brand,SUM(Count) AS Total_users FROM agg_user WHERE Year = {Year} and Quarter = {Quarter} GROUP BY Brand ORDER BY Total_users DESC  ;")
            df = pd.DataFrame(cursor.fetchall(), columns=['Year', 'Brand', 'Total_users'])
            # df.Total_Users = df.Total_users.astype(float)
            fig = px.bar(df,
                    title='Top 10',
                    x="Total_users",
                    y="Brand",
                    orientation='h',
                    color='Total_users',
                    color_continuous_scale=px.colors.sequential.Agsunset)
                # fig = st.bar_chart(df,x)
            st.plotly_chart(fig,use_container_width=True)
        
        # st.markdown("### :violet[District]")
        st.markdown("""
        <div style='background-color: rgba(255,255,255,0.04); 
                    border: 1px solid #6F36AD; 
                    padding: 16px; 
                    border-radius: 12px;
                    margin-bottom: 25px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #9D4EDD;'>TOP 10 DISTRICTS</h3>
        """, unsafe_allow_html=True)
        cursor.execute(f"SELECT District , SUM(RegisteredUsers ) AS  Total_users FROM  map_user WHERE Year = {Year} and Quarter = {Quarter} GROUP BY District ORDER BY Total_users  DESC LIMIT 10  ;")
        df = pd.DataFrame(cursor.fetchall(), columns=['District', 'Total_users'])
        df.Total_Users = df.Total_users.astype(float)
        fig = px.bar(df,
                    title='Top 10',
                    x="Total_users",
                    y="District",
                    orientation='h',
                    color='Total_users',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig,use_container_width=True)         
    

        # st.markdown("### :violet[Pincode]")
        st.markdown("""
        <div style='background-color: rgba(255,255,255,0.04); 
                    border: 1px solid #6F36AD; 
                    padding: 16px; 
                    border-radius: 12px;
                    margin-bottom: 25px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #9D4EDD;'>TOP 10 PINCODES</h3>
        """, unsafe_allow_html=True)
        cursor.execute(f"SELECT pincodes, SUM(RegisteredUsers) AS Total_users FROM top_user WHERE Year = {Year} and Quarter = {Quarter} GROUP BY pincodes ORDER BY Total_users DESC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['pincodes', 'Total_users'])
        fig = px.pie(df,
                    values='Total_users',
                    names='pincodes',
                    title='Top 10',
                    color_discrete_sequence=px.colors.sequential.Agsunset,
                    hover_data=['Total_users'])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig,use_container_width=True)
            
        # st.markdown("### :violet[State]")
        st.markdown("""
        <div style='background-color: rgba(255,255,255,0.04); 
                    border: 1px solid #6F36AD; 
                    padding: 16px; 
                    border-radius: 12px;
                    margin-bottom: 25px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #9D4EDD;'>TOP USERS</h3>
        """, unsafe_allow_html=True)
        if Year == [2022, 2023, 2024] and Quarter in [2,3,4]:
            st.markdown(f"#### Sorry No Data to Display for {Year} Qtr {Quarter}")
        else:
            cursor.execute(f"SELECT State , SUM(RegisteredUsers) AS  Total_user, SUM(AppOpens) AS total_app_opens FROM agg_user WHERE Year = {Year} and Quarter = {Quarter} GROUP BY State ORDER BY Total_user   DESC LIMIT 10  ;")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_user','total_app_opens'])
            fig = px.pie(df, values='Total_user',
                            names='State',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['total_app_opens'],
                            labels={'Ttotal_app_opens':'total_app_opens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)   
 
elif selected == "Business Case Study":
    st.markdown("## :violet[Strategic Insights]")
    scenario = st.sidebar.selectbox("**Choose Scenario**", (
        "Decoding Transaction Dynamics",
        "Device Dominance & Engagement",
        "Insurance Penetration",
        "Market Expansion",
        "User Engagement Strategy"
    ))

    # Scenario 1: Transaction Dynamics
    if scenario == "Decoding Transaction Dynamics":
        st.markdown("""
        <div style='background-color: rgba(255,255,255,0.04); 
                    border: 1px solid #6F36AD; 
                    padding: 16px; 
                    border-radius: 12px;
                    margin-bottom: 25px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #9D4EDD;'>Decoding Transaction Dynamics</h3>
        </div>
        """, unsafe_allow_html=True)

        # Example chart
        cursor.execute("SELECT State, SUM(Transaction_Amount) FROM map_transaction GROUP BY State")
        df = pd.DataFrame(cursor.fetchall(), columns=['State','Total_Amount'])
        fig = px.bar(df, x="State", y="Total_Amount", title="Transaction Amount by State")
        st.plotly_chart(fig, use_container_width=True)

        # Insights
        st.write("**Key Insights:**")
        st.write("1. Karnataka and Maharashtra consistently lead in transaction volumes.")
        st.write("2. Tamil Nadu shows steady quarter-on-quarter growth.")
        st.write("3. Delhi exhibits seasonal fluctuations in transaction activity.")
        st.write("4. Gujarat spikes during festive quarters.")
        st.write("5. Overall upward trend across India year-on-year.")

    # Scenario 2: Device Dominance
    if scenario == "Device Dominance & Engagement":
        st.markdown("<h3 style='color: #9D4EDD;'>Device Dominance & Engagement</h3>", unsafe_allow_html=True)
        cursor.execute("SELECT Brand, SUM(RegisteredUsers), SUM(AppOpens) FROM agg_user GROUP BY Brand")
        df = pd.DataFrame(cursor.fetchall(), columns=['Brand','RegisteredUsers','AppOpens'])
        df['Engagement_Ratio'] = df['AppOpens']/df['RegisteredUsers']
        fig = px.bar(df, x="Brand", y="Engagement_Ratio", title="Engagement Ratio by Device Brand")
        st.plotly_chart(fig, use_container_width=True)

        st.write("**Key Insights:**")
        st.write("1. Apple users show the highest engagement ratio.")
        st.write("2. Xiaomi and Samsung dominate user base but moderate engagement.")
        st.write("3. Vivo and Oppo underperform despite registrations.")
        st.write("4. Engagement varies significantly across brands.")
        st.write("5. Optimizing for high-engagement devices boosts retention.")

    # Scenario 3: Insurance Penetration
    if scenario == "Insurance Penetration":
        st.markdown("<h3 style='color: #9D4EDD;'>Insurance Penetration</h3>", unsafe_allow_html=True)
        cursor.execute("SELECT State, SUM(Transaction_count) FROM map_insurance GROUP BY State")
        df = pd.DataFrame(cursor.fetchall(), columns=['State','Insurance_Count'])
        fig = px.bar(df, x="State", y="Insurance_Count", title="Insurance Transactions by State")
        st.plotly_chart(fig, use_container_width=True)

        st.write("**Key Insights:**")
        st.write("1. Karnataka leads in insurance adoption.")
        st.write("2. Maharashtra and Tamil Nadu are strong performers.")
        st.write("3. Delhi shows growth potential in insurance uptake.")
        st.write("4. Gujarat demonstrates moderate activity.")
        st.write("5. Campaigns in low-performing states can expand adoption.")

    # Scenario 4: Market Expansion
    if scenario == "Market Expansion":
        st.markdown("<h3 style='color: #9D4EDD;'>Market Expansion</h3>", unsafe_allow_html=True)
        cursor.execute("SELECT State, SUM(Transaction_Count), SUM(Transaction_Amount) FROM map_transaction GROUP BY State")
        df = pd.DataFrame(cursor.fetchall(), columns=['State','Count','Amount'])
        df['Avg_Value'] = df['Amount']/df['Count']
        fig = px.bar(df, x="State", y="Avg_Value", title="Average Transaction Value by State")
        st.plotly_chart(fig, use_container_width=True)

        st.write("**Key Insights:**")
        st.write("1. Delhi has the highest average transaction value.")
        st.write("2. Gujarat and Maharashtra show strong values.")
        st.write("3. Tamil Nadu and Karnataka high volume but lower average value.")
        st.write("4. High-value states indicate affluent user base.")
        st.write("5. Targeting high-value states improves revenue per user.")

    # Scenario 5: User Engagement Strategy
    if scenario == "User Engagement Strategy":
        st.markdown("<h3 style='color: #9D4EDD;'>User Engagement Strategy</h3>", unsafe_allow_html=True)
        cursor.execute("SELECT State, SUM(RegisteredUsers), SUM(AppOpens) FROM map_user GROUP BY State")
        df = pd.DataFrame(cursor.fetchall(), columns=['State','RegisteredUsers','AppOpens'])
        df['Engagement_Ratio'] = df['AppOpens']/df['RegisteredUsers']
        fig = px.bar(df, x="State", y="Engagement_Ratio", title="User Engagement Ratio by State")
        st.plotly_chart(fig, use_container_width=True)

        st.write("**Key Insights:**")
        st.write("1. Karnataka and Delhi show high engagement ratios.")
        st.write("2. Gujarat has low engagement despite registrations.")
        st.write("3. Maharashtra balances user base and engagement.")
        st.write("4. Low-engagement states present re-engagement opportunities.")
        st.write("5. Region-specific campaigns can boost effectiveness.")


# Footer
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        # border-top: 1px solid #ddd;
    }
    </style>

    <div class="footer">
        Project 1-Made with ❤️Love by Saravana Kumar | Data Analyst | Powered by Streamlit❤️
    </div>
""", unsafe_allow_html=True)