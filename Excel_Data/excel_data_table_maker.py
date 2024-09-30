from openpyxl import Workbook, load_workbook
from openpyxl.styles import PatternFill,  Border, Side

import os


green_fill = PatternFill(start_color="26DE22", end_color="26DE22", fill_type="solid")  # Green color
red_fill = PatternFill(start_color="EF4B11", end_color="EF4B11", fill_type="solid")    # Red color
yellow_fill = PatternFill(start_color="F7EC09", end_color="F7EC09", fill_type="solid") # Yellow color

thick_border = Border(left=Side(style='thick'),
                      right=Side(style='thick'),
                      top=Side(style='thick'),
                      bottom=Side(style='thick'))



# Define the path to your desired directory and file
file_directory = r"D:\Documents\Custom Office Templates\Desktop\Update Tables Data"
file_path = os.path.join(file_directory, "test_updates.xlsx")

# Create a new Workbook
wb = Workbook()
ws = wb.active

# Set the title of the active worksheet
ws.title = "Random Test"

ws.column_dimensions['A'].width = 6

for col in ['B', 'C', 'D', 'E', 'F']:
    ws.column_dimensions[col].width = 20

ws.column_dimensions['G'].width = 50

for row in range(1, 51):
    ws.row_dimensions[row].height = 20

ws['B2'].fill = green_fill
ws['C2'] = "Test Passed"

ws['B3'].fill = yellow_fill
ws['C3'] = "Test Passed With Some Trouble"

ws['B4'].fill = red_fill
ws['C4'] = "Test Failed"

ws['B7']= "Version"
ws['C7']= "Board"
ws['D7']= "Sensor Hub"
ws['E7']= "Battery"
ws['F7']= "Remote"
ws['G7']= "Notes"

for row in ws.iter_rows(min_row=7, max_row=12, min_col=2, max_col=7):
    for cell in row:
        cell.border = thick_border
# Check if the directory exists, and create it if not
if not os.path.exists(file_directory):
    os.makedirs(file_directory)

# Save the workbook at the specified path
wb.save(file_path)

print(f"Excel file created successfully at {file_path}")
