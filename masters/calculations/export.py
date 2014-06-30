from openpyxl.writer.excel import save_virtual_workbook
from openpyxl import Workbook
from openpyxl.cell import get_column_letter

class ExportToExcel(object):
    def __init__(self, data):
        self.data = data
        self.wb = Workbook()

    def write_summary(self):
        # The summary will always be the first worksheet
        ws = self.wb.active
        ws.title = "Reactor Summary"
        summary_data = self.data["summary"]

        _r = 1
        for k, v in summary_data.iteritems():
            _c = 1
            col = get_column_letter(_c)
            ws.cell('%s%s'%(col, _r)).value = k
            _r += 1
            for k_2, v_2 in v.iteritems():
                col = get_column_letter(_c)
                ws.cell('%s%s'%(col, _r)).value = k_2
                ws.cell('%s%s'%(col, _r+1)).value = v_2  # _r + 1 so that data can be in bottom
                _c += 1
            _r += 3  # Leaving a space and accomodating for _r+1 above

    def write_general_data(self, ws, data):
        _r = 2
        for row in data:
            col = get_column_letter(1)  # Assuming 1st entry is for Time
            ws.cell('%s%s'%(col, _r)).value = row["step"]
            if _r == 2: # First pas through the loop need to update the header
                ws.cell('%s%s'%(col, 1)).value = "Time (Min)"
            _c = 2
            for k, v in row["ions"].iteritems():
                col = get_column_letter(_c) # Reserver first column for step
                if _r == 2: # First pas through the loop need to update the header
                    ws.cell('%s%s'%(col, 1)).value = k
                ws.cell('%s%s'%(col, _r)).value = v
                _c += 1
            _r += 1

    def write_bioxidation(self):
        biox_ws = self.wb.create_sheet()
        biox_ws.title = "Bioxidation Data"

        biox_data = self.data["bioxidation"]
        self.write_general_data(biox_ws, biox_data)

    def write_chemical(self):
        chem_ws = self.wb.create_sheet()
        chem_ws.title = "Chemical Data"

        chem_data = self.data["chemical"]
        self.write_general_data(chem_ws, chem_data)

    def run(self):
        self.write_summary()
        self.write_bioxidation()
        self.write_chemical()
        # Export to Django
        return save_virtual_workbook(self.wb)
