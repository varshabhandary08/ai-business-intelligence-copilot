import os
import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)
)

# Page Title
st.title("AI Business Intelligence Copilot")

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload Sales Dataset",
    type=["csv"]
)

if uploaded_file:

    # Read Dataset
    df = pd.read_csv(uploaded_file)

    sales_col = find_column(
        df,
        ["Sales", "Revenue", "Amount", "Total Sales"]
    )

    profit_col = find_column(
        df,
        ["Profit", "Margin", "Net Profit", "Earnings"]
    )

    order_col = find_column(
        df,
        ["Order ID", "Invoice ID", "Transaction ID"]
    )

    # Success Message
    st.success("Dataset Loaded Successfully!")

    st.subheader("Detected Columns")

    st.write("Sales:", sales_col)
    st.write("Profit:", profit_col)
    st.write("Order ID:", order_col)

    # Preview
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Shape
    st.subheader("Dataset Shape")
    st.write(df.shape)

    # ==========================
    # BUSINESS KPIs
    # ==========================

    st.subheader("Business KPIs")

    total_sales = df[sales_col].sum()
    total_profit = df[profit_col].sum()
    total_orders = df[order_col].nunique()

    avg_order_value = total_sales / total_orders

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Sales", f"${total_sales:,.2f}")
        st.metric("Total Profit", f"${total_profit:,.2f}")

    with col2:
        st.metric("Total Orders", total_orders)
        st.metric(
            "Average Order Value",
            f"${avg_order_value:,.2f}"
        )

    # ==========================
    # SALES BY REGION
    # ==========================

    st.subheader("Sales by Region")

    sales_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig1 = px.bar(
        sales_region,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # ==========================
    # PROFIT BY CATEGORY
    # ==========================

    st.subheader("Profit by Category")

    profit_category = (
        df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        profit_category,
        x="Category",
        y="Profit",
        title="Profit by Category"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ==========================
    # MONTHLY SALES TREND
    # ==========================

    st.subheader("Monthly Sales Trend")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"]
    )

    monthly_sales = (
        df.groupby(
            df["Order Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = (
        monthly_sales["Order Date"]
        .astype(str)
    )

    fig3 = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        title="Monthly Sales Trend"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # ==========================
    # AI INSIGHTS
    # ==========================

    st.subheader("AI Business Insights")

    top_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    top_category = (
        df.groupby("Category")["Profit"]
        .sum()
        .idxmax()
    )

    top_segment = (
        df.groupby("Segment")["Sales"]
        .sum()
        .idxmax()
    )

    best_month = (
        monthly_sales.loc[
            monthly_sales["Sales"].idxmax(),
            "Order Date"
        ]
    )

    st.write(f"✅ Top Sales Region: {top_region}")
    st.write(f"✅ Highest Profit Category: {top_category}")
    st.write(f"✅ Largest Customer Segment: {top_segment}")
    st.write(f"✅ Best Sales Month: {best_month}")

    # ==========================
    # RECOMMENDATIONS
    # ==========================

    st.subheader("Recommendations")

    lowest_region = (
        df.groupby("Region")["Sales"]
        .sum()
        .idxmin()
    )

    st.write(
        f"📌 Consider increasing marketing efforts in the {lowest_region} region."
    )

    st.write(
        f"📌 Continue investing in the {top_category} category because it generates the highest profit."
    )

    # ==========================
    # CHATBOT
    # ==========================

    st.subheader("AI Business Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input(
        "Ask a question about your business data..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.write(question)

        dataset_summary = f"""
        Total Sales: {total_sales}
        Total Profit: {total_profit}
        Total Orders: {total_orders}

        Top Region: {top_region}
        Lowest Region: {lowest_region}

        Top Category: {top_category}

        Top Segment: {top_segment}

        Best Month: {best_month}

        Sales by Region:
        {sales_region.to_string(index=False)}

        Profit by Category:
        {profit_category.to_string(index=False)}
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an expert business analyst. Answer questions using the provided business dataset summary."
                },
                {
                    "role": "user",
                    "content": f"""
                    Dataset Summary:

                    {dataset_summary}

                    Question:
                    {question}
                    """
                }
            ]
        )

        answer = response.choices[0].message.content

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)