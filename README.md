# Premier League Markov Chain Simulation

## Project Overview

This project uses a **Markov Chain model** to predict the final league table for the English Premier League. The predictions are based on team-specific transition matrices derived from match results, which estimate the likelihood of a team winning, drawing, or losing future matches. We've built an interactive **Streamlit application** where users can input a season to analyze. The program fetches data for the selected season, computes predictions, and displays the actual and Markov Chain-predicted points for each team.

---

## What Are Markov Chains?

A **Markov Chain** is a mathematical system that transitions between states based on certain probabilities. The key idea is that the next state depends only on the current state, not the sequence of events that preceded it. 

For example, in football:
- States: Win, Draw, or Loss in a match.
- Transition Probabilities: The likelihood of moving from one state (e.g., a win) to another (e.g., a loss) in the next game.

Markov Chains are represented using **transition matrices**, where each matrix entry shows the probability of transitioning from one state to another.

---

## How We Applied Markov Chains to Football

### Steps:
1. **Extract Match Results**: We gathered match results for each team from historical data.
2. **Create Transition Matrices**:
   - For each team, we calculated probabilities of transitioning between states (Win, Draw, Loss) based on recent match results.
   - Example:
     - If a team won their last match, the matrix shows the probabilities of a win, draw, or loss in the next match.
   - Transition Matrix Example:
     ```
     From/To    Win    Draw    Loss
     Win        0.6    0.3     0.1
     Draw       0.4    0.4     0.2
     Loss       0.2    0.3     0.5
     ```
3. **Simulate Future Matches**:
   - Using these matrices, we simulated the remaining matches in the season for each team.
   - The model estimated how many points each team might earn based on probabilities of wins (3 points), draws (1 point), and losses (0 points).

---

## How the Application Works

### Workflow:
1. **User Input**: 
   - The user enters the season they want to analyze (e.g., "2024-2025").
2. **Data Retrieval**:
   - The application checks if the season's data exists in the database:
     - If **data exists**: It directly uses the data for predictions.
     - If **data does not exist**: The program scrapes match data from the web, saves it to the database, and uses it for predictions.
3. **Simulation**:
   - The application calculates:
     - Actual Premier League points based on match results.
     - Markov Chain-predicted points based on the simulation of future matches.
4. **Display Results**:
   - The final league table is displayed, showing:
     - Team Names
     - Actual Points
     - Markov Chain-Predicted Points

---

## Example Use Case

- User selects **2024-2025** season.
- The program checks if `2024_2025` data is available in the database.
- If data is unavailable:
  1. The program scrapes match results online for the 2024-2025 season.
  2. Saves the data to the database.
- The program computes team-specific transition matrices, simulates the remaining season, and displays the league table with:
  - **Actual Points**: Points from real match results.
  - **Markov Chain Points**: Points predicted using the Markov Chain model.

---

## Key Features

- **Interactive Interface**: Enter any Premier League season and get predictions instantly.
- **Markov Chain Simulation**: Accurate and data-driven predictions for future matches.
- **Dynamic Data Handling**: Automatically fetches data if not available in the database.

---

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```
3. Open the application in your browser and enter the desired season to start your analysis.
