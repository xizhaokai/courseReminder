import xlrd
import os

def getCourseInfo():
    # 获取时间表
    timeList = list()
    with open('时间表.csv', 'r', encoding='utf-8') as f:
        s = f.read()
        for line in s.split('\n')[1:]:
            l = line.split(',')
            if len(l) == 2:
                timeList.append(l[1])

    codeList = dict()
    with open('codes.csv', 'r', encoding='utf-8') as f:
        s = f.read()
        for line in s.split('\n')[1:]:
            l = line.split(',')
            if len(l) == 2:
                codeList[l[0]] = l[1]

    # 获取课程表数据
    workBook = xlrd.open_workbook('course.xls')
    dataJson = dict()
    for sheetName in workBook.sheet_names():
        code = codeList[sheetName]
        dataJson[code] = dict()
        table = workBook.sheet_by_name(sheetName)
        mergedCells = set() # 合并单元格集合
        for cells in table.merged_cells:
            for x in range(cells[0], cells[1]):
                for y in range(cells[2], cells[3]):
                    mergedCells.add((x, y))
        for weekDay in range(5):
            for i in range(len(timeList)):
                course = table.cell(i+1, weekDay+1).value
                if len(course) == 0:
                    continue
                hour, minute = timeList[i].split(':')
                minutePure = int(hour) * 60 + int(minute) - 22 # 提前22分钟推送
                hour, minute = int(minutePure / 60), int(minutePure % 60)
                realWeekDay = i+1
                if(hour - 8 <0):
                    hour = 16+hour
                    realWeekDay = i
                else:
                    hour = hour - 8
                # hour = 16 + hour if hour - 8 < 0 else hour - 8 #<---这个是干啥的？
                cronTime = '{} {} * * {}'.format(minute, hour, realWeekDay)
                dataJson[code][cronTime] = timeList[i] + course
    return dataJson

def genWorkflows(dataJson):
    for root, dirs, files in os.walk('./workflows'):
        for file in files:
            os.remove(os.path.join(root, file))
    with open('template.yml', 'r', encoding='utf-8') as f:
        s = f.read()
        for classCode, data in dataJson.items():
            for cronTime, information in data.items():
                temp = s.replace('classCode', classCode)
                temp = temp.replace('informationContent', information)
                temp = temp.replace('cronTimeContent', cronTime)
                cronTimeList = cronTime.split(' ')
                workflowName = '{}{}{}{}'.format(classCode, cronTimeList[0], cronTimeList[1], cronTimeList[4])
                temp = temp.replace('workflowName', workflowName)
                with open(os.path.join('./.github/workflows', workflowName + '.yml'), 'w+', encoding='utf-8') as f:
                    f.write(temp)
        
data = getCourseInfo()
genWorkflows(data)
