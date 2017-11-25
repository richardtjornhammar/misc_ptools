class Tree(dict):
    def __init__ (self, fname ):
        self.node_list=None
        self.node_dict=None
        self.list_dict=None
        self.tuples=None
        self.filename=fname
        self.generate_tree_tuples()
        self.build_nodes_from_tuples()

    def build_nodes_from_tuples( self ) :
        tup_list = self.tuples
        all_names=list(); idname_dict = dict()
        for ltp in tup_list:
            [all_names.append(name) for name in ltp]
        uni_names = list(set(all_names)); num=0; node_ids=dict()
        for name in uni_names:
            idname_dict[num]=name
            node_ids[name]=num ; num += 1
        node_list = list() ; num=0; list_ids = dict()
        for ltp in tup_list:
            p = ltp[0] ; c = ltp[1]
            nid = node_ids[c]
            bNew = True
            for inod in range(len(node_list)):
                if nid == node_list[inod]['node']:
                    bNew = False
                    node_list[inod]['ancestors'].append(node_ids[p])
                    node_list[inod]['label'] = c
                    break
            if bNew :
                list_ids[nid] = num ; num +=1
                node = dict()
                node ['node'] = nid
                node ['ancestors'] = [node_ids[p]]
                node ['label'] = c
                node_list.append( node )
        allnns = set(node_ids.values())
        allids = set(list_ids.keys())
        un_added_root_ids = list( allnns - allids )
        num = len(node_list)
        for rid in un_added_root_ids:
            node=dict()
            node['node']=rid
            node['ancestors']=[]
            node['label']=idname_dict[rid]
            node_list.append( node )
            list_ids[rid] = num ; num +=1
        self.node_list = node_list
        self.node_dict = node_ids
        self.list_dict = list_ids

    def generate_tree_tuples(self):
        t = list()
        with open(self.filename) as f:
            for line in f:
                (key, val) = line.split()
                t.append((key,val))
        self.tuples = t

    def return_ancestor_of(self, name, at_level=-1):
        nid = self.node_dict[name]
        rnode = self.node_list[self.list_dict[nid]]
        lineage = [rnode]
        ancestors = rnode['ancestors']
        while ancestors :
            if len(ancestors)==0 or not (ancestors[0] in self.list_dict.keys()) :
                break
            pnode = self.node_list[self.list_dict[ancestors[0]]]
            ancestors = pnode['ancestors']
            lineage.append(pnode)
        return ( lineage[at_level]['label'] )

if __name__ == '__main__':
    """
    d = {}
    t = list()
    lnr = 0
    with open('/home/richard/Work/data/naming_and_annotations/reactome/ReactomePathwaysRelation.txt') as f:
        for line in f:
            (key, val) = line.split()
            d[key] = val
            t.append((key,val))
            lnr += 1.0
    tree=Tree()
    react_nodes, node_dict, list_dict = tree.build_nodes_from_tuples(t)
    nid = node_dict['R-HSA-352230']
    njd = node_dict['R-HSA-382551']
    rnode = react_nodes[list_dict[nid]]
    lineage = [rnode]
    ancestors = rnode['ancestors']
    while ancestors :
        if len(ancestors)==0 or not (ancestors[0] in list_dict.keys()) :
           print ( pnode )
           print ( ancestors)
           break
        pnode = react_nodes[list_dict[ancestors[0]]]
        ancestors = pnode['ancestors']
        lineage.append(pnode)
    print ( lineage )
    print ( lineage[-1]['label'] )
    """
    atree = Tree('/home/richard/Work/data/naming_and_annotations/reactome/ReactomePathwaysRelation.txt')
    print( atree . return_ancestor_of( 'R-HSA-352230' ) )

