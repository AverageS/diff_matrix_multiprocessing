import multiprocessing as mp
import numpy as np
import itertools as its
import copy

BLOCK_SIZE = 8
WORKERS_COUNT = 4


S = [
    220, 236, 223, 65, 38, 225, 196, 58, 102, 173, 76, 226, 232, 107, 212, 48, 248, 39, 80, 213, 175, 32, 217, 241, 82,
    195, 160, 222, 221, 202, 192, 201, 14, 182, 96, 83, 13, 61, 174, 171, 219, 228, 98, 79, 42, 218, 1, 123, 133, 110,
    109, 128, 54, 72, 101, 142, 30, 157, 193, 74, 46, 104, 115, 10, 231, 90, 186, 106, 144, 161, 136, 67, 84, 117, 227,
    245, 235, 179, 154, 118, 216, 141, 86, 147, 71, 36, 176, 125, 91, 255, 159, 124, 85, 70, 56, 52, 149, 209, 250, 28,
    57, 140, 145, 229, 0, 44, 237, 11, 112, 210, 233, 180, 3, 130, 191, 68, 103, 132, 183, 33, 239, 151, 100, 207, 27,
    172, 155, 135, 50, 49, 197, 63, 77, 137, 22, 113, 200, 69, 251, 53, 189, 242, 152, 166, 188, 167, 129, 7, 240, 40,
    75, 35, 211, 198, 214, 21, 122, 47, 121, 158, 64, 181, 234, 170, 249, 150, 94, 163, 66, 253, 126, 26, 162, 95, 12,
    243, 215, 19, 59, 9, 168, 238, 108, 165, 178, 8, 203, 208, 230, 15, 204, 164, 97, 169, 138, 17, 134, 153, 105, 41,
    131, 43, 246, 23, 92, 4, 156, 206, 81, 114, 99, 244, 120, 224, 143, 139, 177, 187, 87, 20, 127, 73, 18, 51, 190,
    111, 93, 89, 45, 6, 34, 55, 199, 88, 31, 25, 24, 247, 146, 254, 62, 5, 184, 16, 78, 37, 205, 119, 2, 60, 116, 185,
    252, 194, 29, 148
]
# S = [3, 0, 6, 2, 7, 4, 5, 1]


def chunked(iterable, block_size):
    it = iter(iterable)
    return iter(lambda: tuple(its.islice(it, block_size)), ())


def one_proc():
    res = np.empty(shape=(0, len(S)), dtype=np.int64)

    for value in range(len(S)):
        row = np.zeros(shape=len(S), dtype=np.int64)
        for i in range(len(S)):
            j = value ^ i
            image = S[i] ^ S[j]
            row[image] += 1
        res = np.vstack([res, row])

    return res


def worker(outq: mp.Queue, s: list, worker_index: int, workers_count: int, block_size: int):
    s_len = len(s)

    for task in chunked(range(worker_index, s_len, workers_count), block_size):
        output_rows = np.empty(shape=(0, s_len), dtype=np.int64)

        for row_num in task:
            row = np.zeros(shape=s_len, dtype=np.int64)
            for i in range(0, s_len):
                j = row_num ^ i
                image = s[i] ^ s[j]
                row[image] += 1
            output_rows = np.vstack([output_rows, row])

        outq.put(zip(task, output_rows))

    return True


if __name__ == '__main__':
    ready_for_reduce = mp.Queue()
    s_len = len(S)
    P_multi = np.empty(shape=(s_len, s_len), dtype=np.int64)

    pool = [mp.Process(target=worker, args=(ready_for_reduce, copy.deepcopy(S), i, WORKERS_COUNT, BLOCK_SIZE)) for i in range(WORKERS_COUNT)]
    for process in pool:
        process.start()

    reduced_counter = 0
    while reduced_counter != s_len:
        ready_task = ready_for_reduce.get()
        for row in ready_task:
            reduced_counter += 1
            P_multi[row[0]] = row[1]

    for process in pool:
        process.join()

    P_one = one_proc()

    print(np.array_equal(P_multi, P_one))
