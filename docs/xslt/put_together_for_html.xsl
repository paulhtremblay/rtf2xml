<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.1" >
    <xsl:output method = "xml" doctype-system = "/home/paul/Documents/data/dtds/sdocbook.dtd"/>



    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>

    <xsl:template match = "input">
        <xsl:apply-templates select = "document('../xml/overview.xml')/article/section"/>
        <xsl:apply-templates select = "document('../xml/installation.xml')/article/section"/>
        <xsl:apply-templates select = "document('../xml/use.xml')/article/section"/>
        <xsl:apply-templates select = "document('../xml/man_page.xml')/article/section"/>
        <xsl:apply-templates select = "document('../xml/api.xml')/article/section"/>
    </xsl:template>

</xsl:stylesheet>
