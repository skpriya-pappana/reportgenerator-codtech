# Automated Report Generator Script

import csv
from fpdf import FPDF

# --- Part 1: Read and Analyze Data ---
data_file = 'sales_data.csv'
sales_data = []

try:
    with open(data_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for row in reader:
            sales_data.append(row)
except FileNotFoundError:
    print(f"Error: The file '{data_file}' was not found.")
    exit()

# Perform a simple analysis: calculate total revenue
total_revenue = 0
for row in sales_data:
    try:
        quantity = int(row[1])
        price = float(row[2])
        total_revenue += quantity * price
    except (ValueError, IndexError):
        print(f"Warning: Skipping invalid row: {row}")
        continue

# --- Part 2: Generate Formatted PDF Report ---
# Create an FPDF object
pdf = FPDF('P', 'mm', 'A4')
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Set up font and title
pdf.set_font('Arial', 'B', 16)
pdf.cell(200, 10, 'Automated Sales Report', 0, 1, 'C')
pdf.ln(10)  # Add a line break

# Add a summary section
pdf.set_font('Arial', '', 12)
pdf.cell(200, 10, f'Total Revenue: ${total_revenue:,.2f}', 0, 1)
pdf.ln(5)

# Add a table header for the data
pdf.set_font('Arial', 'B', 12)
pdf.cell(60, 10, 'Product', 1, 0, 'C')
pdf.cell(40, 10, 'Quantity', 1, 0, 'C')
pdf.cell(40, 10, 'Price', 1, 1, 'C')

# Add the data to the table
pdf.set_font('Arial', '', 12)
for row in sales_data:
    pdf.cell(60, 10, row[0], 1, 0)
    pdf.cell(40, 10, row[1], 1, 0)
    pdf.cell(40, 10, f'${float(row[2]):,.2f}', 1, 1)

# Save the PDF to a file
pdf_file_name = 'sales_report.pdf'
pdf.output(pdf_file_name)
print(f"Report generated successfully as '{pdf_file_name}'")