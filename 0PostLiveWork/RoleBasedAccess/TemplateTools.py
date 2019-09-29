# Tools to analyse template given the emplyee information
# Updating any modification to geneDiagram.py
# Version 1.0

import re

def getTemplateIndirect(infoString, infoStringAdd=''):
    template = ''

    if infoString == '':
        return template

    if infoStringAdd != '':
        infoString = infoString + ' ' + infoStringAdd

    if re.search('Medical Student', infoString, re.I):
        if re.search('Cardiology', infoString, re.I):
            template = 'Cardiology Med Student'
        else:
            template = 'Medical Student'

    elif re.search('Foundation Year', infoString, re.I):
        if re.search('General Practice|Emergency', infoString, re.I):
            template = 'ED FY Doctor'
        else:
            template = 'Foundation Year Doctor'

    elif re.search('Radiologist', infoString, re.I):
        if re.search('Consultant', infoString, re.I):
            template = 'Consultant Radiologist'
        else:
            template = 'ST1-4 Radiologist'

    elif re.search('Anaesthetist', infoString, re.I):
        if re.search('Registrar|Associate', infoString, re.I):
            template = 'Anaesthetist'
        else:
            template = 'Named Consultant Anaesthetist'

    elif re.search('General Practitioner', infoString, re.I):
        template = 'ED Consultant'

    elif re.search('Surgeon|Surgery', infoString, re.I):
        if re.search('Associate|Registrar', infoString, re.I):
            template = 'Surgeon'
        else:
            template = 'Surgeon Consultant'

    elif re.search('Consultant', infoString, re.I):
        if re.search('Cardiology', infoString, re.I):
            template = 'Cardiologist'
        elif re.search('General Practice|Emergency Medicine', infoString, re.I):
            template = 'ED Consultant'
        elif re.search('Anaesthetics|Intensive Care Medicine', infoString, re.I):
            template = 'Named Consultant Anaesthetist'
        elif re.search('Oncology|Haematology', infoString, re.I):
            template = 'Consultant (Oncology)'
        else:
            template = 'Consultant (all types)'

    elif re.search('Specialty|Specialist', infoString, re.I):
        if re.search('Associate|Registrar', infoString, re.I):
            if re.search('Cardiology', infoString, re.I):
                template = 'Cardiology Registrar'
            elif re.search('General Practice|Emergency Medicine', infoString, re.I):
                template = 'ED Physician'
            elif re.search('Anaesthetics|Intensive Care Medicine', infoString, re.I):
                template = 'Anaesthetist'
            else:
                template = 'Doctor - ST1+ (SpR/SHO)'
        else:
            if re.search('Anaesthetics|Intensive Care Medicine', infoString, re.I):
                template = 'Named Consultant Anaesthetist'
            elif re.search('Oncology|Haematology', infoString, re.I):
                template = 'Consultant (Oncology)'
            else:
                template = 'Consultant (all types)'

    else:
        template = '0NOT_KNOWN'

    return template
