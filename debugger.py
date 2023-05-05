def parse_registerf(content, reg_handle):
    # data in the format index : [val, changecounter]
    reg_data = {}
    check_str = 'Wrote register \'' + reg_handle.strip() + '\' '
    output_file = open("out.txt", "w")
    debug= open("out2.txt", "w")
    for i in content:
        debug.write(i)
        if(check_str in i):
            
            k = i.split(check_str + 'at index ')
            key_val = k[1].split()
            try:
                counter = reg_data[key_val[0]][1]
            except:
                counter = 0
            reg_data[key_val[0]] = [key_val[3], counter + 1]
    
    for key, val in reg_data.items():
        output_file.write(key + ": " + val[0] + " - " + val[1] + "\n")

    output_file.close()
    debug.close()

def parse_register_largef(file_handler, reg_handle, final_time_lst):
    # data in the format: index : [val, changecounter]
    reg_data = {}
    check_str = 'Wrote register \'' + reg_handle.strip() + '\' '
    output_file = open("out.txt", "w")
    debug= open("out2.txt", "w")

    while(True):
        try:
            k = file_handler.readline()
            if(k[0] == "[" and (int(k[1:3]) > final_time_lst[0] or (int(k[1:3]) ==  final_time_lst[0] and int(k[4:6]) > final_time_lst[1]) or ( (int(k[1:3]) == final_time_lst[0] and int(k[4:6]) == final_time_lst[1]) and float(k[7:13]) > final_time_lst[1]))):
                print("Reached Limit")
                break
            if(check_str in k):
                debug.write(k)
                line_sp = k.split(check_str + 'at index ')
                key_val = line_sp[1].split()
                try:
                    counter = reg_data[key_val[0]][1]
                except:
                    counter = 0
                reg_data[key_val[0]] = [key_val[3], counter + 1]
        except:
            break
    
    for key, val in reg_data.items():
        output_file.write(key + ": " + val[0] + " - " + str(val[1]) + "\n")

    output_file.close()
    debug.close()





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
            call_type = 0 # 0 for small files, 1 for large files/ timeperiod specified
            final_time_lst = 0
            if(timeperiod == 0):
                content = file.read()
                call_type = 0
            else:
                call_type = 1
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
                            break
                    except:
                        print("Invalid File Type or Empty File")
                        break
                
                




            control_name = input("Name of the Control Process with Register (Typically MyIngress): ")
            reg_name = input("Name of Register to Track: ")
            reg_handle = control_name + '.' + reg_name
            if(call_type == 1):
                parse_register_largef(file, reg_handle, final_time_lst)
                file.close()
            else:
                file.close()
                parse_registerf(content, reg_handle)

    elif(command == "2"):
        track_pathf(0, 0, 0)
    elif(command == "3"):
        break
    else:
        print("Invalid Command")
        

