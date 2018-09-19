import time
from multiprocessing import Pool, Process

from google.refine import refine

start_time=time.time()
# input raw dataset A
projectID=refine.Refine(refine.RefineServer()).new_project('Menupart.csv','Portal_rodentsSP4')[1]

#parallel operation B and operation C
def do_work(work_type):
    if work_type==1:
        refine.RefineProject(refine.RefineServer(),projectID).text_transform('sponsor','value.toLowercase()')
    elif work_type==2:
        refine.RefineProject(refine.RefineServer(),projectID).text_transform('id','value.toNumber()')



if __name__=='__main__':
    p=Pool(2)
    p.map(do_work,[1,2])
    end_time=time.time()
    total_time=end_time-start_time
    print('sp time: '+str(total_time))

# sp time: 0.0615239143372
