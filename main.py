import streamlit as st
from football_scraper import FootballScraper
from match_simulation import prepare_data, calculate_final_points
from db_manager import EPLTableData
import pandas as pd
import re

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

        # Database manager
        try:
            db_config = st.secrets["database"]
            db = EPLTableData(
                host=db_config["host"],
                user=db_config["user"],
                password=db_config["password"],
                database=db_config["database"]
            )
        except:    
            db = EPLTableData(
                host='localhost',
                user='root',
                password='aditya',
                database='plmc'
            )

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



# import streamlit as st
# from football_scraper import FootballScraper
# from match_simulation import prepare_data, calculate_final_points
# from db_manager import EPLTableData
# import pandas as pd

# def main():
#     st.title("Premier League Simulation")

#     # Scraper instance
#     scraper = FootballScraper()

#     # Get user input for the season year
#     season_input = st.text_input("Enter the season year (e.g., 2023, 2024):", value="2024")
#     if st.button("Get Markov Chain Predicted Premier League Table", use_container_width=True):
#         # Check if the season exists in the database
#         db = EPLTableData(
#             host="localhost",
#             user="root",
#             password="aditya",
#             database="plmc"
#         )

#         # Check if the data for the given season is already in the database
#         season = int(season_input)
#         existing_data = db.fetch_data(season)

#         if existing_data.empty:
#             st.write(f"Season {season} not found in the database. Scraping data...")
#             st.write("Please wait while we scrape and save the data...")

#             # Scrape and save data if not found
#             df = scraper.scrape_all_teams()  # You can enable this when needed.
#             # df = pd.read_csv('all_teams_matches.csv')  # Or keep this for local data

#             # Insert the scraped data into the database
#             db.insert_dataframe(df)
#             st.success(f"Data for season {season} scraped and saved successfully!")
#         else:
#             st.write(f"Season {season} found in the database. Fetching data...")

#         # Fetch the data for the season
#         # retrieved_data = db.fetch_data(season)

#         # Close the database connection
#         db.close_connection()

#         # Data preparation
#         prepared_df = prepare_data(existing_data)

#         st.write("Simulating points, please wait...")

#         try:
#             # Ensure data is not empty
#             if prepared_df.empty:
#                 st.error("No data available for simulation. Please scrape data first.")
#             else:
#                 # Process data and simulate points
#                 final_table = calculate_final_points(prepared_df, remaining_home_matches=18, remaining_away_matches=19)

#                 # Display simulation results
#                 st.success("Points simulation completed!")

#                 # Display only the final league table
#                 # final_table = results[['Team', 'EPLPoints', 'MCPoints']]  # Adjust based on the actual result column names
#                 st.dataframe(final_table, use_container_width=True, height=750)

#         except Exception as e:
#             st.error(f"An error occurred during simulation: {e}")

# if __name__ == "__main__":
#     main()