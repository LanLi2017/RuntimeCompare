import json
import time
from multiprocessing import Pool

from google.refine import refine

file_path = 'Menupart.csv'
file_name = 'MenupartSPtest'

# input raw dataset A
projectID = refine.Refine(refine.RefineServer()).new_project(file_path, file_name)[1]

with open('runtime_Model.json')as f:
    data = json.load(f)


# need further develop for the OR operation...
def or_operation(dicts):
    if dicts['op'] == 'core/column-rename':
        old_col = dicts['oldColumnName']
        new_col = dicts['newColumnName']
        refine.RefineProject(refine.RefineServer(), projectID).rename_column(old_col, new_col)
    elif dicts['op'] == 'core/text-transform':
        column_name = dicts['columnName']
        expression = dicts['expression']
        refine.RefineProject(refine.RefineServer(), projectID).text_transform(column_name, expression)
    elif dicts['op'] == 'core/column-split':
        column_name = dicts['columnName']
        separator = dicts['separator']
        refine.RefineProject(refine.RefineServer(), projectID).split_column(column_name, separator)


# pool for  parallel processes
p = Pool(5)


# loop 1000 times for two models
def time_it(func, times=1000):
    start = time.time()
    for _ in range(times):
        func()
    end = time.time()
    return end - start


# Linear task
def linear_model():
    for dicts in data:
        or_operation(dicts)


# Parallel task
def parallel_model():
    p.map(or_operation, data)


def main():
    print('Parallel time: ' + str(time_it(parallel_model)) + '\n')
    print('Linear time: ' + str(time_it(linear_model)) + '\n')


if __name__ == '__main__':
    main()
