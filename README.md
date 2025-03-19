# SOFE 4620U - NBA Lineup Prediction for Optimized Team Performance

## Team 18  
Naftanan Mamo (100822222)  
Calvin Reveredo (100825740)  
Rodney Stanislaus (100822918)

## Project Objectives  
The goal of this project is to design and develop a machine learning model that predicts the optimal fifth player for a home team in an NBA game, given partial lineup data and other game-related features. The model aims to maximize the home team's overall performance by analyzing historical NBA game data.

## Key Objectives
1. **Data Analysis**: Utilize a dataset containing NBA game lineups from ***2007*** to ***2015***, which includes features such as `season`, `home_team`, `away_team`, `starting_min`, and player identifiers for both home and away teams (`home_0` to `home_4` and `away_0` to `away_4`).
2. **Feature Engineering**: Preprocess and transform the dataset to extract meaningful features that can be used to train the machine learning model.
3. **Model Development**: Build a machine learning model that predicts the optimal fifth player for the home team based on partial lineup data and other relevant features.
4. **Performance Optimization**: Ensure the model maximizes the home team's performance by evaluating its predictions against historical game outcomes.
5. **Insights and Recommendations**: Provide actionable insights into how teams can optimize their lineups for better performance in future games.

## Instructions for Setting Up and Running the Code  
This section provides step-by-step instructions to set up the project environment, install dependencies, and run the code.

### Prerequisites
Before running the code, ensure you have the following installed:
- Python 3.x
- pip (Python package manager)

### Step 1: Clone the Repository
Clone the repository to your local machine using the following command:
```
git clone https://github.com/Calizard/NBA_Lineup_Prediction.git  
```
```
cd NBA_Lineup_Prediction
```
### Step 2: Set Up a Virtual Environment (Optional but Recommended)
To avoid conflicts with other Python projects, it is recommended to create a virtual environment:
```
python -m venv venv
.\venv\Scripts\activate
```
### Step 3: Install Required Libraries
Run the following command to install the required libraries:
```
pip install pandas scikit-learn logging
```
### Step 4: Run the Preprocessing Script (OptionaL)
If you want to run the dataset preprocessing step again, remove the matchups_combined_cleaned.csv file from NBA-CSV folder, and run the process_csv.py script to preprocess the data and generate the cleaned dataset (Note: this file is already provided in the repo):  
```
python process_csv.py
```
This script will:
- Filter out rows with -1 outcomes from the 2007-2015 matchup CSV files.  
- Combine all datasets into a single cleaned file (matchups_combined_cleaned.csv) in the NBA-CSV folder.  

### Step 5: Run the Lineup Prediction Script
Run the nba_lineup_prediction.py script to train the model, make predictions, and evaluate the results:
```
python nba_lineup_prediction.py
```
This script will:

1. Load the training data from matchups_combined_cleaned.csv.
2. Preprocess the data and train a RandomForestClassifier model.
3. Load the test data from NBA_test.csv.
4. Make predictions for the optimal fifth player for the home team.
5. Save the predictions to a CSV file for manual viewing.
6. Report the prediction accuracy based on the provided labels in NBA_test_labels.csv, indicating the number of matchs per year and across the dataset.
