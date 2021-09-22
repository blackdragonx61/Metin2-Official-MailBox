///Add
#include "service.h"

//Find
	HEADER_GD_REQUEST_CHANNELSTATUS	= 140,

///Add
#if defined(__BL_MAILBOX__)
	HEADER_GD_MAILBOX_LOAD = 145,
	HEADER_GD_MAILBOX_CHECK_NAME = 146,
	HEADER_GD_MAILBOX_WRITE = 147,
	HEADER_GD_MAILBOX_DELETE = 148,
	HEADER_GD_MAILBOX_CONFIRM = 149,
	HEADER_GD_MAILBOX_GET = 150,
	HEADER_GD_MAILBOX_UNREAD = 151,
#endif

//Find
	HEADER_DG_RESPOND_CHANNELSTATUS		= 181,

///Add
#if defined(__BL_MAILBOX__)
	HEADER_DG_RESPOND_MAILBOX_LOAD = 185,
	HEADER_DG_RESPOND_MAILBOX_CHECK_NAME = 186,
	HEADER_DG_RESPOND_MAILBOX_UNREAD = 187,
#endif

//Find
typedef struct SSafeboxLoadPacket
{
	...
} TSafeboxLoadPacket;

///Add
#if defined(__BL_MAILBOX__)
enum EMAILBOX
{
	MAILBOX_TAX = 5,
	MAILBOX_REMAIN_DAY = 30,
	MAILBOX_REMAIN_DAY_GM = 7,
	MAILBOX_LEVEL_LIMIT = 20,
	MAILBOX_PRICE_YANG = 1000,
	MAILBOX_PAGE_SIZE = 9,
	MAILBOX_PAGE_COUNT = 10,
	MAILBOX_MAX_MAIL = MAILBOX_PAGE_SIZE * MAILBOX_PAGE_COUNT,
};

typedef struct SMailBoxRespondUnreadData
{
	SMailBoxRespondUnreadData() :
		bHeader(0),
		bItemMessageCount(0),
		bCommonMessageCount(0),
		bGMVisible(false) 
	{}
	BYTE bHeader;
	BYTE bItemMessageCount;
	BYTE bCommonMessageCount;
	bool bGMVisible;
} TMailBoxRespondUnreadData;

typedef struct SMailBox
{
	char	szName[CHARACTER_NAME_MAX_LEN + 1];
	BYTE	Index;
} TMailBox;

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
	long							alSockets[ITEM_SOCKET_MAX_NUM];
	TPlayerItemAttribute			aAttr[ITEM_ATTRIBUTE_MAX_NUM];
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

typedef struct SMailBoxTable
{
	char szName[CHARACTER_NAME_MAX_LEN + 1];
	bool bIsDeleted;
	packet_mailbox_message Message;
	packet_mailbox_add_data AddData;
} TMailBoxTable;
#endif