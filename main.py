from lxml import etree
import time


class XMLComparison():
    def __init__(self, left_filename='left.xml', right_filename='right.xml'):
        self.start = time.clock()
        parser = etree.XMLParser(remove_blank_text=True)
        self.left = etree.parse(left_filename, parser=parser)
        self.left = self.left.getroot()
        self.left = self._convert_xml_to_dictionary(self.left)
        self.right = etree.parse(right_filename, parser=parser)
        self.right = self.right.getroot()
        self.right = self._convert_xml_to_dictionary(self.right)
        print('time to convert: ' + str(time.clock() - self.start))
        self.stack = []
        self._difference_log = []

    def _convert_xml_to_dictionary(self, node):
        xml_dict = {}
        for node in node.iterchildren():
            key = node.tag.split('}')[1] if '}' in node.tag else node.tag
            value = node.text if node.text else self._convert_xml_to_dictionary(node)
            if key in xml_dict:
                xml_dict[key].append(value)
            else:
                xml_dict[key] = [value]
        return xml_dict

    def compare_xml_dictionaries(self):
        self._compare_dictionaries(self.left, self.right)
        self._compare_dictionaries(self.right, self.left, checking_reverse=True)
        [print(i) for i in self._difference_log]

    def _compare_dictionaries(self, left, right, checking_reverse=False):
        for key, values in left.items():
            if key in right:
                for i, value in enumerate(values):
                    if type(value) == dict:
                        self.stack.append(key)
                        self._compare_dictionaries(left[key][i], right[key][i], checking_reverse=checking_reverse)
                    elif left[key] != right[key]:
                        if checking_reverse is False:
                            self._difference_log.append('Mismatch on key: {}, values: {} vs {} with ancestors: {}'.format(key, str(left[key]), str(right[key]), str(self.stack)))
                        break
            else:
                self._difference_log.append('Private key exists on ' + ('right' if checking_reverse else 'left') + 'but not left:' + key)
        try:
            self.stack.pop()
        except Exception as e:
            pass


start = time.clock()
xml_comparison = XMLComparison()
xml_comparison.compare_xml_dictionaries()
end = time.clock()
print('finished in:')
print(end - start)
