import sys, os, tempfile, commands




"""


"""


class XslConvert:

    def __init__(self, 
            processor, 
        ):

        """



        """
        self.__determine_processor(processor)



    def __determine_processor(self, processor):
        if processor == 'xsltproc':
            self.__processor = 'xsltproc'
        elif processor == 'xmllint':
            self.__processor = 'xmllint'
        elif processor == '4suite':
            self.__processor = '4suite'
        elif processor == 'xalan':
            self.__processor = 'xalan'
        elif processor == 'saxon':
            self.__processor = 'saxon'
        else:
            sys.stderr.write('%s not a valid processor choice\n' % processor)
            sys.exit(1)
    
    def transform(self, file, xsl_file, output, params = {}):
        """
        Requires:

            file -- the file to parse

            xsl_file --the xsl style sheet

        Returns:

            nothing

        Logic:

            Check for the existence of the files and the stylesheet. Determine
        the processor to be used, and let the othe methods do the processing.

        """

        if not (os.path.exists(file)):
            sys.stderr.write('module is xsl_convert\n')
            sys.stderr.write('method is transform\n')
            sys.stderr.write('"%s" does not exist\n' % file)
            sys.exit(1)
        if not (os.path.exists(xsl_file)):
            sys.stderr.write('"%s" does not exist\n' % xsl_file)
            sys.exit(1)

        if self.__processor == 'xmllint':
            exit_status, out_text = self.__transform_xmllint(file, xsl_file, output, params)
        elif self.__processor == 'xalan':
            exit_status, out_text = self.__transform_xalan(file, xsl_file, output, params)
        elif self.__processor == '4suite':
            exit_status, out_text = self.__transform_4suite(file, xsl_file, output, params)
        elif self.__processor == 'xsltproc':
            exit_status, out_text = self.__transform_xsltproc(file, xsl_file, output, params)
        elif self.__processor == 'saxon':
            exit_status, out_text = self.__transform_saxon(file, xsl_file, output, params)
        return exit_status, out_text

    def __transform_xmllint(self, file, xsl_file, output, params = {}):
        import libxml2
        import libxslt

        new_params = {}
        keys = params.keys()
        for key in keys:
            new_params[key] = '"%s"' % params[key]
        params = new_params
            


        try:
            xml_doc = file
            # parse stylesheet
            styledoc = libxml2.parseFile(xsl_file)
            style = libxslt.parseStylesheetDoc(styledoc)
            # parse doc
            doc = libxml2.parseFile(xml_doc)
            result = style.applyStylesheet(doc, params)
            style.saveResultToFilename(output, result, 0)
            style.freeStylesheet()
            doc.freeDoc()
            result.freeDoc()
        except libxml2.parserError:
            return 1, ''
        return 0, ''



    def __transform_4suite(self, file, xsl_file, output, params):

        import codecs
        from Ft.Xml import InputSource
        from Ft.Xml.Xslt.Processor import Processor

        document = InputSource.DefaultFactory.fromUri(file)
        stylesheet = InputSource.DefaultFactory.fromUri(xsl_file)
            # there's also a fromString() method

        processor = Processor()
        processor.appendStylesheet(stylesheet)  
        result = processor.run(document, topLevelParams=params)
        (utf8_encode, utf8_decode, utf8_reader, utf8_writer) = codecs.lookup("utf-8")
        write_obj = utf8_writer(open(output, 'w'))
        write_obj.write(result)
        write_obj.close()
        return result, ''

    def __transform_xalan(self, file, xsl_file, output, params):
        command = 'java org.apache.xalan.xslt.Process \
          -in %s -xsl %s -out %s' %  (file, xsl_file, output)
        
        param_string = ''
        keys = params.keys()
        for key in keys:
            param_string += ' %s "%s"' % (key, params[key])
            
        if param_string:
            command += ' -PARAM %s' % param_string
        # print command
        (exit_status, out_text) = commands.getstatusoutput(command)
        return exit_status, out_text

    def __transform_xsltproc(self, file, xsl_file, output, params = {}):
        command = 'xsltproc ' 
        
        param_string = ''
        keys = params.keys()
        for key in keys:
            param_string += ' %s "%s"' % (key, params[key])
            
        if param_string:
            command += ' --stringparam %s' % param_string

        command += ' -o %s %s %s' % (output, xsl_file, file)
        # sys.stdout.write('executing command "%s\n"' % command)
        (exit_status, out_text) = commands.getstatusoutput(command)
        return exit_status, out_text
        # os.system(command)

    def __transform_saxon(self, file, xsl_file, output, params):
        command = 'java  com.icl.saxon.StyleSheet -o %s %s %s'   %\
            (output, file, xsl_file)
        keys = params.keys()
        param_string = ''
        for key in keys:
            param_string += ' %s=%s ' % (key, param[key])
        if param_string:
            command += param_string
        (exit_status, out_text) = commands.getstatusoutput(command)
        return exit_status, out_text

        
if __name__ == '__main__':
    test_xml_dir = '/home/paul/lib/python/xml_tools_trem/test_files/xml_files'
    test_xsl_dir = '/home/paul/lib/python/xml_tools_trem/test_files/xsl_stylesheets'
    output_dir = '/home/paul/paultemp'

    file = 'simple.xml'
    xsl_file = 'simple1.xsl'
    output = 'output.xml'


    test_file = os.path.join(test_xml_dir, file)
    test_xsl = os.path.join(test_xsl_dir, xsl_file)
    test_output = os.path.join(output_dir, output)

    test_obj = XslConvert('xalan')
    test_obj.transform (test_file, test_xsl, test_output, params = {'test-param': 'changed in xalan'})
