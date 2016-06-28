#########################################################################
#                                                                       #
#                                                                       #
#   copyright 2016 Paul Henry Tremblay                                  #
#                                                                       #
#                                                                       #
#########################################################################

import sys, os, rtf2xml.copy, string
class GetCharMap:
    """

    Return the character map for the given value

    """

    def __init__(self, bug_handler, char_file):
        """

        Required:

            'char_file'--the file with the mappings



        Returns:

            nothing

            """
        self.__char_file = char_file

    def get_char_map(self, map):
        found_map = 0
        map_dict = {}
        read_obj = open(self.__char_file, 'r')
        line = 1
        while line:
            line = read_obj.readline()
	    begin_element = '<%s>' % map;
	    end_element = '</%s>' % map
            if not found_map:
                if string.find(line, begin_element) >= 0:
                    found_map = 1
            else:
		if string.find(line, end_element) >= 0:
                    break
                else:
                    line = line[:-1]
                    fields = line.split(':')
                    fields[1].replace('\\colon', ':')
                    map_dict[fields[1]] = fields[3]
            
        read_obj.close()
        if not found_map:
            msg = 'no map found\n'
            msg += 'map is "%s"\n'
            raise self.__bug_handler, msg
        return map_dict

