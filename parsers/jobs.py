from time import time
import runner
from runner import Dataset


dt = '2017-06-01'


start = time()
assert runner.CBR_USD(dt).upload()
assert runner.BrentEIA(dt).upload()
assert runner.USTbonds(dt).upload()
assert runner.RosstatKEP_Monthly(dt).upload()
assert runner.RosstatKEP_Quarterly(dt).upload()    
assert runner.RosstatKEP_Annual(dt).upload() 
print("Uploaded dataset:", round(time() - start, 1), "sec")


start = time()
Dataset('2017-11-01').upload()
print("Uploaded dataset:", round(time() - start, 1), "sec")


# Suggestions (to discuss):
 
     0.     
    
    
    
#    1. can have a verbose version what prints results:
#
#      'Uploaded 350 datapoints in 0.12 seconds in 1 attempt(s)'
#      'Failed with 350 datapoints in 10.52 seconds in 3 attempt(s)'
#
#       may introduce timing as decorator

#
#    2. WONTFIX: can have a less restrictive BaseParser interface for the dates, eg accept
#       '2000-06', (2000, 6), 2000
#
#       can be done with 'arrow' 

#
#    3. NOT TODO:  generator vs list?

#
#    4. how risky and how long is this: Dataset(dt).upload() ?

#                                                                                              #
#    5. is kep being uploaded?

#                                                                                              #
#    6. webhook idea for kep

#                                                                                              #
#    7. heroku's actual cron - deploys nothing yet

#
#    8. hide token
