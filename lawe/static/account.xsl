<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/account">
<html>
<head>
<link rel="stylesheet" type="text/css" href="/static/operations.css"/>
</head>
<body>
	Остаток: <xsl:value-of select="total"/>
	<p/>
	<table>
		<thead>
			<tr>
				<td class='date_field'>Дата</td>
				<td class='amount_field'>Приход</td>
				<td class='amount_field'>Расход</td>
				<td>Назначение</td>
				<td class='credit_field'>Корр счет</td>
			</tr>
		</thead>
		<tbody>
			<xsl:for-each select="operation">
			<tr>
				<td class='date_field'><xsl:value-of select="date"/></td>
				<td class='amount_field'><xsl:value-of select="income"/></td>
				<td class='amount_field'><xsl:value-of select="outcome"/></td>
				<td><xsl:value-of select="description"/></td>
				<td class='credit_field'><xsl:value-of select="other"/></td>
			</tr>
			</xsl:for-each>
		</tbody>
	</table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>

