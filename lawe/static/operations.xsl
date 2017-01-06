<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/operations">
<html>
<head>
</head>
<body>
	<form method='POST'>
		<select name="debit_id">
			<option value='a1'>Account1</option>
			<option value='a2'>Account2</option>
			<option value='a3'>Account3</option>
		</select>
		<select name="credit_id">
			<option value='a1'>Account1</option>
			<option value='a2'>Account2</option>
			<option value='a3'>Account3</option>
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
