# Table of Contents
1. [Challenge Summary](README.md#challenge-summary)
1. [Dependencies](README.md#dependencies)
1. [Usage](README.md#usage)
1. [Method Overview](README.md#method-overview)
1. [Assumptions](README.md#assumptions)


## Challenge Summary

A financial company's data scientists have come up with a model to predict the future value of various stocks. Two data input files contain information regarding stock values, one providing the actual value of each stock every hour and the second lists the predicted value of various stocks at a certain hour during the same time period.

To test the validity of their predictions, the data scientists would like to calculate the `average error` , the average difference between the actual stock prices and predicted values, over a specified sliding time window.

For more information, see [full challenge description](https://github.com/InsightDataScience/prediction-validation).

## Dependencies

The code was developed using Python 3.6.5, using no additional libraries beyond the `sys` module to handle command-line arguments. 

## Usage

### Python Script
The average error can be calculated for any input files using the python source file:

```
> python3 prediction-validation.py [path_to/window.txt] [path_to/actual.txt] [path_to/predicted.txt] [path_to/comparison.txt]
```
where

1. `[path_to/window.txt]` is location of the file containing the specified averaging window
1. `[path_to/actual.txt]` is the location of the file containing the actual stock values
1. `[path_to/predicted.txt]` is the location of the file containing the predicted stock values and
1. `[path_to/comparison.txt]` is the location of the file to be used for the average error output

### Bash Script 
Alternatively, a bash script has been set-up in the parent directory.  By default, this script will use input files (`window.txt`, `actual.txt`, `predicted.txt`) stored in the `input` folder and write the average error results to `comparison.txt` in the `output` folder.

```
> ./run.sh
```

Please ensure that the `run.sh` script has execute access.

## Method Overview

The main portion of the method can be described using the following three steps:

#### Storing actual stock price information in a hash table

Opening `actual.txt`, the information in each line is first parsed using the Python `split` operator, using the designated pipe delimiter (`|`).  The actual stock price is then stored in a dictionary, Python's implementation for a hash table, using the joint `(time, stock)` tuple as a key.  Using a hash table will allow for constant-time look-ups in the next step.

#### Iterating through predicted stock price information, accumulating total error by time

Opening `predicted.txt`, the information once again is parsed using `split`. We then look-up whether an actual stock price exists matching our predicted information.  If a match exists, we calculate the absolute error (`|actual - predicted|`).  During this process, we make use of two additional dictionaries: one holding the total error for each time unit and another holding the total number of actual-predicted comparisons made for each time unit. Both of these dictionaries use only `time` as a key and are updated whenever we find a match between the actual and predicted data sets.

#### Iterating through windows, calculating average error

During the previous two steps, we also store `mintime` and `maxtime`, which are the lowest and highest times recorded in either the actual or predicted datasets.  Using these combined with the `window` size, we iterate over each window.  In each window, we add together the total errors in our dictionary from the previous step, as well as the total number of predictions made during the window.  Dividing these two quantities yields the average error made during the window.  This average error is passed to output along with the window boundaries.

## Assumptions

Below are the assumptions made during the development of this solution:

1. All of the input files exist and are properly formatted according to the [challenge description](https://github.com/InsightDataScience/prediction-validation)
1. If the `window` size is larger than the scope of the data, no output file will be produced.  While we could have chosen to output the average error across all of the data in this case, we feel this could be possibly misleading.  A warning message is displayed to the user in this scenario.
1. If more than one actual stock price exists for any `(time, stock)` tuple, the price that appears later in the file is used.
1. If more than one predicted stock price exists for any `(time, stock)` tuple, all predictions are factored into the total/average error.
