import subprocess

# Display List Section
def Display_List():
    # Initialize an empty list to store display information
    display_list = []
    
    # Get information about connected displays
    DisCon_Display = subprocess.check_output('xrandr').decode()
    lines = DisCon_Display.split('\n')

    # Filter connected and disconnected displays
    for line in lines:
        if 'connected p' in line:
            index = line.find(' (')
            before = line[:index]
            resolution = line.split()[3]
            status = line.split()[1]
            name = line.split()[0]
            display_list.append([name, status, resolution])
        elif 'disconnected' in line:
            index = line.find(' (')
            before = line[:index]
            name2 = line.split()[0]
            status2 = line.split()[1]
            display_list.append([name2, status2])      
    return '\n'.join(map(str, display_list))

# Set Resolution
def Set_Resolution():
    # Get user input for display name and resolution
    Display_name = input('Display Name: ')
    X = input('X-axis(Horizontal): ')   
    Y = input('Y-axis(Vertical): ')        
    
    # Generate commands to set resolution
    command = f"cvt {X} {Y} | grep Modeline | cut -d' ' -f2-"
    output = subprocess.check_output(command, shell=True)
    cvt_out = output.decode()
    command2 = f"cvt {X} {Y} | grep Modeline | cut -d' ' -f2"
    output2 = subprocess.check_output(command2, shell=True)
    cvt_out2 = output2.decode()
    
    # Set new mode, add mode, and output mode
    command4 = f'xrandr --newmode {cvt_out}'
    try:
        subprocess.run(command4, shell=True)
    except Exception as e:
       return print('(newmode) Error is :',e)  
    
    command5 = f'xrandr --addmode {Display_name} {cvt_out2}'
    try:
        subprocess.run(command5, shell=True)
    except Exception as e:
        return print('(addmode) Error :',e)   
    
    command6 = f'xrandr --output {Display_name} --mode {cvt_out2}'
    try:
        subprocess.run(command6, shell=True)
    except Exception as e:
        return print('(output) Error :',e)  
    
    # File Locations
    file = '/etc/lightdm/lightdm.conf'
    config = 'display-setup-script=/etc/lightdm/my_conf.sh'
    
    # Edit File Config
    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            if line.startswith('#display-setup-script='):
                f.write(config+'\n')
            else:    
                f.write(line)
    
    # Make File And Give Access
    subprocess.run(['touch', '/etc/lightdm/my_conf.sh'])
    subprocess.run(['chmod', '+x', '/etc/lightdm/my_conf.sh'])
    
    # Write xrandr commands to configuration file
    my_conf = '/etc/lightdm/my_conf.sh'
    Xconf = f'''xrandr --newmode {cvt_out}
    xrandr --addmode {Display_name} {cvt_out2}
    xrandr --output {Display_name} --mode {cvt_out2}'''
    with open(my_conf,'w') as m:
        m.write(Xconf)
    
    # Update autostart configuration file
    file2 = '/root/.config/autostart/lxrandr-autostart.desktop'
    config2 = 'Exec=/etc/lightdm/my_conf.sh'
    if not subprocess.run(['test', '-f', file2]).returncode:
        with open(file2,'r') as f2:
            lines2 = f2.readlines()
        with open(file2,'w') as f2:
            for line in lines2:
                if line.startswith('Exec='):
                    f2.write(config2+'\n')         
                else:    
                    f2.write(line)        
    else:
        pass
# Automatically set resolution
def auto():
    Active_List = []
    command = 'xrandr --listactivemonitors'
    A = subprocess.check_output(command,shell=True).decode()
    A = A.split()
    Active_List.append(A[-1])
    for i in Active_List:
        command = f'xrandr --output {i} --auto'
        try:
            subprocess.run(command, shell=True)
        except Exception as e:
            return print('auto Error :',e)
    
    # Write commands to configuration file
    my_conf = '/etc/lightdm/my_conf.sh'
    with open(my_conf,'w') as m:    
        for i in Active_List:
            command = f'xrandr --output {i} --auto'
            m.write(command+'\n')
    
    # Update autostart configuration file
    file2 = '/root/.config/autostart/lxrandr-autostart.desktop'
    config2 = 'Exec=/etc/lightdm/my_conf.sh'
    if not subprocess.run(['test', '-f', file2]).returncode:
        with open(file2,'r') as f2:
            lines2 = f2.readlines()
        with open(file2,'w') as f2:
            for line in lines2:
                if line.startswith('Exec='):
                    f2.write(config2+'\n')         
                else:    
                    f2.write(line)        
    else:
        pass

# Set Resolution Extended
def Set_Extend():
    # Get user input for main display and second display
    Display_name = input('Display Name: ')
    X = input('X-axis For Main Display(Horizontal): ')
    Y = input('Y-axis For Main Display(Vertical): ')
    Sec_Display = input("Second Display Name :")        
    Pos = input('What is the position of your second monitor relative to the main monitor?(left,right,below,above) :')
    
    # Generate commands to set resolution
    command = f"cvt {X} {Y} | grep Modeline | cut -d' ' -f2-"
    output = subprocess.check_output(command, shell=True)
    cvt_out = output.decode()
    command2 = f"cvt {X} {Y} | grep Modeline | cut -d' ' -f2"
    output2 = subprocess.check_output(command2, shell=True)
    cvt_out2 = output2.decode()
    
    # Set new mode, add mode, and output mode for extended display
    command4 = f'xrandr --newmode {cvt_out}'
    try:
        subprocess.run(command4, shell=True)
    except Exception as e:
        return print('(newmode) Error is :',e)  
    
    command5 = f'xrandr --addmode {Display_name} {cvt_out2}'
    try:
        subprocess.run(command5, shell=True)
    except Exception as e:
        return print('(addmode) Error :',e)
    
    command7 = f'xrandr --output {Display_name} --mode {cvt_out2} --output {Sec_Display} --auto --{Pos}-of {Display_name}'
    try:
        subprocess.run(command7,shell=True)
    except Exception as e:
        return print('(output) Error :',e)
    
    # Update configuration files
    file = '/etc/lightdm/lightdm.conf'
    config = 'display-setup-script=/etc/lightdm/my_conf.sh'
    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            if line.startswith('#display-setup-script='):
                f.write(config+'\n')
            else:    
                f.write(line)
    
    subprocess.run(['touch', '/etc/lightdm/my_conf.sh'])
    subprocess.run(['chmod', '+x', '/etc/lightdm/my_conf.sh'])
    
    my_conf = '/etc/lightdm/my_conf.sh'
    Xconf = f'''xrandr --newmode {cvt_out}
    xrandr --addmode {Display_name} {cvt_out2}
    xrandr --output {Display_name} --mode {cvt_out2} --output {Sec_Display} --auto --{Pos}-of {Display_name}'''
    with open(my_conf,'w') as m:
        m.write(Xconf)
    
    file2 = '/root/.config/autostart/lxrandr-autostart.desktop'
    config2 = 'Exec=/etc/lightdm/my_conf.sh'
    if not subprocess.run(['test', '-f', file2]).returncode:
        with open(file2,'r') as f2:
            lines2 = f2.readlines()
        with open(file2,'w') as f2:
            for line in lines2:
                if line.startswith('Exec='):
                    f2.write(config2+'\n')         
                else:    
                    f2.write(line)        
    else:
        pass
# Start Script
def main():
    print("1. Show Monitors List")
    print("2. Set Resolution")
    print("3. Automatically Set Resolution")
    print("4. Set Extended Monitors")
    choice = input("Enter your choice: ")

    if choice == "1":
        print(Display_List())
    elif choice == "2":
        Set_Resolution()
    elif choice == "3":
        auto()
    elif choice == "4":
       Set_Extend() 
    else:
        print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()