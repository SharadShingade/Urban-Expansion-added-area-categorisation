import sys, time, os, win32com.client, glob, arcpy, numpy, random, shapefile
import os.path, ntpath, shutil, glob






arcpy.env.overwriteOutput = 1
arcpy.CheckOutExtension('spatial')
tempWS = r"F:\Inclusion\Temp"   # provide temporary workspace
arcpy.env.scratchWorkspace = tempWS
arcpy.env.extent =""


#tempWS = r"C:\UGA_temp"
   
raw_data = r"F:\Inclusion\Output"  # provide ULA output folder path, Note Data folder str: Output\CITYNAME folder

circle_file = r"F:\Inclusion\CIRCLE" # provide Halton Circle files path, Note Data folder str: CIRCLE\CITYNAME folder 

centriod_data = r"F:\Inclusion\Halton_centriod" # provide path to save halton circle centriod points

merged_data = r"F:\Inclusion\Merged_data"  # provide path to save locale categorization merged files 

Excel_data = r"F:\Inclusion\Excelsheet"    # provide path to export merged locale file in to excel note
                                           # Note: this file is raw we need to extract only specific column for this
                                           # refer excel_processing_v1.py script



basepath = os.path.basename

#print basepath

#all_raw_data = [x[0] for x in os.walk(raw_data)][1:]

#print "\n data directory %s...." %all_raw_data

for current_data_dir in os.listdir(raw_data):

    dirname = ntpath.basename(current_data_dir)
    print dirname

    Development_t1_t2 = r"%s\%s\New_Development_t1_t2.img" % (raw_data,current_data_dir)
    Development_t2_t3 = r"%s\%s\New_Development_t2_t3.img" % (raw_data,current_data_dir)
    inclusion_2 = r"%s\%s\inclusion_t2.img" % (raw_data,current_data_dir)
    inclusion_3 = r"%s\%s\inclusion_t3.img" % (raw_data,current_data_dir)

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
    outFeatureClass = r"%s\%s.shp" % (centriod_data,dirname)
    halton_point = arcpy.FeatureToPoint_management(inFeatures, outFeatureClass, "CENTROID")

    arcpy.AddField_management(halton_point, "Added_area", "TEXT", field_length= 30)

    ##############################################

    Dev_t1_t2 = Development_t1_t2
    
    infill_t2_SQL = "VALUE = 1"
    extension_t2_SQL = "VALUE = 2"
    leapfrog_t2_SQL = "VALUE = 3"
    
    infill_attExtract = arcpy.sa.ExtractByAttributes(Dev_t1_t2, infill_t2_SQL)
    extension_attExtract = arcpy.sa.ExtractByAttributes(Dev_t1_t2, extension_t2_SQL)
    leapfrog_attExtract = arcpy.sa.ExtractByAttributes(Dev_t1_t2, leapfrog_t2_SQL)
    print "Extraction of infill, extension and leapfrog T2 complted"

    ######

    Dev_t2_t3 = Development_t2_t3
    
    infill_t3_SQL = "VALUE = 1"
    extension_t3_SQL = "VALUE = 2"
    leapfrog_t3_SQL = "VALUE = 3"
    
    infill_attExtract_ = arcpy.sa.ExtractByAttributes(Dev_t2_t3, infill_t3_SQL)
    extension_attExtract_ = arcpy.sa.ExtractByAttributes(Dev_t2_t3, extension_t3_SQL)
    leapfrog_attExtract_ = arcpy.sa.ExtractByAttributes(Dev_t2_t3, leapfrog_t3_SQL)
    print "Extraction of infill, extension and leapfrog T3 complted"

    #######
    incl_t2= inclusion_2

    incl_t2_SQL = "VALUE = 1"

    inclusion_attExtract = arcpy.sa.ExtractByAttributes(incl_t2, incl_t2_SQL)
    print "Extraction of inclusion T2 completed"

    #####
    incl_t3= inclusion_3

    incl_t3_SQL = "VALUE = 1"

    inclusion_attExtract_ = arcpy.sa.ExtractByAttributes(incl_t3, incl_t3_SQL)
    print "Extraction of inclusion T3 completed"

    ######

    #Raster to vector Conversion

    # T2 Conversion

    #outPolygons = r"F:\Testing\temp\Output.gdb\%s_ftpt" % dirname
    infill_t2_outPoly = r"%s\%s_infill_t2" % (tempWS,dirname)
    extension_t2_outPoly = r"%s\%s_extension_t2" % (tempWS,dirname)
    leapfrog_t2_outPoly = r"%s\%s_leapfrog_t2" % (tempWS,dirname)

    infill_t2_poly = arcpy.RasterToPolygon_conversion(infill_attExtract, infill_t2_outPoly, "NO_SIMPLIFY")
    extension_t2_poly = arcpy.RasterToPolygon_conversion(extension_attExtract, extension_t2_outPoly, "NO_SIMPLIFY")
    leapfrog_t2_poly = arcpy.RasterToPolygon_conversion(leapfrog_attExtract, leapfrog_t2_outPoly, "NO_SIMPLIFY")

    print "conversion Raster to polygon T2 completed"

    # T3 Conversion


    infill_t3_outPoly = r"%s\%s_infill_t3" % (tempWS,dirname)
    extension_t3_outPoly = r"%s\%s_extension_t3" % (tempWS,dirname)
    leapfrog_t3_outPoly = r"%s\%s_leapfrog_t3" % (tempWS,dirname)

    infill_t3_poly = arcpy.RasterToPolygon_conversion(infill_attExtract_, infill_t3_outPoly, "NO_SIMPLIFY")
    extension_t3_poly = arcpy.RasterToPolygon_conversion(extension_attExtract_, extension_t3_outPoly, "NO_SIMPLIFY")
    leapfrog_t3_poly = arcpy.RasterToPolygon_conversion(leapfrog_attExtract_, leapfrog_t3_outPoly, "NO_SIMPLIFY")

    print "conversion Raster to polygon T3 completed"

    # inclusion conversion

    inclusion_t2_outPoly = r"%s\%s_inclusion_t2" % (tempWS,dirname)
    inclusion_t3_outPoly = r"%s\%s_inclusion_t3" % (tempWS,dirname)

    inclusion_t2_poly = arcpy.RasterToPolygon_conversion(inclusion_attExtract, inclusion_t2_outPoly, "NO_SIMPLIFY")
    inclusion_t3_poly = arcpy.RasterToPolygon_conversion(inclusion_attExtract_, inclusion_t3_outPoly, "NO_SIMPLIFY")

    print " Inclusion conversion Raster to polygon T2, T3 completed"


    # Spatial Join

    #join_files = [x for x in glob.glob(r"F:\Testing\temp\%s_infill_t2" % dirname)]

    join_files_infill_t2 = r"%s\%s_infill_t2.shp"  % (tempWS,dirname)

    join_infill_t2_file = r"%s\%s_joined_infill_t2" % (tempWS,dirname)

    

    join_infill_t2 = arcpy.SpatialJoin_analysis(target_features =outFeatureClass , join_features = join_files_infill_t2 ,
                                                join_operation = "JOIN_ONE_TO_ONE", match_option = "INTERSECT",
                                                join_type = "KEEP_COMMON",
                                                out_feature_class = join_infill_t2_file)

    infill_t2 = r"%s\%s_joined_infill_t2.shp" % (tempWS,dirname)

    arcpy.CalculateField_management(infill_t2,"Added_area",'"""infill_t2"""',"PYTHON_9.3")

    print "infill_t2_done"

    ### infill_t3

    join_files_infill_t3 = r"%s\%s_infill_t3.shp"  % (tempWS,dirname)

    join_infill_t3_file = r"%s\%s_joined_infill_t3" % (tempWS,dirname)

    

    join_infill_t3 = arcpy.SpatialJoin_analysis(target_features =outFeatureClass , join_features = join_files_infill_t3 ,
                                                join_operation = "JOIN_ONE_TO_ONE", match_option = "INTERSECT",
                                                join_type = "KEEP_COMMON",
                                                out_feature_class = join_infill_t3_file)

    infill_t3 = r"%s\%s_joined_infill_t3.shp" % (tempWS,dirname)

    arcpy.CalculateField_management(infill_t3,"Added_area",'"""infill_t3"""',"PYTHON_9.3")

    print "infill_t3_done"


    ### extension t2

    join_files_extension_t2 = r"%s\%s_extension_t2.shp"  % (tempWS,dirname)

    join_extension_t2_file = r"%s\%s_joined_extension_t2" % (tempWS,dirname)

    

    join_extension_t2 = arcpy.SpatialJoin_analysis(target_features =outFeatureClass , join_features = join_files_extension_t2 ,
                                                join_operation = "JOIN_ONE_TO_ONE", match_option = "INTERSECT",
                                                join_type = "KEEP_COMMON",
                                                out_feature_class = join_extension_t2_file)

    extension_t2 = r"%s\%s_joined_extension_t2.shp" % (tempWS,dirname)

    arcpy.CalculateField_management(extension_t2,"Added_area",'"""extension_t2"""',"PYTHON_9.3")

    print "extension_t2_done"


    ### extesnion t3

    join_files_extension_t3 = r"%s\%s_extension_t3.shp"  % (tempWS,dirname)

    join_extension_t3_file = r"%s\%s_joined_extension_t3" % (tempWS,dirname)

    

    join_extension_t3 = arcpy.SpatialJoin_analysis(target_features =outFeatureClass , join_features = join_files_extension_t3 ,
                                                join_operation = "JOIN_ONE_TO_ONE", match_option = "INTERSECT",
                                                join_type = "KEEP_COMMON",
                                                out_feature_class = join_extension_t3_file)

    extension_t3 = r"%s\%s_joined_extension_t3.shp" % (tempWS,dirname)

    arcpy.CalculateField_management(extension_t3,"Added_area",'"""extension_t3"""',"PYTHON_9.3")

    print "extension_t3_done"

    #### leapfrog t2

    join_files_leapfrog_t2 = r"%s\%s_leapfrog_t2.shp"  % (tempWS,dirname)

    join_leapfrog_t2_file = r"%s\%s_joined_leapfrog_t2" % (tempWS,dirname)

    

    join_leapfrog_t2 = arcpy.SpatialJoin_analysis(target_features =outFeatureClass , join_features = join_files_leapfrog_t2 ,
                                                join_operation = "JOIN_ONE_TO_ONE", match_option = "INTERSECT",
                                                join_type = "KEEP_COMMON",
                                                out_feature_class = join_leapfrog_t2_file)

    leapfrog_t2 = r"%s\%s_joined_leapfrog_t2.shp" % (tempWS,dirname)

    arcpy.CalculateField_management(leapfrog_t2,"Added_area",'"""leapfrog_t2"""',"PYTHON_9.3")

    print "leapfrog_t2_done"


    ### leapfrog t3

    join_files_leapfrog_t3 = r"%s\%s_leapfrog_t3.shp"  % (tempWS,dirname)

    join_leapfrog_t3_file = r"%s\%s_joined_leapfrog_t3" % (tempWS,dirname)

    

    join_leapfrog_t3 = arcpy.SpatialJoin_analysis(target_features =outFeatureClass , join_features = join_files_leapfrog_t3 ,
                                                join_operation = "JOIN_ONE_TO_ONE", match_option = "INTERSECT",
                                                join_type = "KEEP_COMMON",
                                                out_feature_class = join_leapfrog_t3_file)

    leapfrog_t3 = r"%s\%s_joined_leapfrog_t3.shp" % (tempWS,dirname)

    arcpy.CalculateField_management(leapfrog_t3,"Added_area",'"""leapfrog_t3"""',"PYTHON_9.3")

    print "leapfrog_t3_done"


    ### inclusion t2 
    
    join_files_inclusion_t2 = r"%s\%s_inclusion_t2.shp"  % (tempWS,dirname)

    join_inclusion_t2_file = r"%s\%s_joined_inclusion_t2" % (tempWS,dirname)

    

    join_inclusion_t2 = arcpy.SpatialJoin_analysis(target_features =outFeatureClass , join_features = join_files_inclusion_t2 ,
                                                join_operation = "JOIN_ONE_TO_ONE", match_option = "INTERSECT",
                                                join_type = "KEEP_COMMON",
                                                out_feature_class = join_inclusion_t2_file)

    inclusion_t2 = r"%s\%s_joined_inclusion_t2.shp" % (tempWS,dirname)

    arcpy.CalculateField_management(inclusion_t2,"Added_area",'"""inclusion_t2"""',"PYTHON_9.3")

    print "inclusion_t2_done"

    ### inclusion T3

    join_files_inclusion_t3 = r"%s\%s_inclusion_t3.shp"  % (tempWS,dirname)

    join_inclusion_t3_file = r"%s\%s_joined_inclusion_t3" % (tempWS,dirname)

    

    join_inclusion_t3 = arcpy.SpatialJoin_analysis(target_features =outFeatureClass , join_features = join_files_inclusion_t3 ,
                                                join_operation = "JOIN_ONE_TO_ONE", match_option = "INTERSECT",
                                                join_type = "KEEP_COMMON",
                                                out_feature_class = join_inclusion_t3_file)

    inclusion_t3 = r"%s\%s_joined_inclusion_t3.shp" % (tempWS,dirname)

    arcpy.CalculateField_management(inclusion_t3,"Added_area",'"""inclusion_t3"""',"PYTHON_9.3")

    print "inclusion_t3_done"


    #### merging all files

    merged_files = r"%s\%s_merged_final" % (merged_data,dirname)
    
    arcpy.Merge_management([infill_t2,infill_t3, extension_t2, extension_t3,leapfrog_t2,leapfrog_t3,inclusion_t2, inclusion_t3], merged_files)

    print "Merged all files..congrats"


    ### Excel Conversion

    
    merged_files_shape = r"%s\%s_merged_final.shp" % (merged_data,dirname)
    

    out_xls = r"%s\%s_merged_added_area.xls" % (Excel_data,dirname)
    

    arcpy.TableToExcel_conversion(merged_files_shape, out_xls)

    print "added area excel conversion completed"

    print "%s city completed congrats" % dirname

    

    

  

    

    

    

    

    


    

    

    


    


    


    

        

