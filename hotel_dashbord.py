import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import logging

# Enable silent logging (optional)
logging.basicConfig(level=logging.ERROR)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("hotel_bookings.csv")

df = load_data()

# Preprocess
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
df['arrival_date'] = pd.to_datetime(df['arrival_date_year'].astype(str) + '-' +
                                    df['arrival_date_month'] + '-' +
                                    df['arrival_date_day_of_month'].astype(str), errors='coerce')

# Sidebar filters
st.sidebar.header("🔍 Filters")
hotel_type = st.sidebar.multiselect("Hotel Type", df['hotel'].unique(), default=df['hotel'].unique())
month = st.sidebar.multiselect("Arrival Month", df['arrival_date_month'].unique(), default=month_order)

df_filtered = df[df['hotel'].isin(hotel_type) & df['arrival_date_month'].isin(month)]

# Page title
st.title("🏨 Hotel Booking Dashboard")

# 1. Booking Cancellation Rate
try:
    st.subheader("📉 Booking Cancellation Rate")
    fig, ax = plt.subplots()
    cancel_rate = df_filtered['is_canceled'].value_counts(normalize=True) * 100
    ax.pie(cancel_rate, labels=['Not Canceled', 'Canceled'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"Cancellation chart error: {e}")

# 2. Bookings by Hotel Type
try:
    st.subheader("🏨 Bookings by Hotel Type")
    fig, ax = plt.subplots()
    sns.countplot(data=df_filtered, x='hotel', palette='pastel', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"Hotel type chart error: {e}")

# 3. Monthly Booking Trends
try:
    st.subheader("📅 Monthly Booking Trends")
    monthly = df_filtered['arrival_date_month'].value_counts().reindex(month_order)
    fig, ax = plt.subplots()
    sns.lineplot(x=monthly.index, y=monthly.values, marker='o', ax=ax)
    ax.set_ylabel("Bookings")
    ax.set_xlabel("Month")
    ax.set_xticklabels(monthly.index, rotation=45, ha='right')
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"Monthly trend chart error: {e}")

# 4. Top 10 Countries
try:
    st.subheader("🌍 Top 10 Countries by Bookings")
    top_countries = df_filtered['country'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_countries.values, y=top_countries.index, palette='mako', ax=ax)
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"Top countries chart error: {e}")

# 5. Lead Time vs Cancellation
try:
    st.subheader("⏱️ Lead Time vs Cancellation")
    fig, ax = plt.subplots()
    sns.boxplot(x='is_canceled', y='lead_time', data=df_filtered, ax=ax)
    ax.set_xticklabels(['Not Canceled', 'Canceled'])
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"Lead time boxplot error: {e}")

# 6. ADR by Hotel
try:
    st.subheader("💰 ADR by Hotel Type")
    fig, ax = plt.subplots()
    sns.boxplot(x='hotel', y='adr', data=df_filtered, palette='Set2', ax=ax)
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"ADR chart error: {e}")

# 7. Market Segment Share
try:
    st.subheader("🎯 Market Segment Share (%)")
    segment = df_filtered['market_segment'].value_counts(normalize=True).mul(100).round(1)
    fig, ax = plt.subplots()
    sns.barplot(x=segment.index, y=segment.values, ax=ax, palette='Set3')
    for i, val in enumerate(segment.values):
        ax.text(i, val + 1, f"{val}%", ha='center')
    ax.set_ylabel("Percentage")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha='right')
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"Market segment error: {e}")

# 8. Distribution Channel Share
try:
    st.subheader("📦 Distribution Channel Share (%)")
    channel = df_filtered['distribution_channel'].value_counts(normalize=True).mul(100).round(1)
    fig, ax = plt.subplots()
    sns.barplot(x=channel.index, y=channel.values, ax=ax, palette='coolwarm')
    for i, val in enumerate(channel.values):
        ax.text(i, val + 1, f"{val}%", ha='center')
    ax.set_ylabel("Percentage")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=20, ha='right')
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"Distribution channel error: {e}")

# 9. Stay Duration Histogram
try:
    st.subheader("🛏️ Stay Duration (Weekday + Weekend)")
    df_filtered['total_stay'] = df_filtered['stays_in_week_nights'] + df_filtered['stays_in_weekend_nights']
    fig, ax = plt.subplots()
    sns.histplot(df_filtered['total_stay'], bins=20, color='teal', ax=ax)
    ax.set_xlabel("Total Nights")
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"Stay duration error: {e}")

# 10. Top 10 Countries by ADR
try:
    st.subheader("🌐 Top 10 Countries by ADR")
    top_adr = df_filtered.groupby('country')['adr'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_adr.values, y=top_adr.index, palette='viridis', ax=ax)
    ax.set_xlabel("Average Daily Rate")
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"Top ADR chart error: {e}")

# 11. Guest Composition
try:
    st.subheader("👨‍👩‍👧‍👦 Guest Composition")
    guests = df_filtered[['adults', 'children', 'babies']].sum()
    fig, ax = plt.subplots()
    sns.barplot(x=guests.index, y=guests.values, palette='Spectral', ax=ax)
    fig.tight_layout()
    st.pyplot(fig)
except Exception as e:
    logging.error(f"Guest composition chart error: {e}")

# Footer
st.markdown("---")
st.markdown("📊 Built with Streamlit | Created by Pravi Jain")
