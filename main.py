import streamlit as st
from football_scraper import FootballScraper
from match_simulation import prepare_data, calculate_final_points
from db_manager import EPLTableData
import pandas as pd
import re
import os

# Fetch database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "3306")  # Default MySQL port


def main():
    st.title("Premier League Simulation - Markov Chain")

    # Create a placeholder for status messages
    status_message = st.empty()

    # User input for season
    season = st.text_input("Enter the season (e.g., 2023-2024):")
    check_button = st.button("Check Season and Proceed", use_container_width=True)

    if check_button:
        if not re.match(r"^\d{4}-\d{4}$", season):
            st.error("Invalid season format. Please use YYYY-YYYY format.")
            return

        db = EPLTableData(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        # Database manager
        # try:
        #     # db_config = st.secrets["database"]
        #     db = EPLTableData(
        #         host=DB_HOST,
        #         user=DB_USER,
        #         password=DB_PASSWORD,
        #         database=DB_NAME
        #     )
        # except:    
        #     pass

        # Sanitize season input
        sanitized_season = season.replace("-", "_")

        # Check if the season table exists in the database
        if db.table_exists(f"{sanitized_season}"):
            status_message.success(f"Data for the season {season} already exists in the database.")
            df = db.fetch_data(sanitized_season)
        else:
            status_message.info(f"Data for the season {season} is not available. Scraping data now...")
            
            # Scraper
            scraper = FootballScraper(season=season)
            try:
                df = scraper.scrape_all_teams()
                # df = pd.read_csv('all_teams_matches.csv')
                status_message.success("Data scraped successfully!")

                # Insert the data into the database
                db.insert_dataframe(df)
                status_message.success(f"Data for the season {season} has been saved to the database.")
            except Exception as e:
                status_message.error(f"Error during data scraping: {e}")
                return
        
        # Close the database connection
        db.close_connection()

        # Data preparation
        status_message.success("Preparing data, please wait...")
        prepared_df = prepare_data(df)

        try:
            # Ensure data is not empty
            if df.empty:
                status_message.error("No data available for simulation. Please scrape data first.")
            else:
                # Process data and simulate points
                status_message.success("Simulating points, please wait...")
                results = calculate_final_points(prepared_df, remaining_home_matches=18, remaining_away_matches=19)

                # Display final league table
                final_league_table = results.sort_values(by="EPLPoints", ascending=False)
                status_message.success("Final league table is ready!")
                st.dataframe(final_league_table[["Team", "EPLPoints", "MCPoints"]], use_container_width=True, height=750)

        except Exception as e:
            status_message.error(f"An error occurred during simulation: {e}")


if __name__ == "__main__":
    main()
