"""
XML => RAM AND RAM => XML => compare files
"""

from schemautils.xmltoram import readxmlfile
from schemautils.ramtoxml import writexmlfile


def comparing_files(sourcefile, resultfile):
    with open(sourcefile, 'r', encoding='utf8') as sf, open(resultfile, 'r', encoding='utf8') as rf:
        equal = True
        for source_line in sf:
            result_line = rf.readline()
            if source_line.split() != result_line.split():
                print('The match in the following lines is broken:')
                print('Source line: ' + source_line)
                print('Result line: ' + result_line)
                equal = False
        return equal


def run(inputfile, outputfile):  # inputfile - входной файл, преобразующийся во внутреннее представление в виде объектов
    schemas = readxmlfile(inputfile)
    for schema in schemas:
        writexmlfile(schema, outputfile)
    if comparing_files(inputfile, outputfile):
        print('Files ' + inputfile + ' and ' + outputfile + ' are the same!')
    else:
        print('Files ' + inputfile + ' and ' + outputfile + ' are different!')


if __name__ == "__main__":
    file1 = 'C:\\Output\\tasks.xml'
    file2 = 'C:\\Output\\taskscheck.xml'
    run(file1, file2)  # передаем пути к 2 файлам в качестве параметров в функцию run()