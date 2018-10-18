def writeFile(fileName, fileData):
    fileName+='.log'
    with open(fileName, 'a') as monthlyLog:
        monthlyLog.write(fileData)    
    
def main():
    import re
    import sys
    import time
    import operator
    import datetime
    from urllib.request import urlretrieve
    
    URL_PATH = 'https://s3.amazonaws.com/tcmg476/http_access_log'
    LOCAL_FILE = 'http.log'
    #LOCAL_FILE = 'sample.log'
    
    print('Downloading HTTP Log:')
    # Downloads remote log file into http.log
    #local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE)    # COMMENTED SO FILE DOESN'T REDOWNLOAD EVERY TIME WE TEST
    print('0% [', end='')
    local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE, lambda x,y,z: print('=', end='', flush=True) if x % 100 == 0 else False)
    print('] 100%')     
    print('Download Complete')
    file = open(LOCAL_FILE)
    
    # Variable Declaration
    totalLines = 0
    statusUnsuccessful = 0
    statusRedirect = 0
    fileRequests = {}
    monthlyRequests = {}
    dailyRequests = {}
    regex = re.compile(".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?)( HTTP.*\"|\") ([2-5]0[0-9]) .*")

    print("\n\nParsing:")
    print("0% [", end='')    
    for line in file:
        totalLines+=1
        errors = []
        data = regex.split(line)
        #print(line)
        #print(data)
        if totalLines%10000 == 0:
            print("=", end='')
        #print("\r")
        if not data or len(data) < 7:       #If regex errors, log error and skip parsing data.
            errors.append(line)
        else:                               #If no regex errors, begin parsing data.
            # data[0] = nothing?
            # data[1] = request date (dd/Mmm/yyyy)
            # data[2] = request time (hh:mm:ss)
            # data[3] = request type. GET, POST, etc.
            # data[4] = requested file
            # data[5] = http version
            # data[6] = http status code
            # data[7] = idk
            
            if data[6][:1] == '4':      #Counts Unsuccessful (4xx) Status Codes
                statusUnsuccessful+=1
                
            elif data[6][:1] == '3':    #Counts Redirected (3xx) Status Codes
                statusRedirect+=1
            
            if data[4] in fileRequests:
                fileRequests[data[4]] += 1
            else:
                fileRequests[data[4]] = 1
                
            writeFile(data[1][3:-5], line)
            if data[1][3:-5] in monthlyRequests:
                monthlyRequests[data[1][3:-5]] += 1
            else:
                monthlyRequests[data[1][3:-5]] = 1
                
            if data[1] in dailyRequests:
                dailyRequests[data[1]] += 1
            else:
                dailyRequests[data[1]] = 1
    
    #for key, value in monthlyRequests.items():
    #    print(key + " - " + str(value))
    #print("nummonths: " + str(len(monthlyRequests)))

    print('] 100%') 
    print('Parsing Complete\n\n')   
    
    fileRequestData = sorted(fileRequests.items(), key=operator.itemgetter(1))
    print("\n1.  Total requests: " + str(totalLines))
    print("\n2.  Monthly requests: " + str(monthlyRequests))
    print(  "    Average weekly requests: " + str(totalLines//7) + " requests    (weeks suck)")
    print(  "    Daily requests: " + str(dailyRequests))
    print("\n3.  Unsuccessful requests (4xx): " + str(statusUnsuccessful))
    print("\n4.  Redirected requests (3xx): " + str(statusRedirect))
    #print("File requests: " + str(fileRequests))
    #print("File request sorted: " + str(fileRequestData))
    #print("File request max: " + str(fileRequestData[len(fileRequestData)-1]))
    #print("File request min: " + str(fileRequestData[0]))
    print("\n5.  Most requested file: {'" + str(fileRequestData[len(fileRequestData)-1][0]) + "', '" + str(fileRequestData[len(fileRequestData)-1][1]) + " requests'}")
    print("\n6.  Least requested file: {'" + str(fileRequestData[0][0]) + "', '" + str(fileRequestData[0][1]) + " request(s)'}")
        
main()