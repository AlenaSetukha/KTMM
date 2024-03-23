import numpy as np
import time
import csv

from Mesh_Triangle import Mesh_Triangle
from Param import Param
from Solve import Ode_Solver
from Plot import one_plot_solution, many_plot_solution


from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QMessageBox,
    QWidget,
    QFileDialog,
    QLabel,
    QMainWindow)

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Название
        self.setWindowTitle("App heat distribution")


        # Инициализация
        self.execTime = 0.
        self.mesh = None
        self.param = None

        self.geom_filename = ''
        self.param_filename = ''
        self.start_temp_filename = ''

        self.ode_sol = []



        # 1 Кнопка Начать расчет
        self.start_button_action = QAction(QIcon('data//start.png'), "Начать расчет", self)
        self.start_button_action.triggered.connect(self.start_button_was_clicked)
        self.start_button_action.setEnabled(False)


        # 1 Кнопка Сохранить как
        self.save_button_action = QAction(QIcon('data//save_as.png'), "Сохранить как ...", self)
        self.save_button_action.triggered.connect(self.save_button_was_clicked)
        self.save_button_action.setEnabled(False)


        # 2 Кнопка Задать параметры
        self.read_param_button_action = QAction(QIcon('data//param.png'), "Задать параметры", self)
        self.read_param_button_action.triggered.connect(self.read_param_button_was_clicked)

        # 2 Кнопка Задать начальную температуру 
        self.read_temp_start_button_action = QAction(QIcon('data//t0.png'), "Задать t0", self)
        self.read_temp_start_button_action.triggered.connect(self.read_temp_start_button_was_clicked)

        # 2 Кнопка Задать геометрию
        self.read_geom_button_action = QAction(QIcon('data//geom.png'), "Задать геометрию", self)
        self.read_geom_button_action.triggered.connect(self.read_geom_button_was_clicked)


        # 2 Кнопка Анимация1
        self.anim1_button_action = QAction(QIcon("data//anim.png"), "Анимация: все на одном", self)
        self.anim1_button_action.triggered.connect(self.anim1_button_was_clicked)
        self.anim1_button_action.setEnabled(False)

        # 2 Кнопка Анимация2
        self.anim2_button_action = QAction(QIcon("data//anim.png"), "Анимация: отдельно", self)
        self.anim2_button_action.triggered.connect(self.anim2_button_was_clicked)
        self.anim2_button_action.setEnabled(False)




        # Создани меню
        menu = self.menuBar()
        file_menu = menu.addMenu("Меню")

        file_submenu = file_menu.addMenu("Параметры")

        file_submenu.addAction(self.read_param_button_action)
        file_submenu.addSeparator()
        file_submenu.addAction(self.read_temp_start_button_action)
        file_submenu.addSeparator()
        file_submenu.addAction(self.read_geom_button_action)


        file_menu.addAction(self.start_button_action)
        file_menu.addSeparator()

        file_submenu1 = file_menu.addMenu("Анимация")
        file_submenu1.addAction(self.anim1_button_action)
        file_submenu1.addSeparator()
        file_submenu1.addAction(self.anim2_button_action)

        file_menu.addSeparator()
        file_menu.addAction(self.save_button_action)




        # Виджет с порядком выполнения прораммы
        rules_str = "Порядок выполнения программы:\n"
        rules_str += "    1. Задайте геометрию, параметры и стартовую температуру\n    2. Выполните расчет\n"
        rules_str += "    3. Выведите анимацию решения на экран, сохраните результаты расчета\n"
        rules_widget = QLabel("Rules")
        rules_widget.setText(rules_str)


        # Виджеты с текущими названиями файлов
        self.geom_filename_widget = QLabel()
        self.geom_filename_str = "Геометрия: " + self.geom_filename
        self.geom_filename_widget.setText(self.geom_filename_str)

        self.param_filename_widget = QLabel()
        self.param_filename_str = "Параметры: " + self.param_filename
        self.param_filename_widget.setText(self.param_filename_str)

        self.start_temp_filename_widget = QLabel()
        self.start_temp_filename_str = "Нач. температура: " + self.start_temp_filename
        self.start_temp_filename_widget.setText(self.start_temp_filename_str)
        



        # Устанавливаем центральный виджет Window
        container_of_widgets = QVBoxLayout()
        container_of_widgets.addWidget(rules_widget)
        container_of_widgets.addWidget(self.geom_filename_widget)
        container_of_widgets.addWidget(self.param_filename_widget)
        container_of_widgets.addWidget(self.start_temp_filename_widget)


        main_widget = QWidget()
        main_widget.setLayout(container_of_widgets)
        self.setCentralWidget(main_widget)





#=======================Обработчики кнопок======================================
    def read_geom_button_was_clicked(self, checked) -> None:
        print('Нажали кнопку Задать геометрию!')
        # Выбор файла с геометрией
        filename = self.get_choosen_filename(message="Файл с геометрией", name_filter="*.obj")
        
        if filename != None:
            self.geom_filename = filename
            self.geom_filename_widget.setText("Геометрия: " + self.geom_filename)
            if self.param_filename != '':
                self.start_button_action.setEnabled(True)
            
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Error in filename")
            dlg.exec()
        return


        


    def read_param_button_was_clicked(self, checked) -> None:
        print('Нажали кнопку Задать параметры!')
        # Выбор файла с параметрами
        filename = self.get_choosen_filename(message="Файл с параметрами", name_filter="*.csv")
        
        if filename != None:
            self.param_filename = filename
            if self.geom_filename != '':
                self.start_button_action.setEnabled(True)
            self.param_filename_widget.setText("Параметры: " + self.param_filename)
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Error in filename")
            dlg.exec()
        return
        




    def read_temp_start_button_was_clicked(self, checked) -> None:
        print('Нажали кнопку Задать начальную температуру!')
        # Выбор файла с нач. температурой
        filename = self.get_choosen_filename(message="начальная температура", name_filter="*.csv")
        
        if filename != None:
            self.start_temp_filename = filename
            if (self.param_filename != '' and self.geom_filename != ''):
                self.start_button_action.setEnabled(True)
            self.start_temp_filename_widget.setText("Нач. температура: " + self.start_temp_filename)
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Error in filename")
            dlg.exec()
        return




    def start_button_was_clicked(self, checked) -> None:
        print('Нажали кнопку старт!')
        if self.geom_filename != '' and self.param_filename != '':
            start_time = time.time()
            #Заполнение данных
            self.mesh = None
            self.mesh = Mesh_Triangle(self.geom_filename)
            self.param = None
            self.param = Param(self.param_filename, self.mesh.num_elmnt, self.start_temp_filename)

            if (self.param.T != -1): #отрезок времени

                solver = Ode_Solver(mesh=self.mesh, param=self.param)
                if (self.start_temp_filename == ''):
                    self.param.start_temp = solver.ode_calculate_temp_stationar(self.param)

                self.ode_sol = solver.ode_calculate_temp(self.param)
            else: #время не ограничено
                pass
 
            self.anim1_button_action.setEnabled(True)
            self.anim2_button_action.setEnabled(True)
            self.save_button_action.setEnabled(True)
            end_time = time.time()
            self.execTime = end_time - start_time
        else:
            QMessageBox.warning(self, 'Warning', 'Не все необходимые файлы заданы')
        return
        


    def anim1_button_was_clicked(self, checked) -> None:
        print('Нажали кнопку Анимация1!')
        one_plot_solution(self.ode_sol, self.param.time_grid)
        return
    
    def anim2_button_was_clicked(self, checked) -> None:
        print('Нажали кнопку Анимация2!')
        many_plot_solution(self.ode_sol, self.param.time_grid)
        return



    def save_button_was_clicked(self, checked) -> None:
        print('Нажали кнопку Сохранить!')
        filename_out = self.get_choosen_filename(message="Сохранить как", name_filter="*.csv")
        if filename_out != None:
            self.save_as(filename_out)
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Warning")
            dlg.setText("Error in filename")
            dlg.exec()
        return



#========================Дополнительные функции====================================
    def get_choosen_filename(self, message: str, name_filter:str) -> str:
        fileName, _ = QFileDialog.getOpenFileName(self, caption=message, filter=name_filter)

        if fileName:
            return fileName
        else:
            None



    def save_as(self, filename:str) -> None:
        #Запись решения задачи:csv
        if not(filename.endswith('.csv')):
            print('Ошибка записи результатов. Не csv файл')
            return 
    
        with open(filename, mode="w", encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter = " ", lineterminator="\r\n")
            file_writer.writerow(['Время выполнения программы: ' + str(self.execTime)])
            file_writer.writerow(['Число элементов: ' + str(self.param.num_elmnts)])
            file_writer.writerow(['Временной промежуток: ' + str(self.param.T)])
            if (self.param.T != -1):
                file_writer.writerow(['Число узлов по времени: ' + str(self.param.N_t)])
            
            for i in range(self.ode_sol.shape[0]):
                file_writer.writerow(self.ode_sol[i])
        return
    
