import pandas as pd
import xlwt
import xlrd
import os , sys,win32com.client, glob
import os.path, ntpath, shutil, glob


inputWS = raw_input("Enter input workspace folder path: ") # input workspace folder

output_data = r"E:\#InclusionProject\Final_excel_data"  # provide workspace where you want to save final excels
#path = os.getcwd()
path = inputWS


for f in glob.glob("%s/*.xls" % inputWS):
    print f

    dirname = ntpath.basename(f).split('.')[0]
    #print dirname

    
    sur_df = pd.read_excel(f)

    final_data = sur_df[['ID_string','Exp_Area','MAJORITY','MAJ_CLASS']]


    outpath = r"%s\%s.xlsx" % (output_data,dirname)

    writer = pd.ExcelWriter(outpath,engine='xlsxwriter') 
    final_data.to_excel(writer,sheet_name='added_area')
    writer.save()
    print "%s ...........completed" % dirname
    


