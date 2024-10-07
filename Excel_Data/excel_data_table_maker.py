import os

from openpyxl import Workbook
from openpyxl.styles import Border, PatternFill, Side

# Define fill colors for the status indicators
green_fill = PatternFill(
    start_color="26DE22", end_color="26DE22", fill_type="solid"
)  # Green color
red_fill = PatternFill(
    start_color="EF4B11", end_color="EF4B11", fill_type="solid"
)  # Red color
yellow_fill = PatternFill(
    start_color="F7EC09", end_color="F7EC09", fill_type="solid"
)  # Yellow color

# Define border style for the table cells
thick_border = Border(
    left=Side(style="thick"),
    right=Side(style="thick"),
    top=Side(style="thick"),
    bottom=Side(style="thick"),
)

# Define the path to your desired directory and file
file_directory = r"D:\Documents\Custom Office Templates\Desktop\Update Tables Data"
file_path = os.path.join(file_directory, "test_updates.xlsx")

# Create a new Workbook and select the active worksheet
wb = Workbook()
ws = wb.active
ws.title = "Random Test"


# Function to add the constant header lines at the top of every worksheet
def add_constant_header(ws):
    """
    Adds the constant header rows (status indicators) at the top of the worksheet.

    :param ws: The active worksheet to add the constant headers to.
    """
    ws["B2"].fill = green_fill
    ws["C2"] = "Test Passed"
    ws["B3"].fill = yellow_fill
    ws["C3"] = "Test Passed With Some Trouble"
    ws["B4"].fill = red_fill
    ws["C4"] = "Test Failed"


# Add the constant header to the active worksheet
add_constant_header(ws)

# Set initial column widths for the worksheet
ws.column_dimensions["A"].width = 6
for col in ["B", "C", "D", "E", "F"]:
    ws.column_dimensions[col].width = 20
ws.column_dimensions["G"].width = 50

# Set initial row heights for the worksheet
for row in range(1, 51):
    ws.row_dimensions[row].height = 20


# Function to add a test update table at a specified starting row
def add_update_table(ws, start_row):
    """
    Adds a formatted update table starting from the specified row in the given worksheet.

    :param ws: The active worksheet to add the table to.
    :param start_row: The starting row index for the table.
    """
    # Define the table headers and values
    headers = ["Version", "Board", "Sensor Hub", "Battery", "Remote", "Notes"]

    # Add the header row for the table
    for col, header in enumerate(headers, start=2):  # Columns B to G
        ws.cell(row=start_row, column=col).value = header

    # Create empty rows below the header for data input
    for row_idx in range(start_row + 1, start_row + 6):  # 5 rows for data input
        for col_idx in range(2, 8):  # Columns B to G
            ws.cell(row=row_idx, column=col_idx).border = (
                thick_border  # Apply thick border to each cell
            )


# Add the first table starting at row 7
add_update_table(ws, 7)

# Add a second table 2 rows below the previous one (previous one ends at row 12, so next starts at row 14)
add_update_table(ws, 14)

# Check if the directory exists, and create it if not
if not os.path.exists(file_directory):
    os.makedirs(file_directory)

# Save the workbook at the specified path
wb.save(file_path)

print(f"Excel file created successfully at {file_path}")
