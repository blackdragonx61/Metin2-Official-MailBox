if app.BL_MAILBOX:
	import mail

# Find
	def SetTitle(self, name):
		...

# Add
	if app.BL_MAILBOX:
		def SetThinBoardSize(self, width, height=12):
			self.toolTipWidth = width
			self.toolTipHeight = height

# Find
	def SetItemToolTip(self, itemVnum):
		...

# Add
	if app.BL_MAILBOX:
		def SetMailBoxItem(self, index):
			item_data = mail.GetMailItemData(index)
			if None == item_data:
				return

			(vnum, count) = item_data

			self.ClearToolTip()
			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(mail.GetMailItemMetinSocket(index, i))
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(mail.GetMailItemAttribute(index, i))

			self.AddItemData(vnum, metinSlot, attrSlot)

			if app.BL_TRANSMUTATION_SYSTEM:
				changelookvnum = mail.GetItemChangeLookVnum( index )
				self.AppendChangeLookInfoItemVnum(changelookvnum)
