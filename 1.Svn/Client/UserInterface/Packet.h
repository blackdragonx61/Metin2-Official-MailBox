//Find
#ifdef __AUCTION__
	HEADER_CG_AUCTION_CMD							= 205,
#endif

///Add
#if defined(__BL_MAILBOX__)
	HEADER_CG_MAILBOX_WRITE = 219,
	HEADER_CG_MAILBOX_WRITE_CONFIRM = 220,
	HEADER_CG_MAILBOX_PROCESS = 221,
#endif

//Find
	HEADER_GC_RESPOND_CHANNELSTATUS				= 210,

///Add
#if defined(__BL_MAILBOX__)
	HEADER_GC_MAILBOX_PROCESS = 220,
	HEADER_GC_MAILBOX = 221,
	HEADER_GC_MAILBOX_ADD_DATA = 222,
	HEADER_GC_MAILBOX_ALL = 223,
	HEADER_GC_MAILBOX_UNREAD = 224,
#endif

//Find
typedef struct packet_item_del
{
	...
} TPacketGCItemDel;

///Add
#if defined(__BL_MAILBOX__)
typedef struct packet_mailbox_process
{
	packet_mailbox_process()
		: bArg1(0), bArg2(0) {}
	BYTE							bHeader;
	BYTE							bSubHeader;
	BYTE							bArg1;
	BYTE							bArg2;
} TPacketMailboxProcess;

typedef struct SMailBoxRespondUnreadData
{
	BYTE							bHeader;
	BYTE							bItemMessageCount;
	BYTE							bCommonMessageCount;
	bool							bGMVisible;
} TMailBoxRespondUnreadData;

typedef struct packet_mailbox_process_all
{
	BYTE							Index;
} TPacketGCMailboxProcessAll;

typedef struct packet_mailbox_add_data
{
	BYTE							bHeader;
	BYTE							Index;
	char							szFrom[CHARACTER_NAME_MAX_LEN + 1];
	char							szMessage[100 + 1];
	int								iYang;
	int								iWon;
	DWORD							ItemVnum;
	DWORD							ItemCount;
	long							alSockets[ITEM_SOCKET_SLOT_MAX_NUM];
	TPlayerItemAttribute			aAttr[ITEM_ATTRIBUTE_SLOT_MAX_NUM];
#if defined(__BL_TRANSMUTATION__)
	DWORD							dwTransmutationVnum;
#endif
} TPacketGCMailBoxAddData;

typedef struct packet_mailbox_message
{
	time_t							SendTime;
	time_t							DeleteTime;
	char							szTitle[25 + 1];
	bool							bIsGMPost;
	bool							bIsItemExist;
	bool							bIsConfirm;
} TPacketGCMailBoxMessage;

typedef struct packet_mailbox
{
	BYTE							bHeader;
	WORD							wSize;
} TPacketGCMailBox;

typedef struct packet_mailbox_write
{
	BYTE							bHeader;
	char							szName[CHARACTER_NAME_MAX_LEN + 1];
	char							szTitle[25 + 1];
	char							szMessage[100 + 1];
	TItemPos						pos;
	int								iYang;
	int								iWon;
} TPacketCGMailboxWrite;

typedef struct packet_mailbox_write_confirm
{
	BYTE							bHeader;
	char							szName[CHARACTER_NAME_MAX_LEN + 1];
} TPacketCGMailboxWriteConfirm;
#endif