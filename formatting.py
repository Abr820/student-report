from gspread_formatting import *

middle_fmt = cellFormat(
    horizontalAlignment = 'CENTER',
    verticalAlignment = 'MIDDLE',
    wrapStrategy = 'WRAP'
    )

header_fmt = cellFormat(
    verticalAlignment = 'MIDDLE',
    wrapStrategy = 'WRAP',
    backgroundColor = color(0.62, 0.77, 0.9),
    textFormat = textFormat(fontSize=11,bold=True)
    )


index_fmt = cellFormat(
    verticalAlignment = 'MIDDLE',
    wrapStrategy = 'WRAP',
    textFormat = textFormat(bold=True),
    horizontalAlignment='LEFT'
    )

name_fmt = cellFormat(
    backgroundColor = color(0, 1, 1),
    textFormat = textFormat(bold=True)
    )


avg_fmt = cellFormat(
    backgroundColor = color(0.95, 0.85, 0.85),
    textFormat = textFormat(bold=True,foregroundColor=color(0.65, 0.1, 0.1))
    )

number_fmt = cellFormat(
    backgroundColor = color(0.7, 0.84, 0.65),
    textFormat = textFormat(foregroundColor=color(0.15, 0.1, 0.3)),
    numberFormat = numberFormat(type='NUMBER',pattern="0")
    )

percent_fmt = cellFormat(
    backgroundColor = color(1, 0.9, 0.6),
    textFormat = textFormat(foregroundColor=color(0.5, 0, 0)),
    numberFormat = numberFormat(type='PERCENT',pattern="0.0%")
    )

float_fmt = cellFormat(
    numberFormat = numberFormat(type='NUMBER',pattern="0.0")
    )


total_fmt = cellFormat(
    backgroundColor = color(1, 0.95, 0.1),
    textFormat = textFormat(bold=True,foregroundColor=color(1, 0.1, 0.1))
    )

correct_fmt = cellFormat(
    backgroundColor = color(0.7, 0.84, 0.65),
    textFormat = textFormat(foregroundColor=color(0.15, 0.1, 0.3))
    )

wrong_fmt = cellFormat(
    backgroundColor = color(0.8, 0.84, 0.3),
    textFormat = textFormat(foregroundColor=color(0.8, 0.15, 0.3))
    )

na_fmt = cellFormat(
    backgroundColor = color(0.8, 0.65, 0.35),
    textFormat = textFormat(foregroundColor=color(0.1, 0.05, 0.15))
    )

def format_result(am,test_num):
    ws_name = f"Result-Test{test_num}"
    ws = am.get_worksheet(ws_name)
    # r , c = am.get_sheet_dim(ws_name)
    c = len(ws.row_values(1))
    r = len(ws.get_all_values())
    import string
    letters = list(string.ascii_lowercase)
    letters.extend([i+b for i in letters for b in letters])

    batch = batch_updater(ws.spreadsheet)
    batch.format_cell_range(ws, '1', header_fmt)
    batch.format_cell_range(ws, 'A', index_fmt)
    batch.format_cell_range(ws, f'A2:A{r-1}', name_fmt)
    batch.format_cell_range(ws, f'{r}', avg_fmt)

    for col in range(3,c,2):
        batch.format_cell_range(ws, f'{letters[col-2]}2:{letters[col-2]}{r-1}', number_fmt)
        batch.format_cell_range(ws, f'{letters[col-1]}2:{letters[col-1]}{r-1}', percent_fmt)
        batch.set_column_width(ws, f'{letters[col-2]}', 60)
        batch.set_column_width(ws, f'{letters[col-1]}', 60)
        ws.merge_cells(f'{letters[col-2]}1:{letters[col-1]}1', merge_type='MERGE_ALL')

    batch.format_cell_range(ws, f'{letters[c-1]}2:{letters[c-1]}{r}', total_fmt)

    batch.set_column_width(ws, 'A', 180)
    batch.set_frozen(ws, rows=1, cols=1)
    batch.set_column_width(ws, f'{letters[c-1]}', 80)
    batch.format_cell_range(ws,f'B1:{letters[c-1]}{r+1}', middle_fmt)

    batch.execute()