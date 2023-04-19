# importing the custom modules

from Code.src.DataEngineering.buildEnrollmentData           import buildEnrollmentData
from Code.src.DataEngineering.buildProfessorData            import buildProfessorData
from Code.src.DataEngineering.buildFinalEnrollStatusData    import buildFinalEnrollStatusData
from Code.src.DataEngineering.buildCatalogData              import buildCourseCatalogData
# from Code.src.dataengineering.buildCourseData               import buildCourseData
# from Code.src.dataengineering.buildInitialDatabaseTables    import buildInitCreateDBS
# from Code.src.dataengineering.normalizeData                 import normalizeData



# We performed WebScraping on the course catalog, to extract a lot of data. You might find remains of the code spread across the project.
# However, the professor expected us to work on a deterministic solution, and was not at all accepting of the ML Approaches. More info available in Code Folder.
# Therefore, the WebScraping code wasn't used, eventually. If a future team wants to delve into WebScraping for reasons, you can take inspiration from WS Code.
# We also combined the data, and stored it in a normalized SQL Database. It made everything so much easier, however, the code was later scraped off. Sorry.

def buildAllData():
    try:
        # # Building the Dataset
        # buildInitCreateDBS()
        buildCourseCatalogData()
        buildEnrollmentData()
        buildProfessorData()
        buildFinalEnrollStatusData()
        # buildCourseData()
        # normalizeData()
        
        # # Build Success Message
        print("\n\n","#"*80, "\n"*2,"\t"*4, "Haha Yes. Build Success 🐶 !!!", "\n"*2, "#"*80)
    except Exception as exc:
        # Build Failure Message
        print("\n\n","#"*80, "\n"*2,"\t"*4, "❌😵 Build Failure 😵❌ \n")
        print(exc)
        print("\n"*2, "#"*80)
