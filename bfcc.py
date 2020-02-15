import sys
import re

def checkBackets(data):
    openb = re.sub('[^\[]','',data)
    closeb = re.sub('[^\]]','',data)
    diff = abs(len(openb) - len(closeb))
    if diff != 0:
        if openb < closeb:
            print('ERROR : {} \'\]\' missing'.format(diff))
        if openb > closeb:
            print('ERROR : {} \'\[\' missing'.format(diff))
        sys.exit(-1)
    else:
        return

def sanitize(data):
    # Remove comments
    new_data = re.sub('[^><.,+-\[\]]','',data)

    # Check balanced square brackets
    checkBackets(new_data)

    return new_data

def convertInstr(data):
    instr_dict = {
            '>':'ptr++;\n',
            '<':'ptr--;\n',
            '+':'(*ptr)++;\n',
            '-':'(*ptr)--;\n',
            '.':'putchar(*ptr);\n',
            ',':'*ptr=getchar();\n',
            '[':'while(*ptr){\n',
            ']':'\n}',
            }
    regex = re.compile("(%s)" % "|".join(map(re.escape, instr_dict.keys())))
    return regex.sub(lambda mo: instr_dict[mo.string[mo.start():mo.end()]], data)


src_path = sys.argv[1]
src_data = open(src_path,'r').read()
c_src_path = src_path + '.c'
c_array_size = 10000

c_header = '#include <stdio.h>\n'
c_header += 'int array[{}];\n'.format(c_array_size)
c_header += 'int*ptr = array;\n'
c_header += 'void main(){\n'
c_footer = '}'
instr = sanitize(src_data)
instr = convertInstr(instr)

cf = open(c_src_path,'w')
cf.write(c_header)
cf.write(instr)
cf.write(c_footer)
cf.close()
