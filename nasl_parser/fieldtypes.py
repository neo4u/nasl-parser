import re
from datetime import datetime

class RegexValueFinder():
    pattern = re.compile(r'.*')
    values = ''
    def __init__(self, value):
        self.values = self.pattern.findall(value)

class SingleNumericType(RegexValueFinder):
    def __init__(self, value):
        self.values = int(value)

class MultiNumericType(RegexValueFinder):
    def __init__(self, value):
        self.pattern = re.compile(r'(\d+)')
        RegexValueFinder.__init__(self, value)
        self.values = [int(value) for value in self.values]

class MultiStringType():
    def __init__(self, value):
        self.values = [item.strip() for item in value.split(',')]

class LocalizedTextType(RegexValueFinder):
    def __init__(self, value):
        self.pattern = re.compile(r'(\w+):(.+)')
        RegexValueFinder.__init__(self, value)
        if len(self.values):
            self.values = {
                self.values[0][0]: self.values[0][1],
            }

class GenericDictType(RegexValueFinder):
    def __init__(self, value):
        attributes = {}
        for attribute in value:
            parsed_attribute = attribute.replace(',value', ', value').split(', value:')
            try:
                attributes.update({
                    parsed_attribute[0].split(':')[1].strip().strip("'"): parsed_attribute[1].strip(),
                })
            except:
                pass
        self.values = attributes

class GenericDateTimeType(RegexValueFinder):
    def __init__(self, value):
        self.pattern = re.compile(r'\s+(.+)\s+')
        RegexValueFinder.__init__(self, value)
        self.values = datetime.strptime(self.values[0], '%Y/%m/%d %H:%M:%S')

class VersionType(RegexValueFinder):
    def __init__(self, value):
        self.pattern = re.compile(r'(\d+\.\d+)')
        RegexValueFinder.__init__(self, value)
        self.values = self.values[0]

class GenericTextType(RegexValueFinder):
    def __init__(self, value):
        self.pattern = re.compile(r'(.+)')
        RegexValueFinder.__init__(self, value)
        self.values = self.values[0]
