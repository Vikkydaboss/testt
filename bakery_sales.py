import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# load data
@st.cache_data
def load_data():
    df = pd.read_csv("bakerysales.csv")
    df.drop(columns='Unnamed: 0', inplace=True)
    df['date'] = pd.to_datetime(df.date)
    df["unit_price"] = df.unit_price.str.replace(",",".").str.replace(" €", "")
    df["unit_price"] = df.unit_price.astype('float')
    # calculate the sales 
    sales = df.Quantity * df.unit_price
    # Create a new column for sales 
    df['sales'] = sales 
    
    return df

df = load_data()
st.title("Bakery Sales App")
st.sidebar.title("Filters")

# display dataset
st.subheader("Data Preview")
st.dataframe(df.head())

# Create a filter for articles and ticket numbers 
articles = df['article'].unique()
ticketNos = df['ticket_number'].value_counts().head(10).reset_index()["ticket_number"]

#Create a multiselect for articles
selected_articles = st.sidebar.multiselect("Products", articles, [articles[0], articles[20]])
selected_ticketNos = st.sidebar.selectbox("Top 10 Tickets", ticketNos[:10])

#filtered articles 
filtered_articles = df[df["article"].isin(selected_articles)]


# display the filtered table

st.subheader("Filtered Table")
if not selected_articles:
    st.error("Select an Article")
else:
    st.dataframe(filtered_articles.sample(3))

# Calculations

total_sales = np.round(df['sales'].sum(),2)
total_qty = np.round(df["Quantity"].sum(),2)
no_of_articles = len(articles)
no_filtered_articles = filtered_articles['article'].nunique()
Total_filtered_sales = np.round(filtered_articles['sales'].sum(),2)
Total_filtered_qty = np.round(filtered_articles['Quantity'].sum(),2)

# display in columns 

col1, col2, col3 = st.columns(3)
#sales
if not selected_articles:
    col1.metric("Total Sales", f'{total_sales}')
else:
    col1.metric('Total Sales', f'{Total_filtered_sales}')

#quantity
if not selected_articles:
    col2.metric("Quantity", f'{total_qty}')
else:
    col2.metric('Quantity', f'{Total_filtered_qty}')

#articles
if not selected_articles:
    col3.metric("No. of products", f'{no_of_articles}')
else:
    col3.metric('No of Products', f'{no_filtered_articles}')


# charts 
st.header("Plotting")
#data
article_group = df.groupby("article")['sales'].sum()
article_group = article_group.sort_values(ascending=False)[:-3]
table = article_group.reset_index()

# Selection from filter 
filtered_table = table[table['article'].isin(selected_articles)]

# bar plot

st.subheader(" Bar Chart ")
fig1, ax1 = plt.subplots(figsize=(10,6))
ax1.bar(filtered_table['article'], filtered_table["sales"])
st.pyplot(fig1)


#pie chart

st.subheader(" Pie Chart ")
fig2, ax2 = plt.subplots(figsize=(7,5))
ax2.pie(filtered_table['sales'],
        labels = selected_articles,
        autopct = "%1.1f%%")
st.pyplot(fig2)

st.subheader('Trend Analysis')
daily_sales = df.groupby('date')['sales'].sum()

fig3, ax3 = plt.subplots(figsize=(12,6))
ax3.plot(daily_sales.index, daily_sales.values)
st.pyplot(fig3)

