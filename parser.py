def count_names(file_data, begin, end, sex):
    number_names = 5
    matching = []
    
    while begin != (end + 1):
        query = 'TX,' + sex + ',' + str(begin)
        
        #s for s in file_data if query in s
        
        matching.append([s.split(',')[2:] for s in file_data if query in s])
        begin+=1
    
    totals = {}
    
    for year in matching:
        for name in year:
            if(name[1] in totals):
                totals[name[1]] = totals[name[1]] + int(name[2].rstrip())
            else:
                totals[name[1]] = int(name[2].rstrip())
    
    
    totals = {v:k for k,v in totals.items()}
    
    i = 0
    keys = []
    values = []
    for key, value in sorted(totals.items()): # Note the () after items!
        #print(key, value)
        if(i+1 > (len(totals)-5)):
            keys.insert(0, value)
            values.insert(0, key)
        i+=1
    
    for i in range(number_names):
        print(str(i+1) + ": " + keys[i] + " (" + str("{:,}".format(values[i])) + ")")
    
    
def main():

    import re    
    from urllib.request import urlretrieve
    
    URL_PATH = 'https://s3.amazonaws.com/tcmg476/http_access_log'
    LOCAL_FILE = 'http.log'
    LOCAL_FILE = 'sample.log'
    file = open(LOCAL_FILE)
    
    print('Downloading Log')
    
    # Downloads remote log file into http.log
    #local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE)    # UNCOMMENTED SO FILE DOESN'T REDOWNLOAD EVERY TIME WE TEST
    # Download progress
    print('0% ', end='')
    #local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE, lambda x,y,z: print('=', end='', flush=True) if x % 100 == 0 else False)
    print(' 100%')     
    print('Download Complete')
    
    # Variable Declaration
    totalLines = 0
    statusUnsuccessful = 0
    statusRedirect = 0
    requestedFiles = set([])
    allFileRequests = []
    regex = re.compile(".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?)( HTTP.*\"|\") ([2-5]0[0-9]) .*")
    
    
    for line in file:
        totalLines+=1   
        line = file.readline()
        errors = []
        data = regex.split(line)
        #print(line)
        print(data)
        # Sanity check the line -- there should be 7 elements in the list (remember that index 0 has the whole string)
        if not data or len(data) < 7:
          print("Error parsing line! Log entry added to ERRORS[] list...")
          errors.append(line)
        
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
        
        requestedFiles.add(data[4])
    
    print("\nTotal requests: " + str(totalLines))
    print("Unsuccessful requests: " + str(statusUnsuccessful))
    print("Redirected requests: " + str(statusRedirect))
    
    
    #Open the data file and save the data in a list called file_data. 
    #Each element of the list is a string in the format:
    # 'TX,GENDER,YEAR_OF_BIRTH,BABY_NAME,OCCURRENCES\n'
    #file_data = open('TX19010-2016.csv').readlines()
    #print(file_data)
    #sex = 'M'
    #cmd = ''
    #while cmd != 'quit()' and cmd != 'quit':
    #    cmd = input('> ')
    #    if cmd == 'girl':
    #        sex = 'F'
    #    elif cmd == 'boy':
    #        sex ='M'
    #    elif cmd != 'quit' and cmd != 'quit()':
    #        years = cmd.split()
    #        begin = int(years[0])
    #        if len(years) > 1:
    #            end = int(years[1])
    #        else:
    #            end = begin
    #        count_names(file_data, begin, end, sex)
        
main()