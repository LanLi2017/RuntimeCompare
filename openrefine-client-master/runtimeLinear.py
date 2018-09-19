import time

from google.refine import refine

start_time=time.time()
# input raw dataset A
projectID=refine.Refine(refine.RefineServer()).new_project('Menupart.csv','Portal_rodents Linear')[1]

# operation B: Lowercase column sponsor
refine.RefineProject(refine.RefineServer(),projectID).text_transform('sponsor','value.toLowercase()')

# operation C: Numeric column id
refine.RefineProject(refine.RefineServer(),projectID).text_transform('id','value.toNumber()')

end_time=time.time()

total_time=end_time-start_time
print('Linear time: '+ str(total_time))

# 0.0769319534302
