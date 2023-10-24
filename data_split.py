import json

def k_fold(file_path:str="", output_folder_path="", k:int=10, mix:bool=False, data_per_category:int=0, categories:int=0, entries_per_category_fold:int=0, clean=True):
    # Check for future divide by 0 and negative numbers
    if k < 1:
        raise Exception("The number of folds can not be 0 or negative")

    folds = []
    final_data = []

    try:
        with open(file_path, "r") as data:
            lines = data.readlines()
            
            # Check if the last line is a newline character
            if lines[len(lines) - 1] == '\n':
                # Delete the character
                del lines[len(lines) - 1]
            
            # Get the total length of data   
            total_data = len(lines)
            # Data per fold
            data_per_fold = total_data/k
            
            # Show user initial information
            print("### Initial Information ###")
            print("Number of folds: ", k)
            print("Length of data: ", total_data)
            print("Data per fold: ", data_per_fold, "\n\n")
            
            # Part 1: Mixing the data
            if mix == True:
                if categories < 2:
                    raise Exception("The number of categories must be greater than 1")
                elif total_data < data_per_category or data_per_category < 1:
                    raise Exception("The data per category must be less than the total data and greater than 0")
                elif data_per_category % entries_per_category_fold > 0:
                    raise Exception("The entries per category per fold should be a multiple of the data per category")
                
                # We know that we have 50 of each data and we want to have each 5 of each data in each fold
                
                new_lines = []
                for count in range(0, data_per_category, entries_per_category_fold):
                    for category in range(categories):
                        new_lines.append(lines[count + (data_per_category * category)])
                        new_lines.append(lines[count + 1 + (data_per_category * category)])
                        new_lines.append(lines[count + 2 + (data_per_category * category)])
                        new_lines.append(lines[count + 3 + (data_per_category * category)])
                        new_lines.append(lines[count + 4 + (data_per_category * category)])
                           
            # Part 2: Getting the folds
            fold_counter = 0     
            for index in range(total_data):
                if index % (data_per_fold) == 0:
                    folds.append([])
                    fold = []
                    # Do not increment the counter for the 0 index
                    if index != 0:
                        fold_counter += 1
                
                # Remove trailing new line characters if clean is true
                fold.append(new_lines[index]) if clean == False else fold.append(new_lines[index].strip())
                folds[fold_counter] = fold
                
            # Pretty print the JSON output
            print(json.dumps(folds, indent=4))
            # print(len(folds))
            
            # Part 3: Showing training data and validation data
            for index in range(k):   
                # Reset variables
                final_data.append([])
                data_set = {"training_data": {}, "validation_data": {}}
                
                # Assign data
                stop = index + (k-1)

                # Copy the list
                folds_copy = folds.copy()
                
                # Remove validation data from copy
                folds_copy.pop(stop % k)
                
                # Return copy of data without validation data
                data_set["training_data"] = folds_copy.copy()
                data_set["validation_data"] = folds[stop % k]
                
                final_data[index] = data_set
            
            for index in range(len(final_data)):    
                # Write the output to a file
                with open(f"{output_folder_path}/output{index + 1}.txt", "w") as output:
                    output.write(json.dumps(final_data[index], indent=4))
                
            print("\n\n## Output has been written to output.txt ##")
                
    except Exception as e:
        print("Something went wrong: ", e)

# Running the function        
k_fold("/Users/bakunga/Downloads/iris/iris.data", "/Users/bakunga/Documents/Projects/Advanced Artificial Intelligence/output", 10, True, 50, 3, 5, False)