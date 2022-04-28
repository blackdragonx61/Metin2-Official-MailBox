//Find
		else if (!stricmp(pszFlag, "ltr"))
			pWin->RemoveFlag(UI::CWindow::FLAG_RTL);

///Add
#if defined(__BL_MAILBOX__)
		else if (!stricmp(pszFlag, "not_capture"))
			pWin->AddFlag(UI::CWindow::FLAG_NOT_CAPTURE);
#endif

//Find
PyObject * wndButtonFlash(PyObject * poSelf, PyObject * poArgs)
{
	...
}

///Add
#if defined(__BL_MAILBOX__)
PyObject* wndButtonEnableFlash(PyObject* poSelf, PyObject* poArgs)
{
	UI::CWindow* pWindow;
	if (!PyTuple_GetWindow(poArgs, 0, &pWindow))
		return Py_BuildException();

	dynamic_cast<UI::CButton*>(pWindow)->EnableFlash();

	return Py_BuildNone();
}

PyObject* wndButtonDisableFlash(PyObject* poSelf, PyObject* poArgs)
{
	UI::CWindow* pWindow;
	if (!PyTuple_GetWindow(poArgs, 0, &pWindow))
		return Py_BuildException();

	dynamic_cast<UI::CButton*>(pWindow)->DisableFlash();

	return Py_BuildNone();
}

PyObject* wndImageResetFrame(PyObject* poSelf, PyObject* poArgs)
{
	UI::CWindow* pWindow;
	if (!PyTuple_GetWindow(poArgs, 0, &pWindow))
		return Py_BuildException();

	dynamic_cast<UI::CAniImageBox*>(pWindow)->ResetFrame();

	return Py_BuildNone();
}
#endif

//Find
		{ "Flash",						wndButtonFlash,						METH_VARARGS },

///Add
#if defined(__BL_MAILBOX__)
		{ "EnableFlash",				wndButtonEnableFlash,				METH_VARARGS },
		{ "DisableFlash",				wndButtonDisableFlash,				METH_VARARGS },
		{ "ResetFrame",					wndImageResetFrame,					METH_VARARGS },
#endif