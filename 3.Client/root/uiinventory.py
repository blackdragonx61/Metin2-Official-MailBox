# Find
				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

# Add
				elif app.BL_MAILBOX and onTopWnd == player.ON_TOP_WND_MAILBOX:
					if self.interface.MarkUnusableDSInvenSlotOnTopWnd(onTopWnd, slotNumber, player.INVENTORY):
						self.wndItem.SetUnusableSlotOnTopWnd(localIndex)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(localIndex)

# Find
				elif onTopWnd == player.ON_TOP_WND_SAFEBOX:
					if player.IsAntiFlagBySlot(slotNumber, item.ANTIFLAG_SAFEBOX):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)

# Add
				elif app.BL_MAILBOX and onTopWnd == player.ON_TOP_WND_MAILBOX:
					if self.interface.MarkUnusableDSInvenSlotOnTopWnd(onTopWnd, slotNumber, player.INVENTORY):
						self.wndItem.SetUnusableSlotOnTopWnd(i)
					else:
						self.wndItem.SetUsableSlotOnTopWnd(i)
