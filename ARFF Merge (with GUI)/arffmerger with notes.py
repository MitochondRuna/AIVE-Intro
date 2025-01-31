import os
import glob
import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

#Functionality for the first "Browse" button. Grabs the path of the folder chosen by the user and saves it in the input_dir variable
def browse_input():
    input_dir_disp.config(state="normal") # Enable the input directory display
    input_dir_disp.delete(0, "end") # Crear any previous directory display
    input_dir = filedialog.askdirectory() # Open dialog to select folder
    input_dir_disp.insert(0, input_dir) # Insert selected folder path into the display
    input_dir_disp.config(state='readonly') # Make the display read-only to prevent user editing

#Functionality for the second "Browse" button. Grabs the path of the folder chosen by the user and saves it in the output_dir variable
def browse_output():
    output_dir_disp.config(state="normal") # Enable the output directory display
    output_dir_disp.delete(0, "end") # Clear previous directory path
    output_dir = filedialog.askdirectory() # Select folder
    output_dir_disp.insert(0, output_dir) # Select folder path
    output_dir_disp.config(state="readonly") # Make it read-only to prevent editing

#Functionality for "Start Merging" button. Gets the user inputs and performs error handling
def get_data():
    global final_in_dir # Store the selected input directory globally
    global final_out_dir # Store the selected output directory globally
    global file_name # Store the filename
    special_chars = "!@#$%^&*()-+?_=,<>/ "  #Disallowed special characters for filenames
    final_in_dir = input_dir_disp.get() # Get the input directory from the GUI
    final_out_dir = output_dir_disp.get() # Get the output directory from the GUI
    file_name = filename_disp.get() # Get the output filename
    if final_in_dir == ""  or final_out_dir == "" or file_name == "": #Checks if any of the input fields are empty, if empty, show an error message below
        messagebox.showinfo("ARFFMerger.exe", "At least one of the input fields are empty.")
    elif any(char in special_chars for char in file_name): #Checks if special characters are present in the file name. Show an error message to prevent problems in filename saving
        messagebox.showinfo("ARFFMerger.exe", "No special characters or white spaces allowed in filename.")
    else: #If no errors in the input fields, close the gui and start the merging
        file_name = file_name.rstrip('arff') # Ensure the file doesn't include 'arff'
        opening_window.destroy() # Close the GUI window

# To merge ARFF files based on common attributes and class counts
def mergeArff(file_list):

    #Initialization of dictionaries and lists for error handling
    class_dict = {} # Store files grouped by class
    attributes_dict = {} # Store files grouped by attribute count
    file_class_lst = [] # Store distinct class labels
    attribute_count_lst = [] #  Store distinct attribute counts
    now = datetime.datetime.now() # Capture the current time for error report filenames
    #Main merging algorithm
    #Process each file and collect both class and attribute information
    for name in files_list: 
        with open(name) as out: 
            currentString = ''
            attribute_count = 0

            while currentString != '@data': #Loop through the lines of the arff file until "@data" line
                currentString = out.readline().strip() # Read and strip each line
                if currentString == '@data':
                    break
                if currentString.startswith("@attribute"): #Counts the numbers of attributes in each file. Done for error handling
                    attribute_count +=1  # Count the number of attributes
                if currentString.startswith("@attribute class"):
                    file_class = currentString.split(',')[-1].lstrip("'").rstrip("'}") # Extract class label 
                    
                    #Grabs the amount of classes per file
# Add the class label to file_class_lst and update class_dict if not already present
            if file_class not in file_class_lst: #Put the obtained file class in the file_class_lst if not yet in that list.
                file_class_lst.append(file_class)
                class_dict[file_class] = []

# Add the attribute count to attribute_count_lst and update attributes_dict if not already present
            if str(attribute_count) not in attribute_count_lst: #Put the obrained number of attributes in the attribute_count_lst if not yet in that list.
                attribute_count_lst.append(str(attribute_count))
                attributes_dict[str(attribute_count)] = []

# Store the filename in both the attribute and class dictionaries
            attributes_dict[str(attribute_count)].append(name.split("\\")[-1]) #Grabs the current filename and puts it in the attributes_dict dictionary
            class_dict[file_class].append(name.split("\\")[-1]) ##Grabs the current filename and puts it in the class_dict dictionary

     # Check if multiple classes are present, which would prevent merging
    if len(file_class_lst) > 1: # If we have more than one element in the file_class_lst, output error message below
        error_message = ''
        for key in class_dict.keys(): 
            # Generate error message listing files grouped by class label
            error_message = error_message + key[-1] + '-class files:' + '\n' + str(class_dict[key])[1:-1] + '\n\n' #Print out the filenames corresponding to their class number
             # Save error details to a file and display it
        error_filename = f"ARFFMERGER_ERROR_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        error_filepath = final_out_dir + '/' + error_filename
        with open(error_filepath, 'w') as err:
            err.writelines("Merging procedure cannot continue while input folder contains files with different number of classes. \n\n" + error_message)
        messagebox.showinfo("ARFFMerger.exe", "Merging procedure cannot continue while input folder contains files with different number of classes. \n\n" + error_message)
        os._exit(0)
        
    # Check if multiple attribute counts are present, which would prevent merging
    if len(attribute_count_lst) > 1: # If we have more than one element in the attribute_count_lst, output error message below
        error_message = ''
        
        for key in attributes_dict.keys():
        # Generate error message listing files grouped by attribute count
            error_message = error_message + key + '-attribute files:' + '\n' + str(attributes_dict[key])[1:-1] + '\n\n' # Print out the filenames corresponding to their attribute number
        # Save error details to a file and display the error
        error_filename = f"ARFFMERGER_ERROR_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        error_filepath = final_out_dir + '/' + error_filename
        with open(error_filepath, 'w') as err:
            err.writelines("Merging procedure cannot continue while input folder contains files with different number of attributes. \n\n" + error_message)
        messagebox.showinfo('ARFFMerger.exe', "Merging procedure cannot continue while input folder contains files with different number of attributes. \n\n" + error_message)
        os._exit(0)

    #Once the code gets to this point, all arff files have the same number of classes and attributes. Merging starts here
    first_file = 0 # Indicates if the first file has been processed
    datastart = 1 # Index of the @data section
    merged_arff = [] # Store merged content
        
    # Process each file, adding their data sections to the merged output
    for name in files_list:
        with open(name) as out:
            if first_file == 0: #Checks if this is this the first file that has been opened, if yes read all the lines in that file
                merged_arff = out.readlines() # Read the first file entirely
                datastart = merged_arff.index("@data\n") #Get the index where the "@data" is located
                first_file = 1 # Update first_file variable to indicate that the first file has been opened    
            # Append only the data part of subsequent files
            if first_file == 1: #Combine the previous data with new data
                merged_arff = merged_arff + out.readlines()[datastart + 1:]
     
    # Create the output file path and save the merged content
    output_path = final_out_dir + '/' + file_name + '.arff' #Setting the output path for the merged file

    with open(output_path, 'w') as output_file:
        output_file.writelines(merged_arff) #Writes the lines for the merged file

        # Save a result file with details of the merged files
    mergedfiles = str(class_dict[file_class_lst[0]])[1:-1]
    result_filename = f"ARFFMERGER_RESULT_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    result_filepath = final_out_dir + '/' + result_filename
    with open(result_filepath, 'w') as err:
        err.writelines(f"Merging succesful.\nFiles merged:\n\n{mergedfiles}\n\nFile saved with name: {file_name}.arff")

    # Display a message confirming successful merging
    messagebox.showinfo("ARFFMerger.exe", f"Merging succesful.\nFiles merged:\n\n{mergedfiles}") #Message box pops out that shows the file names involved in the merge
  

#Initialize GUI window
opening_window = Tk()
opening_window.title("ARFFMerger.exe") # Set the window title
opening_window.geometry("750x100") # Set window size

#Make GUI elements
input_dir_disp = Entry(opening_window, width = 80, state = "readonly") # Display for input folder path
output_dir_disp = Entry(opening_window, width = 80, state = "readonly") # Display for output folder path
filename_disp = Entry(opening_window, width = 60, text = "Insert filename here") # Input for output filename
files_dir_btn = Button(opening_window, text="Browse", command=browse_input, bd = 3)  # Button to browse for input folder
output_dir_btn = Button(opening_window, text="Browse", command=browse_output, bd = 3) # Button to browse for output folder
merge_btn = Button(opening_window, text = "Start Merging", command=get_data, bd = 3) # Button to start the merging process
files_label = Label(opening_window,text = "Folder containing arff files:")
filedest_label = Label(opening_window, text = "Output file destination:")
filename_label = Label(opening_window, text = "Merged output filename:")

#Layout GUI elements like labels, textboxes, and buttons using grid layout, in a grid
input_dir_disp.grid(row = 0, column = 1)
output_dir_disp.grid(row = 1, column = 1)
filename_disp.grid(row = 2, column = 1, sticky = 'W')
files_dir_btn.grid(row = 0,column = 2, padx = 2)
output_dir_btn.grid(row = 1, column = 2, pady = 2)
merge_btn.grid(row = 2, column = 2, sticky = 'N')
files_label.grid(row = 0,column = 0, sticky = 'W')
filedest_label.grid(row = 1, column = 0, sticky = 'W')
filename_label.grid(row=2, column = 0, sticky = 'W')

# Enters the main loop of the Tkinter application to keep the GUI active until user interaction is completed
opening_window.mainloop()

#Check for user input
special_chars = "!@#$%^&*()-+?_=,<>/ "
if final_in_dir == "" or final_out_dir == "" or file_name == "" or any(char in special_chars for char in file_name): #If any of the user inputs are empty or if special characters are present in the filename, exit the .exe file
    os._exit(0)

#Grab the filenames of files in the input directory(chosen by user) which have the file extension .arff
files_list = glob.glob(os.path.join(final_in_dir,'*.arff'))
filenames = os.listdir(final_in_dir) # List all the filenames in the input directory

#Run the merging script, passing the list of .arff files to be merged
mergeArff(files_list)

