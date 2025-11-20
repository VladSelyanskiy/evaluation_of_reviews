# Related third party imports
import dill  # type: ignore

# Local imports
from tools.service_config import config


class Classifier:
    """
    Классификатор, использующий модели логистической регрессии и наивного Байеса.
    """

    classes = {0: "negative", 1: "positive"}

    # Загрузка модели логистической регрессии
    with open(config.LOGISTIC_REGRESSION_CLASSIFIER_PATH, "rb") as f:
        logreg_model = dill.load(f)["model"]

    # Загрузка модели наивного Байеса
    with open(config.NAIVE_BAYES_CLASSIFIER_PATH, "rb") as f:
        nb_model = dill.load(f)["model"]

    def use_model_nb(self, text: str) -> tuple[int, float]:
        """
        Возвращает предсказание, используя модель наивного Байеса.

        Аргументы:
        text -- входной текст для классификации

        Возвращает:
        Метку класса для текста и её вероятность.
        """
        prediction = int(self.nb_model.predict([text])[0])
        proba = float(self.nb_model.predict_proba([text])[0][prediction])
        return (prediction, proba)

    def use_model_lr(self, text: str) -> tuple[int, float]:
        """
        Возвращает предсказание, используя модель логистической регрессии.

        Аргументы:
        text -- входной текст для классификации

        Возвращает:
        Метку класса для текста и её вероятность.
        """
        prediction = int(self.logreg_model.predict([text])[0])
        proba = float(self.logreg_model.predict_proba([text])[0][prediction])
        return (prediction, proba)
