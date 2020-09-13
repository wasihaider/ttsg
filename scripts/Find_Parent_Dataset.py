import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.model_selection import train_test_split
from scripts.constants_ttsg import DATASET_FILE_PATH


#############################################################################################

class DatasetPreprocessing:
    """
    This class will have objects which will pre-process given data-set
    """
    def __init__(self):
        self.__df = pd.read_csv(DATASET_FILE_PATH)
        self.train_data = None
        self.test_data = None
        self.y_train = None
        self.y_test = None
        self.split_data_to_train_test()
        self.__numClasses = None
        self.__vectorizer = None

    ######################################################

    def get_data(self):
        """
        This method is to get data frame of all the dataset used
        :return __df: dataframe of all dataset(private var of this class)
        """
        return self.__df

    ######################################################

    def split_data_to_train_test(self):
        """
        This method splits data frame to train test dependent vars and independent vars
        :return: Returns nothing
        """
        try:
            sentences = self.__df['sentence'].values  # Getting sentences
            y = self.__df['label'].values  # Getting class type

            sentences = np.array(sentences)  # converting to numpy arrays
            y = np.array(y)
            # here the data is split in train and test with(75% in train and 25% in test)
            self.train_data, self.test_data, self.y_train, self.y_test = train_test_split(sentences, y,
                                                                                           test_size=0.25,
                                                                                           random_state=1000)
        except Exception as e:
            print("Exception in Find_Parent_Dataset.py (split_data_to_train_test method): ", str(e))

    ######################################################

    def get_num_classes(self):
        """
        This method calculates and returns the expected number of outputs or classes to predict
        :return __numClasses: number of classes( or labels and outputs)
        """
        try:
            self.__numClasses = max(self.y_train) + 1
            return self.__numClasses
        except Exception as e:
            print("Exception in Find_Parent_Dataset.py (get_num_classes method): ", str(e))

    ######################################################

    def transform(self, data):
        """
        This methods transforms sentence given with CountVectorizer
        :param data: sentence to transform
        :return __vectorizer.transform(data): transformed sentence
        """
        try:
            self.__vectorizer = CountVectorizer()
            self.__vectorizer = self.__vectorizer.fit(self.train_data)
            return self.__vectorizer.transform(data)
        except Exception as e:
            print("Exception in Find_Parent_Dataset.py (transform method): ", str(e))


#############################################################################################

if __name__ == '__main__':
    data = DatasetPreprocessing()
    print(type(data.train_data), type(data.y_train))
    sentence = [data.train_data[0]]
    sentence = data.transform(sentence)
    print(type(sentence))
#
#############################################################################################
