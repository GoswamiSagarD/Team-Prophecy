# importing required libraries
import os
import json

def buildCourseCatalogData():
    print("#"*40, "\t", "\n", "Course Catalog Data")

    print("Building the Program Requirements Information from the Course Catalog.. [1/2]")

    # WARNING: DO NOT TRY THIS AT HOME.
    # This code will cause a serious head-ache. Please maintain proper caution when going through this.
    # This data is manually extracted from the course catalog, and is not guaranteed to be accurate or up-to-date in coming semesters.
    course_catalog = {
        "MS Data Analytics Engineering" : {
            "Core" : ['AIT 580', 'STAT 515', 'OR 531', 'CS 504'],
            "Capstone" : ['DAEN 690'],
            "Elective" : [
                'AIT 524', 'AIT 526', 'AIT 582', 'AIT 590',
                'AIT 614', 'AIT 622', 'AIT 624', 'AIT 636', 'AIT 664',
                'AIT 722', 'AIT 724', 'AIT 736', 'AIT 736', 'AIT 746',
                'DAEN 698',
                'DFOR 510', 'DFOR 660', 'DFOR 661', 'DFOR 663', 'DFOR 664', 'DFOR 698', 'DFOR 761',
                'DFOR 767', 'DFOR 768', 'DFOR 780',
                'BENG 501', 'BENG 526', 'BENG 538', 'BENG 550', 'BENG 575',
                'CS 550', 'CS 580', 'CS 650', 'CS 657', 'CS 688', 'CS 775', 'CS 782', 'CS 787',
                'ECE 508', 'ECE 527', 'ECE 528', 'ECE 530', 'ECE 535', 'ECE 537', 'ECE 612',
                'GBUS 720', 'GBUS 721', 'GBUS 738', 'GBUS 739', 'GBUS 740', 'GBUS 744',
                'HAP 671', 'HAP 719', 'HAP 720', 'HAP 725', 'HAP 730', 'HAP 770', 'HAP 780', 'HAP 819', 'HAP 823', 'HAP 880',
                'INFS 623', 'INFS 740',
                'LING 650', 'LING 675', 'LING 685', 'LING 687', 'LING 689', 'LING 775',
                'ME 551', 'ME 552', 'ME 553', 'ME 554', 'ME 620', 'ME 621',
                'ME 714', 'ME 721', 'ME 742', 'ME 745', 'ME 750', 'ME 751', 'ME 753', 'ME 754', 'ME 755', 'ME 762',
                'OR 538', 'OR 541', 'OR 542', 'OR 568', 'OR 588',
                'OR 603', 'OR 604', 'OR 610', 'OR 645', 'OR 670', 'OR 688',
                'STAT 544', 'STAT 654', 'STAT 662', 'STAT 663', 'STAT 672',
                'SYST 508', 'SYST 538', 'SYST 542', 'SYST 568', 'SYST 573',
                'SYST 584', 'SYST 588', 'SYST 618', 'SYST 664', 'SYST 670', 'SYST 688'
            ],
        },
        "MS Computer Science" : {
            "Core" : ['CS 530', 'CS 531'],
            "Capstone" : [],
            "Elective" : [
                'CS 540', 'CS 550', 'CS 551' 'CS 555', 'CS 571', 'CS 580', 'CS 583', 'CS 584', 'CS 587','CS 595',
                'CS 600','CS 630', 'CS 633', 'CS 635', 'CS 640',
                'CS 650', 'CS 655', 'CS 657', 'CS 658','CS 662', 'CS 663', 'CS 667', 
                'CS 672', 'CS 673', 'CS 675', 'CS 678', 
                'CS 681', 'CS 682', 'CS 683', 'CS 684', 'CS 685', 'CS 686', 'CS 687', 'CS 688', 'CS 689',
                'CS 695', 'CS 697', 
                'CS 706','CS 719', 'CS 747', 'CS 752','CS 756','CS 773', 'CS 774', 'CS 777', 'CS 779',
                'CS 782', 'CS 787', 'CS 788', 'CS 795', 'CS 798', 'CS 799',
                'CS 895',
                'INFS 623', 'INFS 740', 'INFS 760', 'INFS 772', 'INFS 774',
                'ISA 562', 'ISA 564', 'ISA 656', 'ISA 673', 'ISA 674', 'ISA 681', 'ISA 697', 'ISA 763', 'ISA 764', 'ISA 785',
                'SWE 619', 'SWE 620', 'SWE 621', 'SWE 622', 'SWE 631', 'SWE 632', 'SWE 637', 'SWE 642',
                'SWE 645', 'SWE 681','SWE 699' 'SWE 721', 'SWE 737', 'SWE 760', 'SWE 795', 'SWE 796'
            ]
        },
        "MS Information Systems" : {
            "Core" : ['COMP 502', 'CS 550', 'INFS 622', 'INFS 580', 'INFS 611'],
            "Capstone" : [],
            "Elective" : [
                'AIT 526', 'AIT 646', 'AIT 642', 'AIT 660', 'AIT 664', 'AIT 670', 'AIT 684',
                'AIT 716', 'AIT 724', 'AIT 726', 'AIT 734', 'AIT 736', 'AIT 746',
                'COMP 642', 'COMP 505', 'COMP 522',
                'ECE 611', 'ECE 612', 'ECE 642', 'ECE 643', 'ECE 646', 'ECE 732', 'ECE 746',
                'CS 531', 'CS 540', 'CS 580', 'CS 583', 'CS 584',
                'CS 635', 'CS 640', 'CS 650', 'CS 657', 'CS 662', 'CS 663', 'CS 672', 'CS 673', 'CS 678',
                'CS 681', 'CS 682', 'CS 683', 'CS 684', 'CS 685', 'CS 686', 'CS 687', 'CS 688',
                'CS 706', 'CS 752', 'CS 755', 'CS 756', 'CS 773', 'CS 777', 'CS 779', 'CS 782', 'CS 787', 'CS 795',
                'INFS 623', 'INFS 640', 'INFS 697', 'INFS 740', 'INFS 760', 'INFS 770', 'INFS 772', 'INFS 774', 'INFS 796', 'INFS 797', 'INFS 799',
                'ISA 562', 'ISA 564', 'ISA 650', 'ISA 652', 'ISA 656', 'ISA 673', 'ISA 674', 'ISA 681', 'ISA 697',
                'ISA 763', 'ISA 764', 'ISA 785', 'ISA 797',
                'OR 541', 'OR 542', 'OR 635', 'OR 640', 'OR 641', 'OR 642', 'OR 643', 'OR 644', 'OR 645', 'OR 647', 'OR 681', 'OR 690',
                'PSYC 734',
                'STAT 544', 'STAT 554', 'STAT 652', 'STAT 656', 'STAT 662', 'STAT 663', 'STAT 674',
                'SWE 620', 'SWE 622', 'SWE 625', 'SWE 626', 'SWE 631', 'SWE 632', 'SWE 642', 'SWE 645', 'SWE 681', 'SWE 699',
                'SWE 721', 'SWE 681', 'SWE 763', 'SWE 795', 'SWE 796', 'SWE 798',
                'SYST 520', 'SYST 530', 'SYST 542', 'SYST 560', 'SYST 573', 'SYST 611', 'SYST 620', 'SYST 659', 'SYST 671', 'SYST 680', 'SYST 683'
            ]
        },
        "MS Applied Info Technology" : {
            "Core" : ['AIT 524', 'AIT 542', 'AIT 664'],
            "Capstone" : [],
            "Elective" : [
                'AIT 512', 'AIT 526', 'AIT 580', 'AIT 582', 'AIT 590',
                'AIT 602', 'AIT 614', 'AIT 622', 'AIT 624', 'AIT 636', 'AIT 655', 'AIT 660', 'AIT 665', 'AIT 670', 'AIT 672',
                'AIT 677', 'AIT 678', 'AIT 679', 'AIT 682', 'AIT 684', 'AIT 685', 'AIT 690', 'AIT 697', 'AIT 699',
                'AIT 701', 'AIT 702', 'AIT 711', 'AIT 712', 'AIT 716', 'AIT 722', 'AIT 724',
                'AIT 726','AIT 734', 'AIT 736','AIT 746', 'AIT 790', 'AIT 799'
            ]
        }
    }

    
    print("Exporting the Course Catalog Data.. [2/2]")
    with open( os.path.join("Code", "src", "prop", "course_catalog.json") , "w") as outfile:
        json.dump(course_catalog, outfile, indent=4)
        print("Course Catalog Data is ready for analysis!")