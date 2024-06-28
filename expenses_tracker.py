import os
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv()

IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")  # Replace with your Imgur client ID

def upload_image_to_imgur(image_path):
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}
    with open(image_path, "rb") as image_file:
        data = {"image": image_file.read()}
    response = requests.post("https://api.imgur.com/3/image", headers=headers, files=data)
    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        st.error("Failed to upload image to Imgur")
        return None

def process_receipt(image_url):
    # Example processing function
    # This would be replaced with actual receipt processing logic
    data = {
        "store": "ALDI",
        "date": "28.11.2020",
        "items": [
            {"product_name": "Apfelschorle 0.5l", "quantity": 1, "price": 0.28, "category": "Getränke"},
            {"product_name": "Pfand", "quantity": 1, "price": 0.25, "category": "Getränke"},
            {"product_name": "Delik. Rohschinken QS", "quantity": 1, "price": 2.12, "category": "Fleisch und Wurstwaren"},
            {"product_name": "Dauerwurst QS", "quantity": 1, "price": 1.34, "category": "Fleisch und Wurstwaren"},
            {"product_name": "Hr. Weihnachtspullover", "quantity": 1, "price": 9.69, "category": "Non-Food-Artikel"}
        ]
    }
    return data

def display_header_image():
    # Placeholder for header image
    st.image("https://via.placeholder.com/728x90.png?text=Expenses+Tracker+Header", use_column_width=True)

def calculate_monthly_expenses(df):
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    df['month'] = df['date'].dt.to_period('M')
    monthly_expenses = df.groupby('month')['price'].sum()
    return monthly_expenses

def get_most_expensive_product_last_two_weeks(df):
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    two_weeks_ago = datetime.now() - timedelta(weeks=2)
    recent_purchases = df[df['date'] >= two_weeks_ago]
    if not recent_purchases.empty:
        most_expensive_product = recent_purchases.loc[recent_purchases['price'].idxmax()]
        return most_expensive_product
    return None

def expenses_tracker_page():
    st.title("💸 Expenses Tracker")

    display_header_image()

    # Display existing data
    csv_file_path = "receipt_data.csv"
    if os.path.exists(csv_file_path):
        df = pd.read_csv(csv_file_path)
        st.write("### Existing Expenses Data")
        st.write(df)

        # Monthly expenses line chart
        monthly_expenses = calculate_monthly_expenses(df)
        st.write("### Monthly Expenses")
        st.line_chart(monthly_expenses)

        # Most expensive product in the last two weeks
        most_expensive_product = get_most_expensive_product_last_two_weeks(df)
        if most_expensive_product is not None:
            st.write("### Most Expensive Product in the Last Two Weeks")
            st.write(most_expensive_product)
        else:
            st.write("No purchases in the last two weeks.")

    uploaded_file = st.file_uploader("Choose a receipt image...", type=["jpg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption='Uploaded Receipt', use_column_width=True)

        # Save the uploaded file temporarily
        temp_file_path = "temp_receipt." + uploaded_file.name.split(".")[-1]
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Upload the image to Imgur to get the URL
        image_url = upload_image_to_imgur(temp_file_path)

        if image_url:
            # Process the image URL
            data = process_receipt(image_url)

            # Convert the data to a DataFrame
            df_new = pd.DataFrame(data['items'])
            df_new['store'] = data['store']
            df_new['date'] = data['date']

            # Display the DataFrame
            st.write(df_new)

            # Append the new data to the CSV file
            try:
                existing_df = pd.read_csv(csv_file_path)
                df = pd.concat([existing_df, df_new], ignore_index=True)
            except FileNotFoundError:
                df = df_new

            df.to_csv(csv_file_path, index=False)

            # Provide download link for the CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='receipt_data.csv',
                mime='text/csv',
            )

if __name__ == "__main__":
    expenses_tracker_page()
