import pandas as pd

# Read the Excel file
input_file = 'hello.xlsx'
df = pd.read_excel(input_file)

# Keep only required columns
df = df[['VulName', 'ImageName', 'Triaged']]

# Filter rows based on 'Triaged' column
df_low = df[df['Triaged'].str.lower() == 'low']
df_medium = df[df['Triaged'].str.lower() == 'medium']
df_high = df[df['Triaged'].str.lower() == 'high']

# Write to a new Excel file with separate sheets
output_file = 'triaged_output.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_low.to_excel(writer, sheet_name='Low', index=False)
    df_medium.to_excel(writer, sheet_name='Medium', index=False)
    df_high.to_excel(writer, sheet_name='High', index=False)

print(f"Data successfully written to {output_file}")
