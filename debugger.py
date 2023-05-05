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
            timeperiod = input("Time period for register analysis in seconds (Enter 0 for entire flow): ")
            try:
                timeperiod = int(timeperiod)
            except: 
                print("Invalid Value")
                break

            if(timeperiod < 0):
                print("Invalid Value")
                break
            elif(timeperiod > 3599):
                print("Value out of bounds. Must be less than 3600 seconds")
                break
            
            content = []
            if(timeperiod == 0):
                content = file.read()
            else:
                while(True):
                    try:
                        k = file.readline()
                        if(k[0] == "["):
                            ini_time = k[1:13].split(":")
                            added_time = {"mins": timeperiod // 60, "secs": timeperiod % 60}
                            if(float(ini_time[2]) + added_time["secs"] > 60):
                                ini_time[2] = (float(ini_time[2]) + added_time["secs"]) % 60
                                added_time["mins"] += 1
                            else:
                                ini_time[2] = float(ini_time[2]) + added_time["secs"]
                            # process time here

                            if(int(ini_time[1]) + added_time["mins"] > 60):
                                ini_time[1] = (int(ini_time[2]) + added_time["mins"]) % 60
                                ini_time[0] = int(ini_time[0]) + 1
                            else:
                                ini_time[1] = float(ini_time[1]) + added_time["mins"]
                            
                            # time at which we need to stop
                            final_time_lst = [int(ini_time[0]), int(ini_time[1]), float(round(ini_time[2],3))]
                            
                            print(final_time_lst)

                            break
                    except:
                        print("Invalid File Type or Empty File")
                        break
                

                while(True):
                    print("hello")
                    try:
                        k = file.readline()
                        print(k)
                        if(k[0] == "[" and (int(k[1:3]) > final_time_lst[0] or int(k[4:6]) > final_time_lst[1] or (int(k[4:6]) == final_time_lst[1] and float(k[7:13]) > final_time_lst[1]))):
                            print("Reached Limit")
                            break
                        content.append(k)
                    except:
                        print("hello2")
                        # print(content)
                        break
                    

                file.close()
        parse_registerf(0, 0, 0)
    elif(command == "2"):
        track_pathf(0, 0, 0)
    elif(command == "3"):
        break
    else:
        print("Invalid Command")
        

