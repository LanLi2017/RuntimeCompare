import json
import time

from google.refine import refine

file_path='Menupart.csv'
file_name='MenupartLineartest'


def judgeFunction(dicts,projectID):
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



start_time=time.time()
# input raw dataset A

projectID=refine.Refine(refine.RefineServer()).new_project(file_path,file_name)[1]

# operation B: Lowercase column sponsor operation C;....
# Linear operations :
with open('runtime_Model.json')as f:
    data=json.load(f)


for dicts in data:
    judgeFunction(dicts,projectID)

# refine.RefineProject(refine.RefineServer(),projectID).text_transform('sponsor','value.toLowercase()')
#
# # operation C: Numeric column id
# refine.RefineProject(refine.RefineServer(),projectID).text_transform('id','value.toNumber()')

end_time=time.time()

total_time=end_time-start_time
print('Linear time: '+ str(total_time))

# Linear time: 0.243105888367
# 0.102478027344  0.16589307785
