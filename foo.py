import time

def subsets(arr):
    res = [[]]

    for x in arr:
        for j in range(len(res)):
            res.append(res[j] + [x])

    return res

for i in range(10, 20):
    start = time.time()
    subsets(range(i))
    end = time.time()
    print(f"For {i} er get {end - start}")
