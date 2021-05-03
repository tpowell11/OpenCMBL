# OpenCMBL by Tom Powell
# 
import lxml.etree
class Column(object):
    "Stores data & atrrributes from LoggerPro Columns"
    def __init__(self,data:list,unit=None):
        self.data = data
        self.unit = unit
class DataSet(object):
    def __init__(self, name:str, id:int):
        self.name = name
        self._ID = id #used to map lines of best fit to datasets
        # ! the number of titles MUST be the same as the
        # ! number of Columns or else things will break
        self.ColumnTitles = []
        self.columns=[] #list[Column]
    def addColumn(self, data:list, unit:str):
        self.columns.append(Column(data,unit))
class cmbl(object):
    def __init__(self, filename:str):
        self.root = lxml.etree.parse(filename)

        self.data = []
        #fields directly from the file
        self.version = float(self.root.find('Version').text)
        self.encoding = str(self.root.find('charset').text)
        self.filename = str(self.root.find('FileName').text)
        self.radians = bool(self.root.find('Radians').text)
        self.creationDate = str(self.root.find("CreationDateTime").text)
        self.modifiedDate = str(self.root.find("ModifiedDateTime").text)
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
        self._name = ""
        self._id = 0
        for instance in self.root.iterfind('.//DataSet'):
            for element in instance.iter("*"):
                #filter out the DataSet of best fit lines
                if element.tag == "DataSetName" and "&&^%" not in element.text:
                    print(element.find("./ID"))
                    self._name = element.text
                    #self.data.append(DataSet(element.text, element.find("ID")))
                if element.tag == "ID" and element.getparent().tag == "DataSet":
                    print(element.text)
                    self.data.append(DataSet(self._name, element.text))
                if element.tag == "DataColumn":
                    _temp = element.find(".//ColumnCells").text.split("\n")
                    del _temp[0] #remove two newlines at beginning and end of data
                    del _temp[-1]
                    self.data[-1].addColumn(_temp,element.find("./ColumnUnits").text)
file = cmbl("test.cmbl")
print(": %s | %s"%(file.data[1]._ID,file.data[1].name))
