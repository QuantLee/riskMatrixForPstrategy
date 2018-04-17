# riskMatrixForPstrategy
<img width="581" alt="workflow" src="https://user-images.githubusercontent.com/26841080/38892039-2320a604-4254-11e8-9a67-2edd821bc32a.png">

Risk project: 
Write a program in Python, using Pandas module to calculate various tests listed below that are related to strategy drawdown. The sample data that is coming from sample_data.csv (won't be showed here because of the NDA) should be first read into Pandas dataframe, and then you can use a combination of Python and Pandas to calculate various metrics below. Assume that such a script will be running every day, showing all the strategies and tests that they violate. 

Strategy
Test it violates (if it violates more than one test, it will be shown on the separate line)
Threshold that is violated 
Current value that violates the test
Strategy’s current GMV
Strategy’s current cumulative PNL
Strategy
Test Violated
Threshold Violated
Current Value that Violates
Current GMV
Current CumuPNL
 
Tests:
AbsDrawDown: absolute current drawdown (in $) exceeds $10M
EQYDrawDown: current drawdown (in % of current gross market value) exceeds 5% 
LargestDrawDown: current drawdown (in %) exceeds (tolerance * previous largest drawdown (in %)); tolerance = 1.2; 
LongestDrawDown: current drawdown (in days) exceeds (tolerance * previous largest drawdown (in days)); tolerance = 1.5; 
LargestDownDay: current largest down day (in %) in past n (configurable) days exceeds (tolerance * previous largest down day (in %), during all such previous n-day periods); tolerance = 2;  
MostConsecutiveDownDays: current largest # of consecutive down days (in days) in past n (configurable) days exceeds (tolerance * previous most consecutive down days (in days), during all such previous n-day periods); tolerance = 1.2; 
FewestUpDays: current # of up days (in days) in past n (configurable) days is less than (tolerance * previous lowest # up days (in days) , during all such previous n-day periods); tolerance = 0.3 ;
