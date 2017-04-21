<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/operations">
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

	<form method='POST'>
		<input type='hidden' name='csrfmiddlewaretoken' value='{cqrf/input/@value}'/>
		<table>
		<tr>
		<td class='date_field'></td>
		<td class='debit_field'>
		<select name="debit_id">
			<xsl:for-each select="account">
				<option value='{id}'><xsl:value-of select='name'/></option>
			</xsl:for-each>
		</select>
		</td>
		<td class='credit_field'>
		<select name="credit_id">
			<xsl:for-each select="account">
				<option value='{id}'><xsl:value-of select='name'/></option>
			</xsl:for-each>
		</select>
		</td>
		<td class='amount_field'>
		<input type='text' size='5' name='amount'/>
		<select name='unit'>
			<option value='RUB'>Руб</option>
			<option value='KG'>Кг</option>
		</select>
		</td>
		<td>
		<input type='text' name='description'/>
		<input type='submit'/>
		</td>
		</tr>
		</table>
	</form>
	<table>
		<thead>
			<tr>
				<td class='date_field'>Дата</td>
				<td class='debit_field'>Дебет</td>
				<td class='credit_field'>Кредит</td>
				<td class='amount_field'>Сумма</td>
				<td>Назначение</td>
			</tr>
		</thead>
		<tbody>
			<xsl:for-each select="operation">
			<tr>
				<td class='date_field'><xsl:value-of select="date"/></td>
				<td class='debit_field'><a href='account/{debit/id}'><xsl:value-of select="debit/name"/></a></td>
				<td class='credit_field'><a href='account/{credit/id}'><xsl:value-of select="credit/name"/></a></td>
				<td class='amount_field'>
					<xsl:value-of select="amount"/>
					<xsl:choose>
						<xsl:when test="unit='RUB'">Руб</xsl:when>
						<xsl:when test="unit='KG'">Кг</xsl:when>
						<xsl:otherwise>???</xsl:otherwise>
					</xsl:choose>
				</td>
				<td><xsl:value-of select="description"/></td>
			</tr>
			</xsl:for-each>
		</tbody>
	</table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
