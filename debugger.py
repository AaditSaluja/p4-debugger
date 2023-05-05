def parse_registerf(filehandler, timeperiod, registername):
    return 0

def track_pathf(filehandler, timeperiod, registername):
    return 0

while True:
    command = input('''
    [1] Parse Registers
    [2] Track Packet Path
    [3] Exit \n
    ''')
    if (command == "1"):
        retries = 0
        
        # 1 indicates that the file is open
        file_status = 0 
        while (retries < 5):
            file = str(input("Filename (you need not include the file extension)): ")).strip()
            try:
                fpath = "log/" + file + ".log"
                file = open(fpath, "r")
                file_status = 1
                break
            except:
                print("Invalid File Name")
                retries += 1

        if(file_status == 1):
            timeperiod = input("Time period for register analysis (Enter 0 for entire flow): ")
            try:
                timeperiod = int(timeperiod)
            except: 
                print("Invalid Value")
                break

            if(timeperiod < 0):
                print("Invalid Value")
                break

            if(timeperiod == 0):
                content = file.read()
            else:
                while(True):
                    try:
                        k = file.readline()
                        if(k[0] == "["):
                            print("Yayy")
                            # process time here
                            break
                    except:
                        print("Invalid File Type or Empty File")
                        break

                file.close()
        parse_registerf(0, 0, 0)
    elif(command == "2"):
        track_pathf(0, 0, 0)
    elif(command == "3"):
        break
    else:
        print("Invalid Command")
        

