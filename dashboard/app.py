import streamlit as st
import pandas as pd
import plotly.express as px

# Daten laden
orders = pd.read_csv("data/olist_orders_dataset.csv")
order_items = pd.read_csv("data/olist_order_items_dataset.csv")

# Zeitstempel in Datum wandeln
orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
orders["month"] = orders["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()

# Order Items mit Orders verknüpfen
merged = pd.merge(order_items, orders, on="order_id")
monthly_revenue = merged.groupby("month")["price"].sum().reset_index()

# Dashboard
st.title("📊 Brazilian E-Commerce Dashboard")

fig = px.bar(monthly_revenue, x="month", y="price", title="Umsatz pro Monat")
st.plotly_chart(fig)

st.write("Umsatz-Details:")
st.dataframe(monthly_revenue)
