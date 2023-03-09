# importing the custom modules
from Code.src.DataEngineering.build_data_experimental import build_data


# defining the main function
def main():
    build_data()


# calling the main function
if __name__ == "__main__":
    main()


# Build Success Message
print("\n\n","#"*80, "\n"*2,"\t"*4, "Build Success", "\n"*2, "#"*80)