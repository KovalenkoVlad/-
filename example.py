from mpi4py import MPI
import numpy as np


def find_min_max_parallel(matrix):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Кількість рядків, що обробляються кожним процесом
    rows_per_proc = matrix.shape[0] // size

    # Поділ масиву між процесами
    if rank == 0:
        start_time = MPI.Wtime()  # Точний замір часу
        # Розподіляємо масиви по процесах
        rows_to_send = [matrix[i * rows_per_proc:(i + 1) * rows_per_proc] for i in range(size)]
    else:
        rows_to_send = None

    # Кожен процес отримує свою частину масиву
    local_rows = comm.scatter(rows_to_send, root=0)

    # Пошук мінімуму та максимуму в частині масиву
    local_min = np.min(local_rows)
    local_max = np.max(local_rows)

    # Збір мінімальних і максимальних значень з кожного процесора
    global_min = comm.reduce(local_min, op=MPI.MIN, root=0)
    global_max = comm.reduce(local_max, op=MPI.MAX, root=0)

    if rank == 0:
        end_time = MPI.Wtime()
        execution_time = end_time - start_time
        return global_min, global_max, execution_time
    else:
        return None


# Ініціалізація MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Параметри матриці
n, m = 1000, 1000

if rank == 0:
    # Створення матриці на процесі 0
    matrix = np.random.randint(1, 10000, size=(n, m))
else:
    matrix = None

# Пошук мінімуму і максимуму паралельно
result = find_min_max_parallel(matrix)

if rank == 0:
    min_value, max_value, par_time = result
    print(f"Паралельне рішення: Min = {min_value}, Max = {max_value}, Час: {par_time:.6f} сек.")
