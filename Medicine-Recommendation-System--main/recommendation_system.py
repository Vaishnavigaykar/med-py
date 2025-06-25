import pandas as pd

# Load the dataset
data = pd.read_csv('dataset/symtoms_df.csv')

# Function to create a mapping of symptoms to diseases
def create_symptom_disease_mapping(data):
    symptom_disease_map = {}
    for index, row in data.iterrows():
        disease = row['Disease']
        symptoms = row[1:].dropna().tolist()  # Get all symptoms, ignoring NaN values
        for symptom in symptoms:
            if symptom not in symptom_disease_map:
                symptom_disease_map[symptom] = []
            symptom_disease_map[symptom].append(disease)
    return symptom_disease_map

# Create the mapping
symptom_disease_map = create_symptom_disease_mapping(data)

# Function to recommend diseases based on input symptoms
def recommend_diseases(input_symptoms):
    recommended_diseases = set()
    for symptom in input_symptoms:
        if symptom in symptom_disease_map:
            recommended_diseases.update(symptom_disease_map[symptom])
    return list(recommended_diseases)

# Example usage
if __name__ == "__main__":
    user_input = ['itching', 'skin_rash']  # Example symptoms
    diseases = recommend_diseases(user_input)
    print("Recommended diseases based on symptoms:", diseases)
