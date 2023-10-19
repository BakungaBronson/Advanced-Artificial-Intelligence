import json

def k_fold(file_path:str="", k:int=10):
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
            
            # Part 1: Getting the folds
            fold_counter = 0     
            for index in range(total_data):
                if index % (data_per_fold) == 0:
                    folds.append([])
                    fold = []
                    # Do not increment the counter for the 0 index
                    if index != 0:
                        fold_counter += 1

                fold.append(lines[index])
                folds[fold_counter] = fold
                
            # Pretty print the JSON output
            print(json.dumps(folds, indent=4))
            print(len(folds))
            
            # Part 2: Showing training data and validation data

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
                
            # Write the output to a file
            with open("/Users/bakunga/Downloads/iris/output.txt", "w") as output:
                output.write(json.dumps(final_data, indent=4))
                
            print("\n\n## Output has been written to output.txt ##")
                
    except Exception as e:
        print("Something went wrong: ", e)
        
k_fold("/Users/bakunga/Downloads/iris/iris.data")