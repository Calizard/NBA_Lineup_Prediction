# SOFE 4620U - NBA Lineup Prediction for Optimized Team Performance

## Team 18  
Naftanan Mamo (100822222)  
Calvin Reveredo (100825740)  
Rodney Stanislaus (100822918)

## Project Objectives  
The goal of this project is to design and develop a machine learning model that predicts the optimal fifth player for a home team in an NBA game, given partial lineup data and other game-related features. The model aims to maximize the home team's overall performance by analyzing historical NBA game data.

## Key Objectives
1. ***Data Analysis***: Utilize a dataset containing NBA game lineups from ***2007*** to ***2015***, which includes features such as `season`, `home_team`, `away_team`, `starting_min`, and player identifiers for both home and away teams (`home_0` to `home_4` and `away_0` to `away_4`).
2. ***Feature Engineering***: Preprocess and transform the dataset to extract meaningful features that can be used to train the machine learning model.
3. ***Model Development***: Build a machine learning model that predicts the optimal fifth player for the home team based on partial lineup data and other relevant features.
4. ***Performance Optimization***: Ensure the model maximizes the home team's performance by evaluating its predictions against historical game outcomes.
5. ***Insights and Recommendations***: Provide actionable insights into how teams can optimize their lineups for better performance in future games.

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

## Overview of the Results  
### Model Performance  
The machine learning model achieved an overall accuracy of ***87.40% (874/1000)*** on the provided test data spanning from 2007 to 2016. Below is the breakdown of correct predictions by year:

| Year |	Correct Predictions |	Accuracy |  
| --- | --- | --- |
| 2007 |	93/100  | 93.00% |
| 2008 |	92/100	| 92.00% |
| 2009 |	92/100	| 92.00% |
| 2010 |	96/100	| 96.00% |
| 2011 |	96/100	| 96.00% |
| 2012 |	94/100	| 94.00% |
| 2013 |	98/100	| 98.00% |
| 2014 |	91/100	| 91.00% |
| 2015 |	93/100	| 93.00% |
| 2016 |	29/100	| 29.00% |

### Analysis of 2016 Test Data
The model's performance dropped significantly for the 2016 test data, achieving only ***29.00%*** accuracy. This decline is attributed to the presence of ***41 new players*** in the 2016 dataset who were not part of the training data (2007-2015). Key observations include:

- ***67 rows*** in the 2016 test data contain at least one new player not present in the training dataset.
- ***29 rows*** contain 2 or more new players, ***8 rows*** contain 3 or more new players, and just ***1 row*** contain 4 new players.
- ***6 rows*** had correct labels that were new players, making it impossible for the model to predict those correctly.

### Adjusted Accuracy for 2016
To better understand the model's performance on the 2016 data, we adjusted the accuracy by excluding rows with new players:

1. ***Excluding rows with 2+ new players and impossible predictions (33 rows removed)***:  
   Adjusted accuracy: ***34.32% (23/67)***.

2. ***Excluding all rows with new players (67 rows removed)***:  
   Adjusted accuracy: ***39.39% (13/33)***.

### List of New Players in 2016
The following players were not present in the training dataset and contributed to the lower accuracy in 2016:

> Emmanuel Mudiay, Jonathon Simmons, Larry Nance, Karl-Anthony Towns, Jahlil Okafor, Justise Winslow, Norman Powell, Josh Richardson, Trey Lyles, Xavier Munford, Stanley Johnson, Devin Booker, Willie Cauley-Stein, Lamar Patterson, Kelly Oubre, Tyus Jones, Cameron Payne, T.J. McConnell, Alan Williams, Nikola Jokic, Montrezl Harrell, Terry Rozier, Christian Wood, Jerian Grant, Marcelo Huertas, Julius Randle, Richaun Holmes, Rondae Hollis-Jefferson, Rashad Vaughn, Bobby Portis, Kristaps Porzingis, Willie Reed, Nemanja Bjelica, Myles Turner, Raul Neto, Frank Kaminsky, Chris McCullough, Mario Hezonja, D'Angelo Russell, Jordan McRae, Delon Wright

### Key Challenges  
1. ***New Players***: The presence of players not included in the training dataset significantly impacted the model's ability to make accurate predictions.

2. ***Impossible Predictions***: In cases where the correct label was a new player, the model had no chance of predicting correctly.

3. ***Data Limitations***: The model's performance is constrained by the availability of historical data, particularly for newer players who debuted in 2016.

## Optional: Identifying New Players in 2016 Test Data
For users interested in understanding how the list of new players in the 2016 test data was identified and compared to the training dataset, an optional script is provided. This script analyzes the last 100 rows of the test data (NBA_test.csv) to determine which players were not present in the training dataset (matchups_combined_cleaned.csv). It also identifies rows in the test data that contain these new players.

### Purpose of the Script
The script performs the following tasks:

- Extracts Unique Players from Training Data: Compiles a list of all unique players present in the training dataset.
- Loads and Processes Test Data: Focuses on the last 100 rows of the test data, which correspond to the 2016 season.
- Identifies New Players: Compares the players in the test data against the training dataset to identify new players who were not part of the training data.
- Analyzes Rows with New Players: Identifies specific rows in the test data that contain these new players and provides a detailed breakdown.

Run the script using the command:  
```
python count_players.py
``` 
This script will display the following output:  
- The number of new players in the 2016 test data.
- A list of new players.
- A detailed breakdown of rows containing new players.
