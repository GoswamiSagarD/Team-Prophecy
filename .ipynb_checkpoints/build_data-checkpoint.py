# importing the custom modules
from Code.src.dataengineering._DataEngineering import buildAllData


# defining the main function
def main():
    buildAllData()


# calling the main function
if __name__ == "__main__":
    try:
        main()
        
        # Build Success Message
        print("\n\n","#"*80, "\n"*2,"\t"*4, "Haha Yes. Build Success !!!", "\n"*2, "#"*80)
    
    except Exception as e:
        # Build Failure Message
        print("\n\n","#"*80, "\n"*2,"\t"*4, "Build Failure \n")
        print(e)
        print("\n"*2, "#"*80)