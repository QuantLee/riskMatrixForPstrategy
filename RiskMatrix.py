import pandas as pd

def currentDrawdown(dailyReturn):
	'''
		pass in a pandas series which can be either PNL or dailyReteturn, return
		the current drawdown value, and historical high index. i is the index
		for peak, j is the index for trough
	'''
	i = dailyReturn.argmax()
	j = dailyReturn.index[-1]
	value = dailyReturn[i] - dailyReturn[j]
	return i, value

def maxDrawdown(dailyReturn):
	'''
		pass in a pandas series, return the historical maximum drawdown, i is
		the index for  peak, j is the index for trough.
	'''
	h, value = currentDrawdown(dailyReturn)
	# hReturn is used to store the historical return before the current peak
	hReturn = dailyReturn[:h]
	j = (hReturn.cummax() - hReturn).argmax()
	i = hReturn[:j].argmax()
	# store the peak-to-trough cumulative days in variable "days"
	days = (j - i).days
	# store the value of maxdDrawdown in "value"
	value = hReturn[i] - hReturn[j]
	return i, j, days, value


def test_AbsDrawDown(strategy, df, PNL, GMV):
	'''
		test if absolute current drawdown (in $) exceeds $10M
	'''
	i, value = currentDrawdown(PNL)
	threshold = 10000000
	if (abs(value) > threshold):
		newDf = pd.DataFrame([[strategy,
							'AbsDrawDown',
							value - threshold,
							value,
							GMV[-1],
							PNL[-1]]],
							columns = df.columns)
		df = pd.concat([df, newDf])
	return df

def test_EQYDrawDown(strategy, df, PNL, GMV, dailyReturn):
	'''
		test current drawdown (in % of current gross market value) exceeds 5%
	'''
	i, value = currentDrawdown(dailyReturn)
	threshold = 0.05
	if (value > threshold):
		newDf = pd.DataFrame([[strategy,
							'EQYDrawDown',
							value - threshold,
							value,
							GMV[-1],
							PNL[-1]]],
							columns = df.columns)
		df = pd.concat([df, newDf])
	return df

def test_LargestDrawDown(strategy, df, PNL, GMV, dailyReturn):
	'''
		test if current drawdown (in %) exceeds (tolerance * previous largest
		drawdown (in %)); tolerance = 1.2
	'''
	# variable i is just a placeholder, will not be used to generate the output
	i, value = currentDrawdown(dailyReturn)
	i, j, days, mValue = maxDrawdown(dailyReturn)
	tolerance = 1.2
	threshold = tolerance * mValue
	if (value > threshold):
		newDf = pd.DataFrame([[strategy,
							'LargestDrawDown',
							value - threshold,
							value,
							GMV[-1],
							PNL[-1]]],
							columns = df.columns)
		df = pd.concat([df, newDf])
	return df


def test_LongestDrawDown(strategy, df, PNL, GMV):
	'''
		test if current drawdown (in days) exceeds (tolerance * previous
		largest drawdown (in days)); tolerance = 1.5;
	'''
	# i is used to store the time of current peak, v is a placeholder
	i, v = currentDrawdown(PNL)
	# value represent the current drawdown(in days)
	value = (PNL.index[-1] - i).days
	tolerance = 1.5
	i, j, days, mValue = maxDrawdown(PNL)
	threshold = days * tolerance
	if (value > threshold):
		newDf = pd.DataFrame([[strategy,
							'LongestDrawDown',
							value - threshold,
							value,
							GMV[-1],
							PNL[-1]]],
							columns = df.columns)
		df = pd.concat([df, newDf])
	return df

def test_LargestDownDay(strategy, df, pnl, PNL, GMV, n):
	'''
		current largest down day (in %) in past n (configurable) days exceeds
		(tolerance * previous largest down day (in %), during all such previous
		n-day periods); tolerance = 2;
	'''
	downPercentage = []
	for i in range(len(pnl) - n + 1):
		window = pnl[i: i+n]
		percent = (window < 0).sum()/n
		downPercentage.append(percent)
	value = downPercentage[-1]
	tolerance = 2
	threshold = max(downPercentage) * tolerance
	if (value > threshold):
		newDf = pd.DataFrame([[strategy,
							'LargestDownDay',
							value - threshold,
							value,
							GMV[-1],
							PNL[-1]]],
							columns = df.columns)
		df = pd.concat([df, newDf])
	return df


def maxConsecutiveDownDays(window):
	'''
		pass-in window is a pandas serie, the output is the maxium number of
		consecutive down days in this time window.
	'''
	window = (window < 0).astype(int)
	N = 0
	maxN = 0
	i = 0
	while(i < len(window)):
		if window[i] == 1:
			N += 1
			i += 1
			if N > maxN:
				maxN = N
		else:
			N = 0
			i += 1
	return maxN


def test_MostConsecutiveDownDays(strategy, df, PNL, GMV, pnl, n):
	'''
		test if current largest # of consecutive down days (in days) in past n
		(configurable) days exceeds (tolerance * previous most consecutive down
		days (in days), during all such previous n-day periods), tolerance = 1.2
	'''
	downDays = []
	for i in range(len(pnl) - n + 1):
		window = pnl[i: i+n]
		downDays.append(maxConsecutiveDownDays(window))

	value = downDays[-1]
	tolerance = 1.2
	threshold = max(downDays) * tolerance
	if (value > threshold):
		newDf = pd.DataFrame([[strategy,
							'MostConsecutiveDownDays',
							value - threshold,
							value,
							GMV[-1],
							PNL[-1]]],
							columns = df.columns)
		df = pd.concat([df, newDf])
	return df

def test_FewestUpDays(strategy, df, pnl, PNL, GMV, n):
	'''
		current # of up days (in days) in past n (configurable) days is less
		than (tolerance * previous lowest # up days (in days) , during all such
		previous n-day periods); tolerance = 0.3 ;
	'''
	upDays= []
	for i in range(len(pnl) - n + 1):
		window = pnl[i: i+n]
		percent = (window > 0).sum()
		upDays.append(percent)
	value = upDays[-1]
	tolerance = 0.3
	threshold = min(upDays) * tolerance
	if (value < threshold):
		newDf = pd.DataFrame([[strategy,
							'FewestUpDays',
							value - threshold,
							value,
							GMV[-1],
							PNL[-1]]],
							columns = df.columns)
		df = pd.concat([df, newDf])
	return df