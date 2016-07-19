import sys
import os
import unittest
import xml.etree.ElementTree as ET

def _check_dir():
    cur_dir = os.path.curdir
    all_paths = os.listdir(cur_dir)
    path_to_test = os.path.join('test', 'test_all.py')
    if not os.path.isfile(path_to_test):
        return False
    if os.path.abspath(path_to_test) != os.path.abspath(__file__):
        return False
    return True

def setup():
    if not _check_dir():
        sys.stderr.write("Please be in home directory to run\n")
        sys.exit(1)
sys.path.insert(0, ".")
import rtf2xml.ParseRtf

def convert_string_to_tree(xmlString):
    return ET.fromstring(xmlString)

def xml_compare_strings(x1, x2):
    x1 = convert_string_to_tree(x1)
    x2 = convert_string_to_tree(x2)
    t = xml_compare(x1, x2)
    return t

def xml_compare(x1, x2, excludes=[]):
    """
    Compares two xml etrees
    :param x1: the first tree
    :param x2: the second tree
    :param excludes: list of string of attributes to exclude from comparison
    :return:
        True if both files match
    """

    if x1.tag != x2.tag:
        return False
    for name, value in x1.attrib.items():
        if not name in excludes:
            if x2.attrib.get(name) != value:
                return False
    for name in x2.attrib.keys():
        if not name in excludes:
            if name not in x1.attrib:
                return False
    if not text_compare(x1.text, x2.text):
        return False
    if not text_compare(x1.tail, x2.tail):
        return False
    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
    if len(cl1) != len(cl2):
        return False
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if not c1.tag in excludes:
            if not xml_compare(c1, c2, excludes):
                return False
    return True

def text_compare(t1, t2):
    """
    Compare two text strings
    :param t1: text one
    :param t2: text two
    :return:
        True if a match
    """
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()

def get_file_strings(result):
    result_string = get_file_string(result)
    return result_string

def get_file_string(path):
    final = ''
    with open(path, 'r', encoding="utf-8-sig") as read_obj:
        line_to_read = 1
        while line_to_read:
            line_to_read = read_obj.readline()
            line = line_to_read
            final += line
    return final

def make_abs_path(path, file_type = 'good'):
    cur_dir = os.path.curdir
    basefile, ext = os.path.splitext(path)
    xml_path = basefile + '.xml'
    test_dir = os.path.join(cur_dir, "test", "test_files", file_type)
    target = os.path.join(test_dir, path)
    result_dir = os.path.join(cur_dir, "test", "test_files", '{0}_results'.format(file_type))
    result = os.path.join(result_dir, xml_path)
    if not os.path.isfile(target):
        raise ValueError("target {0} not found".format(target))
    if not os.path.isfile(result):
        raise ValueError("retuls {0} not found".format(xml_path))
    return target, result

class MyTest(unittest.TestCase):

    def setUp(self):
        pass


    def test_tree_compare1(self):
        x1 = """<root>   </root>
        """
        x2 = """<root> </root> """
        t =  xml_compare_strings( x1, x2)
        self.assertTrue(t)

    def test_simplest(self):
        target, result = make_abs_path("simplest.rtf")
        result_string = get_file_strings(result)
        parse_obj =rtf2xml.ParseRtf.ParseRtf(target)
        xml_string = parse_obj.parse_rtf()
        self.assertTrue(xml_compare_strings(xml_string, result_string))

    def test_plain_tag(self):
        #this passes the test, though the XML is wrong!
        target, result = make_abs_path("italics_plain.rtf")
        result_string = get_file_strings(result)
        parse_obj =rtf2xml.ParseRtf.ParseRtf(target)
        xml_string = parse_obj.parse_rtf()
        self.assertTrue(xml_compare_strings(xml_string, result_string))


if __name__ == '__main__':
    setup()
    unittest.main()
