def gen_cmd_script(file):
    name = file.path
    while name.find('/') != -1:
        name = name[name.find('/') + 1:]
    path = f"data/{name[:name.find('.')]}/encounter.py"

    script = open(path, 'w')
    script.write('import src.lib.control as control\n\n')
    script.write('def encounter(settings, test=None):\n')
    for cmd in file.commands:
        cmd = cmd.split(',')
        
        if cmd[0] == 'Button Press':
            script.write(f"    control.input(settings.control['{cmd[1].replace(' ', '_').lower()}'], {cmd[2]}, test=test, print_input='{cmd[1]}')\n")
        if cmd[0] == 'Repeated Button Press':
            script.write(f"    control.repeat_button_input(settings.control['{cmd[1].replace(' ', '_').lower()}'], {cmd[2]}, interval={cmd[3]}, test=test, print_input='{cmd[1]}')\n")
        if cmd[0] == 'Soft Reset':
            script.write(f"    control.soft_reset(settings.control['l'], settings.control['r'], settings.control['start'], settings.control['select'], {cmd[2]}, test=test)\n")
        if cmd[0] == 'End':
            script.write('    return\n')

    script.close()
    return path