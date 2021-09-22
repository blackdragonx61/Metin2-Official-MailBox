/*
* blackdragonx61 / Mali
* 06.09.2021
*/

#pragma once

class CPythonMail : public CSingleton<CPythonMail>
{
public:
	CPythonMail();
	virtual ~CPythonMail();

	struct SMailBoxAddData
	{
		SMailBoxAddData(const char* _From, const char* _Message, const int _Yang, const int _Won, 
			const DWORD _ItemVnum, const DWORD _ItemCount, const long* _Sockets, const TPlayerItemAttribute* _Attrs
#if defined(__BL_TRANSMUTATION__)
			, const DWORD _TransmutationVnum
#endif
		);
		~SMailBoxAddData();
		std::string							sFrom;
		std::string							sMessage;
		int									iYang;
		int									iWon;
		DWORD								ItemVnum;
		DWORD								ItemCount;
		long								alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
		TPlayerItemAttribute				aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
#if defined(__BL_TRANSMUTATION__)
		DWORD								dwTransmutationVnum;
#endif
	};

	SMailBoxAddData* GetMailAddData(const BYTE Index);

	struct SMailBox
	{
		SMailBox(const time_t _SendTime, const time_t _DeleteTime, const char* _Title, const bool _IsGM,
			const bool _IsItem, const bool _IsConfirm);
		~SMailBox();
		void ResetAddData();
		time_t								Sendtime;
		time_t								Deletetime;
		std::string							sTitle;
		bool								bIsGMPost;
		bool								bIsItemExist;
		bool								bIsConfirm;
		SMailBoxAddData*					AddData;
	};

	SMailBox* GetMail(const BYTE Index);
	using MailVec = std::vector<SMailBox*>;
	const MailVec& GetMailVec() const;

	void Destroy();
	void ResetAddData(const BYTE Index);
	void AddMail(CPythonMail::SMailBox* mail);

	enum EMAILBOX_GC
	{
		MAILBOX_GC_OPEN,
		MAILBOX_GC_POST_WRITE_CONFIRM,
		MAILBOX_GC_POST_WRITE,
		MAILBOX_GC_SET,
		MAILBOX_GC_ADD_DATA,
		MAILBOX_GC_POST_GET_ITEMS,
		MAILBOX_GC_POST_DELETE,
		MAILBOX_GC_POST_ALL_DELETE,
		MAILBOX_GC_POST_ALL_GET_ITEMS,
		MAILBOX_GC_UNREAD_DATA,
		MAILBOX_GC_ITEM_EXPIRE,
		MAILBOX_GC_CLOSE,
		MAILBOX_GC_SYSTEM_CLOSE,
	};

	enum EMAILBOX_CG
	{
		MAILBOX_CG_CLOSE,
		MAILBOX_CG_ALL_DELETE,
		MAILBOX_CG_ALL_GET_ITEMS,
		MAILBOX_CG_DELETE,
		MAILBOX_CG_GET_ITEMS,
		MAILBOX_CG_ADD_DATA,
	};

	enum EMAILBOX_POST_ALL_DELETE
	{
		POST_ALL_DELETE_FAIL,
		POST_ALL_DELETE_OK,
		POST_ALL_DELETE_FAIL_EMPTY,
		POST_ALL_DELETE_FAIL_DONT_EXIST,
	};

	enum EMAILBOX_POST_ALL_GET_ITEMS
	{
		POST_ALL_GET_ITEMS_FAIL,
		POST_ALL_GET_ITEMS_OK,
		POST_ALL_GET_ITEMS_EMPTY,
		POST_ALL_GET_ITEMS_FAIL_DONT_EXIST,
		POST_ALL_GET_ITEMS_FAIL_CANT_GET,
		POST_ALL_GET_ITEMS_FAIL_USE_TIME_LIMIT,
	};

	enum EMAILBOX_POST_DELETE_FAIL
	{
		POST_DELETE_FAIL,
		POST_DELETE_OK,
		POST_DELETE_FAIL_EXIST_ITEMS,
		POST_TIME_OUT_DELETE,
	};

	enum EMAILBOX_POST_GET_ITEMS
	{
		POST_GET_ITEMS_FAIL,
		POST_GET_ITEMS_OK,
		POST_GET_ITEMS_NONE,
		POST_GET_ITEMS_NOT_ENOUGHT_INVENTORY,
		POST_GET_ITEMS_YANG_OVERFLOW,
		POST_GET_ITEMS_WON_OVERFLOW,
		POST_GET_ITEMS_FAIL_BLOCK_CHAR,
		POST_GET_ITEMS_USE_TIME_LIMIT,
		POST_GET_ITEMS_RESULT_MAX,
	};

	enum EMAILBOX_POST_WRITE
	{
		POST_WRITE_FAIL,
		POST_WRITE_OK,
		POST_WRITE_INVALID_NAME,
		POST_WRITE_TARGET_BLOCKED,
		POST_WRITE_BLOCKED_ME,
		POST_WRITE_FULL_MAILBOX,
		POST_WRITE_WRONG_TITLE,
		POST_WRITE_YANG_NOT_ENOUGHT,
		POST_WRITE_WON_NOT_ENOUGHT,
		POST_WRITE_WRONG_MESSAGE,
		POST_WRITE_WRONG_ITEM,
		POST_WRITE_LEVEL_NOT_ENOUGHT,
		POST_WRITE_USE_TIME_LIMIT,
	};

private:
	MailVec vecMail;
};
