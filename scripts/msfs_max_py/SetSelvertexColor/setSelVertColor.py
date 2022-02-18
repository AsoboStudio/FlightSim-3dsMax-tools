from pymxs import runtime as rt

def HasEditPolyn(node = None):
	if node != None:
		cls = rt.classOf(node)
		if cls == rt.Editable_Poly or cls == rt.Editable_Mesh:
			return True
	return False
				

def setSelectedObjVertexColor():
    rt.execute('max modify mode')
    s = list(rt.selection)
    if s != None and len(s) > 0:
        for nod in s:
            if HasEditPolyn(nod):
                rt.Select(nod)
                rt.subobjectLevel = 1
                rt.actionMan.executeAction( 0 ,"40021")
                nod.SetVertexColor(rt.color( 255, 255, 255), rt.name('VertexColor'))
                nod.SetVertexColor(rt.color( 255, 255, 255), rt.name('Illumination'))
                nod.SetVertexColor(rt.color(255,0,0), rt.name('Alpha'))
                rt.subobjectLevel = 0
                print("Obj {0} Finished".format(nod))
            else:
                print("OBJ {0} is not an Editable Poly, tool cannot perform vertex modifications".format(nod))

def run():
    setSelectedObjVertexColor()
#setSelectedObjVertexColor()