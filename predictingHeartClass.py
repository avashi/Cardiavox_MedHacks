from keras.models import model_from_json
import wave, struct
import numpy as np
from scipy.signal import decimate

json_file = open('model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("set_a_weights.h5")
print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# score = loaded_model.evaluate(X, Y, verbose=0)
f = wave.open('/Users/parthpatel/Desktop/Sandwich/heartbeat-sounds/set_b/murmur__162_1307101835989_A.wav', 'rb')


frames = f.readframes(-1)
sample_x = struct.unpack('h'*f.getnframes(), frames)
sample_x = np.asarray(sample_x)
length = 396900
result = np.empty((length, ), dtype = 'float32')
l = len(sample_x)
pos = 0
while pos + l <= length:
    result[pos:pos+l] = sample_x
    pos += l
if pos < length:
    result[pos:length] = sample_x[:length-pos]
sample_x = result
X = decimate(sample_x, 8, axis=0)
X = decimate(X, 8, axis=0)
X = X / np.std(X, axis=0).reshape(-1,1)
X = X[:,:,np.newaxis]
y_hat = loaded_model.predict(X)
y_hat = y_hat[0]
print(y_hat)
for ind in [0,1,2]:
    if y_hat[ind] == max(y_hat):
        y_hat = ind
        break
print("Predicted: " + str(y_hat))
