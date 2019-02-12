__author__ = "spowell"
import arcpy

work_space = arcpy.env["scriptWorkspace"]

try:

    arcpy.env.workspace = work_space
    assert work_space

    # Don't allow any more connections to the geodatabase
    # and disconnect existing users
    arcpy.AddMessage(f"Disallowing new connections.")
    arcpy.AcceptConnections(work_space, False)
    arcpy.AddMessage(f"Disconnecting all Users.")
    arcpy.DisconnectUser(work_space, "ALL")

    data_sets = arcpy.ListDatasets("", r"Feature")
    for data_set in data_sets:
        data_set_desc = arcpy.Describe(data_set)
        if not data_set_desc.isVersioned:
            try:
                arcpy.AddMessage(f"Registering {data_set} as Versioned.")
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


