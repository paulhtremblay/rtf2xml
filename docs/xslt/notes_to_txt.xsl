
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method = "text"/>

    <xsl:template match="article">
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match = "author|title|abstract"/>

    <xsl:template match = "section/title">
        <xsl:value-of select = "translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
    </xsl:template>


    <xsl:template match = "revhistory/revision[last()]">
        <xsl:text>Version: </xsl:text>
        <xsl:value-of select = "revnumber"/>
        <xsl:text>&#xA;</xsl:text>
        <xsl:text>Date: </xsl:text>
        <xsl:value-of select = "date"/>
        <xsl:text>&#xA;</xsl:text>
    </xsl:template>

</xsl:stylesheet>

