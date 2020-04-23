import MaxPlus
import node as sdk_node


def add_bone_to_skin_modifier_of_selected_node(bone):
    op = r"""skinOps.addBone $.modifiers[#Skin] (getnodeByName"{0}") 1""".format(bone.GetName())
    MaxPlus.Core.EvalMAXScript(op)

def get_bones_list_from_skin_modifier(skinmodifier):
    influence_list = list()
    if skinmodifier:
        for ref in list(skinmodifier.Refs):
            if ref:
                if ref.ClassID == MaxPlus.ClassIds.NodeObject:
                    influence_list.append(MaxPlus.INode._CastFrom(ref))
        return influence_list


def get_skin_modifier(node):
    for modifier in node.Modifiers:
        if modifier.ClassID == MaxPlus.ClassIds.Skin:
            return modifier


'''
:return modifier
'''
def add_skin_modifier(target):
    mod = MaxPlus.Factory.CreateObjectModifier(MaxPlus.ClassIds.Skin)
    target.AddModifier(mod)
    return mod



