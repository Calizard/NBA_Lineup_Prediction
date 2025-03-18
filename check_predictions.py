import pandas as pd

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
    print(f"Overall Model Accuracy: {correct_predictions}/{total_predictions} ({accuracy:.2f}%)")
    
    # Calculate accuracy for each year (2007-2016)
    years = range(2007, 2017)  # Years from 2007 to 2016
    for i, year in enumerate(years):
        start = i * 100  # Starting index for the year
        end = start + 100  # Ending index for the year
        correct_predictions_year = (predicted[start:end] == actual[start:end]).sum()
        print(f"Correct predictions for {year}: {correct_predictions_year}/100")

if __name__ == "__main__":
    compare_predictions("nba_predictions.csv", "NBA-Test/NBA_test_labels.csv")