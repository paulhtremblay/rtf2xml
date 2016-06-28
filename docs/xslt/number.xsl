<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.1">
    <xsl:output method = "xml"/>
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template> 

    <xsl:template match = "orderedlist">
        <orderedlist>
            <xsl:for-each select = "listitem">
                <xsl:element name = "listitem">
                    <xsl:attribute name = "number">
                        <xsl:number/>
                    </xsl:attribute>
                
                <xsl:apply-templates/>
                </xsl:element>
            </xsl:for-each>
        </orderedlist>
    </xsl:template>

    <xsl:template match = "section">
        <xsl:element name = "section">
            <xsl:attribute name = "number">
                <xsl:number/>
            </xsl:attribute>
            <xsl:attribute name = "id">
                <xsl:value-of select = "@id"/>
            </xsl:attribute>
            <xsl:apply-templates/>
        </xsl:element>
    </xsl:template>

</xsl:stylesheet>
