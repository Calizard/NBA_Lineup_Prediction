import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Load data
def load_data(file_path):
    return pd.read_csv(file_path)

def generate_training_samples(df):
    training_samples = []

    for i in range(5):  # Mask each of home_0 to home_4
        temp_df = df.copy()
        temp_df["target_player"] = temp_df[f"home_{i}"]  # Store correct player
        temp_df[f"home_{i}"] = "?"  # Mask the player
        training_samples.append(temp_df)

    return pd.concat(training_samples, ignore_index=True)

def preprocess_data(df):
    df = generate_training_samples(df)  # Create training samples

    # Encode categorical features (players)
    player_cols = ["home_0", "home_1", "home_2", "home_3", "home_4",
                   "away_0", "away_1", "away_2", "away_3", "away_4",
                   "target_player"]

    player_encoder = LabelEncoder()

    # Fit label encoder on all players
    all_players = pd.concat([df[col] for col in player_cols])
    unique_players = all_players.unique().tolist()
    unique_players.append("Unknown")  # Add "Unknown" explicitly
    player_encoder.fit(unique_players)

    for col in player_cols:
        df[col] = player_encoder.transform(df[col])

    # Encode team names
    team_cols = ["home_team", "away_team"]
    team_encoder = LabelEncoder()
    team_encoder.fit(df[team_cols].values.ravel())

    for col in team_cols:
        df[col] = team_encoder.transform(df[col])

    # Define feature columns
    features = ["season", "home_team", "away_team", "starting_min",
                "home_0", "home_1", "home_2", "home_3", "home_4",
                "away_0", "away_1", "away_2", "away_3", "away_4"]

    return df, player_encoder, team_encoder, features


# Train the Random Forest model
def train_model(df, features):
    X = df[features]
    y = df["target_player"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=50, max_depth=25, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy against an 80:20 train/test split: {accuracy:.4f}")

    return model

def predict_missing_player(model, df, features, player_encoder, team_encoder):
    # Identify the missing position (which home_X contains "?")
    df["missing_position"] = df[["home_0", "home_1", "home_2", "home_3", "home_4"]].apply(
        lambda row: row[row == "?"].index[0] if any(row == "?") else None, axis=1
    )

    # Encode categorical players (handling unknowns)
    for col in ["home_0", "home_1", "home_2", "home_3", "home_4",
                "away_0", "away_1", "away_2", "away_3", "away_4"]:
        df[col] = df[col].apply(lambda x: x if x in player_encoder.classes_ else "Unknown")
        df[col] = df[col].map(lambda x: player_encoder.transform([x])[0] if x in player_encoder.classes_ else player_encoder.transform(["Unknown"])[0])

    # Encode teams
    for col in ["home_team", "away_team"]:
        df[col] = team_encoder.transform(df[col])

    # Predict the missing player
    df["predicted_player"] = model.predict(df[features])

    # Decode player labels back to names
    df["predicted_player"] = df["predicted_player"].apply(lambda x: player_encoder.inverse_transform([x])[0])

    return df

def compare_predictions(predictions_file, labels_file):
    # Load CSV files
    predictions_df = pd.read_csv(predictions_file)
    labels_df = pd.read_csv(labels_file)
    
    # Extract relevant columns
    predicted = predictions_df["predicted_player"]
    actual = labels_df["removed_value"]
    
    # Calculate overall accuracy
    correct_predictions = (predicted == actual).sum()
    total_predictions = len(predicted)
    accuracy = (correct_predictions / total_predictions) * 100
    print(f"Model Accuracy against provided 2007-2016 test data: {correct_predictions}/{total_predictions} ({accuracy:.2f}%)")
    
    # Calculate accuracy for each year (2007-2016)
    years = range(2007, 2017)  # Years from 2007 to 2016
    for i, year in enumerate(years):
        start = i * 100  # Starting index for the year
        end = start + 100  # Ending index for the year
        correct_predictions_year = (predicted[start:end] == actual[start:end]).sum()
        print(f"Correct predictions for {year}: {correct_predictions_year}/100")

# Main execution
if __name__ == "__main__":
    # Define folder paths
    nba_csv_folder = "NBA-CSV"
    nba_test_folder = "NBA-Test"

    # Load training data
    train_file = os.path.join(nba_csv_folder, "matchups_combined_cleaned.csv")
    train_df = load_data(train_file)

    # Preprocess and train model
    train_df, player_encoder, team_encoder, features = preprocess_data(train_df)
    model = train_model(train_df, features)

    # Load test data and make predictions
    test_file = os.path.join(nba_test_folder, "NBA_test.csv")
    test_df = load_data(test_file)
    predictions = predict_missing_player(model, test_df, features, player_encoder, team_encoder)

    # Save predictions
    predictions.to_csv("nba_predictions.csv", index=False)
    print("Predictions saved to nba_predictions.csv")

    # Report prediction results
    compare_predictions("nba_predictions.csv", "NBA-Test/NBA_test_labels.csv")
