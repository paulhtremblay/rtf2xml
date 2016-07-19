#!/usr/bin/env python

    
    
#########################################################################
#                                                                       #
#                                                                       #
#   copyright 2016 Paul Henry Tremblay                                  #
#                                                                       #
#                                                                       #
#########################################################################
"""
not used anymore?

"""

import sys, os, re, rtf2xml.copy
import rtf2xml.get_char_map
import rtf2xml.configuration_dir
import rtf2xml.options_trem

class Encode:
    """

    Return the character map for the given value

    """

    def __init__(
            self,
            bug_handler,
            encoding = 'ansicpg1252',
            
            ):
        """

        Required:

            'char_file'--the file with the mappings



        Returns:

            nothing

            """
        self.__encoding = encoding
        self.__initiate_values()
        self.__bug_handler = bug_handler


    def __initiate_values(self):
        rtf_dir = rtf2xml.configuration_dir.get_dir()
        if not os.path.isfile(the_char_map):
            msg = ('Cannot find character set "%s" \n' % the_char_map)
            raise self.__bug_hander(msg)

        self.__sub_dict = {}
        char_map_obj = rtf2xml.get_char_map.GetCharMap(the_char_map)
        char_dict = char_map_obj.get_char_map(map = self.__encoding)
        self.__parse_standard_char_map(char_dict)
        char_dict = char_map_obj.get_char_map('ms_standard')
        self.__parse_standard_char_map(char_dict, ms = 1)
        the_keys = self.__sub_dict.keys()
        self.__sub_string = '|'.join(the_keys)
        self.__sub_string = '(%s)' % self.__sub_string
        self.__sub_string = r'%s' % self.__sub_string

    def __parse_standard_char_map(self, char_dict, ms = 0):
        final_dict = {}
        the_keys = char_dict.keys()
        for the_key in the_keys:
            the_num = char_dict.get(the_key)
            if the_num[0:5] == '<udef':
                pass
            else:
                the_num = the_num[3:-1]
                the_num = int(the_num, 16)
                the_char = unichr(the_num)
                if not ms:
                    convert_string = '\\u%s\\%s' % (the_num, the_key)
                else:
                    convert_string = '\\%s' % (the_key)
                final_dict[the_char] = convert_string
        
        self.__sub_dict.update(final_dict) 


    def encode_line(self, line):
        line = line.replace('\t', '\\tab')
        try:
            line.encode('us-ascii')
        except UnicodeError as msg:
            line = self.__standard_sub(line)
        return line

    def __standard_sub(self, line):
        line = re.sub(self.__sub_string, self.__replace_func, line) 
        try:
            line.encode('us-ascii')
        except UnicodeError as  msg:
            line = self.__encode_each_char(line)
        return line
    
    def __replace_func(self, match_obj):
        # sys.stderr.write( repr(match_obj.group(1)))
        uni_char = match_obj.group(1)
        replace = self.__sub_dict.get(uni_char) 
        if replace:
            return replace
        else:
            sys.stderr.write('No match for "%s" \n' % uni_char.encode('utf-8'))
            return '???'

    def __encode_each_char(self, line):
        final_string = ''
        for char in line:
            num = ord(char)
            if num > 127:
                char = '\\u%s\\\'33'  % num
                final_string += char
            else:
                final_string += char
        return final_string
            
        
    def encode_file(self, in_file, out_file = None):
        line_to_read = 1
        read_obj = open(in_file, 'r')
        if out_file:
            write_obj = open(out_file, 'w')
        while line_to_read:
            line_to_read = unicode(read_obj.readline(), 'utf-8')
            line = line_to_read
            line = unicode(line)
            line = self.encode_line(line)
            if out_file:
                write_obj.write(line)
            else:
                sys.stdout.write(line.encode('utf-8'))

def get_options():

    return_dict = {}
    options_dict = {
                    'help'              :       [0, 'h'],
                    'output'            :       [1, 'o'],
            }
            
    options_obj = rtf2xml.options_trem.ParseOptions(
                    system_string = sys.argv,
                    options_dict = options_dict
                )

    options, arguments = options_obj.parse_options()

    if options == 0:
        sys.stderr.write('The script will now quit\n')
        sys.exit(1)

    if len(arguments) != 1:
        sys.stderr.write('Please provide a file to work on.\n')
        sys.stderr.write('Script will now quit.\n')
        sys.exit(1)
    in_file = arguments[0]
    if not os.path.isfile(in_file):
        sys.stderr.write('Cannot find file "%s"\n' %  in_file)
        sys.stderr.write('Script will now quit\n')
        sys.exit(1)
    return_dict['in_file'] = in_file

    if 'output' in options:
        output = options['output']
        return_dict['output'] = output

    return return_dict




if __name__ == '__main__':
    
    return_dict = get_options()
    encode_obj = Encode()
    in_file = return_dict.get('in_file')
    encode_obj.encode_file(in_file)


