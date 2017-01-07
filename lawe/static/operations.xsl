<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/operations">
<html>
<head>
</head>
<body>
	<form method='POST'>
		<input type='hidden' name='csrfmiddlewaretoken' value='{cqrf/input/@value}'/>
		<select name="debit_id">
			<xsl:for-each select="account">
				<option value='{id}'><xsl:value-of select='name'/></option>
			</xsl:for-each>
		</select>
		<select name="credit_id">
			<xsl:for-each select="account">
				<option value='{id}'><xsl:value-of select='name'/></option>
			</xsl:for-each>
		</select>
		<input type='number' name='amount'/>
		<input type='text' name='description'/>
		<input type='submit'/>
	</form>
	<table>
	<xsl:for-each select="operation">
		<tr>
			<td><xsl:value-of select="date"/></td>
			<td><xsl:value-of select="debit/name"/></td>
			<td><xsl:value-of select="credit/name"/></td>
			<td><xsl:value-of select="amount"/></td>
			<td><xsl:value-of select="description"/></td>
		</tr>
	</xsl:for-each>
	</table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
