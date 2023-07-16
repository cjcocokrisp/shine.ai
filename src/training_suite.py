from PySide6 import QtWidgets, QtCore, QtGui
from src.training_tips import TrainingTipsWindow
from src.training_view import TrainingView
from pathlib import Path
import tensorflow as tf
from PIL import Image
import numpy as np
from time import sleep

class ModelTrainingSuite(QtWidgets.QWidget):

    def __init__(self, parent, file, settings):
        super().__init__()

        path = file.path
        while path.find('/') != -1:
            path = path[path.find('/') + 1:]
        path = path[:path.find('.')]

        self.parent = parent

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(ToolBar(self, path, settings))
        self.layout.addWidget(ImagePreview('data/' + path))
        self.layout.addWidget(TrainingDock('data/' + path, file, settings))

    def closeEvent(self, event):
        self.parent.setDisabled(False)

class ToolBar(QtWidgets.QWidget):

    def __init__(self, parent, path, settings):
        super().__init__()

        self.parent = parent
        self.settings = settings
        
        self.icon = QtWidgets.QLabel()
        self.icon.setPixmap(QtGui.QPixmap('assets/ui/poke-ball.png'))


        self.tips_button = QtWidgets.QPushButton('Tips')
        self.tips_button.clicked.connect(self.load_tips)
        self.close_button = QtWidgets.QPushButton('Close')
        self.close_button.clicked.connect(self.parent.close)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setColumnStretch(2, 1)

        self.layout.addWidget(self.icon, 0, 0)
        self.layout.addWidget(QtWidgets.QLabel(path), 0, 1)
        self.layout.addWidget(self.tips_button, 0, 3)
        self.layout.addWidget(self.close_button, 0, 4)

    def load_tips(self):
        self.tips_menu = TrainingTipsWindow()
        self.tips_menu.setWindowTitle('Model Training Tips')
        self.tips_menu.show()

class ImagePreview(QtWidgets.QWidget):
    
    def __init__(self, dir_name):
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.addWidget(RenderImages('Training Dataset', dir_name + '/dataset'))
        self.layout.addWidget(RenderImages('Testing Data', dir_name + '/test_data'))

class RenderImages(QtWidgets.QScrollArea):

    class FileModel(QtWidgets.QWidget):

        class ImageDisplay(QtWidgets.QWidget):
            def __init__(self, path):
                super().__init__()

                self.image = QtWidgets.QLabel()
                self.image.setPixmap(QtGui.QPixmap(path))

                self.layout = QtWidgets.QHBoxLayout(self)
                self.layout.addWidget(self.image)

        def __init__(self, path):
            super().__init__()

            self.explorer = QtWidgets.QFileSystemModel()
            self.explorer.setRootPath('./' + path)
            self.explorer.setReadOnly(True)
            self.explorer.setNameFilters(['*.png'])
            self.explorer.setNameFilterDisables(False)

            self.tree_view = QtWidgets.QTreeView()
            self.tree_view.setModel(self.explorer)
            self.tree_view.setRootIndex(self.explorer.index('./' + path))
            self.tree_view.clicked.connect(self.show_img)

            self.layout = QtWidgets.QHBoxLayout(self)
            self.layout.addWidget(self.tree_view)

        def show_img(self, index):
            file = self.sender().model().filePath(index)
            self.img_display = self.ImageDisplay(file)
            self.img_display.setWindowTitle('Image Preview')
            self.img_display.show()

    def __init__(self, img_type, path):
        super().__init__()

        self.header = QtWidgets.QLabel(img_type)
        self.header.setStyleSheet('font-size: 16px')

        self.tab = QtWidgets.QTabWidget()
        self.tab.addTab(self.FileModel(path + '/not_shiny'), 'Not Shiny')
        self.tab.addTab(self.FileModel(path + '/shiny'), 'Shiny')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.header, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.tab)

class TrainingDock(QtWidgets.QWidget):

    def __init__(self, path, file, settings):
        super().__init__()

        self.path = path
        self.file = file
        self.settings = settings

        self.epoch = EpochWidget()

        self.upload_train_not = [QtWidgets.QPushButton('Upload Not Shiny Training Data'),
                                 path + '/dataset/not_shiny/']               
        self.upload_train_not[0].setFixedWidth(180)
        self.upload_train_not[0].clicked.connect(self.upload_imgs)

        self.upload_train_shiny = [QtWidgets.QPushButton('Upload Shiny Training Data'),
                                   path + '/dataset/shiny/']
        self.upload_train_shiny[0].setFixedWidth(180)
        self.upload_train_shiny[0].clicked.connect(self.upload_imgs)

        self.upload_test_not = [QtWidgets.QPushButton('Upload Not Shiny Test Data'),
                                path + '/test_data/not_shiny/']
        self.upload_test_not[0].setFixedWidth(180)
        self.upload_test_not[0].clicked.connect(self.upload_imgs)

        self.upload_test_shiny = [QtWidgets.QPushButton('Upload Shiny Test Data'),
                                  path + '/test_data/shiny/']
        self.upload_test_shiny[0].setFixedWidth(180)
        self.upload_test_shiny[0].clicked.connect(self.upload_imgs)

        self.train_button = QtWidgets.QPushButton('Train')
        self.train_button.clicked.connect(self.train_model)

        self.button_check = [self.upload_train_not, self.upload_train_shiny,
                             self.upload_test_not, self.upload_test_shiny]

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setColumnStretch(1, 1)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.epoch, 0, 0)
        self.layout.addWidget(self.train_button, 1, 0)
        self.layout.addWidget(self.upload_test_not[0], 0, 2, alignment=QtCore.Qt.AlignRight)
        self.layout.addWidget(self.upload_test_shiny[0], 1, 2, alignment=QtCore.Qt.AlignRight)
        self.layout.addWidget(self.upload_train_not[0], 0, 3, alignment=QtCore.Qt.AlignRight)
        self.layout.addWidget(self.upload_train_shiny[0], 1, 3, alignment=QtCore.Qt.AlignRight)

    def upload_imgs(self):
        for button in self.button_check:
            if self.sender() == button[0]:
                path = button[1]
        self.dialog = QtWidgets.QFileDialog(self)
        self.dialog.setNameFilters(['*.png', '*.jpg', '*.jpeg', '*.webp'])
        self.dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
        if self.dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            selected = self.dialog.selectedFiles()
            for file in selected:
                name = file
                while name.find('/') != -1:
                    name = name[name.find('/') + 1:]

                img = Image.open(file)
                img.convert('RGB')
                img.save(path + name, 'png')
                img.close()

    def train_model(self):

        self.results_screen = TrainingView()
        self.results_screen.setWindowTitle('Training Model...')
        self.results_screen.resize(int(self.settings.general['window_width']), int(self.settings.general['window_height']))
        self.results_screen.show()

        data_dir = Path(self.path + '/dataset')
        self.img_height = 200
        self.img_width = 200

        train_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="training",
            seed = 501, # oshawott's dex num because he's awesome
            image_size=(self.img_height, self.img_width),
            crop_to_aspect_ratio=True,
            shuffle=True
        )

        valid_ds = tf.keras.utils.image_dataset_from_directory(
            data_dir,
            validation_split=0.2,
            subset="validation",
            seed = 501, # ohsawott's dex num because he's awesome
            image_size=(self.img_height, self.img_width),
            crop_to_aspect_ratio=True,
            shuffle=True
        )

        self.class_names = train_ds.class_names
        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.cache().prefetch(buffer_size=AUTOTUNE)
        valid_ds = valid_ds.cache().prefetch(buffer_size=AUTOTUNE)

        number_of_classes = len(self.class_names)
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Rescaling(1/.255, input_shape=(self.img_height, self.img_width, 3)))
        model.add(tf.keras.layers.Conv2D(32, 3, padding='same', activation='relu')) # for mudkip used 32
        model.add(tf.keras.layers.MaxPooling2D())
        model.add(tf.keras.layers.Conv2D(64, 3, padding='same', activation='relu')) # for mudkip used 64
        model.add(tf.keras.layers.MaxPooling2D())
        model.add(tf.keras.layers.Conv2D(128, 3, padding='same', activation='relu')) # for mudkip used 128
        model.add(tf.keras.layers.MaxPooling2D())
        model.add(tf.keras.layers.Dropout(0.2))
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(256, activation='relu')) # for mudkip used 256
        model.add(tf.keras.layers.Dense(number_of_classes))
        model.compile(optimizer='adam',
                    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])
        model.summary()

        epochs = int(self.epoch.form.text())
        model.fit(train_ds, validation_data=valid_ds, epochs=epochs)

        results = self.test_model(model)

        self.results_screen.config_results(results[0], results[1], results[2])

        model.save(self.path + '/model')

    def test_model(self, model):
        num_normal = 0
        num_shiny = 0
        normal_score = 0
        shiny_score = 0

        overall_compiled = []
        not_compiled = []
        shiny_compiled = []

        normal_tests = Path(self.path + '/test_data/' + 'not_shiny')
        not_info = {}
        for file in normal_tests.iterdir():
            img = tf.keras.utils.load_img(file, target_size=(self.img_height, self.img_width), keep_aspect_ratio=True)
            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            if self.class_names[np.argmax(score)] == 'not_shiny':
                normal_score += 1
            num_normal += 1

            not_info[str(file)] = self.class_names[np.argmax(score)]

        shiny_tests = Path(self.path + '/test_data/' + 'shiny')
        shiny_info = {}
        for file in shiny_tests.iterdir():
            img = tf.keras.utils.load_img(file, target_size=(self.img_height, self.img_width), keep_aspect_ratio=True)
            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            if self.class_names[np.argmax(score)] == 'shiny':
                shiny_score += 1
            num_shiny += 1

            shiny_info[str(file)] = self.class_names[np.argmax(score)]

        overall_percent = ((shiny_score + normal_score) / (num_normal + num_shiny)) * 100
        normal_percent = (normal_score / num_normal) * 100
        shiny_percent = (shiny_score / num_shiny) * 100

        self.file.update_parameter("Accuracy", int(overall_percent))

        overall_compiled.append(int(overall_percent))
        overall_compiled.append(shiny_score + normal_score)
        overall_compiled.append(num_normal + num_shiny)
        not_compiled.append(int(normal_percent))
        not_compiled.append(normal_score)
        not_compiled.append(num_normal)
        not_compiled.append(not_info)
        shiny_compiled.append(int(shiny_percent))
        shiny_compiled.append(shiny_score)
        shiny_compiled.append(num_shiny)
        shiny_compiled.append(shiny_info)

        return overall_compiled, not_compiled, shiny_compiled

class EpochWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.form = QtWidgets.QLineEdit('10')
        self.form.setValidator(QtGui.QIntValidator(0, 100))
        self.form.setFixedWidth(25)

        self.layout = QtWidgets.QFormLayout(self)
        self.layout.addRow(QtWidgets.QLabel('Epoches:'), self.form)