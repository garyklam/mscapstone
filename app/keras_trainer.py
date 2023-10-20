import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications.efficientnet import EfficientNetB5
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, BatchNormalization, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers


# Define constants
image_size = (456, 456)
batch_size = 16
num_classes = 46
num_epochs = 20

# Load and preprocess the data
# train_datagen = ImageDataGenerator(
#     rescale=1./255,
#     # validation_split=0.2,
#     # rotation_range=20,  # Randomly rotate images by 20 degrees
#     # width_shift_range=0.2,  # Randomly shift images horizontally by 20% of the width
#     # height_shift_range=0.2,  # Randomly shift images vertically by 20% of the height
#     # shear_range=0.2,  # Apply shear transformation with a shear intensity of 0.2
#     # zoom_range=0.2,  # Apply zoom transformation within a range of 0.2
#     # horizontal_flip=True,  # Randomly flip images horizontally
#     # fill_mode='nearest'  # Use the nearest neighbor strategy to fill newly created pixels
# )
train_datagen = ImageDataGenerator(
    rescale=1./255, validation_split=0.2)

train_generator = train_datagen.flow_from_directory(
    'C:\\Users\\garyk\\Downloads\\Train_species_upscale',
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='training'
)

validation_generator = train_datagen.flow_from_directory(
    'C:\\Users\\garyk\\Downloads\\Train_species_upscale',
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical',
    subset='validation'
)

img_augmentation = Sequential(
    [
        layers.RandomRotation(factor=0.15),
        layers.RandomTranslation(height_factor=0.1, width_factor=0.1),
        layers.RandomFlip(),
        layers.RandomContrast(factor=0.1),
    ],
    name="img_augmentation",
)
inputs = layers.Input(shape=(456, 456, 3))
x = img_augmentation(inputs)
model = EfficientNetB5(include_top=False, input_tensor=x, weights='imagenet')# base_model.load_weights('C:\\Users\\garyk\\PycharmProjects\\pythonProject\\noisystudent\\noisy.student.notop-b5.h5')

# Freeze the pre-trained layers
model.trainable = False

# Add custom classification layers
x = GlobalAveragePooling2D(name="avg_pool")(model.output)
x = BatchNormalization()(x)

top_dropout_rate = 0.2
x = Dropout(top_dropout_rate, name="top_dropout")(x)
outputs = Dense(46, activation="softmax", name="pred")(x)

# Create the final model
model = Model(inputs=inputs, outputs=outputs, name="EfficientNet")

# Compile the model
optimizer = tf.keras.optimizers.Adam(learning_rate=1e-2)
model.compile(optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"])

hist = model.fit(train_generator, epochs=num_epochs, validation_data=validation_generator, verbose=2)

# history = model.fit(
#     train_generator,
#     steps_per_epoch=train_generator.samples // batch_size,
#     epochs=num_epochs,
#     validation_data=validation_generator,
#     validation_steps=validation_generator.samples // batch_size
# )

# # Display the loss and accuracy for each epoch
# loss_values = history.history['loss']
# accuracy_values = history.history['accuracy']
# val_loss_values = history.history['val_loss']
# val_accuracy_values = history.history['val_accuracy']
#
# for epoch in range(num_epochs):
#     print(f"Epoch {epoch+1}:")
#     print(f"  Loss: {loss_values[epoch]:.4f}")
#     print(f"  Accuracy: {accuracy_values[epoch]:.4f}")
#     print(f"  Validation Loss: {val_loss_values[epoch]:.4f}")
#     print(f"  Validation Accuracy: {val_accuracy_values[epoch]:.4f}")
#     print()

# Save the model
model.save('5_19_keras_effnetb0_20')
