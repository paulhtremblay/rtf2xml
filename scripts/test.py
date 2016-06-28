#!/usr/bin/env python
import os, sys, copy, tempfile, shutil, commands, getopt
import rtf2xml.ParseRtf





class Test:
    def __init__(self):
        self.__get_opts()
        self.__error = []
        self.__get_test_files()
        self.__test_good()
        self.__test_bad()
        for error in self.__error:
            print '\n***************************\n'
            print 'File:"%s"\n' % error[0]
            print error[1]
            print '***************************\n'

        self.__validate()
        if os.path.isdir(self.__out_dir):
            shutil.rmtree(self.__out_dir)
            pass

    def __help_message(self):
        print"""
python test.py 
    [ --msv-jar <path> ] 
    [ --clean ]
    [ --local ]

the --msv-jar allows you to validate your output tests.

The --local option allows you to test the package before installation.

the --clean option makes sure that you are testing your installation.
        """

    def __get_opts(self):
        self.__msv_jar = None
        try:
            options, arguments = getopt.getopt(sys.argv[1:], 'h', ['help', 'clean','local', 'msv-jar=' ])
        except getopt.GetoptError, error:
            sys.stderr.write(str(error))
            self.__help_message()
            sys.exit(1)
        self.__local = None
        self.__clean = None
        for opt, opt_arg in options:
            if 'msv-jar' in opt:
                self.__msv_jar = opt_arg
            if '-h' in opt or '--help' in opt:
                self.__help_message()
                sys.exit(0)
            if '--local' in opt:
                self.__local = 1
            if '--clean' in opt:
                self.__clean = 1
    
    def __get_test_files(self):
        self.__script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
        if self.__local:
            current_dir = os.getcwd()
            needed_dir = os.path.abspath(os.path.join(self.__script_dir, '..'))
            if current_dir != needed_dir:
                sys.stderr.write('You have to be in "%s" to run a local test of the script.\n' % needed_dir)
                sys.exit(1)
        if self.__clean:
            current_dir = os.getcwd()
            needed_dir = os.path.abspath(os.path.join(self.__script_dir, '..'))
            if current_dir == needed_dir:
                sys.stderr.write('Get out of "%s" to run a test of what you have installed.\n' % needed_dir)
                sys.exit(1)

        self.__test_dir = os.path.abspath(os.path.join(self.__script_dir, '..', 'test_files'))
        if not os.path.isdir(self.__test_dir):
            sys.stderr.write('Can\'t find "test_files" directory\n')
            sys.exit(1)
        self.__good_dir = os.path.join(self.__test_dir, 'good')
        if not os.path.isdir(self.__good_dir):
            sys.stderr.write('Can\'t find "good" directory\n')
            sys.exit(1)
        self.__invalid_dir = os.path.join(self.__test_dir, 'invalid')
        if not os.path.isdir(self.__invalid_dir):
            sys.stderr.write('Can\'t find "invalid" directory\n')
            sys.exit(1)
        self.__out_dir = os.path.join(self.__test_dir, 'out_files')
        if os.path.isdir(self.__out_dir):
            pass
            shutil.rmtree(self.__out_dir)
        os.mkdir(self.__out_dir)


    def __test_good(self):
        paths = os.listdir(self.__good_dir)
        for path in paths:
            path = os.path.join(self.__good_dir, path)
            filename, ext = os.path.splitext(path)
            if ext != '.rtf':
                continue
            if os.path.isdir(path):
                continue
            new_filename = os.path.basename(path) + '.xml'
            out_path = os.path.join(self.__out_dir, new_filename)
            status, msg = self.__run_script(in_file = path, out_file = out_path)
            if status:
                info = [path, msg]
                self.__error.append(info)

    def __test_bad(self):
        paths = os.listdir(self.__invalid_dir)
        for path in paths:
            path = os.path.join(self.__invalid_dir, path)
            filename, ext = os.path.splitext(path)
            if ext != '.rtf':
                continue
            if os.path.isdir(path):
                continue
            new_filename = tempfile.mktemp()
            out_path = os.path.join(self.__out_dir, new_filename)
            status, msg = self.__run_script(in_file = path, out_file = out_path)
            if not status:
                info = [path, 'Should have produced an error']
                self.__error.append(info)
            try:
                os.remove(out_path)
            except OSError:
                pass
            

    def __validate(self):
        if not self.__msv_jar:
            return
        # print 'validating output ...\n\n'
        temp_path_list = os.listdir(self.__out_dir)
        path_list = []
        for path in temp_path_list:
            if os.path.isdir(path):
                continue
            filename, ext = os.path.splitext(path)
            if ext != '.xml':
                continue
            path_list.append(os.path.join(self.__out_dir, path))
        paths = ' '.join(path_list)
        rng = os.path.abspath(os.path.join(self.__script_dir, '..', 'relax' , 'rtf2xml1.0.rng'))
        command = 'java -jar %s -standalone  %s  %s' % (self.__msv_jar, rng, paths)
        exit_status, msg = commands.getstatusoutput(command)
        lines = msg.split('\n')
        for line in lines:
            if line[0:11] == 'validating ':
                continue
            if '-------' in line:
                continue
            if line.strip() == 'the document is valid.':
                continue
            if line.strip() == 'start parsing a grammar.':
                continue
            print line
        
    

    def __run_script(self, in_file, out_file):
        if self.__local:
            script_name = 'python '
            script_name += os.path.join(self.__script_dir, 'rtf2xml')
        else:
            script_name = 'rtf2xml'
        command = '%s --output %s %s' % (script_name, out_file,  in_file)
        exit_status, msg = commands.getstatusoutput(command)
        return exit_status, msg



if __name__ == '__main__':
    test_obj = Test()
