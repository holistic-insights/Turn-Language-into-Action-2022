import autokeras as ak
import numpy as np
import pandas as pd
import tensorflow as tf
from autokeras import TextRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tensorflow.keras.models import load_model

if __name__ == "__main__":
    comments = pd.read_csv('Data/comments_sentiment.csv')
    posts = pd.read_csv('Data/posts.csv')

    # each post's overall sentiment is the average of all its comments' sentiment scores
    posts['sentiment'] = posts['urn'].apply(lambda x: comments[comments.post_urn == x]['sentiment'].mean())
    posts = posts[posts['sentiment'].notna()]
    posts = posts[['text', 'sentiment']].reset_index(drop=True)

    # split into train-test
    split = int(posts.shape[0] * 0.8)
    train = posts[:split]
    test = posts[split:]

    x_train = np.array(train.text)
    y_train = np.array(train.sentiment)
    x_test = np.array(test.text)
    y_test = np.array(test.sentiment)

    # fit text regressor
    text_reg = TextRegressor(overwrite=True, max_trials=1)
    text_reg.fit(
        x_train,
        y_train,
        validation_split=0.15
    )

    # export and save model
    model = text_reg.export_model()
    try:
        model.save('model_autokeras', save_format='tf')
    except Exception:
        model.save('model_autokeras.h5')

    # load saved model and predict
    loaded_model = load_model('model_autokeras', custom_objects=ak.CUSTOM_OBJECTS)
    y_pred = loaded_model.predict(tf.expand_dims(x_test, -1))

    print(mean_squared_error(y_test, y_pred), mean_absolute_error(y_test, y_pred), r2_score(y_test, y_pred))
