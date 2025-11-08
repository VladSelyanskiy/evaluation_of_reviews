# Standard python library imports
import pickle

# Related third party imports
import tensorflow as tf

# Local imports
from shemas.service_config import config


class LSTM2Classes:
    model_path = config.LSTM_FOR_2_ClASSES_CLASSIFIER_PATH
    tokenizer_path = config.TOKENIZER_FOR_LSTM2CLASSES_PATH

    def __init__(self, max_sequence_length=100):
        # Загрузка модели
        self.LSTM_model = tf.keras.models.load_model(self.model_path)
        self.max_sequence_length = max_sequence_length

        # Загрузка токенизатора
        try:
            with open(self.tokenizer_path, "rb") as f:
                self.tokenizer = pickle.load(f)
        except FileNotFoundError:
            print("Токенизатор не найден.")
            self.tokenizer = None

    def use_model_lstm(self, text) -> int:
        sequence = self.tokenizer.texts_to_sequences([text])
        data = tf.keras.preprocessing.sequence.pad_sequences(
            sequence, maxlen=self.max_sequence_length
        )
        prediction = self.LSTM_model.predict(data)
        return prediction[0]
