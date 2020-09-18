fn createMesh objs name:unsupplied transform:(matrix3 1) =	--generere le mesh qui va etre export�
(
    local obj = mesh vertices:#([0,0,0],[10,0,0],[0,10,0]) faces:#([1,2,3]) name:name transform:transform		--creation d'un mesh contenant un triangle (cr�er un mesh vide pose probleme)
    converttopoly obj
    --ADD_TO_LAYER "KittyHawk_Exporter(don't use)" obj		--mets les objets dans un layer temporaire pour etre sur que l'objet est visible lors de l'export
    multimat_new=#()
    for j in objs do				--pour tous les objets
    (
        obj_temp=snapshot j
        if classof j.baseobject == Loft	then  addmodifier  obj_temp (Edit_Normals())		--cas specifique des lofts pour eviter que les loft ne s'exportent pas
        obj_temp.parent=undefined
        converttomesh	obj_temp		--permet de virer le mode sous objet
        resetXform	obj_temp			--resetXform pour les attach d'objet avec normales specifiques
        converttomesh	obj_temp		-- reconvertion en mesh pour ecraser la pile
        local save_mat=obj_temp.material			--hack pour pas perdre l'history du undo quand attach (probleme avec les multi mat)
        if classof  save_mat == Multimaterial then		--cas du multimaterial
        (
            ID_true_used=#{}			-- contient  bitarray
            T_Faces_matID=#()
            T_Faces_matID.count=save_mat.count
            for f=1 to obj_temp.numfaces do
            (
                local face_matID=(getFaceMatID  obj_temp	f)
                if not(ID_true_used[face_matID]) then 						--si c'est un nouvel ID pas encore trait�
                (
                    T_Faces_matID[face_matID]=#{f}
                    ID_true_used[face_matID]=true
                )
                else																				--si c'est un ID deja trait�
                (
                    append 	(T_Faces_matID[face_matID])	 f
                )
            )
            for index_mat in ID_true_used do			-- pour chaque material vraiment appliqu� au mesh
            (
                mat_current=save_mat[index_mat]

                matID=finditem multimat_new mat_current
                if matID==0 then
                (
                    append multimat_new mat_current
                    new_Id=multimat_new.count
-- 						format "obj_temp.numfaces = %\n" obj_temp.numfaces
                    for f in (T_Faces_matID[index_mat]) do	setFaceMatID  obj_temp	f		new_Id
                )
                else		for f in (T_Faces_matID[index_mat]) do	setFaceMatID  obj_temp	f		matID
            )
        )
        else
        (
            mat_current=save_mat

            matID=finditem multimat_new mat_current
            if matID==0 then
            (
                append multimat_new mat_current
                new_Id=multimat_new.count
-- 					format "obj_temp.numfaces = %\n" obj_temp.numfaces
                for f=1 to obj_temp.numfaces do	setFaceMatID  obj_temp	f		new_Id
            )
            else		for f=1 to obj_temp.numfaces do	setFaceMatID  obj_temp	f		matID
        )

        obj_temp.material=undefined
        with undo off		(polyop.attach  obj obj_temp)
    )

    local final_mat = multimaterial numsubs:(multimat_new.count)
    final_mat.name=obj.name+"_mat"		--nom du multimat specifique a l'objet (au cas ou, on sait jamais)


    for i=1 to (multimat_new.count) do
    (
        if multimat_new[i]==undefined
            then (		final_mat[i] = FlightSim ()		;		final_mat[i].name = "Newmat"	)
            else	final_mat[i] = multimat_new[i]
    )
    polyop.deleteFaces obj 1		--on supprime la face cr�� avec le mesh

    obj.material=final_mat			--on assigne le material


    return obj
)

