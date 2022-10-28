
from sympy import *
import sys
import time
import itertools as it


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
    return ind, graph


def list_of_states(graph):
    # to use `reduce` function with `union` 
    X = []  # set of states
    for value in graph.values():
        for i in value:
            if i not in X:
                X.append(i)

    Y = []  # set of outputs
    for key in graph.keys():
        if key not in Y and str(key).startswith('y'):
            Y.append(key)
    return X, Y


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

# sorted(a, key=str)
def sort_list(list1):
  list2 = []
  for element in list1:
    list2.append(str(element))  

  zipped_pairs = zip(list2, list1)
 
  z = [x for _, x in sorted(zipped_pairs)] 
  return z



def search_add_unions(result):
  #Extract the total number of elements in the model
  full_lenght = len({i for lst in result for i in lst})

  #Iter over the dimension of the unions
  n = len(result)
  for r in range(n):
    models_to_add = []

    #Iter over all the possible pair combinations
    for combination in list(it.combinations(result, 2)):
      union_model = {i for lst in combination for i in lst}
      len_model_1 = len(combination[0])
      len_model_2 = len(combination[1])

      #We add a new submodel just if its dimension is smaller than the one of the
      #full model and bigger than each one of the two model that compose the union
      if (len(union_model) <= full_lenght) and (len(union_model) > len_model_1) and (len(union_model) > len_model_2):
        new_model = sort_list(list(union_model))

        #We add the submodel just if it's not already found before, we want to
        #avoid repetitions of models in the output
        if new_model not in (models_to_add):
          if new_model not in (result):
            models_to_add.append(new_model)
            #print(new_model)

    #Add all the models found in this iteration
    for model in models_to_add:
      result.append(model)

  #Final sorting before returning, TO BE FIXED
  for element in result:
    element = sort_list(element)
  return result



def output(res, ind, filename):
    ln = []
    for i in res:
        il = []
        for j in i:
            il.append(ind[j])
        ln.append(il)

    # with open(...) as f:

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
    ind, graph = read_input(input)
    X, Y = list_of_states(graph)
    models = find_models(graph, Y)
    res_partial = algorithm(graph, models, Y)
    res = search_add_unions(res_partial)
    #print(res)
    output(res, ind, input[:-4])


if __name__ == '__main__':
    # measure process time
    start_time = time.process_time()
    main()
    print("Process Time: %s seconds" % (time.process_time() - start_time))
