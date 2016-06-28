<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.1" >
    <xsl:variable name = "script-name">trem_backup</xsl:variable>

    <xsl:output method = "xml" indent = "yes" 
            doctype-system = "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
            doctype-public = "-//W3C//DTD XHTML 1.0 Strict//EN"
            />

    <xsl:template match = "article">

        <html>
            <head>
                <link rel= "stylesheet" type = "text/css" href = "styles.css"/>
                <title>rtf2xml</title>
            </head>
            <body>
                <div class = "root">
                <h1 id = "intro">
                    Documentation for rtf2xml
                </h1>
                <xsl:apply-templates select = "/article/toc" mode = "toc"/>
                </div>
            </body>
        </html>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match = "/article/toc" mode = "toc">
        <h2 id = "toc">Table Of Contents</h2>
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match = "/article/toc" />

    <xsl:template match = "article/articleinfo"/>
    
    <!--Make a page for each main section-->
    <xsl:template match = "/article/section">
        <xsl:document href = "../html/{@id}.html" method = "xml"
            doctype-system = "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"
            doctype-public = "-//W3C//DTD XHTML 1.0 Strict//EN"
            >
            <html>
                <head>
                    <link rel= "stylesheet" type = "text/css" href = "styles.css"/>
                    <title>
                        <xsl:value-of select = "title"/>
                    </title>
                </head>
                <body>
                    <div class = "root">
                    <p class = "home-link">
                        <a href = "index.html">HOME</a>
                    </p>
                    <xsl:apply-templates/>
                    <p class = "home-link">
                        <a href = "index.html">HOME</a>
                    </p>
                    </div>
                </body>
            </html>
        </xsl:document>



    </xsl:template>
    <xsl:template match = "toc-level1">
        <p class = "toc-level1">
            <xsl:element name = "a">
                <xsl:attribute name = "href">
                    <xsl:value-of select = "@link"/>
                    <xsl:text>.html</xsl:text>
                </xsl:attribute>
                <xsl:value-of select = "@number"/>
                <xsl:text> </xsl:text>
                <xsl:apply-templates/>
            </xsl:element>
        </p>
    </xsl:template>


    <xsl:template match = "toc-level2">
        <p class = "toc-level2">
            <xsl:element name = "a">
                <xsl:attribute name = "href">
                    <xsl:value-of select = "@link"/>
                    <xsl:text>.html#</xsl:text>
                    <xsl:value-of select = "@local-link"/>
                </xsl:attribute>
                <xsl:value-of select = "@number"/>
                <xsl:text> </xsl:text>
                <xsl:apply-templates/>
            </xsl:element>
        </p>
    </xsl:template>



    <xsl:template match = "toc-level3">
        <p class = "toc-level3">
            <xsl:element name = "a">
                <xsl:attribute name = "href">
                    <xsl:value-of select = "@link"/>
                    <xsl:text>.html#</xsl:text>
                    <xsl:value-of select = "@local-link"/>
                </xsl:attribute>
                <xsl:value-of select = "@number"/>
                <xsl:text> </xsl:text>
                <xsl:apply-templates/>
            </xsl:element>
        </p>
    </xsl:template>

    <xsl:template match = "para">
        <p>
        <xsl:apply-templates/>
        </p>
    </xsl:template>

    <xsl:template match = "para[@role='code']">
        <pre>
            <xsl:apply-templates/>
        </pre>
    </xsl:template>


    <xsl:template match = "para[@role='code'][@id='interface-code']">
       <p>
           <a href="python_example.py">python_example.py</a>
       </p>
        <pre>
            <xsl:apply-templates/>
        </pre>
    </xsl:template>

    <xsl:template match="subtitle">
        <h3>
            <xsl:apply-templates/>
        </h3>
    </xsl:template>

    <xsl:template match = "article/section/section|article/section/section/section">
        <xsl:element name = "div">
            <xsl:attribute name = "id">
                <xsl:value-of select = "@id"/>
            </xsl:attribute>
            <xsl:element name = "a">
                <xsl:attribute name = "name">
                    <xsl:value-of select = "@id"/>
                </xsl:attribute>
            </xsl:element>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match = "/article/section/title">
        <h1 class = "section">
            <xsl:apply-templates/>
        </h1>
    </xsl:template>


    <xsl:template match = "/article/section/section/title">
        <h2 class = "sub-section">
            <xsl:apply-templates/>
        </h2>
    </xsl:template>

    <xsl:template match = "/article/section/section/section/title">
        <h3 class = "sub-sub-section">
            <xsl:apply-templates/>
        </h3>
    </xsl:template>


    <!--requirements
    <xsl:template match = "/article/section/section[@id ='requirements']/title" 
    priority = "2">
        <h2>Step by Step:</h2>
        <h2 class = "sub-section">
            <xsl:apply-templates/>
        </h2>
    </xsl:template>
    
    <xsl:template match = "/article/section/section/section/title">
        <h3 class = "sub-sub-section">
            <xsl:apply-templates/>
        </h3>
    </xsl:template>
-->

    <!--orderedlist to ol-->
    <xsl:template match = "orderedlist">
        <ol>
            <xsl:apply-templates/>
        </ol>
    </xsl:template>


    <!--itemizedlist to ul-->
    <xsl:template match = "itemizedlist">
        <ul>
            <xsl:apply-templates/>
        </ul>
    </xsl:template>


    <!--listitem to li-->
    <xsl:template match = "listitem">
        <xsl:text>
            
        </xsl:text>

        <li>
            <xsl:apply-templates/>
        </li>
    </xsl:template>

    <!--
    <xsl:template match = "phrase[@role= 'term']">
        <xsl:element name = "div">
            <xsl:attribute name = "class">
                <xsl:text>option-term</xsl:text>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>
    -->

    <xsl:template match = "option">
        <b class = "option">
            <xsl:apply-templates/>
        </b>
    </xsl:template>


    <xsl:template match = "emphasis[@role = 'option']">
        <b class = "option">
            <xsl:apply-templates/>
        </b>
    </xsl:template>

    <xsl:template match = "emphasis[@role = 'target']">
        <b class = "target">
            <xsl:apply-templates/>
        </b>
    </xsl:template>

    <xsl:template match = "para[@role = 'option']">
        <p class = "option">
            <xsl:apply-templates/>
        </p>
    </xsl:template>

    <xsl:template match = "para[@role = 'literal']">
        <pre >
            <xsl:apply-templates/>
        </pre>
    </xsl:template>

    <xsl:template match = "ulink">
        <xsl:element name = "a">
            <xsl:attribute name = "href">
                <xsl:value-of select = "@url"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

    <xsl:template match = "command">
        <code>
            <xsl:apply-templates/>
        </code>
    </xsl:template>


    <xsl:template match = "computeroutput">
        <pre>
            <xsl:apply-templates/>
        </pre>
    </xsl:template>

    <xsl:template match = "emphasis[@role = 'bold']">
        <b>
            <xsl:apply-templates/>
        </b>
    </xsl:template>

    <xsl:template match = "emphasis">
        <i>
            <xsl:apply-templates/>
        </i>
    </xsl:template>
</xsl:stylesheet>
