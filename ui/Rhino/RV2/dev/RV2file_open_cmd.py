from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json

import compas_rhino
from compas_rv2.rhino import get_system
from compas_rv2.rhino import get_scene
from compas_rv2.rhino import select_filepath_open
from compas_rv2.datastructures import Pattern
from compas_rv2.datastructures import FormDiagram
from compas_rv2.datastructures import ForceDiagram
from compas_rv2.datastructures import ThrustDiagram
from compas.utilities import DataDecoder


__commandname__ = "RV2file_open"


HERE = compas_rhino.get_document_dirname()


def RunCommand(is_interactive):

    system = get_system()
    if not system:
        return

    scene = get_scene()
    if not scene:
        return

    filepath = select_filepath_open(system['session.dirname'], system['session.extension'])
    if not filepath:
        return

    dirname, basename = os.path.split(filepath)
    filename, extension = os.path.splitext(basename)

    system['session.dirname'] = dirname
    system['session.filename'] = filename

    with open(filepath, "r") as f:
        session = json.load(f, cls=DataDecoder)

    scene.clear()

    if 'settings' in session:
        scene.settings = session['settings']

    if 'data' in session:
        data = session['data']

        if 'pattern' in data and data['pattern']:
            pattern = Pattern.from_data(data['pattern'])

            scene.add(pattern, name="pattern")

        else:
            if 'form' in data and data['form']:
                form = FormDiagram.from_data(data['form'])
                thrust = form.copy(cls=ThrustDiagram)  # this is not a good idea

                scene.add(form, name="form")
                scene.add(thrust, name="thrust")

            if 'force' in data and data['force']:
                force = ForceDiagram.from_data(data['force'])

                force.primal = form
                form.dual = force

                scene.add(force, name="force")

    scene.update()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    RunCommand(True)
