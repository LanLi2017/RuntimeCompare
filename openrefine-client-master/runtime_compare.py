import json
import time
from multiprocessing import Pool, Process

from google.refine import refine

file_path='Menupart.csv'
file_name='MenupartSPtest'


# input raw dataset A
projectID=refine.Refine(refine.RefineServer()).new_project(file_path,file_name)[1]

with open('runtime_Model.json')as f:
    data=json.load(f)


# need further develop for the ...
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


# pool for  parallel processes
p=Pool(5)


# loop 1000 times for two models
def time_it(func, times=1000):
    start = time.time()
    for _ in range(times):
        func()
    end = time.time()
    return end-start


# Linear task
def Linear_model():
    for dicts in data:
        OR_operation(dicts)


# Parallel task
def Parallel_model():
    p.map(OR_operation,data)


def main():
    print('Parallel time: '+str(time_it(Parallel_model))+'\n')
    print('Linear time: '+str(time_it(Linear_model))+'\n')



if __name__=='__main__':
    main()


