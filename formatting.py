from gspread_formatting import *
import string


letters = list(string.ascii_uppercase)
letters.extend([i+b for i in letters for b in letters])

brd_fmt = cellFormat(
    borders = borders(
        top = border(style='SOLID_THICK'),
        bottom = border(style='SOLID_THICK'),
        left = border(style='SOLID_THICK'),
        right = border(style='SOLID_THICK')
        )
    )

brd_side_fmt = cellFormat(
    borders = borders(
        left = border(style='SOLID'),
        right = border(style='SOLID')
        )
    )

brd_left_fmt = cellFormat(
    borders = borders(
        left = border(style='SOLID_THICK'),
        right = border(style='SOLID')
        )
    )

brd_right_fmt = cellFormat(
    borders = borders(
        left = border(style='SOLID'),
        right = border(style='SOLID_THICK')
        )
    )

brd_sub_fmt = cellFormat(
    borders = borders(
        bottom = border(style='SOLID_MEDIUM'),
        left = border(style='SOLID_MEDIUM'),
        right = border(style='SOLID_MEDIUM')
        )
    )

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

sub_header_fmt = cellFormat(
    verticalAlignment = 'MIDDLE',
    wrapStrategy = 'WRAP',
    backgroundColor = color(0.82, 0.87, 0.95),
    textFormat = textFormat(bold=True,underline=True)
    )


index_fmt = cellFormat(
    verticalAlignment = 'MIDDLE',
    wrapStrategy = 'WRAP',
    textFormat = textFormat(bold=True),
    horizontalAlignment='LEFT'
    )

name_fmt = cellFormat(
    backgroundColor = color(0, 1, 1),
    textFormat = textFormat(bold=True,foregroundColor=color(0, 0, 0))
    )


avg_fmt = cellFormat(
    backgroundColor = color(0.95, 0.85, 0.85),
    textFormat = textFormat(bold=True,foregroundColor=color(0.65, 0.1, 0.1))
    )

number_fmt = cellFormat(
    backgroundColor = color(0.7, 0.84, 0.65),
    textFormat = textFormat(bold=False,foregroundColor=color(0.15, 0.1, 0.3)),
    numberFormat = numberFormat(type='NUMBER',pattern="0")
    )

percent_fmt = cellFormat(
    backgroundColor = color(1, 0.9, 0.6),
    textFormat = textFormat(bold = False,foregroundColor=color(0.5, 0, 0)),
    numberFormat = numberFormat(type='PERCENT',pattern="0.0%")
    )

float_fmt = cellFormat(
    numberFormat = numberFormat(type='NUMBER',pattern="0.0")
    )


total_fmt = cellFormat(
    backgroundColor = color(1, 0.95, 0.1),
    textFormat = textFormat(bold=True,foregroundColor=color(1, 0.1, 0.1)),
    numberFormat = numberFormat(type='PERCENT',pattern="0.0%")
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

def format_report(am,col_type):
    worksheet_name = "Report"
    if col_type == 'topic':
        worksheet_name += "-Topic"
    elif col_type == 'subject':
        worksheet_name += "-Subject"
    elif col_type == 'test':
        worksheet_name += "-Test"

    ws = am.get_worksheet(worksheet_name)
    if ws is None:
        return
    # r , c = am.get_sheet_dim(ws_name)
    c = len(ws.row_values(1))
    r = len(ws.get_all_values())

    batch = batch_updater(ws.spreadsheet)
    batch.format_cell_range(ws, '1', header_fmt+brd_fmt)
    batch.format_cell_range(ws, '2', sub_header_fmt+brd_sub_fmt)
    batch.format_cell_range(ws, 'A', index_fmt+brd_sub_fmt)
    batch.format_cell_range(ws, f'A3:A{r-1}', name_fmt)

    for col in range(1,c,3):
        batch.format_cell_range(ws, f'{letters[col]}3:{letters[col]}{r-1}', correct_fmt+brd_left_fmt)
        batch.format_cell_range(ws, f'{letters[col+1]}3:{letters[col+1]}{r-1}', na_fmt+brd_side_fmt)
        batch.format_cell_range(ws, f'{letters[col+2]}3:{letters[col+2]}{r-1}', wrong_fmt+brd_right_fmt)
        batch.set_column_width(ws, f'{letters[col]}', 50)
        batch.set_column_width(ws, f'{letters[col+1]}', 50)
        batch.set_column_width(ws, f'{letters[col+2]}', 50)


    # batch.format_cell_range(ws, f'{letters[c-3]}2:{letters[c-1]}{r-1}', total_fmt)

    batch.format_cell_range(ws, f'{r}', avg_fmt+brd_fmt)

    batch.set_column_width(ws, 'A', 180)
    batch.set_frozen(ws, rows=2, cols=1)
    # batch.set_column_width(ws, f'{letters[c-1]}', 80)
    batch.format_cell_range(ws,f'B1:{letters[c-1]}{r}', middle_fmt)
    if col_type == 'topic':
        batch.format_cell_range(ws,f'B3:{letters[c-1]}{r-1}', cellFormat(numberFormat = numberFormat(type='NUMBER',pattern="0")))
        batch.format_cell_range(ws,f'{r}', cellFormat(numberFormat = numberFormat(type='NUMBER',pattern="0.0")))
    else:
        batch.format_cell_range(ws,f'B3:{letters[c-1]}{r}', cellFormat(numberFormat = numberFormat(type='PERCENT',pattern="0.0%")))

    batch.execute()

    #unmerge the previous merging before merge again
    ws.unmerge_cells(1,1,r,c+2)

    for col in range(1,c,3):
        ws.merge_cells(f'{letters[col]}1:{letters[col+2]}1', merge_type='MERGE_ALL')
    ws.merge_cells('A1:A2', merge_type='MERGE_ALL')

def format_result(am,test_num):
    ws_name = f"Result-Test{test_num}"
    ws = am.get_worksheet(ws_name)
    if ws is None:
        return
    c = len(ws.row_values(1))
    r = len(ws.get_all_values())

    batch = batch_updater(ws.spreadsheet)
    batch.format_cell_range(ws, '1', header_fmt+brd_fmt)
    batch.format_cell_range(ws, '2', sub_header_fmt+brd_sub_fmt)
    batch.format_cell_range(ws, 'A', index_fmt+brd_sub_fmt)
    batch.format_cell_range(ws, f'A3:A{r-1}', name_fmt)

    for col in range(3,c,2):
        batch.format_cell_range(ws, f'{letters[col-2]}3:{letters[col-2]}{r-1}', number_fmt+brd_left_fmt)
        batch.format_cell_range(ws, f'{letters[col-1]}3:{letters[col-1]}{r-1}', percent_fmt+brd_right_fmt)
        batch.set_column_width(ws, f'{letters[col-2]}', 60)
        batch.set_column_width(ws, f'{letters[col-1]}', 60)
        batch.format_cell_range(ws, f'{letters[col-2]}{r}', cellFormat(numberFormat = numberFormat(type='NUMBER',pattern="0.0")))
        batch.format_cell_range(ws, f'{letters[col-1]}{r}', cellFormat(numberFormat = numberFormat(type='PERCENT',pattern="0.0%")))

    batch.format_cell_range(ws, f'{letters[c-1]}3:{letters[c-1]}{r}', total_fmt+brd_fmt)
    batch.format_cell_range(ws, f'{r}', avg_fmt+brd_fmt)

    batch.set_column_width(ws, 'A', 180)
    batch.set_frozen(ws, rows=2, cols=1)
    batch.set_column_width(ws, f'{letters[c-1]}', 80)
    batch.format_cell_range(ws,f'B1:{letters[c-1]}{r}', middle_fmt)

    batch.execute()

    #unmerge the previous merging before merge again
    ws.unmerge_cells(1,1,r,c+2)

    for col in range(3,c,2):
        ws.merge_cells(f'{letters[col-2]}1:{letters[col-1]}1', merge_type='MERGE_ALL')
    ws.merge_cells('A1:A2', merge_type='MERGE_ALL')
    ws.merge_cells(f'{letters[c-1]}1:{letters[c-1]}2', merge_type='MERGE_ALL')

def format_response(am):
    ws_name = "Responses"
    ws = am.get_worksheet(ws_name)
    if ws is None:
        return
    c = len(ws.row_values(1))
    r = len(ws.get_all_values())

    batch = batch_updater(ws.spreadsheet)
    batch.format_cell_range(ws, '1', header_fmt+brd_fmt)
    batch.format_cell_range(ws, 'A', index_fmt+brd_sub_fmt)
    batch.format_cell_range(ws, f'A2:A{r}', name_fmt)

    for col in range(1,c,1):
        batch.set_column_width(ws, f'{letters[col-1]}', 70)

    batch.set_column_width(ws, 'A', 180)
    batch.set_frozen(ws, rows=1, cols=1)
    batch.format_cell_range(ws,f'B1:{letters[c-1]}{r}', middle_fmt)

    rule = ConditionalFormatRule(
        ranges=[GridRange.from_a1_range(f'B2:{letters[c-1]}{r}', ws)],
        booleanRule=BooleanRule(
                condition=BooleanCondition('NOT_BLANK'),
                format=correct_fmt
            )
        )

    rules = get_conditional_format_rules(ws)
    rules.append(rule)

    batch.execute()
    rules.save()

def format_answer(am):
    ws_name = "Answers"
    ws = am.get_worksheet(ws_name)
    if ws is None:
        return
    c = len(ws.row_values(1))
    r = len(ws.get_all_values())

    batch = batch_updater(ws.spreadsheet)
    batch.format_cell_range(ws, '1', header_fmt+brd_fmt)
    batch.format_cell_range(ws, 'A', index_fmt+brd_sub_fmt)
    batch.format_cell_range(ws, f'A2:A{r}', name_fmt)

    batch.format_cell_range(ws, f'B2:B{r}', correct_fmt+brd_side_fmt)
    batch.set_column_width(ws, 'B', 70)
    
    batch.format_cell_range(ws, f'C2:C{r}', na_fmt)
    batch.set_column_width(ws, 'C', 1500)

    batch.set_column_width(ws, 'A', 80)
    batch.set_frozen(ws, rows=1, cols=1)
    batch.format_cell_range(ws,'B', middle_fmt)
    batch.format_cell_range(ws,'C', cellFormat(horizontalAlignment = 'LEFT',wrapStrategy = 'WRAP'))

    batch.execute()

def format_fundamental(am):
    ws_name = "Fundamental"
    ws = am.get_worksheet(ws_name)
    if ws is None:
        return
    c = len(ws.row_values(1))
    r = len(ws.get_all_values())

    batch = batch_updater(ws.spreadsheet)
    batch.format_cell_range(ws, '1', header_fmt+brd_fmt)
    batch.format_cell_range(ws, 'A', index_fmt)

    for col in range(1,c,1):
        batch.set_column_width(ws, f'{letters[col]}', 165)

    batch.set_column_width(ws, 'A', 60)
    batch.set_frozen(ws, rows=1, cols=0)
    batch.format_cell_range(ws,f'A1:{letters[c-1]}{r}', middle_fmt)

    rule = ConditionalFormatRule(
        ranges=[GridRange.from_a1_range(f'A2:{letters[c-1]}{r}', ws)],
        booleanRule=BooleanRule(
                condition=BooleanCondition('NOT_BLANK'),
                format=correct_fmt+cellFormat(textFormat = textFormat(bold=True))
            )
        )

    rules = get_conditional_format_rules(ws)
    rules.append(rule)

    batch.execute()
    rules.save()

def format_all(am):
    col_types = ['topic','subject','test']
    for rep in col_types:
        format_report(am,rep)
    
    tests = am.get_tests()
    for t in tests:
        format_result(am,t)
    
    format_answer(am)
    format_response(am)
    format_fundamental(am)