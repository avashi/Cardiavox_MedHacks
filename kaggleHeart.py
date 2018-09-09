import wave, struct, csv
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from scipy.signal import decimate
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Conv1D, MaxPool1D, GlobalAvgPool1D, Dropout, BatchNormalization, Dense
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping
from keras.utils import np_utils
from keras.regularizers import l2




def batch_generator(x_train, y_train, batch_size):
    x_batch = np.empty((batch_size, x_train.shape[1], x_train.shape[2]), dtype='float32')
    y_batch = np.empty((batch_size, y_train.shape[1]), dtype='float32')
    full_idx = range(x_train.shape[0])

    while True:
        batch_idx = np.random.choice(full_idx, batch_size)
        x_batch = x_train[batch_idx]
        y_batch = y_train[batch_idx]

        for i in range(batch_size):
            sz = np.random.randint(x_batch.shape[1])
            x_batch[i] = np.roll(x_batch[i], sz, axis = 0)

        yield x_batch, y_batch

CLASSES = ['artifact', 'normal', 'murmur']
CODE_BOOK = {x:i for i,x in enumerate(CLASSES)}
NB_CLASSES = len(CLASSES)
output = []

with open('/Users/parthpatel/Desktop/Sandwich/heartbeat-sounds/set_a.csv', 'r') as files:
    reader = csv.reader(files)
    next(reader)
    time = []
    output = []
    count = 0;
    for row in reader:
        labels = 0
        count += 1
        audio = []
        filename = row[1]
        # if count >= 125 and count < 437:
        #     filename = filename[0:6] + filename[16:]
        #     files = filename.split("_",2)
        #     filename = files[0] + "_" + files[1] + "__" + files[2]
        # elif count >= 437:
        #     filename = filename[0:6] + filename[16:22] + filename[31:]
        #     print(filename)
        f = wave.open('/Users/parthpatel/Desktop/Sandwich/heartbeat-sounds'+'/'+filename, 'r')
        frames = f.readframes(-1)

        samples = struct.unpack('h'*f.getnframes(), frames)
        samples = np.asarray(samples)
        length = 396900
        result = np.empty((length, ), dtype = 'float32')
        l = len(samples)
        pos = 0
        while pos + l <= length:
            result[pos:pos+l] = samples
            pos += l
        if pos < length:
            result[pos:length] = samples[:length-pos]
        samples = result
        framerate = f.getframerate()
        t = [float(i)/framerate for i in range(len(samples))]
        time.append(t)
        if len(output) == 0:
            labels = int(row[4])
            samples = np.hstack((samples,labels))
            output = samples
        else:
            labels = int(row[4])
            samples = np.hstack((samples,labels))
            output = np.vstack((output,samples))
    print('go')

fData = output[:,0:396900]
fTarget = output[:,396900]
print(fTarget)
fData = np.array(fData)
# fData = fData.astype(np.float)
fTarget = np.array(fTarget)
# fTarget = fTarget.astype(np.float)
new_labels = np.array(fTarget, dtype='int')
y_data = np_utils.to_categorical(new_labels,3)
print(y_data)
# regr = MLPClassifier(hidden_layer_sizes=(100,100,100),max_iter=1000)
# higher alpha, lbfgs?, hidden layers?, activation function?, amount of data, multioutput regressor, train size,
x_train, x_test, y_train, y_test = train_test_split(
    fData, y_data, test_size=0.25)
# scores = cross_val_score(regr, x_train, y_train, cv=10)
# print("CVscores")
# print(scores)
# print("mean")
# print(scores.mean())
x_train = decimate(x_train, 8, axis=1)
x_train = decimate(x_train, 8, axis=1)
# x_train = decimate(x_train, 4, axis=1)
# print(len(x_train[0]))
x_test = decimate(x_test, 8, axis=1)
x_test = decimate(x_test, 8, axis=1)
# x_test = decimate(x_test, 4, axis=1)

x_train = x_train / np.std(x_train, axis=1).reshape(-1,1)
x_test = x_test / np.std(x_test, axis=1).reshape(-1,1)

x_train = x_train[:,:,np.newaxis]
x_test = x_test[:,:,np.newaxis]

model = Sequential()
model.add(Conv1D(filters=4, kernel_size=9, activation='relu',
                input_shape = x_train.shape[1:],
                kernel_regularizer = l2(0.025)))
model.add(MaxPool1D(strides=4))
model.add(BatchNormalization())
model.add(Conv1D(filters=4, kernel_size=9, activation='relu',
                kernel_regularizer = l2(0.05)))
model.add(MaxPool1D(strides=4))
model.add(BatchNormalization())
model.add(Conv1D(filters=8, kernel_size=9, activation='relu',
                 kernel_regularizer = l2(0.1)))
model.add(MaxPool1D(strides=4))
model.add(BatchNormalization())
model.add(Conv1D(filters=16, kernel_size=9, activation='relu'))
model.add(MaxPool1D(strides=4))
model.add(BatchNormalization())
model.add(Dropout(0.25))
model.add(Conv1D(filters=64, kernel_size=4, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.5))
model.add(Conv1D(filters=32, kernel_size=1, activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.75))
model.add(GlobalAvgPool1D())
model.add(Dense(3, activation='softmax'))


weight_saver = ModelCheckpoint('set_a_weights.h5', monitor='val_loss',
                               save_best_only=True, save_weights_only=True)
model.compile(optimizer=Adam(1e-5), loss='categorical_crossentropy', metrics=['accuracy'])
annealer = LearningRateScheduler(lambda x: 1e-4 * 0.8**x)
hist = model.fit_generator(batch_generator(x_train, y_train, 8),epochs=30, steps_per_epoch=1000,validation_data=(x_test, y_test),callbacks=[weight_saver, annealer],verbose=2)

model.load_weights('set_a_weights.h5')

plt.plot(hist.history['loss'], color='b')
plt.plot(hist.history['val_loss'], color='r')
plt.show()
plt.plot(hist.history['acc'], color='b')
plt.plot(hist.history['val_acc'], color='r')
plt.show()

print(len(x_test))
print(len(x_test[0]))
y_hat = model.predict(x_test)
print(y_hat)
np.set_printoptions(precision=2, suppress=True)
for i in range(3):
    plt.plot(y_hat[:,i], c='r')
    plt.plot(y_test[:,i], c='b')
    plt.show()
    print(CLASSES[i])
print(y_test)
# 1,0,0 = 0
# 0,1,0 = 1
# 0,0,1 = 2
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
