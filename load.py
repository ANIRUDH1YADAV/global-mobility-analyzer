import pandas as pd
from sqlalchemy import create_engine

# Replace YOUR_PASSWORD with your actual MySQL password
engine = create_engine('mysql+pymysql://root:AN1rudh01@localhost:3306/us_visa_db')

# Load CSV
df = pd.read_csv(r'C:\Users\aniru\Downloads\EasyVisa.csv')
print("CSV loaded! Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Push to MySQL
df.to_sql('visa_applications', con=engine, if_exists='replace', index=False)
print("Done! Rows loaded into MySQL:", len(df))