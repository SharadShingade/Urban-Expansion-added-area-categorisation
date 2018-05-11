import sys, time, os, win32com.client, glob, arcpy, numpy, random, shapefile
import os.path, ntpath, shutil, glob






arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension('spatial')
tempWS = r"F:\Inclusion\Temp"   # provide temporary workspace
arcpy.env.scratchWorkspace = tempWS
arcpy.env.extent =""


   
raw_data = r"E:\#InclusionProject\Output"  # provide ULA output folder path, Note Data folder str: Output\CITYNAME folder

circle_file = r"E:\#InclusionProject\CIRCLE" # provide Halton Circle files path, Note Data folder str: CIRCLE\CITYNAME folder 

centriod_data = r"E:\#InclusionProject\Halton_centriod" # provide path to save halton circle T1 and T2 files

merged_data = r"E:\#InclusionProject\Merged_data"  # provide path to save locale majority merged files

reclassWS = r"E:\#InclusionProject\Reclass"        # provide path to save reclassified files

dbaseWS = r"E:\#InclusionProject\Dbase_table"       # provide path to save Dbase files

Excel_data = r"E:\#InclusionProject\Excelsheet"    # provide path to export merged locale file in to excel note
                                           # Note: this file is raw we need to extract only specific column for this
                                           # refer excel_processing_v1.py script

basepath = os.path.basename

for current_data_dir in os.listdir(raw_data):

    dirname = ntpath.basename(current_data_dir)
    print dirname

    Development_t1_t2 = r"%s\%s\New_Development_t1_t2.img" % (raw_data,current_data_dir)
    Development_t2_t3 = r"%s\%s\New_Development_t2_t3.img" % (raw_data,current_data_dir)
    inclusion_2 = r"%s\%s\inclusion_t2.img" % (raw_data,current_data_dir)
    inclusion_3 = r"%s\%s\inclusion_t3.img" % (raw_data,current_data_dir)

    city_urbft_t1 = r"%s\%s\city_urbFootprint_clp_t1.img" % (raw_data,current_data_dir)
    city_urbft_t2 = r"%s\%s\city_urbFootprint_clp_t2.img" % (raw_data,current_data_dir)
    

    #break
    

    #print Development_t1_t2

    #floornames = [os.path.basename(x) for x in glob.glob(r"%s\%s\%s_*.shp" %(circle_file,dirname,dirname))]
    halton_files = [x for x in glob.glob(r"%s\%s\%s_*.shp" %(circle_file,dirname,dirname))]
    
    #print floornames
    #print halton_files # absolute path as it is
    for halton in halton_files:
        halton = halton # use halton[:-4] if you want to remove ".shp" from your shapefile path 
        #print halton

    # halton circle to halton centriod

    inFeatures = halton
    outFeatureClass_1 = r"%s\%s_t1.shp" % (centriod_data,dirname)
    outFeatureClass_2 = r"%s\%s_t2.shp" % (centriod_data,dirname)
    
    #halton_point = arcpy.FeatureToPoint_management(inFeatures, outFeatureClass, "CENTROID")

    #arcpy.AddField_management(halton_point, "Added_area", "TEXT", field_length= 30)

    arcpy.MakeFeatureLayer_management(inFeatures,"halton_lyr")

    arcpy.SelectLayerByAttribute_management ("halton_lyr", "NEW_SELECTION", "Exp_Area = 'T1'")
    halton_t1 = arcpy.CopyFeatures_management("halton_lyr", outFeatureClass_1)

    arcpy.SelectLayerByAttribute_management ("halton_lyr", "NEW_SELECTION", "Exp_Area = 'T2'")
    halton_t2 = arcpy.CopyFeatures_management("halton_lyr", outFeatureClass_2)

    ##############################################

    # reclassifying built-up existing area

    urbft_RemapVal = arcpy.sa.RemapValue([[1,1],[2,1],[3,1],[4,"NODATA"],[5,"NODATA"],[6,"NODATA"],[7,"NODATA"]])

    outReclassify_t1 = arcpy.sa.Reclassify(city_urbft_t1, "VALUE",urbft_RemapVal, "NODATA")
    city_urbft_t1_file = outReclassify_t1.save(r"%s\%s_urbft_t1_remap.img" % (reclassWS,dirname))

    ## 

    outReclassify_t2 = arcpy.sa.Reclassify(city_urbft_t2, "VALUE",urbft_RemapVal, "NODATA")
    city_urbft_t2_file = outReclassify_t1.save(r"%s\%s_urbft_t2_remap.img" % (reclassWS,dirname))


    # reclassifying New_DEVloment file

    New_DEV_RemapVal = arcpy.sa.RemapValue([[0,"NODATA"],[1,2],[2,3],[3,4]])
    #New_DEV_RemapVal = arcpy.sa.RemapValue([[0,0],[1,2],[2,3],[3,4]])
    #New_DEV_RemapVal = arcpy.sa.RemapValue([[2,2],[3,3],[4,4]])


    Devlt_t1_t2 = arcpy.sa.Reclassify(Development_t1_t2, "VALUE",New_DEV_RemapVal, "NODATA")
    Devlt_t1_t2_file = Devlt_t1_t2.save(r"%s\%s_Devlt_t1_t2_remap.img" % (reclassWS,dirname))

    Devlt_t2_t3 = arcpy.sa.Reclassify(Development_t2_t3, "VALUE",New_DEV_RemapVal, "NODATA")
    Devlt_t2_t3_file = Devlt_t2_t3.save(r"%s\%s_Devlt_t2_t3_remap.img" % (reclassWS,dirname))

    # reclassifying inclusion

    Inclusion_RemapVal = arcpy.sa.RemapValue([[0,"NODATA"],[1,5]])


    Inclus_t2 = arcpy.sa.Reclassify(inclusion_2, "VALUE",Inclusion_RemapVal, "NODATA")
    Inclus_t2_file = Inclus_t2.save(r"%s\%s_Inclus_t2_remap.img" % (reclassWS,dirname))

    Inclus_t3 = arcpy.sa.Reclassify(inclusion_3, "VALUE",Inclusion_RemapVal, "NODATA")
    Inclus_t3_file = Inclus_t3.save(r"%s\%s_Inclus_t3_remap.img" % (reclassWS,dirname))


    ## merge raster

    output_location = r"%s" % reclassWS
    output_file_t1 = r"%s_t1_mosiac.img" % dirname

    urb_1 = r"%s\%s_urbft_t1_remap.img" % (reclassWS,dirname)
    Dev_1 = r"%s\%s_Devlt_t1_t2_remap.img" % (reclassWS,dirname)
    Incl_1 = r"%s\%s_Inclus_t2_remap.img" % (reclassWS,dirname)


    List_data_t1 = [urb_1,Dev_1,Incl_1]
    invalueRaster_t1 = arcpy.MosaicToNewRaster_management(List_data_t1,output_location, output_file_t1,"","8_BIT_UNSIGNED", "30", "1", "MAXIMUM","FIRST")

    ##

    output_file_t2 = r"%s_t2_mosiac.img" % dirname

    urb_2 = r"%s\%s_urbft_t2_remap.img" % (reclassWS,dirname)
    Dev_2 = r"%s\%s_Devlt_t2_t3_remap.img" % (reclassWS,dirname)
    Incl_2 = r"%s\%s_Inclus_t3_remap.img" % (reclassWS,dirname)

    List_data_t2 = [urb_2,Dev_2,Incl_2]
    invalueRaster_t2 = arcpy.MosaicToNewRaster_management(List_data_t2,output_location, output_file_t2,"","8_BIT_UNSIGNED", "30", "1", "MAXIMUM","FIRST")

    ## Zonal majority class

    #inZoneData = "zones.shp"
    #zoneField = "Classes"
    #inValueRaster = "valueforzone" dbaseWS
    #invalueRaster_t1 = r"%s\%s_t1_mosiac.img" %(reclassWS,dirname)
    outTable_t1 = r"%s\%s_t1_dbase.dbf" % (dbaseWS,dirname)
    # Execute ZonalStatisticsAsTable
    majority_t1 = arcpy.sa.ZonalStatisticsAsTable(outFeatureClass_1,"ID_string", invalueRaster_t1,outTable_t1,"DATA","MAJORITY")

    outTable_t2 = r"%s\%s_t2_dbase.dbf" % (dbaseWS,dirname)
    majority_t2 = arcpy.sa.ZonalStatisticsAsTable(outFeatureClass_2,"ID_string", invalueRaster_t2,outTable_t2,"DATA","MAJORITY")


    ### join data with halton shapefile
    #T1

    outjoin_t1 = r"%s\%s_t1_join.shp" % (centriod_data,dirname)
    

    arcpy.JoinField_management(outFeatureClass_1, "ID_string", outTable_t1, "ID_string")
    halton_t1_join = arcpy.CopyFeatures_management(outFeatureClass_1, outjoin_t1)

    # T2


    outjoin_t2 = r"%s\%s_t2_join.shp" % (centriod_data,dirname)
    

    arcpy.JoinField_management(outFeatureClass_2, "ID_string", outTable_t2, "ID_string")
    halton_t2_join = arcpy.CopyFeatures_management(outFeatureClass_2, outjoin_t2)

    

    ### Merge joined data

    merged_files = r"%s\%s_merged_final" % (merged_data,dirname)
    
    arcpy.Merge_management([halton_t1_join,halton_t2_join], merged_files)

    print "Merged all files..congrats"

    ### Add field and Calculate Majority pixel class

    merged_files_shape = r"%s\%s_merged_final.shp" % (merged_data,dirname)
    fieldName = "MAJ_CLASS"
    expression = "getClass(!MAJORITY!)"

    arcpy.AddField_management(merged_files_shape, fieldName, "TEXT")

    codeblock ="""
def getClass(MAJORITY):
        if MAJORITY == 1:
           return "Existing"
        elif MAJORITY == 2:
           return "Infill"
        elif MAJORITY == 3:
           return "Extension"
        elif MAJORITY == 4:
           return "Leapfrog"
        elif MAJORITY == 5:
           return "Inclusion"
        else:
           return "open space"
    """


    arcpy.CalculateField_management(merged_files_shape, fieldName, expression, "PYTHON", codeblock)

    


    ### Excel Conversion

    
    #merged_files_shape = r"%s\%s_merged_final.shp" % (merged_data,dirname)
    

    out_xls = r"%s\%s_majority_pixels.xls" % (Excel_data,dirname)
    

    arcpy.TableToExcel_conversion(merged_files_shape, out_xls)

    print "majority area excel conversion completed"

    print "%s city completed congrats" % dirname
    


    


    

    

    

    
    

    

    

    

    

    

    

    

    

   
    

    
