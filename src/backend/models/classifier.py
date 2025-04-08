import dill


class Classifier:
    """
    Классификатор, использующий модели логистической регрессии и наивного Байеса.
    """

    classes = {0: "negative", 1: "positive"}

    # Загрузка модели логистической регрессии
    with open(
        r"src\backend\models_weights\logistic_regression_classifier.pickle", "rb"
    ) as f:
        logreg_model = dill.load(f)["model"]

    # Загрузка модели наивного Байеса
    with open(r"src\backend\models_weights\naive_bayes_classifier.pickle", "rb") as f:
        nb_model = dill.load(f)["model"]

    def use_model_nb(self, text: str) -> int:
        """
        Возвращает предсказание, используя модель наивного Байеса.

        Аргументы:
        text -- входной текст для классификации

        Возвращает:
        Метку класса для текста.
        """
        prediction = self.nb_model.predict([text])
        return prediction[0]

    def use_model_lr(self, text: str) -> int:
        """
        Возвращает предсказание, используя модель логистической регрессии.

        Аргументы:
        text -- входной текст для классификации

        Возвращает:
        Метку класса для текста.
        """
        prediction = self.logreg_model.predict([text])
        return prediction[0]
