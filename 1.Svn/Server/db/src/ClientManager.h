//Find
size_t CreatePlayerSaveQuery(char * pszQuery, size_t querySize, TPlayerTable * pkTab);

///Add
#if defined(__BL_MAILBOX__)
typedef std::vector<SMailBoxTable> MailVec;
typedef std::map<std::string, MailVec> MailBoxMap;
#endif

//Find
	bool		InitializeTables();

///Add
#if defined(__BL_MAILBOX__)
	bool		InitializeMailBoxTable();
#endif

//Find
	void		QUERY_REMOVE_AFFECT(CPeer * pkPeer, TPacketGDRemoveAffect * p);

///Add
#if defined(__BL_MAILBOX__)
	bool		GET_MAIL(const char* name, const BYTE index, SMailBoxTable** mail);
	void		QUERY_MAILBOX_LOAD(CPeer * pkPeer, DWORD dwHandle, TMailBox*);
	void		QUERY_MAILBOX_CHECK_NAME(CPeer * pkPeer, DWORD dwHandle, TMailBox*);
	void		QUERY_MAILBOX_WRITE(CPeer * pkPeer, DWORD dwHandle, TMailBoxTable*);
	void		QUERY_MAILBOX_DELETE(CPeer * pkPeer, DWORD dwHandle, TMailBox*);
	void		QUERY_MAILBOX_CONFIRM(CPeer* pkPeer, DWORD dwHandle, TMailBox*);
	void		QUERY_MAILBOX_GET(CPeer * pkPeer, DWORD dwHandle, TMailBox*);
	void		QUERY_MAILBOX_UNREAD(CPeer * pkPeer, DWORD dwHandle, TMailBox*);
	void		MAILBOX_BACKUP();
#endif

//Find
	ItemTableVNumMap		m_map_itemTableByVnum;

///Add
#if defined(__BL_MAILBOX__)
	int						m_iMailBoxBackupSec;
	MailBoxMap				m_map_mailbox;
#endif