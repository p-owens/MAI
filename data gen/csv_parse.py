import pandas as pd
import numpy as np
import os
import getopt, sys

#both speficied in THZ
first_freq = 191.6
last_freq = 195.9

lower_freq = 191.6
upper_freq = 195.9
step_size = 0.1
freq_rng = np.arange(lower_freq, upper_freq, step_size)


def main():
    #file_name = input_arguments(sys.argv[1:])

    #os.chdir(os.path.dirname(__file__)) # get cwd

    path = os.path.dirname(__file__) + "/test"
    os.chdir(path)
    files = os.listdir(os.getcwd())

    #create an empty np array to combine all the data in
    combined = np.zeros([1, 2])

    for i in range(len(files)):

        #load datafile
        dfs = pd.read_csv(files[i],                        
                            header=6,
                            names=['THz', 'dBm', 'disc'],
                            chunksize=1_000_000, #read the csv file in chunks of 1,000,000
                            )         

        #loop through each chunk of data
        for df in dfs:
            # drop the second freq col for the noise bins
            df = df.drop(columns=['disc'])      

            #drop keywords
            df = remove_kw(df)
            #change data in df to be numeric
            df = df.apply(pd.to_numeric)
            #get rid of any col with power greather than 100 dBm (noise)
            df = df[df.dBm < 100]   

            #change to numpy, easier to manipulate data
            array = df.to_numpy()          
            #combine all data in one big numpy array
            combined = np.concatenate((combined, array))
    
    combined = combined[1:, :]          #get rid of first row with 0's
    
    combined[:,0] = (combined[:,0] - lower_freq) * 10 #convert freq to ch. num.
    combined[:,1] = np.power(10, combined[:,1] / 10)   #convert output power to mW
    

    combined = combined.transpose()     #transpose
    #arranges the 2 row matrix in the N rows corresponding to the number of runs
    arranged = arrange_by_run(combined) 
    inputs, outputs = fill_vals(arranged)      #fill with zeros in nessicary locatoins
    inputs_df = pd.DataFrame(inputs) #convert list to dataframe
    outputs_df = pd.DataFrame(outputs) #convert list to dataframe
    
    #save dataframe as .csv
    inputs_df.to_csv(os.path.dirname(__file__) + '/x_val.csv', header=None, index=False) 
    outputs_df.to_csv(os.path.dirname(__file__) + '/y_val.csv', header=None, index=False) 

        


def remove_kw(df):

    #remove unnessicary keywords
    df = df[df.THz != "//Parameterized"]
    df = df[df.THz != "#Frequency"]
    df = df[df.THz != "//TRACE"]
    df = df[df.THz != "#(THz)"]
    df = df[df.THz != "//NoiseBins"]
    df = df[df.THz != "#LowerFrequency"]

    df = df[df.THz != "//DATASET"]
    df = df[df.THz != "//created"]
    return df


def arrange_by_run(arr):
    #function to arrange csv file as rows of simulation runs
    #each run is two consecutive rows, first frequencies then powers
    start = 0
    modified = []
    max_val = arr[0].size

    for x in range(max_val - 2):
        if arr[0,x] > arr[0,x + 1]:
            modified.append(arr[0, start:(x + 1)]) 
            modified.append(arr[1, start:(x + 1)]) 
            start = (x + 1)
    modified.append(arr[0, start:max_val]) 
    modified.append(arr[1, start:max_val])   
    return modified

def input_arguments(ip_args):
    #function to allow the input argument to be specified
    if len(ip_args) == 0:
        return "data.csv"
    elif len(ip_args) == 1:
        return str(ip_args[0])
    else:
        print("ERROR: Only specify one file at a time.\n Or specify no files to default to data.csv")
        return  str(ip_args[0])

def fill_vals(arr):

    pos = arr[0::2][:]
    val  = arr[1::2][:]    
    
    complete = np.zeros([int((len(arr))), len(freq_rng)])
    complete[0::2,:] = freq_rng

    outputs = np.zeros([len(pos), len(freq_rng)])
    inputs = np.zeros([len(pos), len(freq_rng)])

    for i in range(len(pos)):
        for j in range(len(pos[i])):
            outputs[i, int(pos[i][j])] = val[i][j]
            inputs[i, int(pos[i][j])] = bool(val[i][j])

    #complete[2::3,:] = outputs
    complete[1::2,:] = inputs
    
    return complete, outputs   
    
    
#call main
if __name__ == '__main__':
    main()