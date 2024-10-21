import os
from colorama import Fore
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Border, PatternFill, Side

# Assume the file directory is defined
file_directory = r"D:\Documents\Custom Office Templates\Desktop\Update Tables Data"
file_path = os.path.join(file_directory, f"Test Updates for v2.3-539.xlsx")

# Define some style objects (colors, borders, etc.)
green_fill = PatternFill(start_color="26DE22", end_color="26DE22", fill_type="solid")
yellow_fill = PatternFill(start_color="F7EC09", end_color="F7EC09", fill_type="solid")
red_fill = PatternFill(start_color="EF4B11", end_color="EF4B11", fill_type="solid")

thick_border = Border(
    left=Side(style="thick"),
    right=Side(style="thick"),
    top=Side(style="thick"),
    bottom=Side(style="thick"),
)


# Function to add the constant header lines at the top of every worksheet
def add_constant_header(ws):
    """
    Adds the constant header rows (status indicators) at the top of the worksheet.
    """
    ws["B2"].fill = green_fill
    ws["C2"] = "Test Passed"
    ws["B3"].fill = yellow_fill
    ws["C3"] = "Test Passed With Some Trouble"
    ws["B4"].fill = red_fill
    ws["C4"] = "Test Failed"


# Function to add or update a test table starting from a specific row
def add_update_table(ws, start_row, tests, ver1, ver2, progress_list):
    """
    Add or update a test table starting at a specific row.
    """
    headers = [f"{ver1}->{ver2}", "Board", "Sensor Hub", "Battery", "Remote", "Notes"]

    # Add the header row for the table
    for col, header in enumerate(headers, start=2):  # Columns B to G
        ws.cell(row=start_row, column=col).value = header

    # Add test rows based on provided data
    for row_idx in range(start_row + 1, start_row + tests + 1):  # 5 rows for data
        ws.cell(row=row_idx, column=2, value="test")  # Version in column B
        ws.cell(
            row=row_idx,
            column=3,
        )  # Version in column C
        for col_idx, progress in enumerate(progress_list, start=3):  # Columns D to G
            ws.cell(row=row_idx, column=col_idx).value = progress
            ws.cell(row=row_idx, column=col_idx).border = thick_border  # Apply border


# Function to update components, ensuring no overwriting of existing content
def update_components(file_path, components_updated, ver1, ver2, progress_list):
    """
    Update an existing workbook without overwriting manually edited content.
    """
    if os.path.exists(file_path):
        # Load the existing workbook
        wb = load_workbook(file_path)
        ws = wb.active  # Assuming updates go to the active sheet
        print(Fore.YELLOW + f"Workbook '{file_path}' found. Updating existing data.")
    else:
        # Create a new workbook and worksheet if it doesn't exist
        wb = Workbook()
        ws = wb.active
        ws.title = f"Updates on v2.3-539"
        print(Fore.YELLOW + f"New workbook created for '{file_path}'.")
        add_constant_header(ws)  # Add header if new workbook

    # Find the next available row to avoid overwriting existing content
    start_row = ws.max_row + 2  # Leave one row gap for spacing

    # Add the update table starting from the next available row
    add_update_table(ws, start_row, components_updated, ver1, ver2, progress_list)

    # Save the updated workbook
    wb.save(file_path)
    print(f"Excel file updated successfully at {file_path}")


# Example usage
if not os.path.exists(file_directory):
    os.makedirs(file_directory)

# Progress list to be inserted into the table
progress_list = ["1", "1", "1", "0", "N/A"]
update_components(file_path, 5, "v2.2", "v2.3", progress_list)
