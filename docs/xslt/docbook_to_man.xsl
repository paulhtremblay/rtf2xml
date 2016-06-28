<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.1" >
    <xsl:variable name = "script-name">rtf2xml</xsl:variable>

    <xsl:output method = "xml" doctype-system = "/home/paul/Documents/data/dtds/block_text.dtd"/>
    
    <xsl:template match = "article">
        <doc>
            <block new-lines-after = "1">
                <xsl:text>.\" @(#)rtf2xml .4 2003/10/1&#x00A;</xsl:text>
            </block>
            <block new-lines-after = "1">
                <xsl:text>.\" Copyright (c) 2003 - Paul H Tremblay&#x00A;</xsl:text>
            </block>
            <xsl:apply-templates select = "articleinfo"/>
            <xsl:apply-templates select = "section[@id = 'man-page']"/>
            <!--
            <xsl:apply-templates select = "section[@id = 'use-examples']"/>
            -->
            <xsl:call-template name = "author"/>
            <xsl:apply-templates select = "section[@id = 'copyright']"/>

        </doc>
    </xsl:template>

    <xsl:template match = "articleinfo">
        <block new-lines-after = "1">
        <xsl:text>.TH </xsl:text>
            <xsl:value-of select = "title"/>
        </block>
        <block>
            <xsl:text>.SH NAME </xsl:text>
            <xsl:value-of select = "$script-name"/>
        </block>
            <xsl:apply-templates select = "abstract/para"/>
        <block>
            <xsl:text>.SH SYNOPSIS </xsl:text>
        </block>
        <xsl:apply-templates select = "/article/section/para[@role = 'command-line-verbose']" mode = "synopsis"/>
        <!--
        <xsl:apply-templates select = "/article/section[@id = 'overview']"/>
        -->
    </xsl:template>

    <xsl:template match = "abstract/para">
        <block new-lines-after = "1">
            .SP 1i
        </block>
        <block>
            <xsl:apply-templates/>
        </block>
    </xsl:template>

    <xsl:template match = "author/firstname" >
    </xsl:template>
    <xsl:template match = "author/surname" >
    </xsl:template>
    <xsl:template match = "articleinfo/title" >
    </xsl:template>

    <xsl:template match = "/article/section/para[@role = 'command-line-verbose']" mode = "synopsis">
        <xsl:apply-templates/>
    </xsl:template>
    
    <!--delete this so it doesn't get copied twice-->
    <xsl:template match = "/article/section/para[@role = 'command-line-verbose']" />

    <!--all options for synopsis-->
    


    <xsl:template match = "emphasis[@role = 'command']">
        <block new-lines-after = "1" new-lines-before = "2">
            <xsl:text>.B </xsl:text>
            <xsl:apply-templates/>
        </block>
    </xsl:template>


    <xsl:template match = "emphasis[@role = 'long-option']|emphasis[@role= 'short-option']">
        <block new-lines-after = "1">
            <xsl:text>.B </xsl:text>
            <xsl:apply-templates/>
        </block>
    </xsl:template>


    <xsl:template match = "emphasis[@role = 'long-option-bracket-before-after']">
        <block new-lines-after = "1">
            <xsl:text>[</xsl:text>
        </block>
        <block new-lines-after = "1">
            <xsl:text>.B </xsl:text>
            <xsl:apply-templates/>
        </block>
        <block new-lines-after = "1">
            <xsl:text>]</xsl:text>
        </block>
    </xsl:template>


    <xsl:template match = "emphasis[@role = 'long-option-bracket-after']">
        <block new-lines-after = "1">
            <xsl:text>.B </xsl:text>
            <xsl:apply-templates/>
        </block>
        <block new-lines-after = "1">
            <xsl:text>]</xsl:text>
        </block>
    </xsl:template>

    <xsl:template match = "emphasis[@role = 'option-argument-bracket-after']">
        <block new-lines-after = "1">
            <xsl:text>.I </xsl:text>
            <xsl:apply-templates/>
        </block>
        <block new-lines-after = "1">
            <xsl:text>]</xsl:text>
        </block>
    </xsl:template>

    <xsl:template match = "emphasis[@role = 'short-option-bracket-before']|emphasis[@role = 'long-option-bracket-before']">
        <block new-lines-after = "1">
            <xsl:text>[</xsl:text>
        </block>
        <block new-lines-after = "1">
            <xsl:text>.B </xsl:text>
            <xsl:apply-templates/>
        </block>
    </xsl:template>

    <xsl:template match = "emphasis[@role = 'option-argument']">
        <block new-lines-after = "1">
            <xsl:text>.I </xsl:text>
            <xsl:apply-templates/>
        </block>
    </xsl:template>

    <xsl:template match = "emphasis[@role = 'arguments']">
        <block new-lines-after = "1">
            <xsl:text>.B </xsl:text>
        </block>
        <block new-lines-after = "1">
            <xsl:apply-templates/>
        </block>
        <block>
            <xsl:text>.sp </xsl:text>
        </block>
    </xsl:template>

    <xsl:template match = "emphasis[@role = 'or']">
        <block new-lines-after = "1">
            <xsl:text>\||\|</xsl:text>
        </block>
    </xsl:template>
    <!--end all options for synopsis-->


    <!--overviw-->

    <xsl:template match = "section[@id = 'options']">
        <block new-lines-after = "1">
            <xsl:text>.sp</xsl:text>
        </block>
        <block new-lines-after = "1">
            <xsl:text>.SH OPTIONS</xsl:text>
        </block>
            <xsl:apply-templates/>
        <block new-lines-after = "1">
            <xsl:text>.sp </xsl:text>
        </block>
    </xsl:template>


    <xsl:template match = "section[@id = 'description']">
        <block new-lines-after = "1">
            <xsl:text>.sp</xsl:text>
        </block>
        <block new-lines-after = "1">
            <xsl:text>.SH DESCRIPTION</xsl:text>
        </block>
        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match = "section[@id = 'overview']/title"/>
    <xsl:template match = "section[@id = 'man-page']/title"/>
    <xsl:template match = "section/title"/>





    <!--use-->


    <xsl:template match = "section[@id = 'options']/para[@role = 'option']">
        <!--
        <xsl:apply-templates select = "option" mode = "use"/>
        -->
        <block>
            <xsl:apply-templates/>
        </block>
    </xsl:template>


    <!--
    <xsl:template match = "section[@id = 'options']/para[@role = 'option']/option" mode = "use">
        <block new-lines-after = "0">
            <xsl:text>.B \ </xsl:text>
        </block>
        <block new-lines-after = "1">
            <xsl:apply-templates/>
        </block>
    </xsl:template>
    -->

    <xsl:template match = "option">
            <xsl:text>\fB</xsl:text>
            <xsl:apply-templates/>
            <xsl:text>\fR</xsl:text>
    </xsl:template>

    <xsl:template match = "emphasis[@role = 'target']">
            <xsl:text>\fI</xsl:text>
            <xsl:apply-templates/>
            <xsl:text>\fR</xsl:text>
    
    </xsl:template>

    <xsl:template match = "phrase[@role = 'term']">
        <block new-lines-after = "1">
            <xsl:text>.in 40p</xsl:text>
        </block>
        <block>
        <xsl:text>
            .sp
        </xsl:text> 
        </block>
        <xsl:apply-templates/>
        <block new-lines-after = "1">
            <xsl:text>.in 70p</xsl:text>
        </block>
        
    </xsl:template>
    
     
    <xsl:template match = "para[@role = 'option']">
        <block new-lines-after = "1">
            <xsl:text>.in 40p</xsl:text>
        </block>
        <block>
        <xsl:text>
            .sp
        </xsl:text> 
        </block>
        <block>
        <xsl:apply-templates/>
        </block>
        <block new-lines-after = "1">
            <xsl:text>.in 70p</xsl:text>
        </block>
        
    </xsl:template>

    <!--
    <xsl:template match = "para[@role = 'option']">
        <block>
            <xsl:apply-templates/>
        </block>
    </xsl:template>
    -->



    <!--default paragraph-->
    <xsl:template match = "para" priority = "0">
        <block new-lines-after = "1">
            <xsl:text>.sp </xsl:text>
        </block>
        <block>
            <xsl:apply-templates/>
        </block>
    </xsl:template>

    <xsl:template match = "para[@role = 'line']">
        <block new-lines-after = "1">
            <xsl:text>.sp </xsl:text>
        </block>
        <block new-lines-after = "1">
            <xsl:text>.in +.3in </xsl:text>
        </block>
        <block>
            <xsl:apply-templates/>
        </block>
        <block new-lines-after = "1">
            <xsl:text>.in -.3in </xsl:text>
        </block>
    </xsl:template>

    <xsl:template match = "section[@id = 'copyright']">
        <block new-lines-after = "1">
            <xsl:text>.SH COPYRIGHT</xsl:text>
        </block>
        <xsl:apply-templates/>
    </xsl:template>


    <xsl:template match = "section[@id = 'copyright']/title"/>

    <xsl:template name = "author">
        <block new-lines-after = "1">
            <xsl:text>.SH AUTHOR</xsl:text>
        </block>
        <block>
            <xsl:value-of select = "/article/articleinfo/author/firstname"/>
            <xsl:text> </xsl:text>
            <xsl:value-of select = "/article/articleinfo/author/surname"/>
        </block>
            <xsl:apply-templates select = "/article/articleinfo/author/authorblurb/para[@role = 'email']"/>
    </xsl:template>
<!--


 <xsl:when test = "preceding-sibling::*[1]/self:: transition">
-->


</xsl:stylesheet>


 
