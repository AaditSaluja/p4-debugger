import pandas as pd
import matplotlib.pyplot as plt

def parse_registerf(content, reg_handle):
    # data in the format index : [val, changecounter]
    reg_data = {}
    check_str = 'Wrote register \'' + reg_handle.strip() + '\' '
    
    track_index = input("Would you like to track change for an index (Enter 1 for yes): ")
    output_file = open("out.txt", "w")
    
    if(track_index == '1'):
        # data in the format index : {counter : val}
        change_dic = {}

    for line in content:
        if(check_str in line):
            k = line.split(check_str + 'at index ')
            key_val = k[1].split()
            try:
                counter = reg_data[key_val[0]][1]
            except:
                counter = 0
            reg_data[key_val[0]] = [key_val[3], counter + 1]
            
            if(track_index == '1'):
                try:
                    change_dic[key_val[0]].update({counter + 1: key_val[3]})
                except:
                    change_dic[key_val[0]] = {counter + 1: key_val[3]}
    
    status = viz_data(reg_data, output_file)
    if(track_index == '1' and status == 1):
        viz_index(change_dic)

    output_file.close()

def parse_register_largef(file_handler, reg_handle, final_time_lst):
    # data in the format: index : [val, changecounter]
    reg_data = {}
    check_str = 'Wrote register \'' + reg_handle.strip() + '\' '

    track_index = input("Would you like to track change for an index (Enter 1 for yes): ")
    if(track_index == '1'):
        # data in the format index : {counter : val}
        change_dic = {}

    output_file = open("out.txt", "w")

    while(True):
        try:
            k = file_handler.readline()
            if(k[0] == "[" and (int(k[1:3]) > final_time_lst[0] or (int(k[1:3]) ==  final_time_lst[0] and int(k[4:6]) > final_time_lst[1]) or ( (int(k[1:3]) == final_time_lst[0] and int(k[4:6]) == final_time_lst[1]) and float(k[7:13]) > final_time_lst[1]))):
                print("Reached Limit")
                break
            if(check_str in k):
                line_sp = k.split(check_str + 'at index ')
                key_val = line_sp[1].split()
                try:
                    counter = reg_data[key_val[0]][1]
                except:
                    counter = 0
                reg_data[key_val[0]] = [key_val[3], counter + 1]

                if(track_index == '1'):
                    try:
                        change_dic[key_val[0]].update({counter + 1: key_val[3]})
                    except:
                        change_dic[key_val[0]] = {counter + 1: key_val[3]}
        except:
            break
    
    # for key, val in reg_data.items():
    #     output_file.write(key + ": " + val[0] + " - " + str(val[1]) + "\n")

    status = viz_data(reg_data, output_file)

    if(track_index == '1' and status == 1):
        viz_index(change_dic)

    output_file.close()
    
    return


def viz_data(reg_data, filehandler):

    if(len(reg_data) == 0):
        print("No Register Updates In Region")
        return 0
    
    data_pd = {"Index": [],
               "Final Value": [],
               "Changes in Timeperiod": []}
    for key, val in reg_data.items():
        filehandler.write(key + ": " + val[0] + " - " + str(val[1]) + "\n")
        data_pd["Index"].append(key)
        data_pd["Final Value"].append(val[0])
        data_pd["Changes in Timeperiod"].append(val[1])

    df = pd.DataFrame(data_pd)
    print(df)
    
    
    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    fig.tight_layout()
    
    plt.savefig('registers.png', bbox_inches='tight')
    
    return 1

def viz_index(change_data):
    index = input("Index to track: ")
    try:
        index_change = change_data[index]
    except:
        print("Index Does Not Exist")
        return
    
    data_pd = {"Change Number": [],
               "Value": [],
               }
    for key, val in index_change.items():
        data_pd["Change Number"].append(key)
        data_pd["Value"].append(val)

    df = pd.DataFrame(data_pd)
    
    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')

    ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    fig.tight_layout()
    
    plt.savefig('index_track.png', bbox_inches='tight')
    
    return

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
            final_time_lst = 0
            if(timeperiod == 0):
                content = file.readlines()
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
                            break
                    except:
                        print("Invalid File Type or Empty File")
                        break
                
                




            control_name = input("Name of the Control Process with Register (Typically MyIngress): ")
            reg_name = input("Name of Register to Track: ")
            reg_handle = control_name + '.' + reg_name
            if(timeperiod != 0):
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
        

