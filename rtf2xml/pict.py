﻿#########################################################################
#                                                                       #
#                                                                       #
#   copyright 2016 Paul Henry Tremblay                                  #
#                                                                       #
#                                                                       #
#########################################################################

import sys, os, tempfile, rtf2xml.copy
class Pict:
    """Process graphic information"""


    def __init__(self,
            in_file,
            bug_handler,
            out_file,
            copy = None,
            orig_file = None,
            run_level = 1,
        ):
        self.__file = in_file
        self.__bug_handler = bug_handler
        self.__copy = copy
        self.__run_level = run_level
        self.__write_to = tempfile.mktemp()
        self.__bracket_count = 0
        self.__ob_count = 0
        self.__cb_count = 0
        self.__pict_count = 0
        self.__in_pict = 0
        self.__already_found_pict = 0
        self.__orig_file = orig_file
        self.__initiate_pict_dict()
        self.__out_file = out_file

        # this is left over
        self.__no_ask = 1

    def __initiate_pict_dict(self):
        self.__pict_dict = {
        'ob<nu<open-brack'    :   self.__open_br_func,
        'bc<nu<clos-brack'    :   self.__close_br_func,
        'tx<nu<__________'    :   self.__text_func,
        }
    
    def __open_br_func(self, line):
        return "{\n"

    def __close_br_func(self, line):
        return "}\n"

    def __text_func(self, line):
        #tx<nu<__________<true text
        return line[18:]

    def __make_dir(self):
        """ Make a dirctory to put the image data in"""
        base_name = os.path.basename(self.__orig_file)
        base_name, ext  = os.path.splitext(base_name)
        if self.__out_file:
            dir_name = os.path.dirname(self.__out_file)
        else:
            dir_name = os.path.dirname(self.__orig_file)
        # self.__output_to_file_func()
        self.__dir_name = base_name + "_rtf_pict_dir/"
        self.__dir_name = os.path.join(dir_name, self.__dir_name)
        if not os.path.isdir(self.__dir_name):
            try:
                os.mkdir(self.__dir_name)
            except OSError as msg:
                msg = str(msg)
                msg += "Couldn't make directory '%s':\n" % (self.__dir_name)
                raise self.__bug_handler
        else:
            if self.__no_ask:
                user_response = 'r'
            else:
                msg = 'Do you want to remove all files in %s?\n' % self.__dir_name
                msg += 'Type "r" to remove.\n'
                msg +=  'Type any other key to keep files in place.\n'
                sys.stderr.write(msg)
                user_response = raw_input()
            if user_response == 'r':
                if self.__run_level > 1:
                    sys.stderr.write('Removing files from old pict directory...\n')
                all_files = os.listdir(self.__dir_name)
                for the_file in all_files:
                    the_file = os.path.join(self.__dir_name, the_file)
                    try:
                        os.remove(the_file)
                    except OSError:
                        pass
                if self.__run_level > 1:
                    sys.stderr.write('Files removed.\n')
    
    def __create_pict_file(self):
        """Create a file for all the pict data to be written to.
        """
        self.__pict_file = os.path.join(self.__dir_name, 'picts.rtf')
        write_pic_obj = open(self.__pict_file, 'w')
        write_pic_obj.close()
        self.__write_pic_obj = open(self.__pict_file, 'a')
    
    def __in_pict_func(self, line):
        if self.__cb_count == self.__pict_br_count:
            self.__in_pict = 0
            self.__write_pic_obj.write("}\n")
            return 1
        else:
            action = self.__pict_dict.get(self.__token_info)
            if action:
                line = action(line)
                self.__write_pic_obj.write(line)
            return 0

    def __default(self, line, write_obj):
        """Determine if each token marks the beginning of pict data. 
        If it does, create a new file to write data to (if that file 
        has not already been created.) Set the self.__in_pict flag to true.
        If the line does not contain pict data, return 1
        """
        """
        $pict_count++;
        $pict_count =  sprintf("%03d", $pict_count);
        print OUTPUT "dv<xx<em<nu<pict<at<num>$pict_count\n";
        """
        if self.__token_info == 'cw<gr<picture___':
            self.__pict_count += 1
            # write_obj.write("mi<tg<em<at<pict<num>%03d\n" % self.__pict_count)

            write_obj.write('mi<mk<pict-start\n')
            write_obj.write('mi<tg<empty-att_<pict<num>%03d\n' % self.__pict_count)
            write_obj.write('mi<mk<pict-end__\n')
            if not self.__already_found_pict:
                self.__create_pict_file()
                self.__already_found_pict=1;
                self.__print_rtf_header()
            self.__in_pict = 1
            self.__pict_br_count = self.__ob_count
            self.__cb_count = 0
            self.__write_pic_obj.write("{\\pict\n")
            return 0
        return 1

    def __print_rtf_header(self):
        """Print to pict file the necessary RTF data for the file to be
        recognized as an RTF file.
        """
        self.__write_pic_obj.write("{\\rtf1 \n")
        self.__write_pic_obj.write("{\\fonttbl\\f0\\null;} \n")
        self.__write_pic_obj.write("{\\colortbl\\red255\\green255\\blue255;} \n")
        self.__write_pic_obj.write("\\pard \n")

    
    def process_pict(self):
        self.__make_dir()
        read_obj = open(self.__file)
        write_obj = open(self.__write_to, 'w')
        line_to_read = 'dummy'
        while line_to_read:
            line_to_read = read_obj.readline()
            line = line_to_read
            self.__token_info = line[:16]
            if self.__token_info == 'ob<nu<open-brack':
                self.__ob_count = line[-5:-1]
            if self.__token_info == 'bc<nu<clos-brack':
                self.__cb_count = line[-5:-1]
            if not self.__in_pict:
                to_print = self.__default(line, write_obj)
                if to_print :
                    write_obj.write(line)

            else:
                to_print = self.__in_pict_func(line)
                if to_print :
                    write_obj.write(line)

        if self.__already_found_pict:
            self.__write_pic_obj.write("}\n")
            self.__write_pic_obj.close()
        read_obj.close()
        write_obj.close()
        copy_obj = rtf2xml.copy.Copy(bug_handler = self.__bug_handler)
        if self.__copy:
            copy_obj.copy_file(self.__write_to, "pict.data")
        copy_obj.rename(self.__write_to, self.__file)
        os.remove(self.__write_to)
        if self.__pict_count == 0:
            try:
                os.rmdir(self.__dir_name)
            except OSError:
                pass
