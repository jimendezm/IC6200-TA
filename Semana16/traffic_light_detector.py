import os
import numpy as np
import pickle
import json
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
from PIL import Image


IMG_SIZE     = (32, 32)
BATCH_SIZE   = 64
EPOCHS       = 20
NUM_CLASSES  = 43
DATA_DIR     = "archive"
MODEL_PATH   = "models/traffic_sign_model.h5"
HISTORY_PATH = "models/history.pkl"

CLASS_NAMES = [
    "Speed limit 20", "Speed limit 30", "Speed limit 50",
    "Speed limit 60", "Speed limit 70", "Speed limit 80",
    "End speed limit 80", "Speed limit 100", "Speed limit 120",
    "No passing", "No passing >3.5t", "Right-of-way intersection",
    "Priority road", "Yield", "Stop", "No vehicles",
    "Vehicles >3.5t prohibited", "No entry", "General caution",
    "Dangerous curve left", "Dangerous curve right", "Double curve",
    "Bumpy road", "Slippery road", "Road narrows right",
    "Road work", "Traffic signals", "Pedestrians",
    "Children crossing", "Bicycles crossing", "Beware ice/snow",
    "Wild animals crossing", "End restrictions", "Turn right ahead",
    "Turn left ahead", "Ahead only", "Go straight or right",
    "Go straight or left", "Keep right", "Keep left",
    "Roundabout mandatory", "End no passing", "End no passing >3.5t"
]


def _load_images_from_csv(csv_path, data_dir):
    df = pd.read_csv(csv_path)
    images, labels = [], []
    errors = 0
    for i, row in df.iterrows():
        path = os.path.join(data_dir, row["Path"])
        try:
            img = Image.open(path).convert("RGB").resize(IMG_SIZE)
            images.append(np.array(img, dtype=np.float32) / 255.0)
            labels.append(int(row["ClassId"]))
        except Exception as e:
            errors += 1
    return np.array(images), np.array(labels)


def load_data(data_dir=DATA_DIR):
    x_train, y_train = _load_images_from_csv(
        os.path.join(data_dir, "Train.csv"), data_dir
    )
    x_test, y_test = _load_images_from_csv(
        os.path.join(data_dir, "Test.csv"), data_dir
    )
    return x_train, y_train, x_test, y_test


def _make_dataset(x, y, augment=False):
    aug = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
        layers.RandomContrast(0.1),
    ])
    ds = tf.data.Dataset.from_tensor_slices((x, y))
    ds = ds.shuffle(len(x), seed=42) if augment else ds
    ds = ds.batch(BATCH_SIZE)
    if augment:
        ds = ds.map(lambda x, y: (aug(x, training=True), y),
                    num_parallel_calls=tf.data.AUTOTUNE)
    return ds.prefetch(tf.data.AUTOTUNE)


def build_model(input_shape=(32, 32, 3), num_classes=NUM_CLASSES):
    inputs = keras.Input(shape=input_shape)

    x = layers.Conv2D(32, 3, padding="same", activation="relu")(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Conv2D(32, 3, padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Dropout(0.25)(x)

    x = layers.Conv2D(64, 3, padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Conv2D(64, 3, padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Dropout(0.25)(x)

    x = layers.Conv2D(128, 3, padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Conv2D(128, 3, padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Dropout(0.3)(x)

    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    return keras.Model(inputs, outputs, name="TrafficSignCNN")


def train(data_dir=DATA_DIR):
    x_train, y_train, x_test, y_test = load_data(data_dir)

    split    = int(len(x_train) * 0.8)
    x_val    = x_train[split:]
    y_val    = y_train[split:]
    x_train  = x_train[:split]
    y_train  = y_train[:split]

    train_ds = _make_dataset(x_train, y_train, augment=True)
    val_ds   = _make_dataset(x_val,   y_val,   augment=False)
    test_ds  = _make_dataset(x_test,  y_test,  augment=False)

    model = build_model()
    model.summary()
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    os.makedirs("models", exist_ok=True)

    callbacks = [
        keras.callbacks.ModelCheckpoint(
            MODEL_PATH, save_best_only=True,
            monitor="val_accuracy", mode="max"
        ),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=3, min_lr=1e-6
        ),
        keras.callbacks.EarlyStopping(
            monitor="val_accuracy", patience=7, restore_best_weights=True
        ),
    ]

    history = model.fit(
        train_ds, validation_data=val_ds,
        epochs=EPOCHS, callbacks=callbacks
    )

    with open(HISTORY_PATH, "wb") as f:
        pickle.dump(history.history, f)

    loss, acc = model.evaluate(test_ds, verbose=0)

    y_pred = np.argmax(model.predict(x_test, verbose=0), axis=1)

    with open("models/metrics.json", "w") as f:
        json.dump({"test_accuracy": float(acc), "test_loss": float(loss)}, f, indent=2)

    _save_plots(history.history, y_test, y_pred)

    return model, acc, loss


def predict(model, image_path, top_k=5):
    img = Image.open(image_path).convert("RGB").resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    arr = np.expand_dims(arr, 0)
    preds   = model.predict(arr, verbose=0)[0]
    indices = np.argsort(preds)[::-1][:top_k]
    return [(CLASS_NAMES[i], float(preds[i])) for i in indices]


def load_model(path=MODEL_PATH):
    return keras.models.load_model(path)


def _save_plots(h, y_true, y_pred):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(h["accuracy"], label="Train")
    axes[0].plot(h["val_accuracy"], label="Val")
    axes[0].set_title("Accuracy")
    axes[0].legend()
    axes[1].plot(h["loss"], label="Train")
    axes[1].plot(h["val_loss"], label="Val")
    axes[1].set_title("Loss")
    axes[1].legend()
    plt.tight_layout()
    plt.savefig("models/training_curves.png", dpi=150)
    plt.close()

    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots(figsize=(18, 16))
    im = ax.imshow(cm, cmap="Blues")
    plt.colorbar(im, ax=ax)
    ax.set_xticks(range(NUM_CLASSES))
    ax.set_yticks(range(NUM_CLASSES))
    ax.set_xticklabels(range(NUM_CLASSES), rotation=90, fontsize=7)
    ax.set_yticklabels(range(NUM_CLASSES), fontsize=7)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    plt.tight_layout()
    plt.savefig("models/confusion_matrix.png", dpi=120)
    plt.close()