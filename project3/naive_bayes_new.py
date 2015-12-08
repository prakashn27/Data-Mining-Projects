import fetchdata
import math

def seperate_data(_data):
	train_len = int(math.floor(len(_data) * 0.7))
	train_data = []
	for i in range(train_len):
		res = []
		for item in _data[i]:
			try:
				x = float(item)
				res.append(x)
			except:
				if item.lower() == "absent":
					res.append(0)
				else:
					res.append(1)
		train_data.append(res)
	test_data = []
	for i in range(train_len, len(_data)):
		res = []
		for item in _data[i]:
			try:
				x = float(item)
				res.append(x)
			except:
				if item.lower() == "absent":
					res.append(0)
				else:
					res.append(1)
		test_data.append(res)
	return train_data, test_data

def seperateByClass(train_data):
	seperated = {}
	for data in train_data:
		attr = int(data[-1])
		if not attr in seperated:
			# create a new instace
			seperated[attr] = list()
			seperated[attr].append(data[:-1])
		else:
			seperated[attr].append(data[:-1])
	return seperated

def mean(nums):
	return sum(nums)/float(len(nums))

def standardDeviation(num):
	avg = mean(num)
	if len(num) == 1:
		return num[0]
	variance = sum([pow(x-avg,2) for x in num])/float(len(num)-1)
	return math.sqrt(variance)

def summarize(instances):
	summaries = [(mean(attribute), standardDeviation(attribute)) for attribute in zip(*instances)]
	del summaries[-1]
	return summaries

def summarizeByClass(separated):
	summaries = {}
	for classValue, instances in separated.iteritems():
		summaries[classValue] = summarize(instances)
	return summaries

def calculateProbability(x, mean, sd):
	exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(sd,2))))
	return (1 / (math.sqrt(2*math.pi) * sd)) * exponent

	#########################

def calculateClassProbabilities(summaries, inputVector):
	probabilities = {}
	for classValue, classSummaries in summaries.iteritems():
		probabilities[classValue] = 1
		for i in range(len(classSummaries)):
			mean, stdev = classSummaries[i]
			x = inputVector[i]
			probabilities[classValue] *= calculateProbability(x, mean, stdev)
	return probabilities
			
def predict(summaries, inputVector):
	probabilities = calculateClassProbabilities(summaries, inputVector)
	bestLabel, bestProb = None, -1
	for classValue, probability in probabilities.iteritems():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel

def getPredictions(summaries, testSet):
	predictions = []
	for i in range(len(testSet)):
		result = predict(summaries, testSet[i])
		predictions.append(result)
	return predictions

def getAccuracy(testSet, predictions):
	correct = 0
	for i in range(len(testSet)):
		if testSet[i][-1] == predictions[i]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

if __name__ == "__main__":
	_data = fetchdata.get_data('project3_dataset2.txt')
	# _data = fetchdata.get_data('test.txt')
	train_data, test_data = seperate_data(_data)
	print len(train_data), len(test_data)
	seperated = seperateByClass(train_data)
	summary = summarizeByClass(seperated)
	# for key in summary:
	# 	print summary[key]
	predictions = getPredictions(summary, test_data)
	accuracy = getAccuracy(test_data, predictions)
	print('Accuracy: {0}%').format(accuracy)


