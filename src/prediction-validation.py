import sys

# Read in the window size as an integer
window = int(open(sys.argv[1], "r").read())

# Create variables to use later on
# 1. mintime: integer used to store the earliest time for which we have either actual or predicted stock price information
# 2. maxtime: integer used to store the latest time for which we have either actual or predicted stock price information
# 3. actual: dictionary/hash table used to store actual price for each (time, stock) combination
# 4. sum_error: dictionary/hash table used to store the total error (|predicted price - actual price|) for each time unit
# 5. counts: dictionary/hash table used to store the total number of predictions made for each time unit
mintime = -1
maxtime = -1
actual = dict()
sum_error = dict()
counts = dict()

# Open actual stock prices file
with open(sys.argv[2]) as f:
    
    # For each line, split the data and add to actual dictionary/hash table using (time, stock) as key
    for line in f:
        values = [x.strip() for x in line.split("|")]
        actual[(int(values[0]), values[1])] = float(values[2])
        
        # If we encounter a time that is lower than our current mintime, set mintime
        if(int(values[0]) < mintime or mintime == -1):
            mintime = int(values[0])
        # If we encounter a time that is greater than our current maxtime, increase maxtime
        if(int(values[0]) > maxtime or maxtime == -1):
            maxtime = int(values[0])
            
            
# Open predicted stock prices file
with open(sys.argv[3]) as g:
    
    # For each prediction, extract the time, stock, and predicted price
    for line in g:
        values = [x.strip() for x in line.split("|")]
        # If the (time, stock) exists in our actual stock prices data
        if (int(values[0]), values[1]) in actual:
            # Calculate the absolute error and add it to the total error for that time point and increase counts
            if(int(values[0])) in sum_error:
                sum_error[int(values[0])] += abs(actual[(int(values[0]), values[1])] - float(values[2]))
                counts[int(values[0])] += 1
            else:
                sum_error[int(values[0])] = abs(actual[(int(values[0]), values[1])] - float(values[2]))
                counts[int(values[0])] = 1
                
        # If we encounter a time that is lower than our current mintime, set mintime
        if(int(values[0]) < mintime or mintime == -1):
            mintime = int(values[0])
        # If we encounter a time that is greater than our current maxtime, increase maxtime
        if(int(values[0]) > maxtime or maxtime == -1):
            maxtime = int(values[0])
                
if window > maxtime - mintime + 1:
    raise Warning("""The specified window is larger than the scope of the data. 
    To calculate average error across the specified input stock information, use window size: """ + str(maxtime - mintime + 1))
               

# Open our output file for writing
output = open(sys.argv[4], "w")

# Ensure that we at least have at least encountered some data
if mintime != -1 and maxtime != -1:
    # Iterate over the windows
    for i in range(mintime, maxtime - window + 2):
        # Variables to keep track of the total error and number of predictions in each window
        sum_error_window = 0
        counts_window = 0

        # Loop through the window, calculating the proper total error and total prediction count for each window
        for j in range(0, window):
            if i + j in sum_error:
                sum_error_window += sum_error[i + j]
            if i + j in counts:
                counts_window += counts[i + j]

        # If our window contained any predictions: output average error, if not: output NA
        if counts_window > 0:
            output.write("|".join([str(i), str(i+window-1), "{:.2f}".format(round(float(sum_error_window) / float(counts_window), 2))]) + "\n")
        else:
            output.write("|".join([str(i), str(i+window-1), str("NA")]) + "\n")

# Close our output file
output.close()

