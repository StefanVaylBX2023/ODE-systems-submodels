
from sympy import *
import sys
import time

def read_input(filename):
    f = open(f'{filename}', 'r')
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
    return ind , graph



def list_of_states(graph):
    
    X = [] # set of states
    for value in graph.values():
        for i in value:
            if i not in X:
                X.append(i)

    Y = [] # set of outputs
    for key in graph.keys():
        if key not in Y and str(key).startswith('y'):
            Y.append(key)
    return X,Y


def dfs(graph, start, path=[]):
    path = path + [start]
    for node in graph[start]:
        if node not in path:
            path = dfs(graph, node, path)
    return path

def find_models(graph, Y):
    models = {}
    for y in Y:
        models[y] = dfs(graph, y)
    return models

def algorithm(graph, models, Y):
    for y in Y:
        for i in Y:
            if i != y:
                if set(graph[i]).issubset(set(models[y])):
                    models[y].append(i)
    
    res = []
    for y in Y:
        res.append(models[y])
    return res
            
        
def output(res, ind, filename):
    ln = []
    for i in res:
        il = []
        for j in i:
            il.append(ind[j])
        ln.append(il)



    f = open(f'{filename}.txt', 'r')
    lines = f.readlines()
    f.close()

    f = open(f'{filename}' + '-res.txt', 'w')
    for i in ln:
        f.write('Submodel ' + str(ln.index(i) + 1) + ':'+'\n')
        
        for j in i:
            f.write(lines[j])
    


    f.close()


def main():
    if len(sys.argv) != 2:
        print('Usage: python3 project.py <input_file>')
        return 
    input = sys.argv[1]
    ind , graph = read_input(input)
    X,Y = list_of_states(graph)
    models = find_models(graph, Y)
    res = algorithm(graph, models, Y)
    output(res, ind, input[:-4])

if __name__ == '__main__':
# measure process time
    start_time = time.process_time()
    main()
    print("Process Time: %s seconds" % (time.process_time() - start_time))











