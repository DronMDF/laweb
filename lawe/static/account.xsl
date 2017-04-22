<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:decimal-format name="Custom" grouping-separator=" "/>
<xsl:template match="/account">
<html>
<head>
<link rel="stylesheet" type="text/css" href="/static/operations.css"/>
</head>
<body>
	<p align='right'>
	<a href='/admin'>Управление</a><xsl:text>&#xa0;</xsl:text>
	<xsl:text>&#xa0;|&#xa0;</xsl:text>
	<xsl:value-of select='user/name'/><xsl:text>&#xa0;</xsl:text>
	<a href='/password_change/'>Сменить пароль</a><xsl:text>&#xa0;</xsl:text>
	<a href='/logout/'>Выйти</a>
	</p>

	<xsl:for-each select="total">
	Остаток: <xsl:value-of select="format-number(., '# ##0', 'Custom')"/>
	<xsl:text>&#xa0;</xsl:text>
	<xsl:choose>
		<xsl:when test="@unit='RUB'">Руб</xsl:when>
		<xsl:when test="@unit='KG'">Кг</xsl:when>
	</xsl:choose>
	<p/>
	</xsl:for-each>

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
				<td class='amount_field'>
					<xsl:choose>
						<xsl:when test="income='-'">
							-
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="format-number(income, '# ##0', 'Custom')"/>
							<xsl:text>&#xa0;</xsl:text>
							<xsl:choose>
								<xsl:when test="unit='RUB'">Руб</xsl:when>
								<xsl:when test="unit='KG'">Кг</xsl:when>
							</xsl:choose>
						</xsl:otherwise>
					</xsl:choose>
				</td>
				<td class='amount_field'>
					<xsl:choose>
						<xsl:when test="outcome='-'">
							-
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="format-number(outcome, '# ##0', 'Custom')"/>
							<xsl:text>&#xa0;</xsl:text>
							<xsl:choose>
								<xsl:when test="unit='RUB'">Руб</xsl:when>
								<xsl:when test="unit='KG'">Кг</xsl:when>
							</xsl:choose>
						</xsl:otherwise>
					</xsl:choose>
				</td>
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

