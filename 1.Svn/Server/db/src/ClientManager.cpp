//Find
	m_iCacheFlushCountLimit(200)

///Add
#if defined(__BL_MAILBOX__)
	, m_iMailBoxBackupSec(3600)
#endif

//Find
	if (!CConfig::instance().GetValue("PLAYER_DELETE_LEVEL_LIMIT_LOWER", &m_iPlayerDeleteLevelLimitLower))
	{
		m_iPlayerDeleteLevelLimitLower = 0;
	}

///Add
#if defined(__BL_MAILBOX__)
	CConfig::instance().GetValue("MAILBOX_BACKUP_SEC", &m_iMailBoxBackupSec);
#endif

//Find
	sys_log(0, "MainLoop exited, Starting cache flushing");

///Add
#if defined(__BL_MAILBOX__)
	CClientManager::instance().MAILBOX_BACKUP();
#endif

//Find
void CClientManager::QUERY_PLAYER_COUNT(CPeer * pkPeer, TPlayerCountPacket * pPacket)
{
	...
}

///Add
#if defined(__BL_MAILBOX__)
void CClientManager::QUERY_MAILBOX_LOAD(CPeer* pkPeer, DWORD dwHandle, TMailBox* p)
{
	if (g_log)
		sys_log(0, "QUERY_MAILBOX (handle: %d ch: %s)", dwHandle, p->szName);
	
	std::vector<SMailBoxTable>* vec = nullptr;
	auto it = m_map_mailbox.find(p->szName);
	if (it != m_map_mailbox.end())
		vec = &it->second;

	if (vec)
	{
		const time_t now = time(nullptr);

		vec->erase(std::remove_if(vec->begin(), vec->end(),
				[now](const TMailBoxTable& mail) { return mail.bIsDeleted || difftime(mail.Message.DeleteTime, now) <= 0; }), vec->end());

		std::sort(vec->begin(), vec->end(), [](const TMailBoxTable& l, const TMailBoxTable& r) {
			return l.Message.SendTime > r.Message.SendTime;
			});
	}

	const WORD size = vec ? static_cast<WORD>(vec->size()) : 0;
	const DWORD dwPacketSize = sizeof(WORD) + sizeof(WORD) + sizeof(SMailBoxTable) * size;

	pkPeer->EncodeHeader(HEADER_DG_RESPOND_MAILBOX_LOAD, dwHandle, dwPacketSize);
	pkPeer->EncodeWORD(sizeof(SMailBoxTable));
	pkPeer->EncodeWORD(size);

	if (vec && vec->empty() == false)
		pkPeer->Encode(&(*vec)[0], sizeof(SMailBoxTable) * size);
}

void CClientManager::QUERY_MAILBOX_CHECK_NAME(CPeer* pkPeer, DWORD dwHandle, TMailBox* p)
{
	TMailBox t;
	std::memcpy(t.szName, "", sizeof(t.szName));
	t.Index = 0; // Index: Mail Count
	
	static std::unordered_set<std::string> NameSet;
	bool bFound = NameSet.find(p->szName) != NameSet.end();
	
	if (bFound == false)
	{
		char s_szQuery[128];
		snprintf(s_szQuery, sizeof(s_szQuery), "SELECT * FROM player%s WHERE name='%s' LIMIT 1", GetTablePostfix(), p->szName);
		std::unique_ptr<SQLMsg> pMsg(CDBManager::instance().DirectQuery(s_szQuery));
		bFound = pMsg->Get()->uiNumRows > 0;
	}

	if (bFound)
	{
		NameSet.emplace(p->szName); // player exists, next time we will use this to avoid using mysql.
		std::memcpy(t.szName, p->szName, sizeof(t.szName));
		auto it = m_map_mailbox.find(p->szName);
		if (it != m_map_mailbox.end())
		{
			const time_t now = time(nullptr);
			for (const SMailBoxTable& mail : it->second)
			{
				if (mail.bIsDeleted)
					continue;

				if (difftime(mail.Message.DeleteTime, now) <= 0)
					continue;

				t.Index++;
			}
		}
	}

	pkPeer->EncodeHeader(HEADER_DG_RESPOND_MAILBOX_CHECK_NAME, dwHandle, sizeof(TMailBox));
	pkPeer->Encode(&t, sizeof(TMailBox));
}

void CClientManager::QUERY_MAILBOX_WRITE(CPeer* pkPeer, DWORD dwHandle, TMailBoxTable* p)
{
	m_map_mailbox[p->szName].emplace_back(*p);
}

bool CClientManager::GET_MAIL(const char* name, const BYTE index, SMailBoxTable** mail)
{
	auto it = m_map_mailbox.find(name);
	if (it == m_map_mailbox.end())
		return false;

	MailVec& mailvec = it->second;
	if (index >= mailvec.size())
		return false;

	*mail = &mailvec.at(index);
	return true;
}

void CClientManager::QUERY_MAILBOX_DELETE(CPeer* pkPeer, DWORD dwHandle, TMailBox* p)
{
	SMailBoxTable* mail = nullptr;
	if (GET_MAIL(p->szName, p->Index, &mail) == false)
		return;

	mail->bIsDeleted = true;
}

void CClientManager::QUERY_MAILBOX_CONFIRM(CPeer* pkPeer, DWORD dwHandle, TMailBox* p)
{
	SMailBoxTable* mail = nullptr;
	if (GET_MAIL(p->szName, p->Index, &mail) == false)
		return;

	mail->Message.bIsConfirm = true;
}

void CClientManager::QUERY_MAILBOX_GET(CPeer* pkPeer, DWORD dwHandle, TMailBox* p)
{
	SMailBoxTable* mail = nullptr;
	if (GET_MAIL(p->szName, p->Index, &mail) == false)
		return;

	mail->AddData.iYang = 0;
	mail->AddData.iWon = 0;
	mail->Message.bIsItemExist = false;
	mail->Message.bIsConfirm = true;
	mail->AddData.ItemVnum = 0;
	mail->AddData.ItemCount = 0;
	memset(mail->AddData.alSockets, 0, sizeof(mail->AddData.alSockets));
	memset(mail->AddData.aAttr, 0, sizeof(mail->AddData.aAttr));
#if defined(__BL_TRANSMUTATION__)
	mail->AddData.dwTransmutationVnum = 0;
#endif
}

void CClientManager::QUERY_MAILBOX_UNREAD(CPeer* pkPeer, DWORD dwHandle, TMailBox* p)
{
	auto it = m_map_mailbox.find(p->szName);
	if (it == m_map_mailbox.end())
		return;

	const MailVec& mailvec = it->second;
	if (mailvec.empty())
		return;
	
	const time_t now = time(nullptr);
	TMailBoxRespondUnreadData t;
	
	for (const SMailBoxTable& mail : it->second)
	{
		if (mail.bIsDeleted)
			continue;

		if (mail.Message.bIsConfirm)
			continue;
		
		if (difftime(mail.Message.DeleteTime, now) <= 0)
			continue;

		if (mail.Message.bIsGMPost)
			t.bGMVisible = true;

		if (mail.Message.bIsItemExist)
			t.bItemMessageCount++;
		else
			t.bCommonMessageCount++;
	}

	if ((t.bItemMessageCount + t.bCommonMessageCount) < 1)
		return;

	pkPeer->EncodeHeader(HEADER_DG_RESPOND_MAILBOX_UNREAD, dwHandle, sizeof(TMailBoxRespondUnreadData));
	pkPeer->Encode(&t, sizeof(TMailBoxRespondUnreadData));
}

void CClientManager::MAILBOX_BACKUP()
{
	CDBManager::instance().DirectQuery("TRUNCATE TABLE player.mailbox");

	if (m_map_mailbox.empty())
		return;

	char s_szQuery[1024];
	const time_t now = time(nullptr);

	for (auto& p : m_map_mailbox)
	{
		auto& mailvec = p.second;
		if (mailvec.empty())
			continue;
		
		mailvec.erase(std::remove_if(mailvec.begin(), mailvec.end(),
			[now](const TMailBoxTable& mail) { return mail.bIsDeleted || difftime(mail.Message.DeleteTime, now) <= 0; }), mailvec.end());

		std::sort(mailvec.begin(), mailvec.end(), [](const TMailBoxTable& l, const TMailBoxTable& r) {
			return l.Message.SendTime > r.Message.SendTime;
			});

		for (const auto& mail : mailvec)
		{
#if defined(__BL_TRANSMUTATION__)
			snprintf(s_szQuery, sizeof(s_szQuery), "INSERT INTO mailbox%s (name, who, title, message, gm, confirm, send_time, delete_time, gold, won, ivnum, transmutation, icount, socket0, socket1, socket2, attrtype0, attrvalue0, attrtype1, attrvalue1, attrtype2, attrvalue2, attrtype3, attrvalue3, attrtype4, attrvalue4, attrtype5, attrvalue5, attrtype6, attrvalue6) VALUES('%s', '%s', '%s', '%s', %d, %d, %ld, %ld, %d, %d, %lu, %lu, %ld, %ld, %ld, %ld, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)",
#else
			snprintf(s_szQuery, sizeof(s_szQuery), "INSERT INTO mailbox%s (name, who, title, message, gm, confirm, send_time, delete_time, gold, won, ivnum, icount, socket0, socket1, socket2, attrtype0, attrvalue0, attrtype1, attrvalue1, attrtype2, attrvalue2, attrtype3, attrvalue3, attrtype4, attrvalue4, attrtype5, attrvalue5, attrtype6, attrvalue6) VALUES('%s', '%s', '%s', '%s', %d, %d, %ld, %ld, %d, %d, %lu, %lu, %ld, %ld, %ld, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d, %d)",
#endif	
				GetTablePostfix(),
				mail.szName, mail.AddData.szFrom, mail.Message.szTitle, mail.AddData.szMessage,
				mail.Message.bIsGMPost, mail.Message.bIsConfirm, mail.Message.SendTime, mail.Message.DeleteTime,
#if defined(__BL_TRANSMUTATION__)
				mail.AddData.iYang, mail.AddData.iWon, mail.AddData.ItemVnum, mail.AddData.dwTransmutationVnum, mail.AddData.ItemCount,
#else
				mail.AddData.iYang, mail.AddData.iWon, mail.AddData.ItemVnum, mail.AddData.ItemCount,
#endif
				mail.AddData.alSockets[0], mail.AddData.alSockets[1], mail.AddData.alSockets[2],
				mail.AddData.aAttr[0].bType, mail.AddData.aAttr[0].sValue,
				mail.AddData.aAttr[1].bType, mail.AddData.aAttr[1].sValue,
				mail.AddData.aAttr[2].bType, mail.AddData.aAttr[2].sValue,
				mail.AddData.aAttr[3].bType, mail.AddData.aAttr[3].sValue,
				mail.AddData.aAttr[4].bType, mail.AddData.aAttr[4].sValue,
				mail.AddData.aAttr[5].bType, mail.AddData.aAttr[5].sValue,
				mail.AddData.aAttr[6].bType, mail.AddData.aAttr[6].sValue
			);

			std::unique_ptr<SQLMsg> pInsert(CDBManager::instance().DirectQuery(s_szQuery));
		}
	}
}
#endif

//Find
			case HEADER_GD_SAFEBOX_LOAD:
				QUERY_SAFEBOX_LOAD(peer, dwHandle, (TSafeboxLoadPacket *) data, 0);
				break;

///Add
#if defined(__BL_MAILBOX__)
			case HEADER_GD_MAILBOX_LOAD:
				QUERY_MAILBOX_LOAD(peer, dwHandle, (TMailBox*)data);
				break;

			case HEADER_GD_MAILBOX_CHECK_NAME:
				QUERY_MAILBOX_CHECK_NAME(peer, dwHandle, (TMailBox*)data);
				break;

			case HEADER_GD_MAILBOX_WRITE:
				QUERY_MAILBOX_WRITE(peer, dwHandle, (TMailBoxTable*)data);
				break;

			case HEADER_GD_MAILBOX_DELETE:
				QUERY_MAILBOX_DELETE(peer, dwHandle, (TMailBox*)data);
				break;

			case HEADER_GD_MAILBOX_CONFIRM:
				QUERY_MAILBOX_CONFIRM(peer, dwHandle, (TMailBox*)data);
				break;

			case HEADER_GD_MAILBOX_GET:
				QUERY_MAILBOX_GET(peer, dwHandle, (TMailBox*)data);
				break;

			case HEADER_GD_MAILBOX_UNREAD:
				QUERY_MAILBOX_UNREAD(peer, dwHandle, (TMailBox*)data);
				break;
#endif

//Find
		if (!(thecore_heart->pulse % (thecore_heart->passes_per_sec * 3600)))
		{
			CMoneyLog::instance().Save();
		}

///Add
#if defined(__BL_MAILBOX__)
		if (!(thecore_heart->pulse % (thecore_heart->passes_per_sec * m_iMailBoxBackupSec)))
		{
			CClientManager::instance().MAILBOX_BACKUP();
		}
#endif