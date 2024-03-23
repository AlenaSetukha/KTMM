import numpy as np
import math
import time

# Класс треугольной сетки
# Функция считывания геометрии .obj из файла
# Список точек - сплошной, без привязки к частям тела
# Предполагается стандартная(без наложения ячеек) аппроксимация поверхности.
# Если ячейки пересекаются по вершинам, то они совпадают.


class Mesh_Triangle:
    def __init__(self, filename:str):
        self.num_elmnt, self.num_frm_in_elmnt, self.vertex_coord, self.elmnt_pnt_indx  = self.read_geom(filename)
        self.Si = self.get_Si()
        self.Sij = self.get_Sij()



    def read_geom(self, filename: str) -> tuple[int, np.ndarray, np.ndarray, np.ndarray]:
        #Определение размеров массивов
        num_frm_in_elmnt_tmp = 0
        with open(filename, 'r', encoding='utf-8') as file:
            num_elmnt, num_frm_in_elmnt, num_pnt = 0, [], 0
            for line in file:
                if line.startswith('g '):
                    if num_elmnt != 0:
                        num_frm_in_elmnt.append(num_frm_in_elmnt_tmp)
                    num_elmnt += 1
                    num_frm_in_elmnt_tmp = 0
                if line.startswith('f '):
                    num_frm_in_elmnt_tmp += 1
                if line.startswith('v '):
                    num_pnt += 1  

            num_frm_in_elmnt.append(num_frm_in_elmnt_tmp)
            num_frm_in_elmnt = np.array(num_frm_in_elmnt, dtype=int)

        #Заполнение массивов
        vertex_coord = np.zeros((num_pnt, 3), dtype=float)                               # [num_points][3]
        element_point_indx = np.zeros((num_elmnt, num_frm_in_elmnt.max(), 3), dtype=int) # [num_elmnt][num_frm_in_elmnt][3]

        num_elmnt, num_pnt = 0, 0

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('v '):   # координаты вершин
                    vertex_coord[num_pnt] = np.array(list(map(float, line[2:].strip().split())))
                    num_pnt += 1

                elif line.startswith('g '): # начало описания пов. элементов
                    num_elmnt += 1
                    num_frm_in_elmnt_tmp = 0

                elif line.startswith('f '): # поверхностные элементы - индексы угловых точек
                    indx = list(map(int, line[2:].strip().split()))
                    element_point_indx[num_elmnt - 1][num_frm_in_elmnt_tmp] = np.array(indx) - np.ones(3, dtype=int)
                    num_frm_in_elmnt_tmp += 1

        return num_elmnt, num_frm_in_elmnt, vertex_coord, element_point_indx




    #Функции расчета площади поверхности одной ячейки
    def s_triangle(self, a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
        return 0.5 * np.linalg.norm(np.cross(b - a, c - a))



    #Функция, формирующая массив площадей каждого элемента
    def get_Si(self) -> np.ndarray:
        Si = np.zeros(self.num_elmnt, dtype=float)
    
        for i in range(self.num_elmnt):
            sum_tmp = 0
            for j in range(self.num_frm_in_elmnt[i]):
                n1, n2, n3 = self.elmnt_pnt_indx[i][j]
                sum_tmp += self.s_triangle(self.vertex_coord[n1], self.vertex_coord[n2], self.vertex_coord[n3])
            Si[i] = sum_tmp

        return Si




    
    

    # Функция расчета площади пересечения двух треугольных ячеек
    def frame_intrsct_area(self, vertex1: np.ndarray, vertex2: np.ndarray, vertex3: np.ndarray,
            vertex4: np.ndarray, vertex5: np.ndarray, vertex6: np.ndarray) -> float:
        
        intersection_area = 0.0
        if (np.allclose(vertex1, vertex4, rtol=pow(10, -5)) and \
            np.allclose(vertex2, vertex5, rtol=pow(10, -5)) and \
            np.allclose(vertex3, vertex6, rtol=pow(10, -5))):
            intersection_area = self.s_triangle(vertex1, vertex2, vertex3)
            return intersection_area

        if  (np.allclose(vertex1, vertex4, rtol=pow(10, -5)) and np.allclose(vertex2, vertex6, rtol=pow(10, -5)) and np.allclose(vertex3, vertex5, rtol=pow(10, -5))) or \
            (np.allclose(vertex1, vertex5, rtol=pow(10, -5)) and np.allclose(vertex2, vertex4, rtol=pow(10, -5)) and np.allclose(vertex3, vertex6, rtol=pow(10, -5))) or \
            (np.allclose(vertex1, vertex5, rtol=pow(10, -5)) and np.allclose(vertex2, vertex6, rtol=pow(10, -5)) and np.allclose(vertex3, vertex4, rtol=pow(10, -5))) or \
            (np.allclose(vertex1, vertex6, rtol=pow(10, -5)) and np.allclose(vertex2, vertex4, rtol=pow(10, -5)) and np.allclose(vertex3, vertex5, rtol=pow(10, -5))) or \
            (np.allclose(vertex1, vertex6, rtol=pow(10, -5)) and np.allclose(vertex2, vertex5, rtol=pow(10, -5)) and np.allclose(vertex3, vertex4, rtol=pow(10, -5))):
            intersection_area = self.s_triangle(vertex1, vertex2, vertex3)
            return intersection_area
        
        return intersection_area
    


    #Функция расчета площади пересечения двух элементов i и j
    def get_intrsct(self, frms_i: np.ndarray, frms_j: np.ndarray) -> float:
        # frms_i, frms_j - [num_frm][3] - номера точек для всех ячеек элемента i и j
        intersection_area = 0.0
        for cell1 in frms_i:
            v1 = np.array([cell1[k] for k in range(len(cell1))])     # номера вершин первой ячейки
            # Координаты вершин первого треугольника
            vertex1 = np.array(self.vertex_coord[v1[0]])
            vertex2 = np.array(self.vertex_coord[v1[1]])
            vertex3 = np.array(self.vertex_coord[v1[2]])
            for cell2 in frms_j:
                v2 = np.array([cell2[k] for k in range(len(cell2))]) # номера вершин второй ячейки
                vertex4 = np.array(self.vertex_coord[v2[0]])
                # Если первая координаты не совпала, точно нет пересечения
                if not(abs(vertex4[0] - vertex1[0]) > pow(10, -5) and \
                    abs(vertex4[0] - vertex2[0]) > pow(10, -5) and \
                    abs(vertex4[0] - vertex3[0]) > pow(10, -5)):
                    # Вычисляем площадь пересечения текущих ячеек
                    vertex5 = np.array(self.vertex_coord[v2[1]])
                    vertex6 = np.array(self.vertex_coord[v2[2]])
                    intersection_area += self.frame_intrsct_area(vertex1, vertex2, vertex3, vertex4, vertex5, vertex6)
        return intersection_area





    #Функция, формирующая площади пересечений элементов
    def get_Sij(self) -> np.ndarray:
        start_time = time.time()

        Sij = np.zeros((self.num_elmnt, self.num_elmnt), dtype=float)

        for i in range(self.num_elmnt):
            for j in range(i + 1):
                if j == i - 1:
                    print(i, j)
                    Sij[i][j] = self.get_intrsct(self.elmnt_pnt_indx[i], self.elmnt_pnt_indx[j])
                    Sij[j][i] = Sij[i][j]


        # Здесь находится код, время выполнения которого вы хотите замерить
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время вычисления Sij: {execution_time} секунд")  
        return Sij

