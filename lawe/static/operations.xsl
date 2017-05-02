<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:decimal-format name="Custom" grouping-separator=" "/>

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
				<td class='date_field'>
					<select name="date" style='width: 100%;'>
						<xsl:for-each select="date">
							<xsl:choose>
								<xsl:when test='@id=0'>
									<option value='{@id}' selected='selected'>
										<xsl:value-of select='.'/>
									</option>
								</xsl:when>
								<xsl:otherwise>
									<option value='{@id}'>
										<xsl:value-of select='.'/>
									</option>
								</xsl:otherwise>
							</xsl:choose>
						</xsl:for-each>
					</select>
				</td>
				<td class='debit_field'>
					<select name="debit_id" style='width: 100%;'>
						<xsl:for-each select="account[not(@hidden)]">
							<xsl:sort select="name"/>
							<option value='{id}'>
								<xsl:value-of select='name'/>
							</option>
						</xsl:for-each>
					</select>
				</td>
				<td class='credit_field'>
					<select name="credit_id" style='width: 100%;'>
						<xsl:for-each select="account[not(@hidden)]">
							<xsl:sort select="name"/>
							<option value='{id}'>
								<xsl:value-of select='name'/>
							</option>
						</xsl:for-each>
					</select>
				</td>
				<td class='amount_field'>
					<input type='text' style='width: 55%;' name='amount'/>
					<select name='unit' style='width: 35%;'>
						<option value='RUB'>руб</option>
						<option value='KG'>кг</option>
					</select>
				</td>
				<td>
					<input type='text' style='width: 90%;' name='description'/>
					<input type='submit' style='width: 10%;' value='Добавить'/>
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
				<!--
				@todo #88:15min Если счет не доступен для пользователя, не должно стоять ссылки.
				 В этом случае мы должны только показывать название без возможности перехода
				-->
				<td class='debit_field'>
					<a href='account/{debit_id}'>
						<xsl:variable name='debit_id' select='number(debit_id)'/>
						<xsl:value-of select='//account[number(id) = $debit_id]/name'/>
					</a>
				</td>
				<td class='credit_field'>
					<a href='account/{credit_id}'>
						<xsl:variable name='credit_id' select='number(credit_id)'/>
						<xsl:value-of select='//account[number(id) = $credit_id]/name'/>
					</a>
				</td>
				<td class='amount_field'>
					<xsl:value-of select="format-number(amount, '# ##0', 'Custom')"/>
					<xsl:text>&#xa0;</xsl:text>
					<xsl:choose>
						<xsl:when test="unit='RUB'">руб</xsl:when>
						<xsl:when test="unit='KG'">кг</xsl:when>
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
