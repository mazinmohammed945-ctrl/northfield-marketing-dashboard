
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Northfield & Co. | E-commerce Analytics",
    page_icon="📊",
    layout="wide",
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data(path="Northfield_Co_Case_Study.xlsx"):
    df = pd.read_excel(path, sheet_name="Master data")
    df["Date"] = pd.to_datetime(df["Date"])

    # Do NOT add Google/Meta roll-ups to their component lines.
    # They are already totals reported by the source system.
    df["Total_Media"] = (
        df["spend_Google"]
        + df["spend_Meta"]
        + df["microsoft_spend"]
        + df["criteo_spend"]
        + df["cost_outbrain"]
        + df["Awin_spend"]
        + df["influencer_spend"]
    )

    df["New_Customer_Share"] = (
        df["Revenue_New_Customer"] / df["Total_Revenue"]
    ).replace([np.inf, -np.inf], np.nan)

    df["ROAS"] = (
        df["Total_Revenue"] / df["Total_Media"]
    ).replace([np.inf, -np.inf], np.nan)

    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Date"].dt.year
    df["Month_Name"] = df["Date"].dt.strftime("%b")
    df["Day_of_Week"] = df["Date"].dt.day_name()

    return df


df = load_data()

# -----------------------------
# Header
# -----------------------------
st.title("Northfield & Co. — E-commerce Analytics Dashboard")
st.caption(
    "US e-commerce | Daily data: 1 Apr 2024 – 31 Jul 2026 | "
    "Primary KPI: Total Revenue | Secondary KPI: New-Customer Revenue"
)

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

promotion_filter = st.sidebar.selectbox(
    "Site-wide promotion",
    ["All days", "Promotion = 1", "Promotion = 0"],
)

mailing_filter = st.sidebar.selectbox(
    "UWG mailing",
    ["All days", "Mailing = 1", "Mailing = 0"],
)

d = df[
    (df["Date"].dt.date >= start_date)
    & (df["Date"].dt.date <= end_date)
].copy()

if promotion_filter == "Promotion = 1":
    d = d[d["Promotion_Discount"] == 1]
elif promotion_filter == "Promotion = 0":
    d = d[d["Promotion_Discount"] == 0]

if mailing_filter == "Mailing = 1":
    d = d[d["UWG_Mailing"] == 1]
elif mailing_filter == "Mailing = 0":
    d = d[d["UWG_Mailing"] == 0]

if d.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

# -----------------------------
# KPI calculations
# -----------------------------
total_revenue = d["Total_Revenue"].sum()
new_revenue = d["Revenue_New_Customer"].sum()
new_share = new_revenue / total_revenue
media_spend = d["Total_Media"].sum()
roas = total_revenue / media_spend

# -----------------------------
# Overview
# -----------------------------
st.subheader("Executive Overview")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Revenue", f"${total_revenue:,.0f}")
c2.metric("New-Customer Revenue", f"${new_revenue:,.0f}")
c3.metric("New-Customer Share", f"{new_share:.1%}")
c4.metric("Paid Media Spend", f"${media_spend:,.0f}")
c5.metric("Revenue / Media Spend", f"{roas:.1f}x")

st.markdown("---")

# Revenue trend
trend = (
    d.groupby("Date", as_index=False)
    .agg(
        Total_Revenue=("Total_Revenue", "sum"),
        Revenue_New_Customer=("Revenue_New_Customer", "sum"),
    )
)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=trend["Date"],
        y=trend["Total_Revenue"],
        mode="lines",
        name="Total Revenue",
    )
)
fig.add_trace(
    go.Scatter(
        x=trend["Date"],
        y=trend["Revenue_New_Customer"],
        mode="lines",
        name="New-Customer Revenue",
    )
)
fig.update_layout(
    title="Daily Revenue Trend",
    xaxis_title="Date",
    yaxis_title="Revenue (USD)",
    hovermode="x unified",
    legend_title="Metric",
)
st.plotly_chart(fig, use_container_width=True)

# Monthly performance
monthly = (
    d.groupby("Month", as_index=False)
    .agg(
        Revenue=("Total_Revenue", "sum"),
        New_Customer_Revenue=("Revenue_New_Customer", "sum"),
        Media_Spend=("Total_Media", "sum"),
        Days=("Date", "count"),
    )
)
monthly["ROAS"] = monthly["Revenue"] / monthly["Media_Spend"]
monthly["New_Customer_Share"] = (
    monthly["New_Customer_Revenue"] / monthly["Revenue"]
)

left, right = st.columns(2)

with left:
    fig = px.bar(
        monthly,
        x="Month",
        y="Revenue",
        title="Monthly Revenue",
        labels={"Revenue": "Revenue (USD)", "Month": ""},
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with right:
    fig = px.line(
        monthly,
        x="Month",
        y="ROAS",
        markers=True,
        title="Monthly Revenue / Paid Media Spend",
        labels={"ROAS": "ROAS", "Month": ""},
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Marketing & promotions
# -----------------------------
st.subheader("Marketing & Promotion Analysis")

promo_labels = {
    "Promotion_Discount": "Site-wide promotion",
    "UWG_Mailing": "UWG mailing",
    "Offline_Promo": "Offline promotion",
    "holiday_list": "Holiday",
    "BFCM_Promo_Effect": "BFCM window",
}

promo_choice = st.selectbox(
    "Compare daily performance by business event",
    list(promo_labels.keys()),
    format_func=lambda x: promo_labels[x],
)

event_summary = (
    d.groupby(promo_choice, as_index=False)
    .agg(
        Avg_Daily_Revenue=("Total_Revenue", "mean"),
        Avg_New_Customer_Revenue=("Revenue_New_Customer", "mean"),
        Avg_Media_Spend=("Total_Media", "mean"),
        Days=("Date", "count"),
    )
)
event_summary["Event"] = event_summary[promo_choice].map(
    {0: "No", 1: "Yes"}
)

fig = px.bar(
    event_summary,
    x="Event",
    y="Avg_Daily_Revenue",
    text_auto=".2s",
    title=f"Average Daily Revenue: {promo_labels[promo_choice]}",
    labels={"Avg_Daily_Revenue": "Average Daily Revenue (USD)", "Event": ""},
)
st.plotly_chart(fig, use_container_width=True)

st.dataframe(
    event_summary[
        ["Event", "Avg_Daily_Revenue", "Avg_New_Customer_Revenue",
         "Avg_Media_Spend", "Days"]
    ].rename(
        columns={
            "Event": "Event",
            "Avg_Daily_Revenue": "Avg daily revenue",
            "Avg_New_Customer_Revenue": "Avg new-customer revenue",
            "Avg_Media_Spend": "Avg media spend",
            "Days": "Days",
        }
    ).style.format({
        "Avg daily revenue": "${:,.0f}",
        "Avg new-customer revenue": "${:,.0f}",
        "Avg media spend": "${:,.0f}",
    }),
    use_container_width=True,
    hide_index=True,
)

# Channel spend
channel_map = {
    "Google": "spend_Google",
    "Meta": "spend_Meta",
    "Awin Affiliate": "Awin_spend",
    "Criteo": "criteo_spend",
    "Microsoft Ads": "microsoft_spend",
    "Outbrain": "cost_outbrain",
    "Influencer": "influencer_spend",
}

channel_spend = pd.DataFrame({
    "Channel": list(channel_map.keys()),
    "Spend": [d[col].sum() for col in channel_map.values()],
})
channel_spend = channel_spend.sort_values("Spend", ascending=True)

fig = px.bar(
    channel_spend,
    x="Spend",
    y="Channel",
    orientation="h",
    title="Paid Media Mix",
    labels={"Spend": "Spend (USD)", "Channel": ""},
    text_auto=".2s",
)
st.plotly_chart(fig, use_container_width=True)

# Google / Meta component view
st.markdown("**Google and Meta component mix**")
component_map = {
    "Google Branded": "spend_Google_Branded",
    "Google Non-Branded": "spend_Google_Non_Branded",
    "Google PMAX": "spend_Google_PMAX",
    "Google Demand Gen": "spend_Google_Demand_Gen",
    "Google Others": "spend_Google_Others",
    "Meta ASC": "spend_Meta_ASC",
    "Meta Retargeting": "spend_Meta_Retargeting",
    "Meta Prospecting": "spend_Meta_Prospecting",
}
component_spend = pd.DataFrame({
    "Component": list(component_map.keys()),
    "Spend": [d[col].sum() for col in component_map.values()],
}).sort_values("Spend", ascending=True)

fig = px.bar(
    component_spend,
    x="Spend",
    y="Component",
    orientation="h",
    title="Platform Component Spend",
    labels={"Spend": "Spend (USD)", "Component": ""},
)
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Acquisition
# -----------------------------
st.subheader("Acquisition & Efficiency")

a, b = st.columns(2)

with a:
    fig = px.scatter(
        d,
        x="Total_Media",
        y="Total_Revenue",
        color="Promotion_Discount",
        hover_data=["Date", "UWG_Mailing", "BFCM_Promo_Effect"],
        title="Revenue vs Total Paid Media Spend",
        labels={
            "Total_Media": "Total Paid Media Spend (USD)",
            "Total_Revenue": "Total Revenue (USD)",
            "Promotion_Discount": "Promotion",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

with b:
    fig = px.scatter(
        d,
        x="spend_Meta",
        y="Revenue_New_Customer",
        color="Promotion_Discount",
        hover_data=["Date", "UWG_Mailing"],
        title="New-Customer Revenue vs Meta Spend",
        labels={
            "spend_Meta": "Meta Spend (USD)",
            "Revenue_New_Customer": "New-Customer Revenue (USD)",
            "Promotion_Discount": "Promotion",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

# Correlation table
corr_cols = [
    "Total_Revenue",
    "Revenue_New_Customer",
    "Total_Media",
    "spend_Google",
    "spend_Meta",
    "Awin_spend",
    "microsoft_spend",
    "criteo_spend",
]
corr = d[corr_cols].corr()["Total_Revenue"].drop("Total_Revenue").sort_values(
    ascending=False
)

corr_df = corr.reset_index()
corr_df.columns = ["Metric", "Correlation_with_Revenue"]

st.dataframe(
    corr_df.style.format({"Correlation_with_Revenue": "{:.2f}"}),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Correlation is descriptive, not causal. Promotions, mailings, seasonality, "
    "media spend and other factors can move together."
)

# -----------------------------
# EDA / data quality
# -----------------------------
st.subheader("Data Quality & Analytical Notes")

q1, q2, q3, q4 = st.columns(4)
q1.metric("Rows", f"{len(d):,}")
q2.metric("Missing values", f"{int(d.isna().sum().sum()):,}")
q3.metric("Duplicate rows", f"{int(d.duplicated().sum()):,}")
q4.metric("Unique dates", f"{d['Date'].nunique():,}")

st.markdown(
    """
**Checks performed in the supplied preprocessing:**
- 852 rows / 23 columns in the Master data.
- Dates run from 1 Apr 2024 to 31 Jul 2026.
- No missing values were reported.
- No duplicate rows were reported.
- Dates were converted to datetime and the expected daily date sequence was checked.
- Google and Meta roll-ups are treated as totals; their component lines are **not** added again.

**Interpretation principle:** this dashboard is exploratory. Differences between event days and non-event days show observed associations in the data; they should not be presented as causal effects without a stronger experimental or statistical design.
"""
)
