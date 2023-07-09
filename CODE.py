import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Dataset!!!", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Sample Dataset EDA")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding = "ISO-8859-1")
else:
    os.chdir(r"C:\Users\ambal\Downloads")
    df = pd.read_csv("dataset.csv", encoding = "ISO-8859-1")

col1, col2 = st.columns((2))
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

col1, col2 = st.columns((2))
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Getting the min and max date 
startDate = pd.to_datetime(df["InvoiceDate"]).min()
endDate = pd.to_datetime(df["InvoiceDate"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["InvoiceDate"] >= date1) & (df["InvoiceDate"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")


# Create for Country
Country = st.sidebar.multiselect("Pick the country",df["Country"].unique())

if not Country:
    df2 = df.copy()
else:
    df2 = df[df["Country"].isin(Country)]
    
    
#create for CustomerID

CustomerID = st.sidebar.multiselect("Pick the CustomerID",df["CustomerID"].unique())

if not CustomerID:
    df3 = df2.copy()
else:
    df3 = df2[df2["CustomerID"].isin(CustomerID)]

# Filter the data based on Country and customer id

if not Country and not CustomerID:
    filtered_df = df
elif Country and CustomerID:
    filtered_df = df3[df["Country"].isin(Country) & df3["CustomerID"].isin(CustomerID)]
else:
    filtered_df = df3[df3["CustomerID"].isin(CustomerID)]

CustomerID_df = filtered_df.groupby(by = ["CustomerID"], as_index = False)["Quantity"].sum()


with col1:
    st.subheader("CustomerID wise Quantity")
    fig = px.bar(CustomerID_df, x = "CustomerID", y = "Quantity", text = ['${:,.2f}'.format(x) for x in CustomerID_df["Quantity"]],
                 template = "seaborn")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.subheader("Country wise quantity")
    fig = px.pie(filtered_df, values = "Quantity", names = "Country", hole = 0.5)
    fig.update_traces(text = filtered_df["Country"], textposition = "outside")
    st.plotly_chart(fig,use_container_width=True)















