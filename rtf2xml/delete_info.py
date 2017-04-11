﻿#########################################################################
#                                                                       #
#                                                                       #
#   copyright 2016 Paul Henry Tremblay                                  #
#                                                                       #
#                                                                       #
#########################################################################

import sys, os, tempfile, rtf2xml.copy
class DeleteInfo:
    """Delelet unecessary destination groups"""


    def __init__(self, 
            in_file , 
            bug_handler,
            copy = None,
            run_level = 1,
            ):
        self.__file = in_file
        self.__bug_handler = bug_handler
        self.__copy = copy
        self.__write_to = tempfile.mktemp()
        self.__bracket_count=0
        self.__ob_count = 0
        self.__cb_count = 0
        self.__after_asterisk = 0
        self.__delete = 0
        self.__initiate_allow()
        self.__ob = 0
        self.__write_cb = 0
        self.__run_level = run_level
        self.__found_delete = 0
        self.__list = 0

    def __initiate_allow(self):
        """
        
        Initiate a list of destination groups which should be printed out.
        
        """

        self.__allowable = ('cw<ss<char-style', 
                            'cw<it<listtable_',
                            'cw<it<revi-table',
                            'cw<ls<list-lev-d',
                            'cw<fd<field-inst',
                            'cw<an<book-mk-st', 
                            'cw<an<book-mk-en',
                            'cw<an<annotation',
                            'cw<cm<comment___',
                            'cw<it<lovr-table',
                            # 'cw<ls<list______',
                        )
        self.__not_allowable = (
                'cw<un<unknown___',
                'cw<un<company___',
                'cw<ls<list-level',
                'cw<fd<datafield_',
                )
        self.__state = 'default'

        self.__state_dict = {
            'default'           : self.__default_func,
            'after_asterisk'    : self.__asterisk_func,
            'delete'           : self.__delete_func,
            'list'              : self.__list_func,
        }


    def __default_func(self,line):
        """Handle lines when in no special state. Look for an asterisk to 
        begin a special state. Otherwise, print out line."""

        ##cw<ml<asterisk__<nu<true
        if self.__token_info == 'cw<ml<asterisk__':
            self.__state = 'after_asterisk'
            self.__delete_count = self.__ob_count
        elif self.__token_info == 'ob<nu<open-brack':
            # write previous bracket, if exists
            if self.__ob:
                self.__write_obj.write(self.__ob)
            self.__ob = line
            return 0
        else:
            # write previous bracket, since didn't fine asterisk
            if self.__ob:
                self.__write_obj.write(self.__ob)
                self.__ob = 0
            return 1


    def __delete_func(self,line):
        """Handle lines when in delete state. Don't print out lines
        unless the state has ended."""
        if self.__delete_count == self.__cb_count:
            self.__state = 'default'
            if self.__write_cb:
                self.__write_cb = 0
                return 1
            return 0

    def __asterisk_func(self,line):
        """
        
        Determine whether to delete info in group

        Note on self.__cb flag.

        If you find that you are in a delete group, and the preivous
        token in not an open bracket (self.__ob = 0), that means
        that the delete group is nested inside another acceptable
        detination group. In this case, you have alrady written 
        the open bracket, so you will need to write the closed one
        as well.
        
        
        """
        # Test for {\*}, in which case don't enter
        # delete state
        self.__after_asterisk = 0 # only enter this function once
        self.__found_delete = 1
        if self.__token_info == 'bc<nu<clos-brack':
            if self.__delete_count == self.__cb_count:
                self.__state = 'default'
                self.__ob = 0
                # changed this because haven't printed out start
                return 0
            else:
                # not sure what happens here!
                # believe I have a '{\*}
                if self.__run_level > 3:
                    msg = 'flag problem\n'
                    raise self.__bug_handler(msg)
                return 1
        elif self.__token_info in self.__allowable :
            if self.__ob:
                self.__write_obj.write(self.__ob)
                self.__ob = 0
                self.__state = 'default'
            else:
                pass
            return 1
        elif self.__token_info == 'cw<ls<list______':
            self.__ob = 0
            self.__found_list_func(line)

        elif self.__token_info in self.__not_allowable:
            if not self.__ob:
                self.__write_cb = 1
            self.__ob = 0
            self.__state = 'delete'
            self.__cb_count = 0
            return 0
        else:
            if self.__run_level > 5:
                msg = 'After an asterisk, and found neither an allowable or non-allowble token\n'
                msg += 'token is "%s"\n' % self.__token_info
                raise self.__bug_handler
            if not self.__ob:
                self.__write_cb = 1
            self.__ob = 0
            self.__state = 'delete'
            self.__cb_count = 0
            return 0
            

    def __found_list_func(self, line):
        """

        print out control words in this group


        """
        self.__state = 'list'

    def __list_func(self, line):
        """

        Check to see if the group has ended.

        Return 1 for all control words.

        Return 0 otherwise.


        """
        if self.__delete_count == self.__cb_count and self.__token_info ==\
            'bc<nu<clos-brack':
            self.__state = 'default'
            if self.__write_cb:
                self.__write_cb = 0
                return 1
            return 0
        elif line[0:2] == 'cw':
            return 1
        else:
            return 0



    def delete_info(self):
        """Main method for handling other methods. Read one line in at 
        a time, and determine wheter to print the line based on the state."""
        line_to_read = 'dummy'
        read_obj = open(self.__file, 'r')
        self.__write_obj = open(self.__write_to, 'w')
        while line_to_read:

            #ob<nu<open-brack<0001

            to_print =1
            line_to_read = read_obj.readline()
            line = line_to_read
            self.__token_info = line[:16]
            if self.__token_info == 'ob<nu<open-brack':
                self.__ob_count = line[-5:-1]
            if self.__token_info == 'bc<nu<clos-brack':
                self.__cb_count = line[-5:-1]
            action = self.__state_dict.get(self.__state)
            if not action:
                sys.stderr.write('No action in dictionary state is "%s" \n'
                        % self.__state)
            to_print = action(line)
            """
            if self.__after_asterisk:
                to_print = self.__asterisk_func(line)
            elif self.__list:
                self.__in_list_func(line)
            elif self.__delete:
                to_print = self.__delete_func(line)
            else:
                to_print = self.__default_func(line)
            """

            if to_print:
                self.__write_obj.write(line)
        self.__write_obj.close()
        read_obj.close()
        copy_obj = rtf2xml.copy.Copy(bug_handler = self.__bug_handler)
        if self.__copy:
            copy_obj.copy_file(self.__write_to, "delete_info.data")
        copy_obj.rename(self.__write_to, self.__file)
        os.remove(self.__write_to)
        return self.__found_delete 

    
