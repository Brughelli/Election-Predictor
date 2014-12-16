"""
 Michael Brughelli
 4830 Final Project
 Classifier.py
 SEE README FOR IMPORTANT INFORMATION
 
 This file is a custom classifier using textblob as a wrapper over a Naive
 Bayes Classifier defined in NLTK's wordnet corpora. It reads in training data 
 (tweets) from a csv file and trains on them to create a classifier based on the 
 training data.  The 'DATASEN.csv' and 'DATAGOV.csv' files contains training data for the 
 Colorado Senate race between Udall and Gardner and Colorado Governor race between Bob
 Beauprez and John Hickenlooper, respectively. The RvsD file contains general Republican vs. 
 Democrat training data. The 'COSEN.csv' and 'COGOV.csv' files contain all data from those 
 races and is what yields the final predictions.  The files 'MarkedSEN.csv' and 'MarkedGOV.csv'
 contain all data that has been marked by and agreed upon by 2 humans.  It is the data used to 
 calculate the accuracy of the predictions. This file is read in and classified for the purpose 
 of determining the accuracy of the classifier.  I use the accuracy(test_data) method given by 
 the textblob library to do just that.
"""
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
import sys

"""
 Each line of the training input file which is formatted as such: tweet content.,category
 (Note that category is either pos or neg and they are separated by a comma.).
 
 make_tuple takes each line of the training input and creates a tuple out of each one.
"""
def make_tuple(line):
	tweet, cat = line.strip("\n").split(",")
	return (tweet, cat)
	
def take_data_in():
	global training_data
	training_data = raw_input("\nEnter training data file name as <filename>.csv then press enter\n")
	
	global testing_data
	testing_data = raw_input("\nEnter testing data file name as <filename>.csv then press enter\n")
	
	global marked_data
	marked_data = raw_input("\nEnter Marked data file name as <filename>.csv then press enter\n")
	
	return training_data, testing_data, marked_data	

def main():
	
	take_data_in()
	training(training_data)
	testing(testing_data)
	accuracy_test(marked_data)
	
	print "\nTo test another race, type python Classifier.py in the terminal\n" 
	
def training(training_data):	
	with open(training_data, 'rU') as fp:
		#The following line ensures the file is decoded into utf-8
		fp = [line.decode('utf-8').strip() for line in fp.readlines()]
		data = [make_tuple(line) for line in fp] #Creates list of tuples
		"""
		Above I create a list of the generated tuples (tweet, cat) because NLTK's 
		classifier requires this format for training and testing data.
		"""
	#print data
		
	train = data
	#print train	
	
	# Now train on the training data with the NLTK wordnet
	global cl
	cl = NaiveBayesClassifier(train)
	
	return cl
	"""
	When marking the data by hand, my assistant and I made the arbitrary decision of
	classifying positive things said about the Republican candidate as 'pos' and
	positive things said about the Democratic candidate as 'neg'.  And then 
	obviously negative things about the Republican were marked 'neg' and negative
	things said about the Democrat were marked 'pos'.
	"""
	
def testing(testing_data):

	#Read in MASTERDATA.csv which is unmarked, final result data
	with open(testing_data, 'r') as fp1: 
		if cl.classify(fp1) == 'pos': #classifies entire MASTERDATA file as either 'pos' or 'neg'
			if testing_data == 'COSEN.csv':
				print "\nCory Gardner will win!"
			elif testing_data == 'COGOV.csv':
				print "\nBob Beauprez will win!"
		else:
			if testing_data == 'COSEN.csv':
				print "\nMark Udall will win!"
			elif testing_data == 'COGOV.csv':
				print "\nJohn Hickenlooper will win!"

def accuracy_test(marked_data):
			
	with open(marked_data, 'r') as fp2:	
		print (str(float(round(cl.accuracy(fp2) * 100)))) + "% accuracy between training and testing data"


main()
