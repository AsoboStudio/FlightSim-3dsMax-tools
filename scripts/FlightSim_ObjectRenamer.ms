
if rlt_Renamer!=undefined then destroydialog rlt_Renamer
rollout rlt_Renamer "Objects Renamer"
(

-- 	radiobuttons	rdb_rename "Rename" items:#("object name","Userdefined")
-- 	checkbox	chk_objectName 	"Object"			pos:[5,5]
-- 	checkbox	chk_objectUD 		"UserDefined"	pos:[5,55]
	edittext txt_SourceString	"Replace" width:280 pos:[5,8]	tooltip:"Enter the string that needs to be replaced"
	edittext txt_TargetString	"By" width:280 pos:[5,35]			tooltip:"Enter New string"
	
	button btn_renameselection	"Rename Selection"		across:2
	button btn_renameAll			"Rename All objects" 	across:2
	
	checkbox	chk_selectObjectsFailed	"Select objects with rename failed"
	

	local	T_Obj_renameFailed=#()	
	local	T_Obj_renameOK=#()	

	fn	checkTextIsNotEmpty =
	(
		T_Obj_renameFailed=#()
		T_Obj_renameOK=#()
		
		result = true
		fs = filterstring	txt_SourceString.text  " \\\/\""	
		if fs.count==0	then messagebox "String to be replaced is empty\nPlease add string to find"
		else if txt_SourceString.text.count<2	then	result	= querybox	"String to be replaced is just one character:\nAre you sure you want to continue?"
		if txt_SourceString.text.count==0	then 	result	= querybox	"New String is empty\nAre you sure you want to continue?"
		return result
	)
		
	fn Replace_object_name		_obj =
	(
		_name=_obj.name

		Sindex = findstring (tolower _name)	(tolower txt_SourceString.text)
		if Sindex !=undefined	 then
		(
			_obj.name = (substring _name	1	(Sindex-1)	)+txt_TargetString.text+ (substring	 _name	(txt_SourceString.text.count+Sindex)	(_name.count))
			append	T_Obj_renameOK		_obj	
		)
		else
		(
			append	T_Obj_renameFailed	_obj	
		)
	)

	
	on btn_renameselection pressed do
	(
		undo "Rename Selection" on 
		(
			if	checkTextIsNotEmpty()	then		
			(
				for o in selection do (Replace_object_name o)
				messagebox (T_Obj_renameOK.count as string+" objects renamed succesfully\n"+T_Obj_renameFailed.count as string+" objects rename Failed")
				if	chk_selectObjectsFailed.checked and	T_Obj_renameFailed.count>0 then select T_Obj_renameFailed
			)
		)
	)
	on btn_renameAll pressed do
	(
		undo "Rename All Objects" on 
		(
			if	checkTextIsNotEmpty()	then		
			(
				for o in objects do (Replace_object_name o)
				messagebox (T_Obj_renameOK.count as string+" objects renamed succesfully\n"+T_Obj_renameFailed.count as string+" objects rename Failed")
				if	chk_selectObjectsFailed.checked and	T_Obj_renameFailed.count>0 then select T_Obj_renameFailed
			)
		)
	)
)
createdialog rlt_Renamer	300	105
