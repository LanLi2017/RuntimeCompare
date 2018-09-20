import json
import time
from multiprocessing import Pool, Process

from google.refine import refine

file_path=raw_input('input the file path: ')
file_name=raw_input('input the file name: ')


start_time=time.time()
# input raw dataset A
projectID=refine.Refine(refine.RefineServer()).new_project(file_path,file_name)[1]

with open('runtime_Model.json')as f:
    data=json.load(f)

# parallel operation B and operation C
def do_work(dicts):
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



if __name__=='__main__':

    p=Pool(2)
    p.map(do_work,[dicts for dicts in data])
    end_time=time.time()
    total_time=end_time-start_time
    print('sp time: '+str(total_time))


# sp time: 0.0958931446075
