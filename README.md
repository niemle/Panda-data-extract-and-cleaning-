# Panda-data-extract-and-cleaning-
This project was created for learning and demonstration purposes only. It is not intended for production use. The data are not real as it is being modified to demonstrate only.

The goal of the code is to extract data from two differents csv files and achieve the following: 
* remove column header whitespace, a problem to during debugging in Visual Studio
* Select only the relevant columns
* Melt the dataframe
* Extract the melted data to seperate Miner from Metric values (like S11 + hashrate/power)
* Drop the original Source columns from melted steps
* pivoted to seperate the value into hashrate versus power
* Similar steps are repeated for the second source of data except for the fact that it has different metric value: Intake, Fan, and chip, from the same Miners
* Finally, to merge the metrics through the matching the Time and Miner columns of the two file, and aligned all the metrics for further calculation.

