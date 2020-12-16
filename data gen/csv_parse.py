import pandas as pd
import numpy as np
import os
import getopt, sys


def main():
    file_name = input_arguments(sys.argv[1:])

    os.chdir(os.path.dirname(__file__)) # get cwd

    #load datafile
    dfs = pd.read_csv(file_name,                        
                        header=6,
                        names=['THz', 'dBm', 'disc'],
                        chunksize=1_000_000, #read the csv file in chunks of 1,000,000
                        ) 

    #create an empty np array to combine all the data in
    combined = np.zeros([1, 2])

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
    combined = combined.transpose()     #transpose
    arranged = arrange_by_run(combined)

    arranged_df = pd.DataFrame(arranged) #convert list to dataframe
    arranged_df.to_csv('runs.csv', header=None, index=False) #save dataframe as .csv

        


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

#call main
if __name__ == '__main__':
    main()