import csv
import os
import pandas as pd

#Import the data file
def Main():
    OS = input("Unix or Windows OS? (U/W) ")
    while not (OS == 'U' or OS == 'W'):
        print("Invalid Response.")
        OS = input("Unix or Windows OS? (U/W) ")
    try: 
        print("Script executed from: ")
        print(os.path.dirname(os.path.realpath("Jess_Titer_Approximation.ipynb")))
        path = os.path.dirname(os.path.realpath("Jess_Titer_Approximation.ipynb"))
        print("The path is: " + path)
    except:
        valid_path = False
        path = input("Couldn't find active directory for this script. Please input the active directory: ")
        while (valid_path == False):
            if (os.path.isdir(path) == False):
                path = input("Input directory was invalid, please try again or enter 'Q' to quit: ")
                if ((path == "Q") or (path == "q")): return "invalid"
            else: valid_path = True

    print("Found directory. Moving Forward")
    
    if (OS == "W"):
        print(path + "\\Peak_Data")
        path_mod = "\\"
    elif(OS == "U"):
        print(path+"/Peak_Data")
        path_mod = "/"
        
    if (os.path.isdir(path + path_mod+ "Peak_Data") == True):
        path_files = path + path_mod+ "Peak_Data"
        i = 1
        dir_items = []
        print("Found template folder, listing template files: ")
        for file in os.listdir(path_files):
            print("\t" + str(i) + ": " + file)
            i+=1
            dir_items.append(file)   
    else: 
        print("Peak_Data folder is not at listed directory. Terminating program.")
        return "invalid"
    for file in dir_items:
        f_name,f_ext = os.path.splitext(file)
        curr_path = path + path_mod+"Peak_Data"+path_mod + file
        read_file = pd.read_csv (r''+curr_path, delimiter = '\t')
        read_file.to_csv (r''+path + path_mod+ "Converted_Files" + path_mod+ f_name+".csv", index=None)
        
        working_file = path +path_mod+"Converted_Files"+path_mod+f_name+".csv"

        print("Currpath is: " + str(curr_path))
        #store file contents in parallel arrays
        with open(working_file, "rt") as x:
            reader = csv.DictReader(x)
            samples = [row["Sample"]for row in reader]
            x.close()
        with open(working_file, "rt") as x:
            reader = csv.DictReader(x)
            height = [row["Height"] for row in reader]
            x.close()
        with open(working_file, "rt") as x:
            reader = csv.DictReader(x)
            area = [row["Area"] for row in reader]
            x.close()
        with open(working_file, "rt") as x:
            reader = csv.DictReader(x)
            mw = [row["MW(kDa)"] for row in reader]
            x.close()

        print(len(samples))
        print(len(height))
        print(len(area))
        output = []   
        curr_index = 0
        i = curr_index


        while(curr_index<len(samples)):
            sample_ref = samples[curr_index]
            while(i<len(samples)) and (samples[i]==sample_ref):
                if (i == curr_index):
                    
                    output.append(str(sample_ref) +","+ str(mw[i])+","+ str(height[i]) 
                                        +","+ str(area[i])+",""\n")
                    
                else:
                    if(i<len(samples)-1) and (samples[i+1]!=sample_ref):
                        sum_area = 0
                        sum_height = 0
                        for val in range(curr_index,i+1):
                            print(area[val])
                            sum_area += float(area[val])
                            sum_height += float(height[val])
                        print("curr area sum: " + str(sum_area))
                        output.append("" +","+ str(mw[i])+","+ str(height[i]) 
                                      +","+ str(area[i])+"," + str(sum_height)+","+str(sum_area)+"\n")
                    elif(i == len(samples)-1):
                        sum_area = 0
                        sum_height = 0
                        for val in range(curr_index,i+1):
                            sum_area += float(area[val])
                            sum_height += float(height[val])
                        output.append("" +","+ str(mw[i])+","+ str(height[i]) 
                                      +","+ str(area[i])+"," + str(sum_height)+","+str(sum_area)+"\n")
                    else: output.append("" +","+ str(mw[i])+","+ str(height[i]) +","+ str(area[i])+"\n")
                i += 1
            
            curr_index = i

        if not (os.path.exists(path + path_mod+"output_files")):
            output_dir = path + path_mod+"output_files"
            os.mkdir(output_dir)
        else: 
            output_dir = path + path_mod+"output_files"
        
        output_file = output_dir + path_mod+f_name+".csv"
        r = open(output_file, 'w')
        with open(output_file, 'w') as target:
            target.write("Sample,MW(kDa),Height,Area,Height Sum,Area Sum\n")
            for line in output:
                target.write(line)
Main()