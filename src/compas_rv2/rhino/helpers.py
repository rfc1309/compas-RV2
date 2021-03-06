from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
from ast import literal_eval
import compas_rhino
from compas_rhino.etoforms import TextForm

try:
    import System
    import Rhino
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

except ImportError:
    pass

else:
    find_object = sc.doc.Objects.Find

    try:
        purge_object = sc.doc.Objects.Purge
    except AttributeError:
        purge_object = None


__all__ = [
    "delete_objects",
    "is_valid_file",
    "select_filepath_open",
    "select_filepath_save",
    "get_rv2",
    "get_scene",
    "get_proxy",
    "get_system",
    "select_vertices",
    "select_edges",
    "select_faces",
]


def delete_objects(guids, purge=False):
    """Delete objects from the Rhino model space.

    Parameters
    ----------
    guids : list
        A list of object IDs.
    purge : bool, optional
        If ``True``, the objects are permanently deleted
        and cannot be restored through, for example, using *undo*.
        If ``False`` (default), the objects are deleted from the model space
        but can still be restored using Rhino's *undo* function.

    """
    rs.EnableRedraw(False)
    if purge and purge_object:
        purge_objects(guids)
    else:
        for guid in guids:
            if rs.IsObjectHidden(guid):
                rs.ShowObject(guid)
        rs.DeleteObjects(guids)


def purge_objects(guids):
    rs.EnableRedraw(False)
    if not purge_object:
        raise RuntimeError('Cannot purge outside Rhino context.')
    for guid in guids:
        if rs.IsObject(guid):
            if rs.IsObjectHidden(guid):
                rs.ShowObject(guid)
            o = find_object(guid)
            purge_object(o.RuntimeSerialNumber)


def match_vertices(diagram, keys):
    temp = compas_rhino.get_objects(name="{}.vertex.*".format(diagram.name))
    names = compas_rhino.get_object_names(temp)
    guids = []
    for guid, name in zip(temp, names):
        parts = name.split('.')
        key = literal_eval(parts[2])
        if key in keys:
            guids.append(guid)
    return guids


def match_edges(diagram, keys):
    temp = compas_rhino.get_objects(name="{}.edge.*".format(diagram.name))
    names = compas_rhino.get_object_names(temp)
    guids = []
    for guid, name in zip(temp, names):
        parts = name.split('.')[2].split('-')
        u = literal_eval(parts[0])
        v = literal_eval(parts[1])
        if (u, v) in keys or (v, u) in keys:
            guids.append(guid)
    return guids


def match_faces(diagram, keys):
    temp = compas_rhino.get_objects(name="{}.face.*".format(diagram.name))
    names = compas_rhino.get_object_names(temp)
    guids = []
    for guid, name in zip(temp, names):
        parts = name.split('.')
        key = literal_eval(parts[2])
        if key in keys:
            guids.append(guid)
    return guids


def select_vertices(diagram, keys):
    guids = match_vertices(diagram, keys)
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)


def select_edges(diagram, keys):
    guids = match_edges(diagram, keys)
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)


def select_faces(diagram, keys):
    guids = match_faces(diagram, keys)
    compas_rhino.rs.EnableRedraw(False)
    compas_rhino.rs.SelectObjects(guids)
    compas_rhino.rs.EnableRedraw(True)


def is_valid_file(filepath, ext):
    """Is the selected path a valid file.

    Parameters
    ----------
    filepath
    """
    if not filepath:
        return False
    if not os.path.exists(filepath):
        return False
    if not os.path.isfile(filepath):
        return False
    if not filepath.endswith(".{}".format(ext)):
        return False
    return True


def select_filepath_open(root, ext):
    """Select a filepath for opening a session.

    Parameters
    ----------
    root : str
        Base directory from where the file selection is started.
        If no directory is provided, the parent folder of the current
        Rhino document will be used
    ext : str
        The type of file that can be openend.

    Returns
    -------
    tuple
        The parent directory.
        The file name.
    None
        If the procedure fails.

    Notes
    -----
    The file extension is only used to identify the type of session file.
    Regardless of the provided extension, the file contents should be in JSON format.

    """
    ext = ext.split('.')[-1]

    filepath = compas_rhino.select_file(folder=root, filter=ext)

    if not is_valid_file(filepath, ext):
        print("This is not a valid session file: {}".format(filepath))
        return

    return filepath


def select_filepath_save(root, ext):
    """Select a filepath for saving a session."""
    filepath = compas_rhino.rs.SaveFileName('save', filter=ext, folder=root)

    if not filepath:
        return

    if filepath.split('.')[-1] != ext:
        filepath = "%s.%s" % (filepath, ext)

    return filepath


def get_rv2():
    if "RV2" not in compas_rhino.sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return None
    return compas_rhino.sc.sticky["RV2"]


def get_scene():
    rv2 = get_rv2()
    if rv2:
        return rv2['scene']


def get_proxy():
    if "RV2.proxy" not in compas_rhino.sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return None
    return compas_rhino.sc.sticky["RV2.proxy"]


def get_system():
    if "RV2.system" not in compas_rhino.sc.sticky:
        form = TextForm('Initialise the plugin first!', 'RV2')
        form.show()
        return None
    return compas_rhino.sc.sticky["RV2.system"]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
