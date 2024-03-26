import numpy as np
import csv

class Param:
    def __init__(self, filename_params:str, num_elmnts:int, filename_temp=''):
        self.num_elmnts = num_elmnts
        self.eps, self.c_coef, self.lambda_ij, self.T, self.N_t = self.read_param(filename_params)
        self.time_grid = []

        if self.T != -1:
            self.time_grid = np.linspace(0, self.T, self.N_t)
        else:
            self.time_grid = np.linspace(0, 1000000, 100000)

        self.start_temp = self.get_start_temp(filename_temp)


    #Чтение параметров задачи: eps, c[i], lambda[i][j], T; csv файл
    def read_param(self, filename:str) -> np.ndarray:
        if not(filename.endswith('.csv')):
            print('Ошибка чтения параметров. Не csv файл')
            return 
    
        lambda_ij = np.zeros((self.num_elmnts, self.num_elmnts), dtype=float)
        time_intrvl = -1 #если не будет считан промежуток, то -1 означает бесконечность
    

        with open(filename, 'r', newline='') as csvfile:
            file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            num_tmp = 0
            # Значения по умолчанию
            time_intrvl = -1       #Если -1, то бесконенчое время расчета
            N_t = 200

            for row in file_reader:
                #Считывание eps[i]
                if (not(num_tmp)):
                    eps = np.array([word for word in row], dtype=float)
                #Считывание c[i]
                if num_tmp == 1:
                    c_coef = np.array([word for word in row], dtype=float)
                #Считывание lambda[i][j]
                if num_tmp > 1 and num_tmp < 2 + self.num_elmnts:
                    lambda_ij[num_tmp - 2] = np.array([word for word in row], dtype=float)
                #Считывание временного отрезка(при наличии)    
                if num_tmp == 2 + self.num_elmnts:
                    time_intrvl_tmp = np.array([word for word in row], dtype=float)
                    time_intrvl = time_intrvl_tmp[0]
                    if time_intrvl == -1:
                        break
                #Считывание кличества шагов по времени    
                if num_tmp == 3 + self.num_elmnts:
                    N_t_tmp = np.array([word for word in row], dtype=int)
                    N_t = N_t_tmp[0]
                num_tmp += 1
        return eps, c_coef, lambda_ij, time_intrvl, N_t



    # Задание стартовых температур каждого элемента
    # Если имя файла не подается, то T0 задаются как решения системы ОДУ
    def get_start_temp(self, filename_temp=''):
        if filename_temp != '':
            with open(filename_temp, 'r', newline='') as csvfile:
                file_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in file_reader:
                    start_temp = np.array([word for word in row], dtype=float)
        else:
            start_temp = []
        return start_temp



