import numpy as np
import math

# Функция считывания геометрии .obj из файла
# Сетка предполагается полностью треугольной, либо полностью четырехугольной
# Список точек - сплошной, без привязки к частям тела
# Предполагается стандартная(без наложения ячеек) аппроксимация поверхности.
# Если ячейки пересекаются, то они совпадают.

def read_geom(filename: str) -> tuple[int, int, np.ndarray, np.ndarray, np.ndarray]:
    #Определение размеров массивов
    num_elmnt = 0
    num_frm_in_elmnt = []
    num_frm_in_elmnt_tmp = 0
    num_pnt = 0
    type = 0                                             # 3 - треугольная, 4 - четырехугольная сетка

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:

            if line.startswith('g '):
                if num_elmnt != 0:
                    num_frm_in_elmnt.append(num_frm_in_elmnt_tmp)

                num_elmnt += 1
                num_frm_in_elmnt_tmp = 0

            if line.startswith('f '):
                num_frm_in_elmnt_tmp += 1
                if type == 0:
                    indx = list(map(int, line[2:].strip().split()))
                    if len(indx) == 3:
                        type = 3
                    elif len(indx) == 4:
                        type = 4
                    else:
                        type = -1
                        return

            if line.startswith('v '):
                num_pnt += 1
    
    num_frm_in_elmnt.append(num_frm_in_elmnt_tmp)
    num_frm_in_elmnt = np.array(num_frm_in_elmnt, dtype=int)


    #Заполнение массивов
    vertex_coord = np.zeros((num_pnt, 3), dtype=float)                                  # [num_points][3]
    element_point_indx = np.zeros((num_elmnt, num_frm_in_elmnt.max(), type), dtype=int) # [num_elmnt][num_frm_in_elmnt][3 or 4]

    num_elmnt = 0
    num_pnt = 0

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
                element_point_indx[num_elmnt - 1][num_frm_in_elmnt_tmp] = np.array(indx) - np.ones(type, dtype=int)
                num_frm_in_elmnt_tmp += 1

    return type, num_elmnt, num_frm_in_elmnt, vertex_coord, element_point_indx





#Функции расчета площади поверхности одной ячейки
def s_triangle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    ab = b - a
    ac = c - a
    vec_prod = np.cross(ab, ac)
    return 0.5 * math.sqrt(np.dot(vec_prod, vec_prod))


def s_quadr(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray) -> float:
    ac = c - a
    bd = d - b
    vec_prod = np.cross(ac, bd)
    return 0.5 * math.sqrt(np.dot(vec_prod, vec_prod))






#Функция, формирующая массив площадей каждого элемента
def get_Si(num_elmnt: int, num_frm_in_elmnt: np.ndarray, vertex_coords: np.ndarray, element_point_indx: np.ndarray) -> np.ndarray:
    Si = np.zeros(num_elmnt, dtype=float)
    
    if (element_point_indx.shape[2] == 3): #type = 3
        for i in range(num_elmnt):
            sum_tmp = 0
            for j in range(num_frm_in_elmnt[i]):
                n1, n2, n3 = element_point_indx[i][j]
                sum_tmp += s_triangle(vertex_coords[n1], vertex_coords[n2], vertex_coords[n3])
            Si[i] = sum_tmp
    else:
        for i in range(num_elmnt):
            sum_tmp = 0
            for j in range(num_frm_in_elmnt[i]):
                n1, n2, n3, n4 = element_point_indx[i][j]
                sum_tmp += s_quadr(vertex_coords[n1], vertex_coords[n2], vertex_coords[n3], vertex_coords[n4])
            Si[i] = sum_tmp

    return Si










# Функция расчета площади пересечения двух треугольных ячеек
def frame_intrsct_area(v1: np.ndarray, v2: np.ndarray, vertex_coords: np.ndarray) -> float:
    intersection_area = 0.0

    # Координаты вершин первого треугольника
    vertex1 = np.array(vertex_coords[v1[0]])
    vertex2 = np.array(vertex_coords[v1[1]])
    vertex3 = np.array(vertex_coords[v1[2]])

    # Координаты вершин второго треугольника
    vertex4 = np.array(vertex_coords[v2[0]])
    vertex5 = np.array(vertex_coords[v2[1]])
    vertex6 = np.array(vertex_coords[v2[2]])

    if np.array_equal(vertex1, vertex4) and np.array_equal(vertex2, vertex5) and np.array_equal(vertex3, vertex6):
        intersection_area = s_triangle(vertex1, vertex2, vertex3)
        return intersection_area

    if (np.array_equal(vertex1, vertex4) and np.array_equal(vertex2, vertex6) and np.array_equal(vertex3, vertex5)) or \
       (np.array_equal(vertex1, vertex5) and np.array_equal(vertex2, vertex4) and np.array_equal(vertex3, vertex6)) or \
       (np.array_equal(vertex1, vertex5) and np.array_equal(vertex2, vertex6) and np.array_equal(vertex3, vertex4)) or \
       (np.array_equal(vertex1, vertex6) and np.array_equal(vertex2, vertex4) and np.array_equal(vertex3, vertex5)) or \
       (np.array_equal(vertex1, vertex6) and np.array_equal(vertex2, vertex5) and np.array_equal(vertex3, vertex4)):
        intersection_area = s_triangle(vertex1, vertex2, vertex3)
        return intersection_area
    return intersection_area





#Функция расчета площади пересечения двух элементов i и j
def get_intrsct(vertex_coords: np.ndarray, n_i: int, n_j: int, frms_i: np.ndarray, frms_j: np.ndarray) -> float:
    # n_i, n_j - число ячеек в i и j элементе
    # frms_i, frms_j - [num_frm][3/4] - номера точек для всех ячеек элемента i и j

    intersection_area = 0.0
    
    for cell1 in frms_i:
        vertices1 = np.array([cell1[k] for k in range(len(cell1))])     # номера вершин первой ячейки
        for cell2 in frms_j:
            vertices2 = np.array([cell2[k] for k in range(len(cell2))]) # номера вершин второй ячейки
            # Вычисляем площадь пересечения текущих ячеек
            intersection_area += frame_intrsct_area(vertices1, vertices2, vertex_coords)

    return intersection_area









#Функция, формирующая площади пересечений элементов
def get_Sij(num_elmnt: int, num_frm_in_elmnt: np.ndarray, vertex_coords: np.ndarray, element_point_indx: np.ndarray) -> np.ndarray:
    Sij = np.zeros((num_elmnt, num_elmnt), dtype=float)

    for i in range(num_elmnt):
        for j in range(num_elmnt):
            if (i == j - 1) or (j == i - 1):
                Sij[i][j] = get_intrsct(vertex_coords, num_frm_in_elmnt[i], num_frm_in_elmnt[j],
                                        element_point_indx[i], element_point_indx[j])

    return Sij










def main():

    #Чтение геометрии
    filename = "model3.obj"
    type, num_elmnt, num_frm_in_elmnt, vertex_coord, elmnt_point_indx = read_geom(filename) 
    num_frm = np.sum(num_frm_in_elmnt)
    if (type != 3 and type != 4):
        print("Неоднородная геометрия!")

    #Создание массивов площадей
    Si = get_Si(num_elmnt, num_frm_in_elmnt, vertex_coord, elmnt_point_indx)
    print(Si)   

    Sij = get_Sij(num_elmnt, num_frm_in_elmnt, vertex_coord, elmnt_point_indx)
    print(Sij)

    
    return




if __name__ == "__main__":
    main()

