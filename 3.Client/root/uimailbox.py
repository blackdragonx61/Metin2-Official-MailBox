import net
import player
import ui
import app
import localeInfo
import uiScriptLocale
import mouseModule
import constInfo
import chat
import item
import grp
import uiPickMoney
import messenger
import uiCommon
import math
import mail

from _weakref import proxy
WORD_MAX = 0xffff
MAILBOX_MAX_DISTANCE = 1000 # ������ npc ���� üũ �Ÿ�(�������� ������� �ʾҴٸ� �� �Ÿ� �̻� �־����� �Ǹ� â�� ����)

# ������ ���� ����
DIVISION_EMPTY	= 0		# �� ����
DIVISION_POST	= 1		# �Ϲ� ����
DIVISION_ITEM	= 2		# ������ or won or yang �� ÷�ε� ����
DIVISION_GM		= 3		# GM �� ���� ����

POST_MAX		= 9		# �ѹ��� ����� ���� MAX
TITLE_MAX_LEN	= 25	# ������ Ŭ���� ���� MAX LEN

POST_WRITE_LIMIT_LEVEL		= 20	# �߼��ϱ� ���� ����	
FRIEND_SELECT_UI_SHOW_MAX	= 10	# ģ�� ����Ʈ SHOW MAX

MAX_YANG		= 9998999	# ���� �� �ִ� yang MAX
MAX_CHEQUE		= 99		# ���� �� �ִ� won MAX
POST_WRITE_COST	= 1000		# ���� ������ �Һ� ���

POST_ICON_PATH	= "d:/ymir work/ui/game/mailbox/mailbox_icon_post.sub"
ITEM_ICON_PATH	= "d:/ymir work/ui/game/mailbox/mailbox_icon_item.sub"
GM_ICON_PATH	= "d:/ymir work/ui/game/mailbox/mailbox_icon_gm.sub"
EMPTY_ICON_PATH = "d:/ymir work/ui/game/mailbox/mailbox_icon_empty.sub"
		
def LoadScript(self, fileName):
	pyScrLoader = ui.PythonScriptLoader()
	pyScrLoader.LoadScriptFile(self, fileName)
		
class Post:
	def __init__(self, button_index, parent, click_func):
		self.button_index		= button_index
		self.button				= None
		self.icon_img			= None
		self.title_window		= None
		self.title_text			= None
		self.remain_time_window = None
		self.remain_time_text	= None
		self.cur_icon_type		= EMPTY_ICON_PATH
		self.data_index			= -1
		self.click_func			= ui.__mem_func__(click_func)
		
		self.__CreatePost( button_index, parent )
		self.Show()
		
	def __del__(self):
		self.button_index		= -1
		self.button				= None
		self.icon_img			= None
		self.title_window		= None
		self.title_text			= None
		self.remain_time_window = None
		self.remain_time_text	= None
		self.cur_icon_type		= EMPTY_ICON_PATH
		self.data_index			= -1
		self.click_func			= None
		
	def SecondToDH(self, time):
		hour = int((time / 60) / 60) % 24
		day = int(int((time / 60) / 60) / 24)
		
		text = ""
		if localeInfo.IsARABIC():
			if day > 99:
				text = "99%s" % localeInfo.DAY
				return text

			if day >= 1:
				text = "%02d%s" % (day, localeInfo.DAY)
				return text

			if hour >= 0:
				text = "%02d%s" % (hour, localeInfo.HOUR)
				
		else:
			text = "["
			
			if day > 99:
				text += "99" + localeInfo.DAY
				text += "]"
				return text

			if day >= 1:
				day_text = "%02d" % day
				text += day_text + localeInfo.DAY
				text += "]"
				return text

			if hour >= 0:
				hour_text = "%02d" % hour
				text += hour_text + localeInfo.HOUR
				text += "]"
		
		return text
		
	def Show(self):
		if self.button:
			self.button.Show()
		if self.icon_img:
			self.icon_img.Show()
		if self.title_window:
			self.title_window.Show()
		if self.remain_time_window:
			self.remain_time_window.Show()
			
	def Hide(self):
		if self.button:
			self.button.Hide()
		if self.icon_img:
			self.icon_img.Hide()
		if self.title_window:
			self.title_window.Hide()
		if self.remain_time_window:
			self.remain_time_window.Hide()
			
	def __CreatePost(self, button_index, parent):			
		self.button = ui.Button()
		self.button.SetParent( proxy(parent) )
		self.button.SetUpVisual( "d:/ymir work/ui/game/mailbox/post_default.sub" )
		self.button.SetDownVisual( "d:/ymir work/ui/game/mailbox/post_default.sub" )
		self.button.SetOverVisual( "d:/ymir work/ui/game/mailbox/post_over.sub" )
		self.button.SetDisableVisual( "d:/ymir work/ui/game/mailbox/post_select.sub" )
		self.button.SetEvent( ui.__mem_func__(self.__ButtonClickFunc) )
		
		pos_y = 34 * button_index + 3 * button_index
		self.button.SetPosition( 0, pos_y )
		self.button.Show()
		
		self.icon_img = ui.ImageBox()
		self.icon_img.SetParent( self.button )
		self.icon_img.LoadImage( self.cur_icon_type )
		self.icon_img.SetPosition(2, 2)
		self.icon_img.AddFlag("attach")
		self.icon_img.Show()
		
		if localeInfo.IsARABIC():
			img_width = self.icon_img.GetWidth()
			button_width = self.button.GetWidth()
			(button_lx, button_ly) = self.button.GetLocalPosition()
			self.icon_img.SetPosition(button_lx + button_width - img_width-2, 2)
			
		self.title_window = ui.ScriptWindow()
		self.title_window.SetParent( self.button )
		self.title_window.SetPosition( 40, 0 )
		self.title_window.SetSize( 180, 34 )
		self.title_window.AddFlag("attach")
		self.title_window.AddFlag("not_pick")
		self.title_window.Show()
		
		if localeInfo.IsARABIC():
			button_width = self.button.GetWidth()
			(button_lx, button_ly) = self.button.GetLocalPosition()
			self.title_window.SetPosition(button_lx + button_width -40, 2)
			
		self.title_text = ui.TextLine()
		self.title_text.SetParent( self.title_window )
		self.title_text.SetPosition( 0, 0 )
		self.title_text.SetHorizontalAlignLeft()
		self.title_text.SetVerticalAlignCenter()
		self.title_text.SetWindowVerticalAlignCenter()
		self.title_text.SetText("1234567890123456789012345")
		self.title_text.AddFlag("attach")
		self.title_text.AddFlag("not_pick")
		self.title_text.Show()
		
		self.remain_time_window = ui.ScriptWindow()
		self.remain_time_window.SetParent( self.button )
		self.remain_time_window.SetPosition( 220, 0 )
		self.remain_time_window.SetSize( 65, 34 )
		self.remain_time_window.AddFlag("attach")
		self.remain_time_window.AddFlag("not_pick")
		self.remain_time_window.Show()
		
		if localeInfo.IsARABIC():
			button_width = self.button.GetWidth()
			(button_lx, button_ly) = self.button.GetLocalPosition()
			self.remain_time_window.SetPosition(button_lx + button_width -220-65, 2)
			
		self.remain_time_text = ui.TextLine()
		self.remain_time_text.SetParent( self.remain_time_window )
		self.remain_time_text.SetPosition( 0, 0 )
		self.remain_time_text.SetHorizontalAlignCenter()
		self.remain_time_text.SetVerticalAlignCenter()
		self.remain_time_text.SetWindowHorizontalAlignCenter()
		self.remain_time_text.SetWindowVerticalAlignCenter()
		self.remain_time_text.SetText( self.SecondToDH( app.GetGlobalTimeStamp() ) )
		self.remain_time_text.AddFlag("attach")
		self.remain_time_text.AddFlag("not_pick")
		self.remain_time_text.Show()
		
	def __ButtonClickFunc(self):
		if DIVISION_EMPTY == self.cur_icon_type:
			return
			
		apply( self.click_func, [self.button_index, self.data_index] )
		
	def SetDataIndex(self, data_index):
		self.data_index = data_index
		
	def SetConfirmColor(self, is_confirm):
		if is_confirm:
			if self.title_text:
				self.title_text.SetFontColor( 0.3, 0.3, 0.3 )
			
			if self.remain_time_text:
				self.remain_time_text.SetFontColor( 0.3, 0.3, 0.3 )
		else:
			if self.title_text:
				self.title_text.SetFontColor( 0.78, 0.78, 0.78 )
			
			if self.remain_time_text:
				self.remain_time_text.SetFontColor( 0.78, 0.78, 0.78 )
			
	def SetDisable(self):
		if self.button:
			self.button.Disable()
	def SetEnable(self):
		if self.button:
			self.button.Enable()
			
	def SetIcon(self, icon_type):
		if not self.icon_img:
			return
		if self.cur_icon_type == icon_type:
			return
		
		if DIVISION_EMPTY == icon_type:
			self.icon_img.LoadImage( EMPTY_ICON_PATH )
		elif DIVISION_POST == icon_type:
			self.icon_img.LoadImage( POST_ICON_PATH )
		elif DIVISION_ITEM == icon_type:
			self.icon_img.LoadImage( ITEM_ICON_PATH )
		elif DIVISION_GM == icon_type:
			self.icon_img.LoadImage( GM_ICON_PATH )
		else:
			return
			
		self.cur_icon_type = icon_type
			
	def SetTitle(self, title):
		if not self.title_text:
			return
		if len(title) > TITLE_MAX_LEN:
			title = title[:TITLE_MAX_LEN]
			
		self.title_text.SetText( title )
		
	def SetRemainTime(self, end_time):
		if not self.remain_time_text:
			return
		leftSec = max(0, end_time - app.GetGlobalTimeStamp())
		if leftSec > 0:
			self.remain_time_text.SetText( self.SecondToDH(leftSec) )
			
	def Clear(self):
		self.SetConfirmColor(0)
		self.SetDataIndex(-1)
		
		self.cur_icon_type = DIVISION_EMPTY
		self.icon_img.LoadImage( EMPTY_ICON_PATH )
		
		self.SetEnable()
		
		if self.title_text:
			self.title_text.SetText("")
		if self.remain_time_text:
			self.remain_time_text.SetText("")
			
			
class PostRead(ui.ScriptWindow):
	def __init__(self, close_call_back_func):
		ui.ScriptWindow.__init__(self)
		self.isLoaded						= 0
		self.close_call_back_func			= ui.__mem_func__(close_call_back_func)
		self.tooltipItem					= None
		
		self.board							= None
		self.from_text						= None
		self.title_text						= None
		self.message_text					= None
		self.won_text						= None
		self.yang_text						= None
		self.item_slot						= None
		self.block_button					= None
		self.delete_button					= None
		self.recv_button					= None
		
		self.block_question_dlg				= None
		self.get_items_question_dlg			= None
		self.post_delete_question_dlg		= None
		
		self.data_index						= -1
		self.item_index						= -1
		self.yang							= 0
		self.won							= 0
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.isLoaded						= 0
		self.close_call_back_func			= None
		self.tooltipItem					= None
		
		self.board							= None
		self.from_text						= None
		self.title_text						= None
		self.message_text					= None
		self.won_text						= None
		self.yang_text						= None
		self.item_slot						= None
		self.block_button					= None
		self.delete_button					= None
		self.recv_button					= None
		
		self.block_question_dlg				= None
		self.get_items_question_dlg			= None
		self.post_delete_question_dlg		= None
		
		self.data_index						= -1
		self.item_index						= -1
		self.yang							= 0
		self.won							= 0
		
	def Close(self):
		if self.close_call_back_func:
			self.close_call_back_func()
			
		self.Hide()
		
		if self.block_question_dlg:
			self.block_question_dlg.Close()
		if self.get_items_question_dlg:
			self.get_items_question_dlg.Close()
		if self.post_delete_question_dlg:
			self.post_delete_question_dlg.Close()
		
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def Show(self):
		self.__LoadWindow()
		ui.Window.Show(self)
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded	= 1
		
		## Load Script
		try:
			LoadScript(self, "UIScript/PostRead.py")
		except:
			import exception
			exception.Abort("PostRead.LoadWindow.LoadObject")
		
		## object
		try:
			self.__BindObject()
		except:
			import exception
			exception.Abort("PostRead.LoadWindow.__BindObject")
			
		## event
		try:
			self.__BindEvent()
		except:
			import exception
			exception.Abort("PostRead.LoadWindow.__BindEvent")
			
		self.Hide()
		
	def __BindObject(self):
		self.board			= self.GetChild("board")
		self.from_text		= self.GetChild("from_text")
		self.title_text		= self.GetChild("title_text")
		self.message_text	= self.GetChild("message_line")
		self.won_text		= self.GetChild("won_text")
		self.yang_text		= self.GetChild("yang_text")
		self.item_slot		= self.GetChild("item_slot")
		self.block_button	= self.GetChild("block_button")
		self.delete_button	= self.GetChild("delete_button")
		self.recv_button	= self.GetChild("recv_button")
		
		if localeInfo.IsARABIC():
			self.GetChild("BGImg").LeftRightReverse()
			self.delete_button.LeftRightReverse()
			self.recv_button.LeftRightReverse()
			
	def __BindEvent(self):
		if self.board:
			self.board.SetCloseEvent( ui.__mem_func__(self.Close) )
			
		if self.message_text:
			self.message_text.SetMax(100)
			self.message_text.SetLimitWidth(235)
			self.message_text.SetMultiLine()
			
		if self.won_text:
			self.won_text.SetText("0")
		if self.yang_text:
			self.yang_text.SetText("0")
			
		if self.item_slot:
			self.item_slot.SetOverInItemEvent( ui.__mem_func__(self.OverInItem) )
			self.item_slot.SetOverOutItemEvent( ui.__mem_func__(self.OverOutItem) )
			self.item_slot.SetUnselectItemSlotEvent( ui.__mem_func__(self.__ClickRecvButton) )
			
		if self.block_button:
			self.block_button.SetEvent( ui.__mem_func__(self.__ClickBlockButton) )
			self.block_button.SetToolTipText( uiScriptLocale.MAILBOX_POST_READ_BLOCK )
		if self.delete_button:
			self.delete_button.SetEvent( ui.__mem_func__(self.__ClickDeleteButton) )
		if self.recv_button:
			self.recv_button.SetEvent( ui.__mem_func__(self.__ClickRecvButton) )	
		
	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip
		
	def Clear(self):
		if self.from_text:
			self.from_text.SetText("")
		if self.title_text:
			self.title_text.SetText("")
		if self.message_text:
			self.message_text.SetText("")
		if self.won_text:
			self.won_text.SetText("0")
		if self.yang_text:
			self.yang_text.SetText("0")
			
		if self.item_slot:
			self.item_slot.SetItemSlot(0, 0)
			self.item_slot.RefreshSlot()
			
		self.data_index	= -1	
		self.item_index = -1
		self.yang		= 0
		self.won		= 0
		
		
	def __ClickBlockButton(self):
		if self.block_question_dlg:
			del self.block_question_dlg
			self.block_question_dlg = None
		
		from_name = ""
		if self.from_text:
			from_name = self.from_text.GetText()
		if from_name == "":
			return
		
		self.block_question_dlg = uiCommon.QuestionDialog()
		self.block_question_dlg.SetText(localeInfo.MAILBOX_POST_READ_BLOCK % (from_name))
		self.block_question_dlg.SetAcceptEvent( ui.__mem_func__(self.__BlockName) )
		self.block_question_dlg.SetCancelEvent( ui.__mem_func__(self.__CloseBlockQuestionDlg) )
		self.block_question_dlg.SetWidth( self.GetWidth() )
		self.block_question_dlg.Open()
		(x,y)	= self.GetLocalPosition()
		height	= self.GetHeight()
		self.block_question_dlg.SetPosition(x, y + height / 3)

	def __BlockName(self):
		from_name = ""
		if self.from_text:
			from_name = self.from_text.GetText()
		if from_name == "":
			return
		# net.SendMessengerBlockAddByNamePacket( from_name )
		self.__CloseBlockQuestionDlg()
		
	def __CloseBlockQuestionDlg(self):
		if not self.block_question_dlg:
			return
		self.block_question_dlg.Close()
		
	def __ClickDeleteButton(self):		
		is_get_items = False
		# ���� �������� �ִ���?
		if -1 != self.item_index:
			is_get_items = True			
		# ���� yang �� �ִ���?
		if self.yang > 0:
			is_get_items = True			
		# ���� won �� �ִ���?
		if self.won > 0:
			is_get_items = True
			
		# ���� ��ǰ�� �ִ�.
		if True == is_get_items:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_DELETE_FAIL_EXIST_ITEMS)
			return
			
		if self.post_delete_question_dlg:
			del self.post_delete_question_dlg
			self.post_delete_question_dlg = None
		
		self.post_delete_question_dlg = uiCommon.QuestionDialog()
		self.post_delete_question_dlg.SetText(localeInfo.MAILBOX_POST_DELETE_QUESTION)
		self.post_delete_question_dlg.SetAcceptEvent( ui.__mem_func__(self.__SendPostDelete) )
		self.post_delete_question_dlg.SetCancelEvent( ui.__mem_func__(self.__ClosePostDeleteQuestionDlg) )
		self.post_delete_question_dlg.SetWidth( self.GetWidth() )
		self.post_delete_question_dlg.Open()
		(x,y)	= self.GetLocalPosition()
		height	= self.GetHeight()
		self.post_delete_question_dlg.SetPosition(x, y + height / 3)
		
	def __SendPostDelete(self):
		net.SendPostDelete( self.data_index )
		self.__ClosePostDeleteQuestionDlg()
	
	def __ClosePostDeleteQuestionDlg(self):
		if not self.post_delete_question_dlg:
			return
		self.post_delete_question_dlg.Close()
				
	def __ClickRecvButton(self):
		if not self.from_text:
			return
		
		# if True == messenger.IsBlockFriendByName( self.from_text.GetText() ):
		# 	print "������ ����� ������ ���� �� ����."
		# 	return
		
		is_get_items = False
		# ���� �������� �ִ���?
		if -1 != self.item_index:
			is_get_items = True			
		# ���� yang �� �ִ���?
		if self.yang > 0:
			is_get_items = True			
		# ���� won �� �ִ���?
		if self.won > 0:
			is_get_items = True
			
		# ���� ��ǰ�� ����.
		if False == is_get_items:
			print "���� ��ǰ�� ����."
			return			
			
		if self.get_items_question_dlg:
			del self.get_items_question_dlg
			self.get_items_question_dlg = None
		
		self.get_items_question_dlg = uiCommon.QuestionDialog()
		self.get_items_question_dlg.SetText(localeInfo.MAILBOX_POST_GET_ITEMS_QUESTION)
		self.get_items_question_dlg.SetAcceptEvent( ui.__mem_func__(self.__SendPostGetItems) )
		self.get_items_question_dlg.SetCancelEvent( ui.__mem_func__(self.__CloseGetItemsQuestionDlg) )
		self.get_items_question_dlg.SetWidth( self.GetWidth() )
		self.get_items_question_dlg.Open()
		(x,y)	= self.GetLocalPosition()
		height	= self.GetHeight()
		self.get_items_question_dlg.SetPosition(x, y + height / 3)
		
	def __SendPostGetItems(self):
		net.SendPostGetItems( self.data_index )
		self.__CloseGetItemsQuestionDlg()
		
	def __CloseGetItemsQuestionDlg(self):
		if not self.get_items_question_dlg:
			return
		self.get_items_question_dlg.Close()
		
	def OverInItem(self):
		if not self.tooltipItem:
			return
			
		if -1 == self.item_index:
			return
			
		self.tooltipItem.SetMailBoxItem( self.item_index )
		
	def OverOutItem(self):
		if not self.tooltipItem:
			return
			
		self.tooltipItem.HideToolTip()
	
	def GetDataIndex(self):
		return self.data_index
		
	def SetDataIndex(self, data_index):
		self.data_index = data_index
		
	def SetFromName(self, from_name):
		if self.from_text:
			self.from_text.SetText( from_name )
			
	def SetTitle(self, title):
		if self.title_text:
			self.title_text.SetText( title )
			
	def SetMessage(self, message):
		if self.message_text:
			self.message_text.SetText( message )
			
	def SetYang(self, yang):
		self.yang = yang
		if self.yang_text:
			self.yang_text.SetText( localeInfo.NumberToMoneyString(yang) )
			
	def SetCheque(self, cheque):
		self.won = cheque
		if self.won_text:
			self.won_text.SetText( localeInfo.NumberToMoneyString(cheque) )
		
	def SetItem(self, index):
		if not self.item_slot:
			return
		if not self.tooltipItem:
			return

		item_data = mail.GetMailItemData( index )
		if None == item_data:
			self.item_index = -1
			self.item_slot.SetItemSlot(0, 0)
		else:
			self.item_index = index
			(vnum, count) = item_data
			self.item_slot.SetItemSlot(0, vnum, count)
			self.item_slot.RefreshSlot()
			
class PostWrite(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded						= 0
		self.inven							= None
		self.ds_window						= None
		self.interface						= None
		self.tooltipItem					= None
		self.send_money_dialog				= None
		self.post_write_question_dlg		= None
		
		self.board							= None
		self.confirm_button					= None
		self.friend_select_button			= None
		self.won_yang_window				= None
		self.won_text						= None
		self.yang_text						= None
		self.send_button					= None
		self.close_button					= None
		self.item_slot						= None
		self.render_box_list				= []
		self.to_name						= ""
		self.to_editline					= None
		self.title_editline					= None
		self.message_editline				= None
		self.mouse_over_img					= None
		self.friend_select_img_window		= None
		self.friend_select_text_window		= None
		self.friend_select_window			= None
		self.friend_select_scroll			= None
		self.message_count_text				= None
		
		self.friend_select_window_height	= 0
		self.friend_select_window_open		= False
		self.friend_img_list				= []
		self.friend_text_list				= []
		self.friend_window_list				= []
		
		self.is_attach_item					= False
		self.send_item_window				= player.RESERVED_WINDOW
		self.send_item_pos					= WORD_MAX
		self.send_money_won					= 0
		self.send_money_yang				= 0
		
		self.Diff							= 0
		self.ScrollPos						= 0
		
		self.friend_names_tuple				= ()
		
		self.is_name_checked				= False
		self.confirm_button_flash			= False
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.isLoaded						= 0
		self.inven							= None
		self.ds_window						= None
		self.interface						= None
		self.tooltipItem					= None
		
		if self.send_money_dialog:
			self.send_money_dialog.Destroy()
			del self.send_money_dialog
		self.send_money_dialog				= None
		
		if self.post_write_question_dlg:
			del self.post_write_question_dlg
		self.post_write_question_dlg		= None
		
		self.board							= None
		self.confirm_button					= None
		self.friend_select_button			= None
		self.won_yang_window				= None
		self.won_text						= None
		self.yang_text						= None
		self.send_button					= None
		self.close_button					= None
		self.item_slot						= None
		self.render_box_list				= []
		self.to_name						= ""
		self.to_editline					= None
		self.title_editline					= None
		self.message_editline				= None
		self.mouse_over_img					= None
		self.friend_select_img_window		= None
		self.friend_select_text_window		= None
		self.friend_select_window			= None
		self.friend_select_scroll			= None
		self.message_count_text				= None
		
		self.friend_select_window_height	= 0
		self.friend_select_window_open		= False
		self.friend_img_list				= []
		self.friend_text_list				= []
		self.friend_window_list				= []
				
		self.is_attach_item					= False
		self.send_item_window				= player.RESERVED_WINDOW
		self.send_item_pos					= WORD_MAX
		self.send_money_won					= 0
		self.send_money_yang				= 0
		
		self.Diff							= 0
		self.ScrollPos						= 0
		
		self.friend_names_tuple				= ()
		
		self.is_name_checked				= False
		self.confirm_button_flash			= False
		
	def Close(self):
		self.Clear()
		self.Hide()		
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def Show(self):
		self.__LoadWindow()
		self.__RefreshFriendNameButton()
		ui.Window.Show(self)
		if self.to_editline:
			self.to_editline.SetFocus()
		
	def Clear(self):
		self.SetOnTopWindowNone()
		self.__ClearSlotItem()
		
		self.__FriendSelectWindow( False )
		
		self.to_name = ""
		
		if self.to_editline:
			self.to_editline.SetText("")
			self.to_editline.KillFocus()
		if self.title_editline:
			self.title_editline.SetText("")
			self.title_editline.KillFocus()
		if self.message_editline:
			self.message_editline.SetText("")
			self.message_editline.KillFocus()
		if self.won_text:
			self.won_text.SetText("0")
		if self.yang_text:
			self.yang_text.SetText("0")
		if self.message_count_text:
			self.message_count_text.SetText("%3d / 100" % 0)
		
		self.is_attach_item			= False
		self.send_item_window		= player.RESERVED_WINDOW
		self.send_item_pos			= WORD_MAX
		self.send_money_won			= 0
		self.send_money_yang		= 0
		self.is_name_checked		= False
		self.confirm_button_flash	= False
		if self.confirm_button:
			self.confirm_button.DisableFlash()
		
		if self.send_money_dialog:
			self.send_money_dialog.Hide()
		
		if self.post_write_question_dlg:
			self.post_write_question_dlg.Close()
			del self.post_write_question_dlg
		self.post_write_question_dlg		= None
		
	def SetOnTopWindowNone(self):
		if not self.interface:
			return
			
		self.interface.SetOnTopWindow(player.ON_TOP_WND_NONE)
		self.interface.RefreshMarkInventoryBag()
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded	= 1
		
		## Load Script
		try:
			LoadScript(self, "UIScript/PostWrite.py")
		except:
			import exception
			exception.Abort("PostWrite.LoadWindow.LoadObject")
		
		## object
		try:
			self.__BindObject()
		except:
			import exception
			exception.Abort("PostWrite.LoadWindow.__BindObject")
			
		## event
		try:
			self.__BindEvent()
		except:
			import exception
			exception.Abort("PostWrite.LoadWindow.__BindEvent")
			
		self.__CreateSendMoneyDialog()
		self.__CreateFriendNameButton()
		self.Hide()
		
	def __BindObject(self):
		self.board						= self.GetChild("board")
		self.confirm_button				= self.GetChild("post_write_confirm_button")
		self.friend_select_button		= self.GetChild("post_friend_select_button")
		self.won_yang_window			= self.GetChild("post_won_yang_window")
		self.won_text					= self.GetChild("won_text")
		self.yang_text					= self.GetChild("yang_text")
		self.send_button				= self.GetChild("post_send_button")
		self.close_button				= self.GetChild("post_close_button")
		self.item_slot					= self.GetChild("item_slot")
		self.to_editline				= self.GetChild("to_editline")
		self.title_editline				= self.GetChild("title_editline")
		self.message_editline			= self.GetChild("message_line")
		self.message_count_text			= self.GetChild("msg_count_text")
		
		self.friend_select_img_window	= self.GetChild("friend_select_img_window")
		self.friend_select_text_window	= self.GetChild("friend_select_text_window")
		self.friend_select_window		= self.GetChild("friend_select_window")
		self.friend_select_scroll		= self.GetChild("post_friend_scrollbar")
		self.mouse_over_img				= self.GetChild("mouse_over_image")
		self.mouse_over_img.Hide()
		
		self.render_box_list.append( self.GetChild("renderbox1") )
		self.render_box_list.append( self.GetChild("renderbox2") )
		self.render_box_list.append( self.GetChild("renderbox3") )
		
		if localeInfo.IsARABIC():
			self.GetChild("BGImg").LeftRightReverse()
			self.send_button.LeftRightReverse()
			self.close_button.LeftRightReverse()
			
			
	def __BindEvent(self):
		if self.board:
			self.board.SetCloseEvent( ui.__mem_func__(self.Close) )
		if self.confirm_button:
			self.confirm_button.SetEvent( ui.__mem_func__(self.__ClickConfirmButton) )
			self.confirm_button.SetToolTipText( uiScriptLocale.MAILBOX_POST_WRITE_CONFIRM_TEXT )
		if self.friend_select_button:
			self.friend_select_button.SetEvent( ui.__mem_func__(self.__ClickFriendSelectButton) )
		if self.won_yang_window:
			self.won_yang_window.SetOnMouseLeftButtonUpEvent( ui.__mem_func__(self.__ClickWonYangWindow) )
		if self.send_button:
			self.send_button.SetEvent( ui.__mem_func__(self.__OpenPostWriteQuestionDialog) )
			
		if self.close_button:
			self.close_button.SetEvent( ui.__mem_func__(self.Close) )
		
		if self.to_editline:
			self.to_editline.SetEscapeEvent( ui.__mem_func__(self.OnPressEscapeKey) )
			self.to_editline.SetReturnEvent( ui.__mem_func__(self.__ClickConfirmButton) )
			self.to_editline.SetTabEvent( ui.__mem_func__(self.__ToEditLineTabEvent) )
			self.to_editline.KillFocus()
			
		if self.title_editline:
			self.title_editline.SetEscapeEvent( ui.__mem_func__(self.OnPressEscapeKey) )
			self.title_editline.SetTabEvent( ui.__mem_func__(self.__TitleEditLineTabEvent) )
			self.title_editline.KillFocus()
		
		if self.message_editline:
			self.message_editline.SetEscapeEvent( ui.__mem_func__(self.OnPressEscapeKey) )
			self.message_editline.SetReturnEvent( ui.__mem_func__(self.__OpenPostWriteQuestionDialog) )
			self.message_editline.SetTabEvent( ui.__mem_func__(self.__MessageEditLineTabEvent) )
			self.message_editline.KillFocus()
		
		if self.won_text:
			self.won_text.SetText("0")
		if self.yang_text:
			self.yang_text.SetText("0")
		if self.message_count_text:
			self.message_count_text.SetText("%3d / 100" % 0)
			
			if localeInfo.IsARABIC():
				self.message_count_text.SetWindowHorizontalAlignLeft()
			
		if self.item_slot:
			self.item_slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot) )
			self.item_slot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot) )
			self.item_slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot) )
			self.item_slot.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot) )
			self.item_slot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem) )
			self.item_slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			
		if self.render_box_list:
			for box in self.render_box_list:
				box.SetOnMouseLeftButtonUpEvent( ui.__mem_func__(self.__ClickRenderBox) )
				box.Hide()
				
		if self.friend_select_scroll:
			self.friend_select_scroll.SetUpButtonUpVisual( "d:/ymir work/ui/game/mailbox/scroll_up_arrow_button_default.sub" )
			self.friend_select_scroll.SetUpButtonOverVisual( "d:/ymir work/ui/game/mailbox/scroll_up_arrow_button_over.sub" )
			self.friend_select_scroll.SetUpButtonDownVisual( "d:/ymir work/ui/game/mailbox/scroll_up_arrow_button_down.sub" )
			
			self.friend_select_scroll.SetDownButtonUpVisual( "d:/ymir work/ui/game/mailbox/scroll_down_arrow_button_default.sub" )
			self.friend_select_scroll.SetDownButtonOverVisual( "d:/ymir work/ui/game/mailbox/scroll_down_arrow_button_over.sub" )
			self.friend_select_scroll.SetDownButtonDownVisual( "d:/ymir work/ui/game/mailbox/scroll_down_arrow_button_down.sub" )
			self.friend_select_scroll.SetUpButtonSizeRefresh()
			self.friend_select_scroll.SetScrollEvent( ui.__mem_func__(self.OnScroll) )
			self.friend_select_scroll.Hide()
	
	def __ToEditLineTabEvent(self):
		self.to_editline.KillFocus()
		self.message_editline.KillFocus()
		self.title_editline.SetFocus()
		
		
	def __TitleEditLineTabEvent(self):
		self.to_editline.KillFocus()
		self.title_editline.KillFocus()
		self.message_editline.SetFocus()

	def __MessageEditLineTabEvent(self):
		self.to_editline.SetFocus()
		self.title_editline.KillFocus()
		self.message_editline.KillFocus()
	
	def __CreateFriendNameButton(self):
		if not self.friend_select_img_window:
			return
		if not self.friend_select_text_window:
			return
		if not self.friend_select_window:
			return
		if not self.friend_select_scroll:
			return
		
		self.friend_select_window_height  = 0
		
		##
		create_count = FRIEND_SELECT_UI_SHOW_MAX
		for i in xrange( FRIEND_SELECT_UI_SHOW_MAX ):
			## image
			img = ui.ImageBox()
			img.SetParent( self.friend_select_img_window )
			
			if 1 == create_count:
				img.LoadImage( "d:/ymir work/ui/game/mailbox/friend_list_pattern_only.sub" )						
			elif i == 0:
				img.LoadImage( "d:/ymir work/ui/game/mailbox/friend_list_pattern_top.sub" )
			elif i == create_count - 1:
				img.LoadImage( "d:/ymir work/ui/game/mailbox/friend_list_pattern_bottom.sub" )
			else:
				img.LoadImage( "d:/ymir work/ui/game/mailbox/friend_list_pattern_middle.sub" )
				
			img_width	= img.GetWidth()
			img_height	= img.GetHeight()
			img.SetPosition( 0, self.friend_select_window_height )
			img.Show()
			self.friend_img_list.append( img )
			
			## text
			text = ui.TextLine()
			text.SetParent( self.friend_select_text_window )
			text.SetPosition( 5, self.friend_select_window_height + img_height / 2 )
			text.SetVerticalAlignCenter()
			text.SetHorizontalAlignLeft()
			text.SetText( "" )
			text.SetSize( 115, img_height )
			text.Show()
			self.friend_text_list.append( text )
			
			## click area
			window = ui.ScriptWindow()
			window.SetParent( self.friend_select_window )
			window.SetPosition( 0, self.friend_select_window_height )
			window.SetSize(131, img_height)
			window.SetOnMouseLeftButtonUpEvent( ui.__mem_func__(self.__ClickFriendName), i )
			window.SetOverEvent( ui.__mem_func__(self.__FriendNameOver), i )
			window.SetOverOutEvent( ui.__mem_func__(self.__FriendNameOverOut), i )
			window.AddFlag("not_capture")
			window.Show()
			self.friend_window_list.append( window )
			
			self.friend_select_window_height = self.friend_select_window_height + img_height
			
			
		self.friend_select_img_window.SetSize( 131, self.friend_select_window_height )
		self.friend_select_img_window.Hide()
		
		self.friend_select_text_window.SetSize( 115, self.friend_select_window_height )
		self.friend_select_text_window.Hide()
		
		self.friend_select_window.SetSize( 131, self.friend_select_window_height )
		self.friend_select_window.Hide()
		
	def __RefreshFriendNameButton(self):
		if FRIEND_SELECT_UI_SHOW_MAX != len(self.friend_img_list):
			return
		if FRIEND_SELECT_UI_SHOW_MAX != len(self.friend_text_list):
			return
		if FRIEND_SELECT_UI_SHOW_MAX != len(self.friend_window_list):
			return
		if not self.friend_select_img_window:
			return
		if not self.friend_select_text_window:
			return
		if not self.friend_select_window:
			return
		if not self.friend_select_scroll:
			return
		
		for i in xrange( FRIEND_SELECT_UI_SHOW_MAX ):
			self.friend_img_list[i].Hide()		## image
			self.friend_text_list[i].Hide()		## text
			self.friend_window_list[i].Hide()	## click area
			
		
		self.friend_names_tuple 			= messenger.GetFriendNames() # get friend names tuple
		friend_list_len						= len( self.friend_names_tuple )
		view_count							= FRIEND_SELECT_UI_SHOW_MAX if friend_list_len > FRIEND_SELECT_UI_SHOW_MAX else friend_list_len
		self.friend_select_window_height	= 0
		
		for i in xrange( view_count ):
			if 1 == view_count:
				self.friend_img_list[i].LoadImage( "d:/ymir work/ui/game/mailbox/friend_list_pattern_only.sub" )						
			elif i == 0:
				self.friend_img_list[i].LoadImage( "d:/ymir work/ui/game/mailbox/friend_list_pattern_top.sub" )
			elif i == view_count - 1:
				self.friend_img_list[i].LoadImage( "d:/ymir work/ui/game/mailbox/friend_list_pattern_bottom.sub" )
			else:
				self.friend_img_list[i].LoadImage( "d:/ymir work/ui/game/mailbox/friend_list_pattern_middle.sub" )
			
			self.friend_img_list[i].Show()
			self.friend_text_list[i].Show()
			self.friend_window_list[i].Show()
			
			img_height = self.friend_img_list[i].GetHeight()
			self.friend_img_list[i].SetPosition( 0, self.friend_select_window_height )
			
			if localeInfo.IsARABIC():
				self.friend_text_list[i].SetPosition( -5, self.friend_select_window_height + img_height / 2 )
			else:	
				self.friend_text_list[i].SetPosition( 5, self.friend_select_window_height + img_height / 2 )
				
			self.friend_text_list[i].SetText( self.friend_names_tuple[i] )
			self.friend_text_list[i].SetSize( 115, img_height )
				
			self.friend_window_list[i].SetPosition( 0, self.friend_select_window_height )
			self.friend_window_list[i].SetSize(131, img_height)
			
			self.friend_select_window_height = self.friend_select_window_height + img_height
			
			
		self.friend_select_img_window.SetSize( 131, self.friend_select_window_height )
		self.friend_select_img_window.Hide()

		self.friend_select_text_window.SetSize( 115, self.friend_select_window_height )
		self.friend_select_text_window.Hide()

		self.friend_select_window.SetSize( 131, self.friend_select_window_height )
		self.friend_select_window.Hide()

		self.friend_select_scroll.SetScrollBarSize( self.friend_select_window_height - 2 )
		self.Diff = friend_list_len - FRIEND_SELECT_UI_SHOW_MAX
		if self.Diff > 0:
			stepSize = 1.0 / self.Diff
			self.friend_select_scroll.SetScrollStep( stepSize )
			self.ScrollPos = 0
			self.__RefreshFriendListText()

	def __CreateSendMoneyDialog(self):
		if self.send_money_dialog:
			return
			
		self.send_money_dialog = uiPickMoney.PickMoneyDialog()
		self.send_money_dialog.LoadDialog()
		self.send_money_dialog.SetMax(7)
		self.send_money_dialog.Hide()
		
	def __OpenPostWriteQuestionDialog(self):
		
		if player.GetStatus(player.LEVEL) < POST_WRITE_LIMIT_LEVEL:
			chat.AppendChat( chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_LEVEL_LIMIT )
			return
			
		if self.to_editline.GetText() == "":
			chat.AppendChat( chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_SEND_FAIL_EMPTY_NAME )
			return
			
		if False == self.is_name_checked:
			chat.AppendChat( chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_NAME_CHECK )
			return
				
		if self.title_editline.GetText() == "":
			chat.AppendChat( chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_SEND_FAIL_EMPTY_TITLE )
			return	
			
		if self.post_write_question_dlg:
			del self.post_write_question_dlg
			self.post_write_question_dlg = None
			
		self.post_write_question_dlg = uiCommon.QuestionDialog2()
		self.post_write_question_dlg.SetText1(localeInfo.MAILBOX_POST_WRITE_QUESTION1 % (self.to_name))
		self.post_write_question_dlg.SetText2(localeInfo.MAILBOX_POST_WRITE_QUESTION2 % (POST_WRITE_COST))
		self.post_write_question_dlg.SetAcceptEvent( ui.__mem_func__(self.__SendPostWrite) )
		self.post_write_question_dlg.SetCancelEvent( ui.__mem_func__(self.__ClosePostWriteQuestionDialog) )
		self.post_write_question_dlg.SetWidth( self.GetWidth() )
		self.post_write_question_dlg.Open()
		(x,y)	= self.GetLocalPosition()
		height	= self.GetHeight()
		self.post_write_question_dlg.SetPosition(x, y + height / 3)
		
	def __ClosePostWriteQuestionDialog(self):
		if not self.post_write_question_dlg:
			return
		self.post_write_question_dlg.Close()
		
	def __ClickWonYangWindow(self):		
		
		if not self.send_money_dialog:
			return
			
		if True == self.send_money_dialog.IsShow():
			self.send_money_dialog.SetTop()
			return
			
		curMoney = player.GetElk()
		if app.ENABLE_CHEQUE_SYSTEM:
			curCheque = player.GetCheque()
		else:
			curCheque = 0
		
		if curMoney < 0:
			curMoney = 0
		
		if curMoney <= 0 and curCheque <= 0:
			return
			
		if curMoney > MAX_YANG:
			curMoney = MAX_YANG
		if curCheque > MAX_CHEQUE:
			curCheque = MAX_CHEQUE
					
		self.send_money_dialog.SetTitleName( localeInfo.MAILBOX_POST_WRITE_SEND_MONEY_TITLE )
		self.send_money_dialog.SetAcceptEvent( ui.__mem_func__(self.SendMoneyAccept) )
		self.send_money_dialog.SetMax(7)
		if app.ENABLE_CHEQUE_SYSTEM:
			self.send_money_dialog.Open(curMoney, curCheque)
		else:
			self.send_money_dialog.Open(curMoney)
		
			
	def SendMoneyAccept(self, money, cheque = 0):
		if self.won_text:
			self.won_text.SetText( localeInfo.NumberToMoneyString(cheque) )
		if self.yang_text:
			self.yang_text.SetText( localeInfo.NumberToMoneyString(money) )
		
		self.send_money_won				= cheque
		self.send_money_yang			= money
		
	def __FriendNameOver(self, index):
		if not self.mouse_over_img:
			return
			
		img = self.friend_img_list[index]
		(x, y) = img.GetLocalPosition()
		
		if localeInfo.IsARABIC():
			img_width = img.GetWidth()
			self.mouse_over_img.SetPosition( 92 + x + img_width, 51 + y )
		else:
			self.mouse_over_img.SetPosition( 92 + x, 51 + y )
		
		self.mouse_over_img.Show()
			
	def __FriendNameOverOut(self, index):
		if not self.mouse_over_img:
			return
		self.mouse_over_img.Hide()
		
	def __ClickFriendName(self, i):
		self.__FriendSelectWindow( False )
		
		idx = i + self.ScrollPos
		
		self.to_name = self.friend_names_tuple[idx]
		self.to_editline.SetText( self.friend_names_tuple[idx] )
		
	def OnScroll(self):
		self.__RefreshFriendListText()
		
	def __RefreshFriendListText(self):
		self.ScrollPos = int(self.friend_select_scroll.GetPos() * self.Diff)
		
		for i in xrange(FRIEND_SELECT_UI_SHOW_MAX):
			idx = i + self.ScrollPos
		
			text = self.friend_text_list[i]
			text.SetText( self.friend_names_tuple[idx] )			
			
	def __ClickConfirmButton(self):
		if not self.to_editline:
			return
		if not self.title_editline:
			return
		if not self.message_editline:
			return
			
		if True == self.is_name_checked:
			return
		
		if self.to_editline.GetText() == "":
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_NAME_EMPTY)
			return
			
		net.SendPostWriteConfirm( self.to_editline.GetText() )
		
		self.to_editline.KillFocus()
		self.title_editline.KillFocus()		
		self.message_editline.KillFocus()
		
	def __ClickFriendSelectButton(self):
		if None == self.friend_names_tuple:
			return
		if 0 == len(self.friend_names_tuple):
			return
		self.__FriendSelectWindow( not self.friend_select_window_open )
		
	def __FriendSelectWindow(self, show):
		if True == show:
			self.friend_select_window_open = True
			if self.friend_select_img_window:
				self.friend_select_img_window.Show()
			if self.friend_select_text_window:
				self.friend_select_text_window.Show()
			if self.friend_select_window:
				self.friend_select_window.Show()
			if self.friend_select_scroll and len(self.friend_names_tuple) > FRIEND_SELECT_UI_SHOW_MAX:
				self.friend_select_scroll.Show()
		else:
			self.friend_select_window_open = False
			if self.friend_select_img_window:
				self.friend_select_img_window.Hide()
			if self.friend_select_text_window:
				self.friend_select_text_window.Hide()
			if self.friend_select_window:
				self.friend_select_window.Hide()
			if self.friend_select_scroll:
				self.friend_select_scroll.Hide()
		
	def __SendPostWrite(self):
		
		if player.GetStatus(player.LEVEL) < POST_WRITE_LIMIT_LEVEL:
			chat.AppendChat( chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_LEVEL_LIMIT )
			return
			
		if "" == self.to_name:
			chat.AppendChat( chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_SEND_FAIL_EMPTY_NAME )
			return
			
		if self.title_editline.GetText() == "":
			chat.AppendChat( chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_SEND_FAIL_EMPTY_TITLE )
			return
			
		if self.send_money_yang > MAX_YANG:
			return
						
		curMoney = player.GetElk()
		if self.send_money_yang + POST_WRITE_COST > curMoney:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_MONEY_NOT_ENOUGHT)
			return
		
		if self.send_money_won > MAX_CHEQUE:
			return
			
		net.SendPostWrite( self.to_name
			, self.title_editline.GetText()
			, self.message_editline.GetText()
			, self.send_item_window
			, self.send_item_pos
			, self.send_money_yang
			, self.send_money_won
		)
		
		self.__ClosePostWriteQuestionDialog()
		
		
	## Item Slot Event
	## �κ� -> post item
	## slot �� �������� �������ش�
	def SelectEmptySlot(self, selectedSlotPos):
		if not self.item_slot:
			return		
		if True == self.is_attach_item:
			return
		if not mouseModule.mouseController.isAttached():
			return
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return
		# if player.GetAcceRefineWindowOpen() == 1:
		# 	return
		if app.BL_TRANSMUTATION_SYSTEM:
			if player.GetChangeLookWindowOpen() == 1:
				return
			
		attachedSlotType	= mouseModule.mouseController.GetAttachedType()
		attachedSlotPos		= mouseModule.mouseController.GetAttachedSlotNumber()
		attachedItemIndex	= mouseModule.mouseController.GetAttachedItemIndex()
		attachedItemCount	= mouseModule.mouseController.GetAttachedItemCount()
				
		mouseModule.mouseController.DeattachObject()
		
		## �κ��丮, ��ȥ���κ��� �����۸� �����ϴ�
		if not attachedSlotType in [player.SLOT_TYPE_INVENTORY, player.SLOT_TYPE_DRAGON_SOUL_INVENTORY]:
			return
			
		window_type = player.INVENTORY
		if player.SLOT_TYPE_DRAGON_SOUL_INVENTORY== attachedSlotType:
			window_type = player.DRAGON_SOUL_INVENTORY
			
		if True == self.CantPostItemSlot( attachedSlotPos, window_type ):
			# ����� �� ���� ������ �Դϴ�
			return
						
		item_count = player.GetItemCount( window_type, attachedSlotPos )
		if attachedItemCount != item_count:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_CAN_NOT_SPLIT_ITEM)
			return
		
		item.SelectItem( attachedItemIndex )
		(width, height) = item.GetItemSize()
		
		self.item_slot.SetItemSlot(0, attachedItemIndex, attachedItemCount)
		self.item_slot.RefreshSlot()
		
		for i in xrange(height, 3):
			self.render_box_list[i].Show()			
			
		self.is_attach_item		= True
		self.send_item_window	= window_type
		self.send_item_pos		= attachedSlotPos		
		
	## slot �� �������� ������ �ش�
	def SelectItemSlot(self):
		self.__ClearSlotItem()
	def UseItemSlot(self):
		self.__ClearSlotItem()
	def __ClickRenderBox(self):
		if not mouseModule.mouseController.isAttached():
			return
		self.__ClearSlotItem()
	def __ClearSlotItem(self):
		if not self.item_slot:
			return		
		if False == self.is_attach_item:
			return
		if mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_ALREADY_ITEM)
			return
			
		self.item_slot.SetItemSlot(0, 0)
		self.item_slot.RefreshSlot()
		
		for i in xrange(3):
			self.render_box_list[i].Hide()

		if self.is_attach_item and self.send_item_window == player.INVENTORY and self.send_item_pos != WORD_MAX:
			self.inven.wndItem.SetCanMouseEventSlot(self.send_item_pos)
			
		self.is_attach_item				= False
		self.send_item_window			= player.RESERVED_WINDOW
		self.send_item_pos				= WORD_MAX
		
	def OverInItem(self):
		if not self.tooltipItem:
			return
		if player.RESERVED_WINDOW == self.send_item_window:
			return
		if WORD_MAX == self.send_item_pos:
			return
		self.tooltipItem.SetInventoryItem( self.send_item_pos, self.send_item_window )
		
	def OverOutItem(self):
		if not self.tooltipItem:
			return
			
		self.tooltipItem.HideToolTip()
	
	def SetInven(self, inven):
		self.inven = inven
		
	def SetDSWindow(self, ds_window):
		self.ds_window = ds_window
		
	def BindInterface(self, interface):
		self.interface = interface
		
	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip
			
	def OnTop(self):
		if not self.interface:
			return
			
		self.interface.SetOnTopWindow(player.ON_TOP_WND_MAILBOX)
		self.interface.RefreshMarkInventoryBag()
		
	def CantPostItemSlot(self, slotIndex, slotWindow = player.INVENTORY):
		itemIndex = player.GetItemIndex( slotWindow, slotIndex )
		if itemIndex:
			if player.IsAntiFlagBySlot( slotWindow, slotIndex, item.ITEM_ANTIFLAG_GIVE ) or player.IsAntiFlagBySlot( slotWindow, slotIndex, item.ITEM_ANTIFLAG_MYSHOP ):
				return True
			else:
				return False
				
		return False
		
		
	def OnUpdate(self):
		self.__NameModifyCheck()
		self.__InvenUpdate()
		self.__DSWindowUpdate()
		self.__RefreshMessageCount()
	
	def __NameModifyCheck(self):
		if True == self.is_name_checked:
			if self.to_editline.GetText() != self.to_name:
				self.is_name_checked		= False
				self.confirm_button_flash	= False
		else:
			if self.to_editline and False == self.confirm_button_flash and False == self.to_editline.IsFocus():
				self.confirm_button_flash = True
				self.confirm_button.EnableFlash()
		
	def __InvenUpdate(self):
		if not self.inven:
			return
			
		if False == self.inven.IsShow():
			return
		
		if False == self.is_attach_item:
			return
		if player.INVENTORY != self.send_item_window:
			return
		if self.send_item_pos == WORD_MAX:
			return
		
		try:
			invenPage = self.inven.GetInventoryPageIndex()
		
			min_range = invenPage * player.INVENTORY_PAGE_SIZE
			max_range = (invenPage + 1) * player.INVENTORY_PAGE_SIZE
			
			inven_slot_pos = self.send_item_pos
			
			if min_range <= inven_slot_pos < max_range:
				inven_slot_pos = inven_slot_pos - min_range
				self.inven.wndItem.SetCantMouseEventSlot(inven_slot_pos)
		except:
			pass
			
	def __DSWindowUpdate(self):
		if not self.ds_window:
			return
			
		if False == self.ds_window.IsShow():
			return
			
		if False == self.is_attach_item:
			return
		if player.DRAGON_SOUL_INVENTORY != self.send_item_window:
			return
		if self.send_item_pos == WORD_MAX:
			return
		
		try:
			self.ds_window.SetCantMouseEventSlot( self.send_item_pos )
		except:
			pass
			
	def __RefreshMessageCount(self):
		if not self.message_count_text:
			return
			
		if True == self.message_editline.IsFocus():
			msg_text = self.message_editline.GetText()
			text_size = len(msg_text)
			
			self.message_count_text.SetText( "%3d / 100" % text_size )			
			
	def PostWriteConfirmResult(self, result):
		if mail.POST_WRITE_FAIL == result:
			# ������ ������ ����
			return
		## ĳ���� Ȯ����.
		elif mail.POST_WRITE_OK == result:
			self.to_name = self.to_editline.GetText()
			self.is_name_checked		= True
			self.confirm_button_flash	= True
			if self.confirm_button:
				self.confirm_button.DisableFlash()
				
			if self.to_editline:
				self.to_editline.KillFocus()
			if self.message_editline:
				self.message_editline.KillFocus()
			if self.title_editline:
				self.title_editline.SetFocus()
		## ��ȿ���� ���� �ɸ��� �̸�
		elif mail.POST_WRITE_INVALID_NAME == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_CONFIRM_FAIL)
		## ������ ������
		elif mail.POST_WRITE_TARGET_BLOCKED == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_CONFIRM_FAIL)
		## ������ ���� ������
		elif mail.POST_WRITE_BLOCKED_ME == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_CONFIRM_FAIL)
		## ������ �������� ������ ����
		elif mail.POST_WRITE_FULL_MAILBOX == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_CONFIRM_FULL_MAILBOX)
		
	def PostWriteResult(self, result):
		if mail.POST_WRITE_FAIL == result:
			#print "������ ������ ����"
			pass
		## ĳ���� Ȯ����.
		elif mail.POST_WRITE_OK == result:
			pass
		## ��ȿ���� ���� �ɸ��� �̸�
		elif mail.POST_WRITE_INVALID_NAME == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_CONFIRM_FAIL)
		## ������ ������
		elif mail.POST_WRITE_TARGET_BLOCKED == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_CONFIRM_FAIL)
		## ������ ���� ������
		elif mail.POST_WRITE_BLOCKED_ME == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_CONFIRM_FAIL)
		## ������ �������� ������ ����
		elif mail.POST_WRITE_FULL_MAILBOX == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_CONFIRM_FULL_MAILBOX)
		## ������ �ǹٸ��� �ʴ�
		elif mail.POST_WRITE_WRONG_TITLE == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_WRONG_TITLE)
		## ������ yang �� �����ϴ�.
		elif mail.POST_WRITE_YANG_NOT_ENOUGHT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_MONEY_NOT_ENOUGHT)
		## ������ won �� �����ϴ�.
		elif mail.POST_WRITE_WON_NOT_ENOUGHT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_MONEY_NOT_ENOUGHT)
		## ������ �ǹٸ��� �ʴ�.
		elif mail.POST_WRITE_WRONG_MESSAGE == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_WRONG_MESSAGE)
		## ������ item �� �ǹٸ��� �ʴ�.
		elif mail.POST_WRITE_WRONG_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_WRONG_ITEM)
		## ������ �����ϴ�
		elif mail.POST_WRITE_LEVEL_NOT_ENOUGHT == result:
			chat.AppendChat( chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_LEVEL_LIMIT )
			
		self.Close()
			
class MailBox(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded					= 0
		self.OpenX						= 0
		self.OpenY						= 0
		self.distance_check				= True
		
		self.inven						= None
		self.ds_window					= None
		self.interface					= None
		self.tooltipItem				= None
		
		self.board						= None
		self.post_list_window			= None
		self.post_write_button			= None
		self.prev_button				= None
		self.next_button				= None
		self.post_all_delete_button		= None
		self.post_all_get_items_button	= None
		
		self.post_list					= []
		self.post_write					= None
		self.post_read					= None
		
		self.all_delete_question_dlg	= None
		self.all_delete_popup			= None
		
		self.all_get_items_question_dlg = None
		self.all_get_items_fail_popup	= None
		
		self.post_data_dict				= {}
		self.post_add_data_dict			= {}
		
		self.cur_page					= 0
		self.active_button_index		= -1
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.isLoaded					= 0
		self.OpenX						= 0
		self.OpenY						= 0
		self.distance_check				= True
		
		self.inven						= None
		self.ds_window					= None
		self.interface					= None
		self.tooltipItem				= None
		
		self.board						= None
		self.post_list_window			= None
		self.post_write_button			= None
		self.prev_button				= None
		self.next_button				= None
		self.post_all_delete_button		= None
		self.post_all_get_items_button	= None
		
		self.post_list					= []
		if self.post_write:
			del self.post_write
		self.post_write					= None
		if self.post_read:
			del self.post_read
		self.post_read					= None
		
		self.all_delete_question_dlg	= None
		self.all_delete_popup			= None
		
		self.all_get_items_question_dlg = None
		self.all_get_items_fail_popup	= None
		
		self.post_data_dict				= {}
		self.post_add_data_dict			= {}
		
		self.cur_page					= 0
		self.active_button_index		= -1
		
	def Destroy(self):
		pass
		
	def Close(self):
		net.SendMailBoxClose()
		self.CloseClear()
		
	def CloseClear(self):
		self.distance_check = True
		
		if self.post_write:
			self.post_write.Close()
		if self.post_read:
			self.post_read.Close()
			
		self.Hide()
		self.cur_page				= 0
		self.post_data_dict			= {}
		self.post_add_data_dict		= {}
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def Show(self):
		self.__LoadWindow()
		ui.Window.Show(self)
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded	= 1
		
		## Load Script
		try:
			LoadScript(self, "UIScript/MailBox.py")
		except:
			import exception
			exception.Abort("MailBox.LoadWindow.LoadObject")
		
		## object
		try:
			self.__BindObject()
		except:
			import exception
			exception.Abort("MailBox.LoadWindow.__BindObject")
			
		## event
		try:
			self.__BindEvent()
		except:
			import exception
			exception.Abort("MailBox.LoadWindow.__BindEvent")
		
		self.__CreatePostList()
		self.Hide()
		
	def __BindObject(self):
		self.board						= self.GetChild("board")
		self.post_list_window			= self.GetChild("post_list_window")
		self.post_write_button			= self.GetChild("post_write_button")
		self.prev_button				= self.GetChild("prev_button")
		self.next_button				= self.GetChild("next_button")
		self.post_all_delete_button		= self.GetChild("post_all_delete_button")
		self.post_all_get_items_button	= self.GetChild("post_all_receive_button")
		
		if localeInfo.IsARABIC():
			self.prev_button.LeftRightReverse()
			self.next_button.LeftRightReverse()
			self.post_all_delete_button.LeftRightReverse()
			self.post_all_get_items_button.LeftRightReverse()
			
	def __BindEvent(self):
		if self.board:
			self.board.SetCloseEvent( ui.__mem_func__(self.Close) )
			
		if self.post_write_button:
			self.post_write_button.SetToolTipText( uiScriptLocale.MAILBOX_POST_WRITE_BUTTON_TEXT, 0, 36 )
			self.post_write_button.SetEvent( ui.__mem_func__(self.__ClickPostWriteButton) )
			
		if self.prev_button:
			self.prev_button.SetEvent( ui.__mem_func__(self.__ClickPrevButton) )
			
		if self.next_button:
			self.next_button.SetEvent( ui.__mem_func__(self.__ClickNextButton) )
			
		if self.post_all_delete_button:
			self.post_all_delete_button.SetEvent( ui.__mem_func__(self.__ClickAllDeleteButton) )
		
		if self.post_all_get_items_button:
			self.post_all_get_items_button.SetEvent( ui.__mem_func__(self.__ClickAllGetItemsButton) )
			
	def SetInven(self, inven):
		self.inven = inven
		
		if self.post_write:
			self.post_write.SetInven( self.inven )
			
	def SetDSWindow(self, ds_window):
		self.ds_window = ds_window
		
		if self.post_write:
			self.post_write.SetDSWindow( self.ds_window )
			
	def BindInterface(self, interface):
		self.interface = proxy(interface)
		
		if self.post_write:
			self.post_write.BindInterface( self.interface )
	
	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip
		
		if self.post_write:
			self.post_write.SetItemToolTip( self.tooltipItem )
			
	def OnUpdate(self):
		if False == self.distance_check:
			return
			
		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.OpenX) > MAILBOX_MAX_DISTANCE or abs(y - self.OpenY) > MAILBOX_MAX_DISTANCE:
			self.Close()
		
	def __CreatePostList(self):
		for button_index in xrange( POST_MAX ):
			self.post_list.append( Post( button_index, self.post_list_window, self.__ClickPost ) )
		
	# ��� ���� ��ư�� ����� ��Ǭ���� �� ������ �ƴ� �ܼ� ������ ������ �� �ִ� ��ư	
	def __ClickAllDeleteButton(self):
		if not self.post_data_dict:
			self.__OpenPostAllDeleteFailPopupDlg()
			return
		if len(self.post_data_dict) <= 0:
			self.__OpenPostAllDeleteFailPopupDlg()
			return
		
		is_send_post_all_delete = False
		
		for data in self.post_data_dict.values():
			(index, send_time, delete_time, title, is_gm_post, is_item_exist, is_confirm) = data
			if False == is_item_exist:
				is_send_post_all_delete = True
				break
				
		# ���� ������ ������ ������ ����â�� ����
		if True == is_send_post_all_delete:
			self.__OpenPostAllDeleteQuestionDlg()
		else:
			print "���� ������ ������ ����"
			
	def __OpenPostAllDeleteQuestionDlg(self):	
		if self.all_delete_question_dlg:
			del self.all_delete_question_dlg
			self.all_delete_question_dlg = None

		self.all_delete_question_dlg = uiCommon.QuestionDialog2()
		self.all_delete_question_dlg.SetText1(localeInfo.MAILBOX_POST_ALL_DELETE_QUESTION1)
		self.all_delete_question_dlg.SetText2(localeInfo.MAILBOX_POST_ALL_DELETE_QUESTION2)
		self.all_delete_question_dlg.SetAcceptEvent( ui.__mem_func__(self.__SendPostAllDelete) )
		self.all_delete_question_dlg.SetCancelEvent( ui.__mem_func__(self.__ClosePostAllDeleteQuestionDialog) )
		self.all_delete_question_dlg.SetWidth( self.GetWidth() )
		self.all_delete_question_dlg.Open()
		(x,y)	= self.GetLocalPosition()
		height	= self.GetHeight()
		self.all_delete_question_dlg.SetPosition(x, y + height / 3)
		
	def __OpenPostAllDeleteFailPopupDlg(self):
		if self.all_delete_popup:
			del self.all_delete_popup
			self.all_delete_popup = None

		self.all_delete_popup = uiCommon.PopupDialog()
		self.all_delete_popup.SetText(localeInfo.MAILBOX_POST_ALL_DELETE_FAIL_EMPTY)
		self.all_delete_popup.SetWidth( self.GetWidth() )
		self.all_delete_popup.Open()
		(x,y)	= self.GetLocalPosition()
		height	= self.GetHeight()
		self.all_delete_popup.SetPosition(x, y + height / 3)
		
	def __SendPostAllDelete(self):
		net.SendPostAllDelete()
		self.__ClosePostAllDeleteQuestionDialog()
		
	def __ClosePostAllDeleteQuestionDialog(self):
		if not self.all_delete_question_dlg:
			return
		self.all_delete_question_dlg.Close()
		
		
	def __ClickAllGetItemsButton(self):		
		if not self.post_data_dict:
			self.__OpenAllGetItemsFailPopup()
			return
		if len(self.post_data_dict) <= 0:
			self.__OpenAllGetItemsFailPopup()
			return
			
		# ���� �� �ִ� �������� �ִ��� �˻� �ؾ� ��.
		is_send_post_all_get_items = False
		
		for data in self.post_data_dict.values():
			(index, send_time, delete_time, title, is_gm_post, is_item_exist, is_confirm) = data
			if True == is_item_exist:
				is_send_post_all_get_items = True
				break
			
		# ���� �� �ִ� ������ ������ ����â�� ����
		if True == is_send_post_all_get_items:
			self.__OpenPostAllGetItemsQuestionDlg()
		else:
			self.__OpenAllGetItemsFailPopup()
			
	def __OpenPostAllGetItemsQuestionDlg(self):
		if self.all_get_items_question_dlg:
			del self.all_get_items_question_dlg
			self.all_get_items_question_dlg = None

		self.all_get_items_question_dlg = uiCommon.QuestionDialog()
		self.all_get_items_question_dlg.SetText(localeInfo.MAILBOX_POST_ALL_GET_ITEMS_QUESTION)
		self.all_get_items_question_dlg.SetAcceptEvent( ui.__mem_func__(self.__SendPostAllGetItems) )
		self.all_get_items_question_dlg.SetCancelEvent( ui.__mem_func__(self.__ClosePostAllGetItemsQuestionDialog) )
		self.all_get_items_question_dlg.SetWidth( self.GetWidth() )
		self.all_get_items_question_dlg.Open()
		(x,y)	= self.GetLocalPosition()
		height	= self.GetHeight()
		self.all_get_items_question_dlg.SetPosition(x, y + height / 3)
		
	def __SendPostAllGetItems(self):
		net.SendPostAllGetItems()
		self.__ClosePostAllGetItemsQuestionDialog()
		
	def __ClosePostAllGetItemsQuestionDialog(self):
		if not self.all_get_items_question_dlg:
			return
		self.all_get_items_question_dlg.Close()
		
	def __OpenAllGetItemsFailPopup(self):		
		if self.all_get_items_fail_popup:
			del self.all_get_items_fail_popup
			self.all_get_items_fail_popup = None

		self.all_get_items_fail_popup = uiCommon.PopupDialog()
		self.all_get_items_fail_popup.SetText(localeInfo.MAILBOX_POST_ALL_GET_ITEMS_FAIL_EMPTY)
		self.all_get_items_fail_popup.SetWidth( self.GetWidth() )
		self.all_get_items_fail_popup.Open()
		(x,y)	= self.GetLocalPosition()
		height	= self.GetHeight()
		self.all_get_items_fail_popup.SetPosition(x, y + height / 3)
		
	def __ClickPost(self, button_index, data_index):
		if not self.post_read:
			self.__CreatePostReadWindow()
		
		if not data_index in self.post_data_dict:
			return
		
		(index, send_time, delete_time, title, is_gm_post, is_item_exist, is_confirm) = self.post_data_dict[data_index]
		
		## �߰� data �� ���ٸ� �����κ��� ������ ��û�ؾ� ��.
		if not data_index in self.post_add_data_dict:
			net.RequestPostAddData( button_index, data_index )
			return
				
		(from_name, message, yang, cheque) = self.post_add_data_dict[data_index]
		
		self.post_read.Show()
		self.post_read.Clear()
		self.post_read.SetDataIndex( data_index )
		self.post_read.SetFromName( from_name )
		self.post_read.SetTitle( title )
		self.post_read.SetMessage( message )
		self.post_read.SetYang( yang )
		self.post_read.SetCheque( cheque )
		self.post_read.SetItem( data_index )
		self.post_read.SetTop()
		
		if self.post_write and self.post_write.IsShow():
			self.post_write.Close()
		
		self.post_list[button_index].SetConfirmColor( is_confirm )
		
		self.__RefreshPostButton( button_index )
		
	def __RefreshMailBoxGMButton(self):
		if not self.interface:
			return
			
		mailbox_gm_button_visible = False
		
		for key, data in self.post_data_dict.items():
			(index, send_time, delete_time, title, is_gm_post, is_item_exist, is_confirm) = data
			
			if True == is_gm_post and False == is_confirm:
				mailbox_gm_button_visible = True
				break
		
		self.interface.MailBoxGMButtonVisible( mailbox_gm_button_visible )
			
	def __ClickPrevButton(self):		
		if None == self.post_data_dict:
			return
			
		min_page = 0
		if self.cur_page - 1 >= min_page:
			self.cur_page = self.cur_page - 1
			self.__AllPostButtonEnable()
			if self.post_read:
				self.post_read.Clear()
				self.post_read.Close()
				
			self.__PostRefresh()
		
		
	def __ClickNextButton(self):
		
		if None == self.post_data_dict:
			return
		
		max_page = int( math.ceil( len(self.post_data_dict) / float(POST_MAX) ) )	# �ø�ó��
		
		if self.cur_page + 1 < max_page:
			self.cur_page = self.cur_page + 1
			self.__AllPostButtonEnable()
			if self.post_read:
				self.post_read.Clear()
				self.post_read.Close()
				
			self.__PostRefresh()		
		
	def __PostRefresh(self):
		if len(self.post_list) != POST_MAX:
			return
		
		for i in xrange( POST_MAX ):
			self.post_list[i].Clear()
			self.post_list[i].Show()
			
		if len(self.post_data_dict) == 0:
			return
		
		cur_page_dict = { k:v for i, (k,v) in enumerate( self.post_data_dict.items() ) if i >= (self.cur_page * POST_MAX) and i < ((self.cur_page+1) * POST_MAX) }
		
		button_index = 0		
		for data_index, data in cur_page_dict.items():
			if button_index >= POST_MAX:
				break
				
			(index, send_time, delete_time, title, is_gm_post, is_item_exist, is_confirm) = data
			self.post_list[button_index].SetDataIndex( index )
				
			if True == is_gm_post:
				self.post_list[button_index].SetIcon( DIVISION_GM )
			elif True == is_item_exist:
				self.post_list[button_index].SetIcon( DIVISION_ITEM )
			else:
				self.post_list[button_index].SetIcon( DIVISION_POST )
				
			self.post_list[button_index].SetTitle( title )
			self.post_list[button_index].SetRemainTime( delete_time )
			self.post_list[button_index].SetConfirmColor( is_confirm )
			self.post_list[button_index].Show()
			button_index = button_index + 1
			
				
		
	def __RefreshPostButton(self, index):
		for i in xrange( POST_MAX ):
			if index == i:
				self.active_button_index = index
				self.post_list[i].SetDisable()
			else:
				self.post_list[i].SetEnable()
				
	def __AllPostButtonEnable(self):
		self.active_button_index = -1
		for i in xrange( POST_MAX ):
			self.post_list[i].SetEnable()
			
	def __CreatePostReadWindow(self):
		if not self.post_read:
			self.post_read = PostRead( self.__AllPostButtonEnable )
			
		if self.post_read:
			self.post_read.SetItemToolTip( self.tooltipItem )
				
	def __CreatePostWriteWindow(self):
		if not self.post_write:
			self.post_write = PostWrite()
		
		if self.post_write:
			self.post_write.BindInterface( self.interface )
			self.post_write.SetInven( self.inven )
			self.post_write.SetDSWindow( self.ds_window )
			self.post_write.SetItemToolTip( self.tooltipItem )
			
	def __ClickPostWriteButton(self):
		# ��������� 20���� �̻���� �����ϴ�
		if player.GetStatus(player.LEVEL) < POST_WRITE_LIMIT_LEVEL:
			chat.AppendChat( chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_WRITE_LEVEL_LIMIT )
			return
			
		if not self.post_write:
			self.__CreatePostWriteWindow()
			
		if False == self.post_write.IsShow():
			self.post_write.Show()
			self.post_write.SetTop()
			
			if self.post_read and self.post_read.IsShow():
				self.post_read.Clear()
				self.post_read.Close()
		
	# ���� ������, yang, won �ޱ⿡ ����
	# ������ �������ش�.
	def __PostGetItemsSuccess(self, data_index):
		if data_index in self.post_data_dict:
			(index, send_time, delete_time, title, is_gm_post, is_item_exist, is_confirm) = self.post_data_dict[data_index]
			self.post_data_dict[data_index] = (index, send_time, delete_time, title, is_gm_post, False, 1)
		
		if data_index in self.post_add_data_dict:
			(from_name, message, yang, cheque) = self.post_add_data_dict[data_index]
			self.post_add_data_dict[data_index] = (from_name, message, 0, 0)
			
		if False == is_gm_post:
			self.post_list[self.active_button_index].SetIcon( DIVISION_POST )
			
		self.post_list[self.active_button_index].SetConfirmColor( 1 )
		
		if self.post_read:
			self.post_read.SetItem( data_index )
			self.post_read.SetYang( 0 )
			self.post_read.SetCheque( 0 )
		
	def __PostGetItemsFail(self, result):
		
		if mail.POST_GET_ITEMS_FAIL == result:
			#print "���� ������ ����"
			pass
		elif mail.POST_GET_ITEMS_NONE == result:
			#print "���� ��ǰ�� ����."
			pass
		elif mail.POST_GET_ITEMS_NOT_ENOUGHT_INVENTORY == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_GET_ITEMS_NOT_ENOUGHT_INVENTORY)
		elif mail.POST_GET_ITEMS_YANG_OVERFLOW == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_GET_ITEMS_YANG_OVERFLOW)
		elif mail.POST_GET_ITEMS_WON_OVERFLOW == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_GET_ITEMS_WON_OVERFLOW)
		elif mail.POST_GET_ITEMS_FAIL_BLOCK_CHAR == result:
			pass
			#print "������ ����� ������ ���� �� ����."
			#print "���� ������� ���̵� ������ ��� ���� �� ����."
			
			
	# ���� ������ ����
	# ������ �������ش�
	def __PostDeleteSuccess(self, data_index):
		if data_index in self.post_data_dict:
			del self.post_data_dict[data_index]
		
		if data_index in self.post_add_data_dict:
			del self.post_add_data_dict[data_index]
			
		if self.post_read:
			self.post_read.Clear()
			self.post_read.Close()
			
		if len(self.post_data_dict) <= self.cur_page * POST_MAX:
			self.cur_page = self.cur_page - 1
			self.cur_page = max( 0, self.cur_page )			
		
		self.__PostRefresh()
			
	def __PostDeleteFail(self, result):		
		if mail.POST_DELETE_FAIL == result:
			return
		elif mail.POST_DELETE_FAIL_EXIST_ITEMS == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MAILBOX_POST_DELETE_FAIL_EXIST_ITEMS)				
			
	def __PostAllDeleteSuccess(self):
			
		index_list = []
		
		for key, data in self.post_data_dict.items():
			(index, send_time, delete_time, title, is_gm_post, is_item_exist, is_confirm) = data
			if False == is_item_exist:
				index_list.append( key )
				
		for key in index_list:
			if key in self.post_data_dict:
				del self.post_data_dict[key]
			if key in self.post_add_data_dict:
				del self.post_add_data_dict[key]
				
		if self.post_read:
			self.post_read.Clear()
			self.post_read.Close()
			
		while len(self.post_data_dict) <= self.cur_page * POST_MAX:
			self.cur_page = self.cur_page - 1
			self.cur_page = max( 0, self.cur_page )
			
			if 0 == self.cur_page:
				break
		
		self.__PostRefresh()
		
		
	def __PostAllDeleteFail(self, result):
		
		if mail.POST_ALL_DELETE_FAIL == result:
			return
		elif mail.POST_ALL_DELETE_OK == result:
			return
		elif mail.POST_ALL_DELETE_FAIL_EMPTY == result:
			return
		elif mail.POST_ALL_DELETE_FAIL_DONT_EXIST == result:
			return
		
	def __PostAllGetItemsSuccess(self, getSuccessKeyList):
		if None == getSuccessKeyList:
			return			
			
		for data_index in getSuccessKeyList:
			if data_index in self.post_data_dict:
				(index, send_time, delete_time, title, is_gm_post, is_item_exist, is_confirm) = self.post_data_dict[data_index]
				self.post_data_dict[data_index] = (index, send_time, delete_time, title, is_gm_post, False, 1)
				
			if data_index in self.post_add_data_dict:
				(from_name, message, yang, cheque) = self.post_add_data_dict[data_index]
				self.post_add_data_dict[data_index] = (from_name, message, 0, 0)
				
		if self.post_read:
			self.post_read.Clear()
			self.post_read.Close()
		
		self.__PostRefresh()
		
	def __PostAllGetItemsFail(self, result):
		
		if mail.POST_ALL_GET_ITEMS_FAIL == result:
			print "POST_ALL_GET_ITEMS_FAIL"
			return
		elif mail.POST_ALL_GET_ITEMS_OK == result:
			#print "POST_ALL_GET_ITEMS_OK"
			return
		elif mail.POST_ALL_GET_ITEMS_EMPTY == result:
			print "POST_ALL_GET_ITEMS_EMPTY"
			return
		elif mail.POST_ALL_GET_ITEMS_FAIL_DONT_EXIST == result:
			print "POST_ALL_GET_ITEMS_FAIL_DONT_EXIST"
			return 
		elif mail.POST_ALL_GET_ITEMS_FAIL_CANT_GET == result:
			print "POST_ALL_GET_ITEMS_FAIL_CANT_GET"
			return
			
	# ���� ������, yang, won �ޱ⿡ ����
	# ������ �������ش�.
	def __PostGetItemsSuccessNoRefresh(self, data_index):
		
		if data_index in self.post_data_dict:
			(index, send_time, delete_time, title, is_gm_post, is_item_exist, is_confirm) = self.post_data_dict[data_index]
			self.post_data_dict[data_index] = (index, send_time, delete_time, title, is_gm_post, False, is_confirm)
		
		if data_index in self.post_add_data_dict:
			(from_name, message, yang, cheque) = self.post_add_data_dict[data_index]
			self.post_add_data_dict[data_index] = (from_name, message, 0, 0)
			
		if False == is_gm_post:
			self.post_list[self.active_button_index].SetIcon( DIVISION_POST )
		
		if self.post_read:
			self.post_read.SetItem( data_index )
			self.post_read.SetYang( 0 )
			self.post_read.SetCheque( 0 )
			
	def CantPostItemSlot(self, slotIndex, slotWindow = player.INVENTORY):
		if not self.post_write:
			return False
		return self.post_write.CantPostItemSlot(slotIndex, slotWindow)
		
	def MailBoxOpen(self, is_distance_check):
		self.distance_check = is_distance_check
		if True == self.distance_check:
			(self.OpenX, self.OpenY, z) = player.GetMainCharacterPosition()
		
		self.post_data_dict = mail.GetMailDict()
		if None == self.post_data_dict:
			return
		
		self.Show()
		self.SetTop()
		self.__PostRefresh()
		
	def MailBoxProcess(self, type, data):
		if mail.MAILBOX_GC_OPEN == type:
			self.MailBoxOpen(data)
			
		elif mail.MAILBOX_GC_POST_WRITE_CONFIRM == type:
			if not self.post_write:
				return
			self.post_write.PostWriteConfirmResult( data )
			
		elif mail.MAILBOX_GC_POST_WRITE == type:
			if not self.post_write:
				return
			self.post_write.PostWriteResult( data )
			
		elif mail.MAILBOX_GC_ADD_DATA == type:
			(button_index, data_index) = data
			
			if data_index in self.post_data_dict:
				(index, send_time, delete_time, title, is_gm_post, is_item_exist, is_confirm) = self.post_data_dict[data_index]
				self.post_data_dict[data_index] = (index, send_time, delete_time, title, is_gm_post, is_item_exist, 1)
				
			add_data = mail.GetMailAddData( data_index )
			if add_data:
				self.post_add_data_dict[data_index] = add_data
				
			self.__ClickPost( button_index, data_index )
			
		elif mail.MAILBOX_GC_POST_GET_ITEMS == type:
		
			(data_index, result) = data
			
			if mail.POST_GET_ITEMS_OK == result:
				self.__PostGetItemsSuccess( data_index )
			else:
				self.__PostGetItemsFail( result )
				
		elif mail.MAILBOX_GC_POST_DELETE == type:

			(data_index, result) = data
			
			if result in [mail.POST_DELETE_OK, mail.POST_TIME_OUT_DELETE]:
				self.__PostDeleteSuccess( data_index )
			else:
				self.__PostDeleteFail( result )
				
		elif mail.MAILBOX_GC_POST_ALL_DELETE == type:
			
			if mail.POST_ALL_DELETE_OK == data:
				self.__PostAllDeleteSuccess()
			else:
				self.__PostAllDeleteFail( data )
				
		elif mail.MAILBOX_GC_POST_ALL_GET_ITEMS == type:
			
			( result, getSuccessKeyList ) = data			
			if mail.POST_ALL_GET_ITEMS_OK == result and getSuccessKeyList:
				self.__PostAllGetItemsSuccess( getSuccessKeyList )
			else:
				self.__PostAllGetItemsFail( result )
		elif mail.MAILBOX_GC_UNREAD_DATA == type:
			if self.interface:
				self.interface.MiniMapMailProcess(type, data)
		elif mail.MAILBOX_GC_ITEM_EXPIRE == type:
			
			if not self.post_data_dict:
				return
				
			if not data in self.post_data_dict:
				return
				
			new_data = mail.GetMailData( data )
			self.post_data_dict[data] = new_data
			
			self.__PostRefresh()
						
			if self.post_read and True == self.post_read.IsShow():
				if self.post_read.GetDataIndex() == data:
					self.post_read.SetItem( data )
					
		elif mail.MAILBOX_GC_CLOSE == type:
			self.CloseClear()
			
		elif mail.MAILBOX_GC_SYSTEM_CLOSE == type:
			if self.interface:
				self.interface.MiniMapMailProcess(type, data)
		else:
			return
