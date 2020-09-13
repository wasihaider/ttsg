from keras.layers import Dense
from scripts.Find_Parent_Dataset import DatasetPreprocessing
from keras.utils import to_categorical
from keras.models import Sequential


#############################################################################################

class FindParentModel:
    def __init__(self):
        self.__dataset = DatasetPreprocessing()

        # get data from the data set in train test data and classes
        self.__train_data = self.__dataset.train_data
        self.__test_data = self.__dataset.test_data
        self.__y_train = self.__dataset.y_train
        self.__y_test = self.__dataset.y_test

        self.__data_transformation()

        self.__model = None

    ######################################################

    def get_train_data(self):
        """
        This method is to get only the training data
        :return: Returns private variable of this class train_data
        """
        return self.__train_data

    ######################################################

    def __data_transformation(self):
        """
        This method transforms all the data set train test split variable with countVectorizer
        :return: Return nothing
        """
        try:
            self.__train_data = self.__dataset.transform(self.__train_data)
            self.__test_data = self.__dataset.transform(self.__test_data)
            # transform y data according to classes categories
            self.__y_train = to_categorical(self.__y_train, num_classes=self.__dataset.get_num_classes())
            self.__y_test = to_categorical(self.__y_test, num_classes=self.__dataset.get_num_classes())
        except Exception as e:
            print("Exception in Model.py, Class FindParentModel (__data_transformation method)", str(e))

    ######################################################

    def __create_structure(self):
        """
        This method just create structure of keras model(The layers, activation functions and neurons)
        :return:
        """
        try:
            input_dim = self.__train_data.shape[1]  # Input Dimension as(20,)

            self.__model = Sequential()
            self.__model.add(Dense(10, input_dim=input_dim, activation='relu'))
            self.__model.add(Dense(20, activation='relu'))
            self.__model.add(Dense(self.__dataset.get_num_classes(), activation='softmax'))
            self.__model.compile(loss='categorical_crossentropy',
                                  optimizer='adam',
                                  metrics=['accuracy'])
            print(self.__model.summary())
        except Exception as e:
            print("Exception in Model.py, Class FindParentModel (__create_structure method)", str(e))

    ######################################################

    def train_model(self):
        """
        This method performs actual training of keras model
        :return: Returns nothing
        """
        try:
            self.__create_structure()
            batch_size = 50
            epochs = 1000

            history = self.__model.fit(self.__train_data, self.__y_train,
                                        batch_size=batch_size,
                                        epochs=epochs,
                                        verbose=1,
                                        validation_split=0.1)  # 10% of the training data will be used as validation
            print(type(self.__model))
        except Exception as e:
            print("Exception in Model.py, Class FindParentModel (train_model method)", str(e))

    ######################################################

    def evaluate_model(self):
        """
        This method is used to evaluate the accuracy of model
        :return: Returns nothing
        """
        try:
            batch_size = 5

            score = self.__model.evaluate(self.__test_data, self.__y_test,
                                           batch_size=batch_size,
                                           verbose=1)
            print("Accuracy: {}".format(score[1]))
        except Exception as e:
            print("Exception in Model.py, Class FindParentModel (evaluate_model method)", str(e))

    ######################################################

    def save_model(self):
        """
        This method saves the model in keras known file extension h5
        :return: Returns nothing
        """
        try:
            self.__model.save('FindParentMode.h5')
        except Exception as e:
            print("Exception in Model.py, Class FindParentModel (save_model method)", str(e))


#############################################################################################

if __name__ == '__main__':
    model = FindParentModel()
    data = model.get_train_data()
    print(type(model.get_train_data()))
    # model.create_structure()
    model.train_model()
    # model.evaluate_model()
    # model.save_model()

#############################################################################################
