import bisect
import random




thetas = [random.random() for _ in range(100)]
sorted_vertices_thetas = sorted([(i, t) for i, t in enumerate(thetas)], key=lambda x: x[1])
print(sorted_vertices_thetas)
index = bisect.bisect_left(sorted_vertices_thetas, .3, key=lambda x: x[1])
print(index, sorted_vertices_thetas[index-1], sorted_vertices_thetas[index], sorted_vertices_thetas[index+1])



