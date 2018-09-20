import json
import time
from multiprocessing import Pool, Process

from google.refine import refine

file_path='Menupart.csv'
file_name='MenupartSPtest'


start_time=time.time()
# input raw dataset A
projectID=refine.Refine(refine.RefineServer()).new_project(file_path,file_name)[1]

with open('runtime_Model.json')as f:
    data=json.load(f)

# parallel operation B and operation C
def OR_operation(dicts):
    if dicts['op']=='core/column-rename':
            oldcol=dicts['oldColumnName']
            newcol=dicts['newColumnName']
            refine.RefineProject(refine.RefineServer(),projectID).rename_column(oldcol,newcol)
    elif dicts['op']=='core/text-transform':
        columnName=dicts['columnName']
        expression=dicts['expression']
        refine.RefineProject(refine.RefineServer(),projectID).text_transform(columnName,expression)
    elif dicts['op']=='core/column-split':
        columnName=dicts['columnName']
        separator=dicts['separator']
        refine.RefineProject(refine.RefineServer(),projectID).split_column(columnName,separator)


def Linear_time_it(func, times=1000):
    start = time.time()
    for _ in range(times):
        func()
    end = time.time()
    print('linear time: '+str(end-start))


# Linear task
def Linear_data():
    for dicts in data:
        OR_operation(dicts)


def parallel_time_it():
    p=Pool(5)
    start = time.time()
    for _ in range(1000):
        p.map(OR_operation,data)
    end = time.time()
    print('Parallel time: '+str(end - start))


def main():
    parallel_time_it()
    Linear_time_it(Linear_data)


if __name__=='__main__':
    main()


