import numpy as np
import math as mt
class WavefrontOBJ:
    def __init__( self, default_mtl='default_mtl' ):
        self.path      = None               # path of loaded object
        self.mtllibs   = []                 # .mtl files references via mtllib
        self.mtls      = [ default_mtl ]    # materials referenced
        self.mtlid     = []                 # indices into self.mtls for each polygon
        self.vertices  = []                 # vertices as an Nx3 or Nx6 array (per vtx colors)
        self.normals   = []                 # normals
        self.texcoords = []                 # texture coordinates
        self.polygons  = []                 # M*Nv*3 array, Nv=# of vertices, stored as vid,tid,nid (-1 for N/A)

    def getting_texcoords(self):
        print(self.texcoords)

    def getting_vertices(self):
        print(self.vertices)


    def minimun_coords(self):
        x = 100000
        y = 100000
        z = 100000
        for vertice in self.vertices:
            if vertice[0] < x and vertice[1] < y and vertice[2] < z :
                x = vertice[0]
                y = vertice[1]
                z = vertice[2]
        return x,y,z


    def min_x_coords(self):
        x = 100000
        for vertice in self.vertices:
            if vertice[0] < x :
                x = vertice[0]
        return x
    
    def min_y_coords(self):
        y = 100000
        for vertice in self.vertices:
            if vertice[1] < y :
                y = vertice[1]
        return y

    def max_coords(self):
        x = -100000
        y = -100000
        z = -100000
        for vertice in self.vertices:
            if vertice[0] > x and vertice[1] > y :
                x = vertice[0]
                y = vertice[1]
                z = vertice[2]
        return x,y,z

    def max_x_coords(self):
        x = -100000
        for vertice in self.vertices:
            if vertice[0] > x :
                x = vertice[0]
        return x

    def max_y_coords(self):
        y = -100000
        for vertice in self.vertices:
            if vertice[1] > y :
                y = vertice[1]
        return y

    def points_distance(self,x1,y1,x2,y2):
        return mt.sqrt(mt.pow((x2-x1),2.0)+mt.pow((y2-y1),2.0))
        

    def getting(self):
        print("vertices",self.vertices)
        # print("normals: ", self.normals)
        print("polygons: ", self.polygons)
        # print("mtllibs: ", self.mtllibs)
        # print("mtls: ", self.mtls)
        # print("mtlid: ", self.mtlid)

# def load_obj( filename: str, default_mtl='default_mtl', triangulate=False ) -> WavefrontOBJ:
#     """Reads a .obj file from disk and returns a WavefrontOBJ instance

#     Handles only very rudimentary reading and contains no error handling!

#     Does not handle:
#         - relative indexing
#         - subobjects or groups
#         - lines, splines, beziers, etc.
#     """
#     # parses a vertex record as either vid, vid/tid, vid//nid or vid/tid/nid
#     # and returns a 3-tuple where unparsed values are replaced with -1
#     def parse_vertex( vstr ):
#         vals = vstr.split('/')
#         vid = int(vals[0])-1
#         tid = int(vals[1])-1 if len(vals) > 1 and vals[1] else -1
#         nid = int(vals[2])-1 if len(vals) > 2 else -1
#         return (vid,tid,nid)

#     with open( filename, 'r' ) as objf:
#         obj = WavefrontOBJ(default_mtl=default_mtl)
#         obj.path = filename
#         cur_mat = obj.mtls.index(default_mtl)
#         for line in objf:
#             toks = line.split()
#             if not toks:
#                 continue
#             if toks[0] == 'v':
#                 obj.vertices.append( [ float(v) for v in toks[1:]] )
#             elif toks[0] == 'vn':
#                 obj.normals.append( [ float(v) for v in toks[1:]] )
#             elif toks[0] == 'vt':
#                 obj.texcoords.append( [ float(v) for v in toks[1:]] )
#             elif toks[0] == 'f':
#                 poly = [ parse_vertex(vstr) for vstr in toks[1:] ]
#                 if triangulate:
#                     for i in range(2,len(poly)):
#                         obj.mtlid.append( cur_mat )
#                         obj.polygons.append( (poly[0], poly[i-1], poly[i] ) )
#                 else:
#                     obj.mtlid.append(cur_mat)
#                     obj.polygons.append( poly )
#             elif toks[0] == 'mtllib':
#                 obj.mtllibs.append( toks[1] )
#             elif toks[0] == 'usemtl':
#                 if toks[1] not in obj.mtls:
#                     obj.mtls.append(toks[1])
#                 cur_mat = obj.mtls.index( toks[1] )
#         return obj

def load_obj( filename: str, default_mtl='default_mtl', triangulate=False ) -> WavefrontOBJ:
    """Reads a .obj file from disk and returns a WavefrontOBJ instance

    Handles only very rudimentary reading and contains no error handling!

    Does not handle:
        - relative indexing
        - subobjects or groups
        - lines, splines, beziers, etc.
    """
    # parses a vertex record as either vid, vid/tid, vid//nid or vid/tid/nid
    # and returns a 3-tuple where unparsed values are replaced with -1
    def parse_vertex( vstr ):
        vals = vstr.split('/')
        vid = int(vals[0])-1
        tid = int(vals[1])-1 if len(vals) > 1 and vals[1] else -1
        nid = int(vals[2])-1 if len(vals) > 2 else -1
        return (vid,tid,nid)

    with open( filename, 'r' ) as objf:
        obj = WavefrontOBJ(default_mtl=default_mtl)
        obj.path = filename
        cur_mat = obj.mtls.index(default_mtl)
        for line in objf:
            toks = line.split()
            if not toks:
                continue
            if toks[0] == 'v':
                obj.vertices.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'vn':
                obj.normals.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'vt':
                obj.texcoords.append( [ float(v) for v in toks[1:]] )
            elif toks[0] == 'f':
                poly = [ parse_vertex(vstr) for vstr in toks[1:] ]
                for i in range(2,len(poly)):
                    obj.polygons.append( (poly[0], poly[i-1], poly[i] ) )
               
            elif toks[0] == 'mtllib':
                obj.mtllibs.append( toks[1] )
            elif toks[0] == 'usemtl':
                if toks[1] not in obj.mtls:
                    obj.mtls.append(toks[1])
                cur_mat = obj.mtls.index( toks[1] )
        return obj


def save_obj( obj: WavefrontOBJ, filename: str ):
    """Saves a WavefrontOBJ object to a file

    Warning: Contains no error checking!

    """
    with open( filename, 'w' ) as ofile:
        for mlib in obj.mtllibs:
            ofile.write('mtllib {}\n'.format(mlib))
        for vtx in obj.vertices:
            ofile.write('v '+' '.join(['{}'.format(v) for v in vtx])+'\n')
        for tex in obj.texcoords:
            ofile.write('vt '+' '.join(['{}'.format(vt) for vt in tex])+'\n')
        for nrm in obj.normals:
            ofile.write('vn '+' '.join(['{}'.format(vn) for vn in nrm])+'\n')
        if not obj.mtlid:
            obj.mtlid = [-1] * len(obj.polygons)
        poly_idx = np.argsort( np.array( obj.mtlid ) )
        cur_mat = -1
        for pid in poly_idx:
            if obj.mtlid[pid] != cur_mat:
                cur_mat = obj.mtlid[pid]
                ofile.write('usemtl {}\n'.format(obj.mtls[cur_mat]))
            pstr = 'f '
            for v in obj.polygons[pid]:
                # UGLY!
                vstr = '{}/{}/{} '.format(v[0]+1,v[1]+1 if v[1] >= 0 else 'X', v[2]+1 if v[2] >= 0 else 'X' )
                vstr = vstr.replace('/X/','//').replace('/X ', ' ')
                pstr += vstr
            ofile.write( pstr+'\n')