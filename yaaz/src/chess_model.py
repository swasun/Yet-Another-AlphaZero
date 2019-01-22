from keras.optimizers import SGD
from keras.layers import Conv2D, Flatten, Input, Dense, BatchNormalization, ReLU, Add
from keras.models import Model
from keras import losses


class ChessModel(object):

    def __init__(self):
        self._model = self._build()

    def predict(self, state):
        return self._model.predict_on_batch(state)

    def fit(self, state, labels):
        return self._model.fit(state, labels, epochs=1, verbose=1, validation_split=0, batch_size=1) 

    def save(self, path):
        self._model.save(path)

    def _residual_layer(self, x):
        resBlock = Conv2D(76, kernel_size=4, padding='same', strides=1)(x)
        resBlock = BatchNormalization()(resBlock)
        resBlock = ReLU()(resBlock)
        resBlock = Conv2D(76, kernel_size=4, padding='same', strides=1)(resBlock)
        resBlock = BatchNormalization()(resBlock)
        resBlock = Add()([x, resBlock])
        resBlock = ReLU()(resBlock)
        return resBlock
        
    def _policy_head(self, x):
        policy = Conv2D(2, kernel_size=1, padding='same', strides=1)(x)
        policy = BatchNormalization()(policy)
        policy = ReLU()(policy)
        policy = Flatten()(policy)
        policy = Dense(4672, name = 'policy_head')(policy)
        return policy
        
    def _value_head(self, x):
        value = Conv2D(1, kernel_size=1, padding='same', strides=1)(x)
        value = BatchNormalization()(value)
        value = ReLU()(value)
        value = Flatten()(value)
        value = Dense(256)(value)
        value = ReLU()(value)
        value = Dense(1, activation='tanh', name = 'value_head')(value)
        return value
        
    def _loss_function(self, y_true, y_pred):
        loss1 = losses.mean_squared_error(y_true, y_pred)
        loss2 = losses.categorical_crossentropy(y_true, y_pred)
        return loss1 + loss2
        
    def _build(self):
        input_stack = Input(shape=(119, 8, 8))
        x = Conv2D(76, kernel_size=4, strides=1, padding='same', input_shape=(119, 8, 8))(input_stack)
        x = BatchNormalization()(x)
        x = ReLU()(x)
        for i in range(2):
            x = self._residual_layer(x)
        policy = self._policy_head(x)
        value = self._value_head(x)
        losses = {"value_head": "mean_squared_error", "policy_head": "categorical_crossentropy"}
        loss_weights = {"policy_head": .5, "value_head": .5}
        model = Model(inputs=input_stack, outputs=(policy, value))
        
        model.compile(
            loss=losses,
            optimizer=SGD(lr=0.1, momentum=0.9),
            loss_weights=loss_weights
        )

        return model
