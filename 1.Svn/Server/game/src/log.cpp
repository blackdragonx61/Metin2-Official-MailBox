///Add
#if defined(__BL_MAILBOX__)
void LogManager::MailLog(const char* const szName, const char* const szWho, const char* const szTitle, const char* const szMessage, const bool bIsGM, const DWORD dwItemVnum, const DWORD dwItemCount, const int iYang, const int iWon)
{
	Query("INSERT DELAYED INTO mailbox_log%s (name, who, title, message, gm, gold, won, ivnum, icount, date) "
		"VALUES('%s', '%s', '%s', '%s', %d, %d, %d, %lu, %lu, NOW()) ",
		get_table_postfix(), szName, szWho, szTitle, szMessage, bIsGM, iYang, iWon, dwItemVnum, dwItemCount);
}
#endif