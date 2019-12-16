import re


def addItems(infoList):
    rownum = []
    rownum_urology = []
    output = []
    for i in range(0, len(infoList)):
        infoString0 = str(infoList[i]).replace('\n', '')
        infoString = str(infoList[i])
        flag = False
        if re.search('Special Needs Dental', infoString0, re.I):
            # print(i)
            # print(infoString0)
            if re.search('^((?!Oral Surgery).)*$', infoString0, re.I):
                if re.search('^((?!Maxillo-Facial Surgery).)*$', infoString0, re.I):
                    # print(i)
                #     infoString0.replace('Special Needs Dental', 'Oral Surgery')
                #     infoString.replace('\nSpecial Needs Dental', 'Oral Surgery' + '\n' + 'Maxillo-Facial Surgery')
                    infoString0 = str(infoList[i]).replace('\n', '').replace('Special Needs Dental',
                                                                         'Oral Surgery' + 'Maxillo-Facial Surgery')
                    infoString = str(infoList[i]).replace('Special Needs Dental', 'Oral Surgery' + '\n' +
                                                      'Maxillo-Facial Surgery')
                    # print(infoString0)
                    # print(infoString)
                    flag = True
                else:
                    # print(7)
                    infoString0 = str(infoList[i]).replace('\n', '').replace('Special Needs Dental',
                                                                             'Oral Surgery')
                    infoString = str(infoList[i]).replace('Special Needs Dental', 'Oral Surgery')
                    # print(infoString)
                    flag = True
            elif re.search('Oral Surgery', infoString0, re.I):
                if re.search('^((?!Maxillo-Facial Surgery).)*$', infoString0, re.I):
                    # print(0)
                # print(infoString)
                # infoString0.replace('Special Needs Dental', 'Maxillo-Facial Surgery')
                # infoString.replace('Special Needs Dental', 'Maxillo-Facial Surgery')
                    infoString0 = str(infoList[i]).replace('\n', '').replace('Special Needs Dental',
                                                                         'Maxillo-Facial Surgery')
                    infoString = str(infoList[i]).replace('Special Needs Dental', 'Maxillo-Facial Surgery')
                    # print(infoString)
                    flag = True
                else:
                    # print(2)
                    infoString0 = str(infoList[i]).replace('\n', '').replace('Special Needs Dental', '')
                    infoString = str(infoList[i]).replace('Special Needs Dental', '')

        if re.search('General Surgery', infoString0, re.I):
            if re.search('^((?!Paediatric Surgery).)*$', infoString0, re.I):
                # rownum.append(i + 6)
            # infoList[i] = infoString + '\n' + 'Paediatric Surgery'
                infoString0 = infoString0 + 'Paediatric Surgery'
                infoString = infoString + '\n' + 'Paediatric Surgery'
                flag = True

        elif re.search('Paediatric Surgery', infoString0, re.I):
            if re.search('^((?!General Surgery).)*$', infoString0, re.I):
                # rownum.append(i + 6)
                infoString0 = infoString0 + 'General Surgery'
                infoString = infoString + '\n' + 'General Surgery'
                flag = True

        if re.search('Urology', infoString0, re.I):
            rownum_urology.append(i + 6)
            flag = True
            if re.search('^((?!Paediatric Urology).)*$', infoString0, re.I):
                infoString0 = infoString0 + 'Paediatric Urology'
                infoString = infoString + '\n' + 'Paediatric Urology'
                # flag = True

        elif re.search('Paediatric Urology', infoString0, re.I):
            rownum_urology.append(i + 6)
            flag = True
            if re.search('^((?!Urology).)*$', infoString0, re.I):
                infoString0 = infoString0 + 'Urology'
                infoString = infoString + '\n' + 'Urology'
                # flag = True

        if re.search('Haematology', infoString0, re.I):
            if re.search('^((?!Paediatric Oncology).)*$', infoString0, re.I):
                infoString0 = infoString0 + 'Paediatric Oncology'
                infoString = infoString + '\n' + 'Paediatric Oncology'
                flag = True

        elif re.search('Paediatric Oncology', infoString0, re.I):
            if re.search('^((?!Haematology).)*$', infoString0, re.I):
                infoString0 = infoString0 + 'Haematology'
                infoString = infoString + '\n' + 'Haematology'
                flag = True

        # if re.search('^((?!Paediatric).) ENT*$', infoString0):
        #     # print(i)
        #     infoString0 = infoString0 + 'Paediatric ENT'
        #     infoString = infoString + '\n' + 'Paediatric ENT'
        #     flag = True
        # elif re.search('Paediatric ENT', infoString0):
        #     print(i)
        #     if re.search('Paediatric ENT', infoString0):
        #         break
        #     else:
        #         infoString0 = infoString0 + 'ENT'
        #         infoString = infoString + '\n' + 'ENT'
        #         flag = True

        # if re.search('ENT', infoString0):
        #     if re.search('^((?!Paediatric).) Paediatric ENT*$', infoString0):
        #         break
        #     else:
        #         print(9)
        #         infoString0 = infoString0 + 'Paediatric ENT'
        #         infoString = infoString + '\n' + 'Paediatric ENT'
        #         flag = True

        if re.search('Paediatric ENT', infoString0):
            # print(infoString0)
            if re.search('ENT''Paediatric ENT', infoString0):
                # ENT and Paediatric ENT come up at he same time
                # print(i)
                # print(infoString0)
                a = 0
            else:
                # print(i)
                # print(infoString0)
                infoString0 = infoString0 + 'ENT'
                infoString = infoString + '\n' + 'ENT'
                flag = True

        elif re.search('ENT', infoString0):
            # print(9)
            infoString0 = infoString0 + 'Paediatric ENT'
            infoString = infoString + '\n' + 'Paediatric ENT'
            flag = True

        if re.search('Bronchoscopy/Thoracoscopy', infoString0, re.I):
            if re.search('^((?!Paediatric Bronchoscopy).)*$', infoString0, re.I):
                infoString0 = infoString0 + 'Paediatric Bronchoscopy'
                infoString = infoString + '\n' + 'Paediatric Bronchoscopy'
                flag = True

        elif re.search('Paediatric Bronchoscopy', infoString0, re.I):
            if re.search('^((?!Bronchoscopy/Thoracoscopy).)*$', infoString0, re.I):
                infoString0 = infoString0 + 'Bronchoscopy/Thoracoscopy'
                infoString = infoString + '\n' + 'Bronchoscopy/Thoracoscopy'
                flag = True

        if re.search('Maxillo-Facial Surgery', infoString0, re.I):
            if re.search('^((?!Oral Surgery).)*$', infoString0, re.I):
                infoString0 = infoString0 + 'Oral Surgery'
                infoString = infoString + '\n' + 'Oral Surgery'
                flag = True

        elif re.search('Oral Surgery', infoString0, re.I):
            if re.search('^((?!Maxillo-Facial Surgery).)*$', infoString0, re.I):
                infoString0 = infoString0 + 'Maxillo-Facial Surgery'
                infoString = infoString + '\n' + 'Maxillo-Facial Surgery'
                flag = True

        while flag:
            # print(i + 6)
            # print(infoString)
            rownum.append(i + 6)
            output.append(infoString)
            flag = False

    return rownum, list(set(rownum_urology)), output
