from gspread_formatting import *
import gspread

cred_file = "acadomate-report-7028d1340299.json"
sheet_name = "Acadomate Report"


fmt = cellFormat(
    backgroundColor = color(1, 0.9, 0.9),
    textFormat = textFormat(bold=True, foregroundColor=color(1, 0, 1)),
    horizontalAlignment='CENTER',
    numberFormat = numberFormat(type='PERCENT',pattern="")
    )

gc = gspread.service_account(filename= cred_file)
sh = gc.open(sheet_name)
worksheet1 = sh.worksheet("Result-Test1")
worksheet2 = sh.worksheet("Result-Test2")

# format_cell_range(worksheet1, 'A2:J11', fmt)

header_fmt = get_user_entered_format(worksheet2, "B1")
print("\nheader (before) : ",header_fmt)
header_fmt = cellFormat(
    backgroundColor = color(0.62, 0.77, 0.9),
    textFormat = textFormat(fontSize=11,bold=True)
    )
print("\nheader (after) : ",header_fmt)
format_cell_range(worksheet1, 'A1:H1', header_fmt)


index_fmt = cellFormat(
    textFormat = textFormat(bold=True),
    horizontalAlignment='LEFT'
    )
print("\nindex : ",index_fmt)
format_cell_range(worksheet1, 'A1:A7', index_fmt)

name_fmt = cellFormat(
    backgroundColor = color(0, 1, 1),
    textFormat = textFormat(bold=True)
    )
print("\nname : ",name_fmt)
format_cell_range(worksheet1, 'A2:A6', name_fmt)


avg_fmt = cellFormat(
    backgroundColor = color(0.95, 0.85, 0.85),
    textFormat = textFormat(bold=True,foregroundColor=color(0.65, 0.1, 0.1))
    )
print("\naverage : ",avg_fmt)
format_cell_range(worksheet1, 'A7:H7', avg_fmt)

number_fmt = cellFormat(
    backgroundColor = color(0.7, 0.84, 0.65),
    textFormat = textFormat(foregroundColor=color(0.15, 0.1, 0.3)),
    numberFormat = numberFormat(type='NUMBER',pattern="0")
    )
print("\nnumber : ",number_fmt)
format_cell_range(worksheet1, 'B2:B6', number_fmt)
format_cell_range(worksheet1, 'D2:D6', number_fmt)
format_cell_range(worksheet1, 'F2:F6', number_fmt)

percent_fmt = cellFormat(
    backgroundColor = color(1, 0.9, 0.6),
    textFormat = textFormat(foregroundColor=color(0.5, 0, 0)),
    numberFormat = numberFormat(type='PERCENT',pattern="0.0%")
    )
print("\npercent : ",percent_fmt)
format_cell_range(worksheet1, 'C2:C6', percent_fmt)
format_cell_range(worksheet1, 'E2:E6', percent_fmt)
format_cell_range(worksheet1, 'G2:G6', percent_fmt)

float_fmt = cellFormat(
    numberFormat = numberFormat(type='NUMBER',pattern="0.0")
    )
format_cell_range(worksheet1, 'B7', float_fmt)
format_cell_range(worksheet1, 'D7', float_fmt)
format_cell_range(worksheet1, 'F7', float_fmt)


total_fmt = cellFormat(
    backgroundColor = color(1, 0.95, 0.1),
    textFormat = textFormat(bold=True,foregroundColor=color(1, 0.1, 0.1))
    )
print("\ntotal : ",total_fmt)
format_cell_range(worksheet1, 'H2:H6', total_fmt)

print("\nmixed : ",index_fmt+header_fmt)