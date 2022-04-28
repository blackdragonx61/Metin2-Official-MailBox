///Add
#include "../UserInterface/Locale_inc.h"

//Find
			void Flash();

///Add
#if defined(__BL_MAILBOX__)
			void EnableFlash();
			void DisableFlash();
#endif

//Find
			BOOL m_isFlash;

///Add
#if defined(__BL_MAILBOX__)
			bool m_isNewFlash;
#endif