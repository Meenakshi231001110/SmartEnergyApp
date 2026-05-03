import pandas as pd
import xml.etree.ElementTree as ET
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import joblib

# Load XML dataset
tree = ET.parse('data.xml')
root = tree.getroot()

# Store records
data = []

# Read XML records
for record in root.findall('record'):
    units = int(record.find('Units_Used').text)
    bill = int(record.find('Bill').text)

    data.append([units, bill])

# Create dataframe
df = pd.DataFrame(data, columns=['Units_Used', 'Bill'])

# Features and target
X = df[['Units_Used']]
y = df['Bill']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save trained model
joblib.dump(model, 'bill_model.pkl')

print("Model trained successfully!")