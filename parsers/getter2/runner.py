from getter import PARSERS
        
dt = '2017-06-01'
total_time = 0
for parser in PARSERS:
    p = parser(dt).extract()
    assert p.parsing_result
    total_time += p.elapsed
    assert p.upload()
print("Total time:", round(total_time, 2))    


# Suggestions (to discuss):
 
#    0.  splitting larger fucntions to smaller ones - need to check 
    
#    1. can have a verbose version what prints results:
#
#      'Uploaded 350 datapoints in 0.12 seconds in 1 attempt(s)'
#      'Failed with 350 datapoints in 10.52 seconds in 3 attempt(s)'
#
#       may introduce timing as decorator

#    2. WONTFIX: can have a less restrictive BaseParser interface for the dates, eg accept
#       '2000-06', (2000, 6), 2000
#
#       can be done with 'arrow' 

#    3. NOT TODO:  generator vs list?

#    4. how risky and how long is this: Dataset(dt).upload() ?

#    5. is kep being uploaded?

#    6. webhook idea for kep

#    7. heroku's actual cron - deploys nothing yet

#    8. hide token
