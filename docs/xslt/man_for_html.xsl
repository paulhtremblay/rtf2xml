<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.1" >
    <xsl:output method = "xml" doctype-system = "/home/paul/Documents/data/dtds/sdocbook.dtd"/>



    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>


    <xsl:template match = "emphasis[@role = 'short-option-bracket-before']|emphasis[@role = 'long-option-bracket-before']">
        <xsl:text> [ </xsl:text>
        <emphasis role = "option">
            <xsl:apply-templates/>
        </emphasis>
    </xsl:template>


    <xsl:template match = "emphasis[@role = 'long-option-bracket-after']">
        <emphasis role = "option">
            <xsl:apply-templates/>
        </emphasis>
        <xsl:text> ] </xsl:text>
    </xsl:template>


    <xsl:template match = "emphasis[@role = 'option-argument-bracket-after']">
        <emphasis role = "target">
            <xsl:apply-templates/>
        </emphasis>
        <xsl:text> ] </xsl:text>
    </xsl:template>

    <xsl:template match = "emphasis[@role = 'long-option-bracket-before-after']">
        <xsl:text> [ </xsl:text>
        <emphasis role = "option">
            <xsl:apply-templates/>
        </emphasis>
        <xsl:text> ] </xsl:text>
    </xsl:template>

    <xsl:template match = "emphasis[@role = 'long-option']">
        <emphasis role = "option">
            <xsl:apply-templates/>
        </emphasis>
    </xsl:template>


</xsl:stylesheet>
