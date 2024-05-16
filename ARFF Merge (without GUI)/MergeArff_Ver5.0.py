import os
import glob
import datetime
def mergeArff(file_list):

    
    attributes_list = []
    data_list = []
    non_redundant_attributes = []
    n=1
    Datastart = 0
    currentStringLength = 0
    classLength = 0
    attributeAmount = 0
    tempattributeAmount = 0
    
    now = datetime.datetime.now()
    filename = f"File_Merging_log_time_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    with open(filename, 'w') as file:
        file.write("ERROR:\n\nMerging Process:\n\n")
    # Extract attributes from .arff file
    for name in file_list:
        with open(name) as out:
            
            currentString = out.readline()
            while currentString.strip()!="@data":      
                if currentString.startswith("@attribute class"):
                    currentStringLength = len(currentString)
                    if(classLength == 0):
                        classLength = currentStringLength
                    if(classLength != 0 and classLength != currentStringLength):
                        with open(filename, 'r') as file:
                            lines = file.readlines()
                        new_lines = []
                        for line in lines:
                            new_lines.append(line)
                            if line.strip().startswith("ERROR:"):
                                new_lines.append("\nCurrent file " + name +" has different amount of class, merging terminated.\n") 
                        with open(filename, 'w') as file:
                            file.writelines(new_lines)
                        os._exit(0)
                if currentString.startswith("@attribute"):
                    tempattributeAmount+=1
                attributes_list.append(currentString)
                currentString = out.readline()
                n+=1
            attributes_list.append(currentString)
            #print(tempattributeAmount)
            if(attributeAmount == 0):
                attributeAmount = tempattributeAmount
            if(attributeAmount != tempattributeAmount):
                with open(filename, 'r') as file:
                    lines = file.readlines()
                new_lines = []
                for line in lines:
                    new_lines.append(line)
                    if line.strip().startswith("ERROR:"):
                        new_lines.append("\nCurrent file " + name +" has different amount of attribute, merging terminated.\n") 
                with open(filename, 'w') as file:
                    file.writelines(new_lines)
                os._exit(0)
            Datastart = n
        n=1
        tempattributeAmount = 0
        
    
    # Extract data from .arff file
    for name in file_list:
        with open(name) as out:
            dataframe = out.readlines()[Datastart:]      
            for single_data in dataframe:
                data_list.append(single_data)
            datanow = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
            with open(filename, 'a') as file:
                    file.write("File "+ name + " has merged. Time: " + datanow + "\n")

    # Remove duplicate attribute 
    for single_attribute in attributes_list:
        if single_attribute not in non_redundant_attributes:
            non_redundant_attributes.append(single_attribute)    


    # Remove @relation and insert customized relation
    for single_attribute in non_redundant_attributes:
        if "@relation" in single_attribute:
            non_redundant_attributes.remove(single_attribute)
    non_redundant_attributes.insert(0, "@relation segment")
    non_redundant_attributes.insert(1, "\n")


    # Write attributes & data into the final output
    with open("MergedArff-V5.arff", "w") as out: 
        for single_attribute in non_redundant_attributes:
            out.write(single_attribute)
        out.write('\n')
        for single_data in data_list:
            out.write(single_data)

# Detect all .arff file in the folder
filepath = os.getcwd()
file_list = glob.glob(os.path.join(filepath,'*.arff'))

print(file_list)

mergeArff(file_list)

print ("Merge Finished")
