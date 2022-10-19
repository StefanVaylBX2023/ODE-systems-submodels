from sympy import *

# parser based on given input in txt file
f = open('input.txt', 'r')
x = []
y = []
graph = {}
ind = {}
count = 0
for line in f:
    line = line.split('=')
    line[0] = list(exp(line[0]).free_symbols)[0]
    #print(line[0])
    if str(line[0]).startswith('d'):
        line[0] = str(line[0]).split('d')[1]
        #print(line[0])
        line[0] = Symbol(line[0])
    graph[line[0]] = list(exp(line[1]).free_symbols)
    ind[line[0]] = count
    count += 1

f.close()
print(ind)

print(graph)


models = {}


X = [] # set of states
for value in graph.values():
    for i in value:
        if i not in X:
            X.append(i)

Y = [] # set of outputs
for key in graph.keys():
    if key not in Y and str(key).startswith('y'):
        Y.append(key)

print(X)
print(Y)

def dfs(graph, start, path=[]):
    path = path + [start]
    for node in graph[start]:
        if node not in path:
            path = dfs(graph, node, path)
    return path


for y in Y:
    models[y] = dfs(graph, y)

print(models)
res = []
for y in Y:
    temp = models[y]
    #print(temp[1:])  
    l = len(temp[1:])
    count = 0
    for i in Y:
        if i != y:
            if set(graph[i]).issubset(set(models[y])):
                models[y].append(i)
            
        

print(models)

res = []
for y in Y:
    res.append(models[y])

print(res)
ln = []
for i in res:
    il = []
    for j in i:
        il.append(ind[j])
    ln.append(il)

print(ln)

# take line in file based on index
f = open('input.txt', 'r')
lines = f.readlines()
f.close()

# write to file
f = open('output.txt', 'w')
for i in ln:
    f.write('Submodel ' + str(ln.index(i) + 1) + ':')
    f.write('\n')
    for j in i:
        f.write(lines[j])
    #new line in file
    f.write('\n')










