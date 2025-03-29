import dill


class Classifier:

    classes = {0: "negative", 1: "positive"}

    with open(
        r"src\backend\models_weights\logistic_regression_classifier.pickle", "rb"
    ) as file:
        logreg_model = dill.load(file)["model"]

    with open(
        r"src\backend\models_weights\naive_bayes_classifier.pickle", "rb"
    ) as file:
        nb_model = dill.load(file)["model"]

    def use_model_nb(self, text):
        prediction = self.nb_model.predict([text])
        return self.classes[prediction[0]]

    def use_model_lr(self, text):
        prediction = self.nb_model.predict([text])
        return self.classes[prediction[0]]
