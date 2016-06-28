#!/usr/bin/env python
import sys
import rtf2xml.ParseRtf


def Handle_Main():
    """Handles options and creates a parse object """
    
    try:
        parse_obj =rtf2xml.ParseRtf.ParseRtf(   
            in_file = 'in.rtf', 

            # these are optional

            # determine the output file
            out_file = 'out.xml',

            # determine the run level. The default is 1.
            run_level = 3,

            # The name of a debug directory, if you are running at
            # run level 3 or higer.
            debug = 'debug_dir',

            # Convert symbol fonts to unicode equivelents. Default
            # is 1
            convert_symbol = 1,

            # Convert Zapf fonts to unicode equivelents. Default
            # is 1.
            convert_zapf = 1,

            # Convert Wingding fonts to unicode equivelents.
            # Default is 1.
            convert_wingdings = 1,

            # Convert RTF caps to real caps.
            # Default is 1.
            convert_caps = 1,

            # Indent resulting XML.
            # Default is 0 (no indent).
            indent = 1,

            # Form lists from RTF. Default is 1.
            form_lists = 1,

            # Convert headings to sections. Default is 0.
            headings_to_sections = 1,

            # Group paragraphs with the same style name. Default is 1.
            group_styles = 1,

            # Group borders. Default is 1.
            group_borders = 1,

            # Write or do not write paragraphs. Default is 0.
            empty_paragraphs = 0,
    ) 

        parse_obj.parse_rtf()

    except rtf2xml.ParseRtf.InvalidRtfException, msg:
        sys.stderr.write(str(msg))
        sys.exit(1)
    except rtf2xml.ParseRtf.RtfInvalidCodeException, msg:
        sys.stderr.write(str(msg))
        sys.exit(1)

if __name__=='__main__':
    Handle_Main()

