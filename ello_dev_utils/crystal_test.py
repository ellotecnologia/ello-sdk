#coding: utf8
import glob
import os
import re
import sys
from win32com.client import Dispatch

def search(filename):
    app = Dispatch('CrystalRunTime.Application')
    rep = app.OpenReport(filename)
    #tbl = rep.Database.Tables.Item(1)

    rep.enableParameterPrompting = False
    #print rep.sqlquerystring

    if re.search('strzero', rep.sqlquerystring, flags=re.IGNORECASE):
        print '->', filename

for filename in glob.glob("d:/dev/relatorios/Personalizado/*.rpt"):
    #print filename
    search(filename)
    #print "Erro em {0} -> {1}".format(filename, e.message)

#prop = tbl.ConnectionProperties('Password')
#prop.Value = 'masterkey' #sys.argv[1]

#prop = tbl.ConnectionProperties('Data Source')
#prop.Value = 'server'

# tbl.TestConnectivity() should return 1

# clear and set 3 parameters
#rep.ParameterFields.Count
#params = rep.ParameterFields
# params(1).Name
#p1 = params(1)
#p2 = params(2)
#p3 = params(3)

#for param in (p1,p2,p3): param.ClearCurrentValueAndRange()

#p1.AddCurrentValue(1)
#p2.AddCurrentValue(456)
#p3.AddCurrentValue('12/31/99')

#rep.PrintOut(promptUser=False)


# rep.exportoptions()
# rep.export()

# rep.sections(1).name

# rep.reportcomments
# rep.reportauthor


#rep.DiscardSavedData()
#rep.ReadRecords()

#rep.PaperOrientation = crDefaultPaperOrientation
#rep.SelectPrinter cDriverName, cPrinterName, cPort

#rep.enableParameterPrompting = False
#rep.ExportOptions.FormatType = intOutformat
#6=txt tab-delimited
#7=csv
#10=paged text file
#14=doc
#22=Excel ?
#29=Excel 8
#30=xls
#31=pdf
#36=Excel 97

#Rept.ExportOptions.FormatType = 7
#
#‘The following needed for CSV formating
#Rept.ExportOptions.CharFieldDelimiter = “,”
#Rept.ExportOptions.CharStringDelimiter = “‘”
#
#Rept.ExportOptions.DestinationType = 1
#Rept.ExportOptions.DiskFileName = strOutfilepath & strDateVal & “.” & strOutfile
#Rept.ExportOptions.ExcelUseConstantColumnWidth = false
#Rept.Export false
#
#rep.ReportTitle
#rep.Database.Verify()
#
#
#rep.Database.Tables.Count
#rep.Database.Tables(1).Name
#rep.Database.Tables.Item(1).Name
#rep.Database.Tables(1).ConnectionProperties
#
#
#table = rep.Database.Tables(1)
#table.Fields.Count
#table.Fields(1).Name



# ============================================================
# ============================================================

#Set CRReport = New CRAXDRT.Report 
#Set CrxApp = CreateObject("crystalruntime.application") 
#Set CRReport = CrxApp.OpenReport(strReportFile) 
#' Set CRReport.ParameterFields(0) = "ThisKey;" & MyNewKey & ";true" 
#
#' KeepGoing: 
#
#For Each dbTable In CRReport.Database.Tables 
#dbTable.SetLogOnInfo "", MyLocation, "", "" 
#dbTable.Location = MyLocation 
#dbTable.SetDataSource MyLocation 
#Next dbTable 
#CRReport.Database.Verify 
#
#
#CRReport.SQLQueryString = strSQL 
#
#frmReportViewer.Show 
#frmReportViewer.CRViewer1.ReportSource = CRReport 
#frmReportViewer.CRViewer1.ViewReport 
#
