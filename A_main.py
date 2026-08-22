# ==================================================
# MAIN MODULE
# ==================================================
# File name   : A_main.py
# Description : Module điều khiển chính
#               của phần mềm.
# 
# --------------------------------------------------
# CẤU TRÚC DỰ ÁN
# --------------------------------------------------
# Project/
# │
# ├── data/
# │   │
# │   ├── processed/        <- dữ liệu để huấn luyện
# │   │   ├── Xin chào/     <- tên nhãn
# │   │   │   ├── 0.npy     <- video mẫu
# │   │   │   ├── 1.npy
# │   │   │   └── ...
# │   │   └── ...
# │   │
# │   └── training_plot/    <- biểu đồ
# │       ├── training_plot.png     <- accuracy, loss
# │       └── confusion_matrix.png  <- ma trận nhầm lẫn
# │
# ├── labels/
# │   │
# │   ├── asl_labels.json
# │   └── ...
# │
# ├── models/
# │   │
# │   ├── asl_model.keras
# │   └── ...
# │
# ├── voices/
# │   │
# │   ├── en_US-lessac-medium.onnx
# │   └── en_US-lessac-medium.onnx.json
# │
# ├── _configurations.py
# ├── _detector.py
# ├── _landmarks_module.py
# ├── _tts_module.py
# │
# ├── A_main.py
# │
# ├── a1_data_collect_module.py
# ├── a2_model_training_module.py
# ├── b1_module1_single_sign.py
# └── b2_module2_multi_signs.py
# --------------------------------------------------


from a1_data_collect_module   import CollectModule
from a2_model_training_module import TrainingModule
from b1_module1_single_sign   import Module1
from b2_module2_multi_signs   import Module2

import resources_rc
import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QStackedWidget
from PySide6.QtWidgets import QLabel

from PySide6.QtGui  import QIcon
from PySide6.QtGui  import QPixmap


# -------------------------------------------------------------
# HOME PAGE
# -------------------------------------------------------------
# 
# Giao diện trang giới thiệu, hướng dẫn người dùng sử dụng
# các tính năng của phần mềm.
# -------------------------------------------------------------
class HomaPage(QWidget):
    def __init__(self):
        super().__init__()
        home_page_layout = QVBoxLayout(self)

        # WIDGET STACK
        stack = QStackedWidget()

        # CREATE PAGES
        num_page = 13
        pages = {}
        for i in range(num_page):
            label = QLabel()
            label.setPixmap(
                QPixmap(f":/resources/Slide{i+1}.PNG")
            )
            label.setScaledContents(True)
            pages[i] = QWidget()
            layout = QVBoxLayout(pages[i])
            layout.addWidget(label)

            stack.addWidget(pages[i])

        # NEXT PAGE BUTTON
        next_btn = QPushButton("Next page")
        next_btn.setFixedWidth(150)
        next_btn.clicked.connect(
            lambda: (
                stack.setCurrentIndex(
                    stack.currentIndex() + 1
                    if stack.currentIndex() < num_page - 1
                    else 0
                )
            )
        )

        # PREVIOUS PAGE BUTTON
        prev_btn = QPushButton("Previous page")
        prev_btn.setFixedWidth(150)
        prev_btn.clicked.connect(
            lambda: (
                stack.setCurrentIndex(
                    stack.currentIndex() - 1
                    if stack.currentIndex() > 0
                    else num_page - 1
                )
            )
        )
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(prev_btn)
        button_layout.addWidget(next_btn)
        button_layout.addStretch()

        home_page_layout.addWidget(stack)
        home_page_layout.addLayout(button_layout)


# -------------------------------------------------------------
# MAIN WINDOW
# -------------------------------------------------------------
# 
# Giao diện chính điều khiển phần mềm, bao gồm tất cả các trang
# -------------------------------------------------------------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hand Gesture Detector")

        mainLayout   = QVBoxLayout(self)
        bottomLayout = QHBoxLayout()

        # Buttons
        home_btn               = QPushButton("Home")
        module1_btn            = QPushButton("Single Sign")
        module2_btn            = QPushButton("Multi Signs")
        collect_module_btn     = QPushButton("Collect Data")
        train_model_module_btn = QPushButton("Train model")

        home_btn.clicked.connect(
            lambda: (
                mainWidget.setCurrentWidget(home_page)
            )
        )
        module1_btn.clicked.connect(
            lambda: (
                mainWidget.setCurrentWidget(module1_window)
            )
        )
        module2_btn.clicked.connect(
            lambda: (
                mainWidget.setCurrentWidget(module2_window)
            )
        )
        collect_module_btn.clicked.connect(
            lambda: (
                mainWidget.setCurrentWidget(collect_window)
            )
        )
        train_model_module_btn.clicked.connect(
            lambda: (
                mainWidget.setCurrentWidget(training_window)
            )
        )

        # Align buttons
        bottomLayout.addWidget(collect_module_btn)
        bottomLayout.addWidget(train_model_module_btn)
        bottomLayout.addWidget(home_btn)
        bottomLayout.addWidget(module1_btn)
        bottomLayout.addWidget(module2_btn)

        # Main window
        mainWidget = QStackedWidget()

        mainLayout.addWidget(mainWidget)
        mainLayout.addLayout(bottomLayout)

        home_page       = HomaPage()
        module1_window  = Module1()
        module2_window  = Module2()
        collect_window  = CollectModule()
        training_window = TrainingModule()

        mainWidget.addWidget(home_page)
        mainWidget.addWidget(module1_window)
        mainWidget.addWidget(module2_window)
        mainWidget.addWidget(collect_window)
        mainWidget.addWidget(training_window)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setWindowIcon(QIcon(":/resources/icon.ico"))
    window.resize(1200, 700)
    window.show()

    app.exec()

if __name__=="__main__":
    main()