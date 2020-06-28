from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rv2.rhino import get_scene


__commandname__ = "RV2thrust_move_supports"


def RunCommand(is_interactive):

    scene = get_scene()
    if not scene:
        return

    # both form and thrust need to be available

    form = scene.get("form")[0]
    if not form:
        print("There is no FormDiagram in the scene.")
        return

    thrust = scene.get("thrust")[0]
    if not thrust:
        print("There is no ThrustDiagram in the scene.")
        return

    # hide the form vertices
    form_vertices = "{}::vertices".format(form.settings['layer'])
    compas_rhino.rs.HideGroup(form_vertices)

    # show the thrust vertices
    thrust_vertices = "{}::vertices".format(thrust.settings['layer'])
    compas_rhino.rs.ShowGroup(thrust_vertices)

    compas_rhino.rs.Redraw()

    # select anchored vertices
    keys = thrust.select_vertices()
    keys[:] = [key for key in keys if thrust.datastructure.vertex_attribute(key, 'is_anchor')]

    if keys:
        if thrust.move_vertices_vertical(keys):
            for key in keys:
                # update the corresponding form diagram vertices
                z = thrust.datastructure.vertex_attribute(key, 'z')
                form.datastructure.vertex_attribute(key, 'z', z)

    # the scene needs to be updated
    # in any case
    # to reset object visualisation
    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
