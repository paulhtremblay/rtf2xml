<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.1" >


    <xsl:template match = "articleinfo">
        <toc>
        <xsl:apply-templates select = "/article/section" mode = "toc"/>
        </toc>
        <articleinfo>
        <xsl:apply-templates/>
        </articleinfo>
    </xsl:template>

    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match = "/article/section" mode = "toc">
        <xsl:element name = "toc-level1">
            <xsl:attribute name = "link">
                <xsl:value-of select = "@id"/>
            </xsl:attribute>
            <xsl:attribute name = "number">
                <xsl:value-of select = "@number"/>
            </xsl:attribute>
            <xsl:apply-templates select = "title" mode = "toc"/>
        </xsl:element>
        <xsl:apply-templates select = "section" mode = "toc"/>
    </xsl:template>

    <xsl:template match = "title" mode = "toc">
        <xsl:apply-templates/>
    </xsl:template>
    
    <!--special template for description-->
    <xsl:template match = "/article/section[@id = 'overview']" mode = "toc">
        <xsl:element name = "toc-level1">
            <xsl:attribute name = "link">
                <xsl:value-of select = "@id"/>
            </xsl:attribute>
            <xsl:attribute name = "number">
                <xsl:value-of select = "@number"/>
            </xsl:attribute>
            <xsl:text>Overview</xsl:text>
        </xsl:element>
        <xsl:apply-templates select = "section" mode = "toc"/>
    </xsl:template>

    <xsl:template match = "title" mode = "toc">
        <xsl:apply-templates/>
    </xsl:template>


    <xsl:template match = "section[@id = 'command-line']|
    section[@id = 'options']|
    section[@id = 'description']
    " 

    mode = "toc" 
    priority = "2"/>

    <xsl:template match = "/article/section/section" mode = "toc">
        <xsl:element name = "toc-level2">
            <xsl:attribute name = "link">
                <xsl:value-of select = "../@id"/>
            </xsl:attribute>
            <xsl:attribute name = "local-link">
                <xsl:value-of select = "@id"/>
            </xsl:attribute>
            <xsl:attribute name = "number">
                <xsl:value-of select = "../@number"/>
                <xsl:text>.</xsl:text>
                <xsl:value-of select = "@number"/>
            </xsl:attribute>
            <xsl:apply-templates select = "title" mode = "toc"/>
        </xsl:element>
        <xsl:apply-templates select = "section" mode = "toc"/>
    </xsl:template>
        
    <xsl:template match = "/article/section/section/section" mode = "toc">
        <xsl:element name = "toc-level3">
            <xsl:attribute name = "link">
                <xsl:value-of select = "../../@id"/>
            </xsl:attribute>
            <xsl:attribute name = "local-link">
                <xsl:value-of select = "@id"/>
            </xsl:attribute>
            <xsl:attribute name = "number">
                <xsl:value-of select = "../../@number"/>
                <xsl:text>.</xsl:text>
                <xsl:value-of select = "../@number"/>
                <xsl:text>.</xsl:text>
                <xsl:value-of select = "@number"/>
            </xsl:attribute>
            <xsl:apply-templates select = "title" mode = "toc"/>
        </xsl:element>
        <xsl:apply-templates select = "section" mode = "toc"/>
    </xsl:template>

    <!--
    <xsl:template match = "section" mode = "toc">
        <xsl:value-of select = "."/>
    </xsl:template>
    -->
    
</xsl:stylesheet>
