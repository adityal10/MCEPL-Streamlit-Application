import requests
from bs4 import BeautifulSoup
import pandas as pd
import time


class FootballScraper:
    def __init__(self, season, league: str = "Premier League"):
        """
        Initializes the scraper with a specific season and league.
        """
        self.season = season
        self.league = league
        self.team_codes = {
            'ARSENAL': '18bb7c10',
            'ASTON VILLA': '8602292d',
            'BOURNEMOUTH': '4ba7cbea',
            'BRENTFORD': 'cd051869',
            'BRIGHTON': 'd07537b9',
            'CHELSEA': 'cff3d9bb',
            'CRYSTAL PALACE': '47c64c55',
            'EVERTON': 'd3fd31cc',
            'FULHAM': 'fd962109',
            'IPSWICH TOWN': 'b74092de',
            'LEICESTER CITY': 'a2d435b3',
            'LIVERPOOL': '822bd0ba',
            'MANCHESTER CITY': 'b8fd03ef',
            'MANCHESTER UNITED': '19538871',
            'NEWCASTLE UNITED': 'b2b47a98',
            'NOTTINGHAM FOREST': 'e4a775cb',
            'SOUTHAMPTON': '33c895d4',
            'SPURS': '361ca564',
            'WEST HAM UNITED': '7c21e445',
            'WOLVES': '8cec06e1'
        }
        self.base_url = "https://fbref.com/en/squads"

    def generate_urls(self):
        """
        Generates URLs for all teams in the specified season and league.
        """
        return {
            team: f"{self.base_url}/{code}/{self.season}/matchlogs/c9/schedule/{team.replace(' ', '-')}-Scores-and-Fixtures-{self.league.replace(' ', '-')}"
            for team, code in self.team_codes.items()
        }

    def scrape_team_data(self, team: str, url: str):
        """
        Scrapes match data for a single team from its URL.
        """
        print(f"Scraping data for {team}...")
        try:
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to retrieve data for {team}. Status code: {response.status_code}")
                return []

            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('table', id='matchlogs_for')
            if not table:
                print(f"No match logs table found for {team}.")
                return []

            rows = table.find_all('tr')
            team_data = []
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all(['th', 'td'])
                if cols:
                    team_data.append({
                        "Team": team,
                        "Date": cols[0].text.strip(),
                        "Time": cols[1].text.strip(),
                        "Round": cols[2].text.strip(),
                        "Day": cols[3].text.strip(),
                        "Venue": cols[4].text.strip(),
                        "Result": cols[5].text.strip(),
                        "GF": cols[6].text.strip(),
                        "GA": cols[7].text.strip(),
                        "Opponent": cols[8].text.strip(),
                        "xG": cols[9].text.strip(),
                        "xGA": cols[10].text.strip(),
                        "Possession": cols[11].text.strip(),
                        "Attendance": cols[12].text.strip(),
                        "Captain": cols[13].text.strip(),
                        "Formation": cols[14].text.strip(),
                        "Opp Formation": cols[15].text.strip(),
                        "Referee": cols[16].text.strip(),
                        "Match Report": cols[17].text.strip() if len(cols) > 17 else "",
                    })
            return team_data
        except Exception as e:
            print(f"An error occurred while scraping {team}: {e}")
            return []

    def scrape_all_teams(self, delay: int = 5):
        """
        Scrapes match data for all teams in the league, adding a delay between requests.
        """
        urls = self.generate_urls()
        all_team_data = []

        for team, url in urls.items():
            team_data = self.scrape_team_data(team, url)
            all_team_data.extend(team_data)
            time.sleep(delay)  # Prevent hitting rate limits

        # print(all_team_data)
        return pd.DataFrame(all_team_data)



    def save_to_csv(self, df: pd.DataFrame, filename: str = "all_teams_matches.csv"):
        """
        Saves the DataFrame to a CSV file.
        """
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

# # If running this file directly, you can test the scraper
# if __name__ == "__main__":
#     scraper = FootballScraper()
#     combined_data = scraper.scrape_all_teams()
#     print(combined_data)
#     scraper.save_to_csv(combined_data)