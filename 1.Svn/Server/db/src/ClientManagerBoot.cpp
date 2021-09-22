//Find
	if (!InitializeShopTable())
	{
		...
	}

///Add
#if defined(__BL_MAILBOX__)
	if (!InitializeMailBoxTable())
	{
		sys_err("InitializeMailBoxTable FAILED");
		return false;
	}
#endif

//Find
bool CClientManager::InitializeBanwordTable()
{
	...
}

///Add
#if defined(__BL_MAILBOX__)
bool CClientManager::InitializeMailBoxTable()
{
	if (m_map_mailbox.empty() == false)
		return true;

	char s_szQuery[512];
#if defined(__BL_TRANSMUTATION__)
	int len = sprintf(s_szQuery, "SELECT name, who, title, message, gm, confirm, send_time, delete_time, gold, won, ivnum, transmutation, icount, ");
#else
	int len = sprintf(s_szQuery, "SELECT name, who, title, message, gm, confirm, send_time, delete_time, gold, won, ivnum, icount, ");
#endif

	for (BYTE i = 0; i < ITEM_SOCKET_MAX_NUM; i++)
		len += sprintf(s_szQuery + len, "socket%d, ", i);

	for (BYTE i = 0; i < ITEM_ATTRIBUTE_MAX_NUM; i++) {
		len += sprintf(s_szQuery + len, "attrtype%d, attrvalue%d ", i, i);
		if (i != ITEM_ATTRIBUTE_MAX_NUM - 1)
			len += sprintf(s_szQuery + len, ", ");
	}

	len += sprintf(s_szQuery + len, "FROM mailbox%s", GetTablePostfix());

	std::unique_ptr<SQLMsg> pkMsg(CDBManager::instance().DirectQuery(s_szQuery));
	
	const SQLResult* pRes = pkMsg->Get();

	if (!pRes->uiNumRows)
		return true;

	MYSQL_ROW data;
	while ((data = mysql_fetch_row(pRes->pSQLResult)))
	{
		uint8_t col = 0;
		SMailBoxTable mail;

		auto name = data[col++];
		mail.bIsDeleted = false;
		mail.AddData.bHeader = 0;
		mail.AddData.Index = 0;
		std::memcpy(mail.szName, name, sizeof(mail.szName));
		std::memcpy(mail.AddData.szFrom, data[col++], sizeof(mail.AddData.szFrom));
		std::memcpy(mail.Message.szTitle, data[col++], sizeof(mail.Message.szTitle));
		std::memcpy(mail.AddData.szMessage, data[col++], sizeof(mail.AddData.szMessage));
		str_to_number(mail.Message.bIsGMPost, data[col++]);
		str_to_number(mail.Message.bIsConfirm, data[col++]);
		str_to_number(mail.Message.SendTime, data[col++]);
		str_to_number(mail.Message.DeleteTime, data[col++]);
		str_to_number(mail.AddData.iYang, data[col++]);
		str_to_number(mail.AddData.iWon, data[col++]);
		str_to_number(mail.AddData.ItemVnum, data[col++]);
#if defined(__BL_TRANSMUTATION__)
		str_to_number(mail.AddData.dwTransmutationVnum, data[col++]);
#endif
		str_to_number(mail.AddData.ItemCount, data[col++]);
		mail.Message.bIsItemExist = mail.AddData.ItemVnum > 0 || mail.AddData.iYang > 0 || mail.AddData.iWon > 0;

		for (BYTE i = 0; i < ITEM_SOCKET_MAX_NUM; i++)
			str_to_number(mail.AddData.alSockets[i], data[col++]);

		for (BYTE i = 0; i < ITEM_ATTRIBUTE_MAX_NUM; i++) {
			str_to_number(mail.AddData.aAttr[i].bType, data[col++]);
			str_to_number(mail.AddData.aAttr[i].sValue, data[col++]);
		}

		m_map_mailbox[name].emplace_back(mail);
	}

	return true;
}
#endif