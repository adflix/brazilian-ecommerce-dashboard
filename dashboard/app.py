import streamlit as st
import pandas as pd
import plotly.express as px

# Daten laden
orders = pd.read_csv("data/olist_orders_dataset.csv")
order_items = pd.read_csv("data/olist_order_items_dataset.csv")
products = pd.read_csv("data/olist_products_dataset.csv")
reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")

orders["order_purchase_timestamp"] = pd.to_datetime(orders["order_purchase_timestamp"])
orders["order_delivered_customer_date"] = pd.to_datetime(orders["order_delivered_customer_date"])
orders["order_estimated_delivery_date"] = pd.to_datetime(orders["order_estimated_delivery_date"])

# TABS
st.title("📊 Brazilian E-Commerce Dashboard")

tab1, tab2, tab3 = st.tabs(["Umsatz", "Lieferzeiten", "Bewertungen"])

with tab1:
    st.header("📈 Umsatzanalyse")
    # Umsatz pro Monat
    orders["month"] = orders["order_purchase_timestamp"].dt.to_period("M").astype(str)
    merged = pd.merge(order_items, orders, on="order_id")
    monthly_revenue = merged.groupby("month")["price"].sum().reset_index()

    fig_month = px.bar(monthly_revenue, x="month", y="price", title="Umsatz pro Monat")
    st.plotly_chart(fig_month)

    # Umsatz pro Produktkategorie
    merged_items = pd.merge(order_items, products, on="product_id")
    category_revenue = merged_items.groupby("product_category_name")["price"].sum().reset_index()

    fig_category = px.bar(category_revenue, x="product_category_name", y="price", title="Umsatz pro Produktkategorie")
    st.plotly_chart(fig_category)

with tab2:
    st.header("📦 Lieferzeiten & Verspätungen")
    orders["delay"] = orders["order_delivered_customer_date"] > orders["order_estimated_delivery_date"]
    delay_rate = orders["delay"].mean() * 100

    st.write(f"Verspätungsrate: **{delay_rate:.2f}%**")

    delay_counts = orders["delay"].value_counts().reset_index()
    delay_counts.columns = ["Verspätet", "Anzahl"]
    fig_delay = px.pie(delay_counts, names="Verspätet", values="Anzahl", title="Pünktlich vs. Verspätet")
    st.plotly_chart(fig_delay)

with tab3:
    st.header("⭐ Preis vs. Bewertung")
    reviewed_orders = pd.merge(order_items, reviews, on="order_id")
    fig_price_rating = px.scatter(reviewed_orders, x="price", y="review_score", opacity=0.6, title="Preis vs. Bewertung")
    st.plotly_chart(fig_price_rating)
