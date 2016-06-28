<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.1" >
    <xsl:output method = "xml" doctype-system = "/home/paul/Documents/data/dtds/sdocbook.dtd"/>



    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match = "article">
        <article>
       <xsl:apply-templates/> 
        </article>
    </xsl:template>


    <!--

    <xsl:template match = "section[@id = 'options']|section[@id = 'command-line']|section[@id = 'description']">
       <xsl:apply-templates/> 
    </xsl:template>


    <xsl:template match = "section[@id = 'options']/title|
    section[@id = 'command-line']/title|
    section[@id = 'description']/title">
       <xsl:apply-templates/> 
    </xsl:template>

    -->

</xsl:stylesheet>
