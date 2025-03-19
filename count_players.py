import pandas as pd

# Load the training CSV file and extract unique players
df = pd.read_csv('NBA-CSV/matchups_combined_cleaned.csv')
players = df[['home_0', 'home_1', 'home_2', 'home_3', 'home_4', 'away_0', 'away_1', 'away_2', 'away_3', 'away_4']]
all_players = pd.concat([players.stack()])
unique_players_first = set(all_players)

# Load the last 100 rows of the test data CSV file
df_test = pd.read_csv('NBA-Test/NBA_test.csv').tail(100)

# Replace "?" with NaN in the player columns
player_columns = ['home_0', 'home_1', 'home_2', 'home_3', 'home_4', 'away_0', 'away_1', 'away_2', 'away_3', 'away_4']
df_test[player_columns] = df_test[player_columns].replace('?', pd.NA)

players_test = df_test[['home_0', 'home_1', 'home_2', 'home_3', 'home_4', 'away_0', 'away_1', 'away_2', 'away_3', 'away_4']]
all_players_test = pd.concat([players_test.stack()])
unique_players_test = set(all_players_test)

# Find new players in the test data that are not in the training file
new_players = unique_players_test - unique_players_first

# Count the number of new players
num_new_players = len(new_players)

print(f"Number of new players in the last 100 rows of test data: {num_new_players}")
print(f"New players: {new_players}")

# Initialize a list to store rows that contain only players from the training set
rows_with_new_players = []

# Iterate through each row in the test data
for index, row in df_test.iterrows():
    # Extract players from the current row, excluding NaN (previously "?")
    home_players = row[['home_0', 'home_1', 'home_2', 'home_3', 'home_4']].dropna().values
    away_players = row[['away_0', 'away_1', 'away_2', 'away_3', 'away_4']].dropna().values
    all_players_in_row = set(home_players) | set(away_players)  # Combine home and away players

    # Find new players in the row that are not in the training set
    new_players_in_row = all_players_in_row - unique_players_first

    # If there are new players, add the row and new players to the list
    if new_players_in_row:
        rows_with_new_players.append({
            'row_number': index + 2,  # Row number
            'new_players': new_players_in_row,
            # 'row_data': row
        })

# Convert the list of rows to a DataFrame for easier viewing
df_new_players = pd.DataFrame(rows_with_new_players)

# Print the results
if not df_new_players.empty:
    print("Rows with new players (not in the training set):")
    for _, row in df_new_players.iterrows():
        print(f"Row {row['row_number']}: New players = {row['new_players']}")
        # print(row['row_data'])
        print("-" * 40)
else:
    print("All rows contain only players from the training set.")