# ============================================
# TRAIN EMOTION MODEL
# ============================================

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Flatten, Dense, Dropout

import matplotlib.pyplot as plt

# ============================================
# DATASET PATH
# ============================================

train_dir = "dataset/train"
test_dir = "dataset/test"

# ============================================
# IMAGE PREPROCESSING
# ============================================

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(
    rescale=1./255
)

train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=(48,48),
    batch_size=64,
    color_mode='grayscale',
    class_mode='categorical'
)

test_data = test_datagen.flow_from_directory(
    test_dir,
    target_size=(48,48),
    batch_size=64,
    color_mode='grayscale',
    class_mode='categorical'
)

# ============================================
# BUILD CNN MODEL
# ============================================

model = Sequential()

model.add(Conv2D(
    32,
    (3,3),
    activation='relu',
    input_shape=(48,48,1)
))

model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Conv2D(
    64,
    (3,3),
    activation='relu'
))

model.add(MaxPooling2D(pool_size=(2,2)))

model.add(Flatten())

model.add(Dense(128, activation='relu'))

model.add(Dropout(0.5))

model.add(Dense(5, activation='softmax'))

# ============================================
# COMPILE MODEL
# ============================================

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ============================================
# TRAIN MODEL
# ============================================

history = model.fit(
    train_data,
    epochs=20,
    validation_data=test_data
)

# ============================================
# SAVE MODEL
# ============================================

model.save("emotion_model.h5")

print("Model Saved Successfully!")

# ============================================
# ACCURACY GRAPH
# ============================================

plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])

plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')

plt.legend(['Train', 'Validation'])

plt.show()

# ============================================
# LOSS GRAPH
# ============================================

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')

plt.legend(['Train', 'Validation'])

plt.show()