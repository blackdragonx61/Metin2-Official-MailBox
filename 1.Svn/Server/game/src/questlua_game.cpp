//Find
	int game_web_mall(lua_State* L)
	{
		...
	}

///Add
#if defined(__BL_MAILBOX__)
	int game_open_mailbox(lua_State* L)
	{
		CMailBox::Open(CQuestManager::instance().GetCurrentCharacterPtr());
		return 0;
	}

	int game_send_gm_mail(lua_State* L)
	{
		if (false == (lua_isstring(L, 1) && lua_isstring(L, 2) && lua_isstring(L, 3) 
			&& lua_isnumber(L, 4) && lua_isnumber(L, 5) && lua_isnumber(L, 6) && lua_isnumber(L, 7)))
		{
			sys_err("Wrong argument.");
			return 0;
		}

		const char* const cPlayerName = lua_tostring(L, 1);
		const char* const cTitle = lua_tostring(L, 2);
		const char* const cMessage = lua_tostring(L, 3);
		const DWORD dwItemVnum = static_cast<DWORD>(lua_tonumber(L, 4));
		const DWORD dwItemCount = static_cast<DWORD>(lua_tonumber(L, 5));
		const int iYang = static_cast<int>(lua_tonumber(L, 6));
		const int iWon = static_cast<int>(lua_tonumber(L, 7));

		CMailBox::SendGMMail(cPlayerName, cTitle, cMessage, dwItemVnum, dwItemCount, iYang, iWon);
		return 0;
	}
#endif

//Find
			{ "open_web_mall",				game_web_mall					},

///Add
#if defined(__BL_MAILBOX__)
			{ "open_mailbox",				game_open_mailbox				},
			{ "send_gm_mail",				game_send_gm_mail				},
#endif