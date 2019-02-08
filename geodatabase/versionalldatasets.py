__author__ = "spowell"
import arcpy

try:
    data_set = arcpy.GetParameterAsText(0)
    is_compress_db = False
    if arcpy.GetArgumentCount() > 1:
        is_compress_db = arcpy.GetParameterAsText(1)
    work_space = arcpy.env["scriptWorkspace"]
    arcpy.env.workspace = work_space
    assert work_space

    arcpy.AddMessage(f"Disallowing new connections.")
    arcpy.AcceptConnections(work_space, False)
    arcpy.AddMessage(f"Disconnecting all Users.")

    datasets = arcpy.ListDatasets("", r"Feature")
    for data_set in datasets:
        # if data_set == "ec.sde.WorkOrders":
        #     continue
        data_set_desc = arcpy.Describe(data_set)
        if not data_set_desc.isVersioned:
            arcpy.DisconnectUser(work_space, "ALL")
            arcpy.AddMessage(f"Registering {data_set} as Versioned.")
            try:
                arcpy.RegisterAsVersioned_management(data_set, "EDITS_TO_BASE")
            except Exception as e:
                arcpy.AddError(f"Could not Version.\n {data_set} {data_set_desc}\n{arcpy.GetMessages(2)}")
                continue
        else:
            arcpy.AddMessage(f"{data_set} is already registered as versioned.")

except arcpy.ExecuteError:
    arcpy.AddError(arcpy.GetMessages(2))

except Exception as e:
    arcpy.AddError(f"Problem in the script.\n {e}")

finally:
    arcpy.AddMessage(f"Accepting User Connections.")
    arcpy.AcceptConnections(work_space, True)

