# --- Import Required Libraries ---
import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
from google.colab import files

# --- Part 1: Upload CSV File ---
print("📁 Please upload your CSV file:")
uploaded = files.upload()  # Opens a file upload dialog

# Get uploaded file name
file_name = list(uploaded.keys())[0]
print(f"\n✅ File uploaded successfully: {file_name}")

# Read CSV file into DataFrame
df = pd.read_csv(file_name)
print("\n📄 Preview of Uploaded Data:")
print(df.head())

# --- Part 2: Generate PDF Report ---
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=12)

# Report Title
pdf.cell(200, 10, txt="Automated Report: CSV Data Summary", ln=True, align='C')
pdf.ln(10)

# Add table header (dynamically from CSV columns)
for column in df.columns:
    pdf.cell(40, 10, txt=str(column), border=1, align='C')
pdf.ln()

# Add data rows
for index, row in df.iterrows():
    for value in row:
        pdf.cell(40, 10, txt=str(value), border=1, align='C')
    pdf.ln()

# --- Part 3: Smart Visualization (Auto-detect columns) ---
categorical_cols = df.select_dtypes(exclude=['number']).columns
numeric_cols = df.select_dtypes(include=['number']).columns

plt.figure(figsize=(8,6))

if len(categorical_cols) > 0 and len(numeric_cols) > 0:
    plt.bar(df[categorical_cols[0]], df[numeric_cols[0]], color='skyblue')
    plt.title(f'{numeric_cols[0]} by {categorical_cols[0]}')
    plt.xlabel(categorical_cols[0])
    plt.ylabel(numeric_cols[0])
    plt.xticks(rotation=45)

elif len(numeric_cols) >= 2:
    plt.scatter(df[numeric_cols[0]], df[numeric_cols[1]], color='mediumseagreen')
    plt.title(f'{numeric_cols[1]} vs {numeric_cols[0]}')
    plt.xlabel(numeric_cols[0])
    plt.ylabel(numeric_cols[1])

else:
    plt.text(0.5, 0.5, "No suitable data for visualization", ha='center', va='center', fontsize=12)

plt.tight_layout()
plt.savefig('data_plot.png')

# Add chart to PDF
pdf.ln(10)
pdf.image('data_plot.png', x=10, y=pdf.get_y(), w=180)

# --- Part 4: Save & Download PDF ---
output_name = "generated_report.pdf"
pdf.output(output_name)
print(f"\n📘 Report generated successfully as '{output_name}'")

# Download the file automatically
files.download(output_name)
