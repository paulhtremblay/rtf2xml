<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    xmlns:block = "http://xml2txt.sourceforge.net"
    version="1.0">
    <xsl:output method = "xml"/>

    <xsl:template match="article">
        <doc>
        <xsl:apply-templates/>
        </doc>
    </xsl:template>

    <xsl:template match = "author|title|abstract|revhistory/revision"/>

    <xsl:template match = "section/title">
        <block>
        <xsl:value-of select = "translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
        </block>
    </xsl:template>


    <xsl:template match = "revhistory/revision[last()]">
        <block>
        <xsl:text>Version: </xsl:text>
        <xsl:value-of select = "revnumber"/>
        </block>
        <block>
        <xsl:text>Date: </xsl:text>
        <xsl:value-of select = "date"/>
        </block>
    </xsl:template>



    <xsl:template match = "para">
        <block>
            <xsl:apply-templates/>
        </block>
    </xsl:template>

</xsl:stylesheet>

