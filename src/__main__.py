# OpenCMBL by Tom Powell (c) 2021
# Main file
import lxml.etree
class Column(object):
    "Stores data & atrrributes from LoggerPro Columns"
    def __init__(self,data:list,unit=None):
        self.data:list[float] = data
        self.unit:str = unit
class DataSet(object):
    def __init__(self, name:str, id:int):
        self.name:str = name
        self._ID:int = id
        #! the number of titles MUST be the same as the
        #! number of Columns or else things will break
        self.ColumnTitles:list[str] = []
        self.columns:list[Column]=[]
    def addColumn(self, data:list, unit:str):
        self.columns.append(Column(data,unit))
class cmbl(object):
    def __init__(self, filename:str):
        self.root = lxml.etree.parse(filename)
        self.data:list[DataSet] = []
        #fields directly from the file
        #* these elements only appear once in the file
        #* therefore, the 'find any in tree' specifier can be used
        self.version = float(self.root.find('.//Version').text)
        self.charset = str(self.root.find('.//charset').text)
        self.filename = str(self.root.find('.//FileName').text)
        self.radians = bool(self.root.find('.//Radians').text)
        self.creationDate = str(self.root.find(".//CreationDateTime").text)
        self.modifiedDate = str(self.root.find(".//ModifiedDateTime").text)
        #graph options
        self.graphTitle = str(self.root.find(".//GraphTitle").text)
        self.gXLabel = str(self.root.find(".//GraphPlotXLabel").text)
        self.gYLabel = str(self.root.find(".//GraphPlotYLabel").text)
        self.isLogX = bool(self.root.find(".//LogXAxis").text)
        self.isLogY = bool(self.root.find(".//LogYAxis").text)
        self.isScatter = bool(self.root.find(".//GraphConnectLines").text)
        self.isBar = bool(self.root.find(".//GraphBarGraph").text)
        self.isDualAxis = bool(self.root.find(".//LogRightYAxis").text) #FIXME
        self.gxmin = float(self.root.find(".//GraphPlotXMin").text)
        self.gxmax = float(self.root.find(".//GraphPlotXMax").text)
        self.gymin = float(self.root.find(".//GraphPlotYMin").text)
        self.gymax = float(self.root.find(".//GraphPlotYMax").text)

        #dataset extraction
        #* _name & _id are internal state, dont use externally
        self._name = ""
        self._id = 0
        for instance in self.root.iterfind('.//DataSet'):
            for element in instance.iter("*"):
                if element.tag == "DataSetName" and "&&^%" not in element.text: 
                    #* Loggerpro uses the DataSetName property to differentiate between
                    #* actual data and user-added lines of best fit. This is a filter for that.
                    self._name = element.text
                if element.tag == "ID" and element.getparent().tag == "DataSet":
                    self.data.append(DataSet(self._name, element.text))
                if element.tag == "DataColumn":
                    _temp = element.find(".//ColumnCells").text.split("\n")
                    del _temp[0] #* due to the way the xml file is written, two newlines need to be removed from the data
                    del _temp[-1] #* these are located at the beginning and end of the splitted text
                    _temp = [float(val) for val in _temp] # swap strs for floats
                    self.data[-1].addColumn(_temp,element.find("./ColumnUnits").text)
file = cmbl("test.cmbl")
