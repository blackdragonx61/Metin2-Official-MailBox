//Find
			case HEADER_GC_MOTION:
				ret = RecvMotionPacket();
				break;

///Add
#if defined(__BL_MAILBOX__)
			case HEADER_GC_MAILBOX_PROCESS:
				ret = RecvMailboxProcess();
				break;

			case HEADER_GC_MAILBOX:
				ret = RecvMailbox();
				break;

			case HEADER_GC_MAILBOX_ADD_DATA:
				ret = RecvMailboxAddData();
				break;

			case HEADER_GC_MAILBOX_ALL:
				ret = RecvMailboxAll();
				break;

			case HEADER_GC_MAILBOX_UNREAD:
				ret = RecvMailboxUnread();
				break;
#endif

//Find
bool CPythonNetworkStream::RecvMotionPacket()
{
	...
}

///Add
#if defined(__BL_MAILBOX__)
#include "PythonMail.h"

bool CPythonNetworkStream::RecvMailboxProcess()
{
	TPacketMailboxProcess p;

	if (!Recv(sizeof(p), &p))
		return false;

	switch (p.bSubHeader)
	{
	case CPythonMail::EMAILBOX_GC::MAILBOX_GC_CLOSE:
		CPythonMail::Instance().Destroy();
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MailBoxProcess", Py_BuildValue("(ii)", p.bSubHeader, p.bArg1));
		break;
	case CPythonMail::EMAILBOX_GC::MAILBOX_GC_OPEN:
	case CPythonMail::EMAILBOX_GC::MAILBOX_GC_POST_WRITE_CONFIRM:
	case CPythonMail::EMAILBOX_GC::MAILBOX_GC_POST_WRITE:
	case CPythonMail::EMAILBOX_GC::MAILBOX_GC_POST_ALL_DELETE:
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MailBoxProcess", Py_BuildValue("(ii)", p.bSubHeader, p.bArg1));
		break;
	case CPythonMail::EMAILBOX_GC::MAILBOX_GC_ADD_DATA:
	case CPythonMail::EMAILBOX_GC::MAILBOX_GC_POST_DELETE:
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MailBoxProcess", Py_BuildValue("(i(ii))", p.bSubHeader, p.bArg1, p.bArg2));
		break;
	case CPythonMail::EMAILBOX_GC::MAILBOX_GC_POST_GET_ITEMS:
		CPythonMail::Instance().ResetAddData(p.bArg1);
		PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MailBoxProcess", Py_BuildValue("(i(ii))", p.bSubHeader, p.bArg1, p.bArg2));
		break;
	default:
		TraceError("CPythonNetworkStream::RecvMailboxProcess: Unknown subheader: %d\n", p.bSubHeader);
		break;
	}

	return true;
}

bool CPythonNetworkStream::RecvMailbox()
{
	TPacketGCMailBox p;
	if (!Recv(sizeof(p), &p))
		return false;

	CPythonMail::Instance().Destroy();
	
	unsigned int iPacketSize = (p.wSize - sizeof(TPacketGCMailBox));
	for (; iPacketSize > 0; iPacketSize -= sizeof(TPacketGCMailBoxMessage))
	{
		TPacketGCMailBoxMessage Message;
		if (!Recv(sizeof(Message), &Message))
			return false;

		CPythonMail::Instance().AddMail(new CPythonMail::SMailBox(Message.SendTime, Message.DeleteTime, Message.szTitle, Message.bIsGMPost, Message.bIsItemExist, Message.bIsConfirm));
	}

	return true;
}

bool CPythonNetworkStream::RecvMailboxAddData()
{
	TPacketGCMailBoxAddData p;

	if (!Recv(sizeof(p), &p))
		return false;

	CPythonMail::SMailBox* _Data = CPythonMail::Instance().GetMail(p.Index);
	if (_Data == nullptr)
	{
		Tracef("RecvMailboxAddData Error: SMailBox is null.\n");
		return true;
	}

	CPythonMail::SMailBoxAddData*& _AddData = _Data->AddData;
	if (_AddData != nullptr)
	{
		Tracef("RecvMailboxAddData Error: SMailBoxAddData is not null.\n");
		return true;
	}

	_Data->bIsConfirm = true;
	_AddData = new CPythonMail::SMailBoxAddData(p.szFrom, p.szMessage, p.iYang, p.iWon, p.ItemVnum, p.ItemCount, p.alSockets, p.aAttr
#if defined(__BL_TRANSMUTATION__)
		, p.dwTransmutationVnum
#endif
	);
	return true;
}

bool CPythonNetworkStream::RecvMailboxAll()
{
	TPacketGCMailBox p;
	if (!Recv(sizeof(p), &p))
		return false;

	PyObject* list = PyList_New(0);

	unsigned int iPacketSize = (p.wSize - sizeof(TPacketGCMailBox));
	for (; iPacketSize > 0; iPacketSize -= sizeof(TPacketGCMailboxProcessAll))
	{
		TPacketGCMailboxProcessAll Index;
		if (!Recv(sizeof(Index), &Index))
			return false;

		CPythonMail::Instance().ResetAddData(Index.Index);
		PyList_Append(list, Py_BuildValue("i", Index.Index));
	}

	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MailBoxProcess", Py_BuildValue("i(iO)",
		CPythonMail::EMAILBOX_GC::MAILBOX_GC_POST_ALL_GET_ITEMS, CPythonMail::EMAILBOX_POST_ALL_GET_ITEMS::POST_ALL_GET_ITEMS_OK, list));

	Py_DECREF(list);
	return true;
}

bool CPythonNetworkStream::RecvMailboxUnread()
{
	TMailBoxRespondUnreadData p;

	if (!Recv(sizeof(p), &p))
		return false;

	const bool bFlash = p.bItemMessageCount > 0;
	PyCallClassMemberFunc(m_apoPhaseWnd[PHASE_WINDOW_GAME], "MailBoxProcess", Py_BuildValue("i(iiiii)", CPythonMail::EMAILBOX_GC::MAILBOX_GC_UNREAD_DATA, 
		bFlash, (p.bItemMessageCount + p.bCommonMessageCount), p.bItemMessageCount, p.bCommonMessageCount, p.bGMVisible));

	return true;
}

bool CPythonNetworkStream::SendPostWriteConfirm(const char* szName)
{
	TPacketCGMailboxWriteConfirm p;
	p.bHeader = HEADER_CG_MAILBOX_WRITE_CONFIRM;
	std::strcpy(p.szName, szName);

	if (!Send(sizeof(p), &p))
	{
		Tracef("SendPostWriteConfirm Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendMailBoxClose()
{
	TPacketMailboxProcess p;
	p.bHeader = HEADER_CG_MAILBOX_PROCESS;
	p.bSubHeader = CPythonMail::EMAILBOX_CG::MAILBOX_CG_CLOSE;

	if (!Send(sizeof(p), &p))
	{
		Tracef("SendMailBoxClose Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendPostDelete(const BYTE Index)
{
	TPacketMailboxProcess p;
	p.bHeader = HEADER_CG_MAILBOX_PROCESS;
	p.bSubHeader = CPythonMail::EMAILBOX_CG::MAILBOX_CG_DELETE;
	p.bArg1 = Index;

	if (!Send(sizeof(p), &p))
	{
		Tracef("SendPostDelete Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendPostAllDelete()
{
	TPacketMailboxProcess p;
	p.bHeader = HEADER_CG_MAILBOX_PROCESS;
	p.bSubHeader = CPythonMail::EMAILBOX_CG::MAILBOX_CG_ALL_DELETE;

	if (!Send(sizeof(p), &p))
	{
		Tracef("SendPostAllDelete Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendPostGetItems(const BYTE Index)
{
	TPacketMailboxProcess p;
	p.bHeader = HEADER_CG_MAILBOX_PROCESS;
	p.bSubHeader = CPythonMail::EMAILBOX_CG::MAILBOX_CG_GET_ITEMS;
	p.bArg1 = Index;

	if (!Send(sizeof(p), &p))
	{
		Tracef("SendPostGetItems Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendPostAllGetItems()
{
	TPacketMailboxProcess p;
	p.bHeader = HEADER_CG_MAILBOX_PROCESS;
	p.bSubHeader = CPythonMail::EMAILBOX_CG::MAILBOX_CG_ALL_GET_ITEMS;

	if (!Send(sizeof(p), &p))
	{
		Tracef("SendPostAllGetItems Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::RequestPostAddData(const BYTE ButtonIndex, const BYTE DataIndex)
{
	TPacketMailboxProcess p;
	p.bHeader = HEADER_CG_MAILBOX_PROCESS;
	p.bSubHeader = CPythonMail::EMAILBOX_CG::MAILBOX_CG_ADD_DATA;
	p.bArg1 = ButtonIndex;
	p.bArg2 = DataIndex;

	if (!Send(sizeof(p), &p))
	{
		Tracef("RequestPostAddData Error\n");
		return false;
	}

	return SendSequence();
}

bool CPythonNetworkStream::SendPostWrite(const char* szName, const char* szTitle, const char* szMessage, const TItemPos& pos, const int iYang, const int iWon)
{
	TPacketCGMailboxWrite p;
	p.bHeader = HEADER_CG_MAILBOX_WRITE;
	std::strcpy(p.szName, szName);
	std::strcpy(p.szTitle, szTitle);
	std::strcpy(p.szMessage, szMessage);
	p.pos = pos;
	p.iYang = iYang;
	p.iWon = iWon;

	if (!Send(sizeof(p), &p))
	{
		Tracef("SendPostWrite Error\n");
		return false;
	}

	return SendSequence();
}
#endif