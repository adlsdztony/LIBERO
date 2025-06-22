import os
import numpy as np
import re

from robosuite.models.objects import MujocoXMLObject
from robosuite.utils.mjcf_utils import xml_path_completion

import pathlib

absolute_path = pathlib.Path(__file__).parent.parent.parent.absolute()

from libero.libero.envs.base_object import (
    register_visual_change_object,
    register_object,
)

class RobosuiteObject(MujocoXMLObject):
    def __init__(self, custom_path, name, obj_name, joints=[dict(type="free", damping="0.0005")]):
        # make sure custom path is an absolute path
        assert(os.path.isabs(custom_path)), "Custom path must be an absolute path"
        # make sure the custom path is also an xml file
        assert(custom_path.endswith(".xml")), "Custom path must be an xml file"
        super().__init__(
            custom_path,
            name=name,
            joints=joints,
            obj_type="all",
            duplicate_collision_geoms=True,
        )
        self.category_name = "_".join(
            re.sub(r"([A-Z])", r" \1", self.__class__.__name__).split()
        ).lower()
        self.object_properties = {"vis_site_names": {}}

@register_object
class Bread(RobosuiteObject):
    def __init__(self,
                 name="bread",
                 obj_name="bread",
                 ):
        super().__init__(
            custom_path=os.path.join(
                str(absolute_path),
                f"assets/robosuite_objects/{obj_name}.xml",
            ),
            name=name,
            obj_name=obj_name,
        )

        self.rotation = {"x": (np.pi / 4, np.pi / 4)}
        self.rotation_axis = None


@register_object
class Lemon(RobosuiteObject):
    def __init__(self,
                 name="lemon",
                 obj_name="lemon",
                 ):
        super().__init__(
            custom_path=os.path.join(
                str(absolute_path),
                f"assets/robosuite_objects/{obj_name}.xml",
            ),
            name=name,
            obj_name=obj_name,
        )

        self.rotation = {}
        self.rotation_axis = None

@register_object
class Cereal(RobosuiteObject):
    def __init__(self,
                 name="cereal",
                 obj_name="cereal",
                 ):
        super().__init__(
            custom_path=os.path.join(
                str(absolute_path),
                f"assets/robosuite_objects/{obj_name}.xml",
            ),
            name=name,
            obj_name=obj_name,
        )

        self.rotation = {"x": (np.pi / 4, np.pi / 4)}
        self.rotation_axis = None

@register_object
class Soda(RobosuiteObject):
    def __init__(self,
                 name="soda",
                 obj_name="soda",
                 ):
        super().__init__(
            custom_path=os.path.join(
                str(absolute_path),
                f"assets/robosuite_objects/{obj_name}.xml",
            ),
            name=name,
            obj_name=obj_name,
        )

        self.rotation = {}
        self.rotation_axis = None


@register_object
class Coke(RobosuiteObject):
    def __init__(self,
                 name="coke",
                 obj_name="coke",
                 ):
        super().__init__(
            custom_path=os.path.join(
                str(absolute_path),
                f"assets/robosuite_objects/{obj_name}.xml",
            ),
            name=name,
            obj_name=obj_name,
        )

        self.rotation = {}
        self.rotation_axis = None


@register_object
class PlateWithHole(RobosuiteObject):
    def __init__(self,
                 name="plate_with_hole",
                 obj_name="plate_with_hole",
                 joints=None
                 ):
        super().__init__(
            custom_path=os.path.join(
                str(absolute_path),
                f"assets/robosuite_objects/{obj_name}.xml",
            ),
            name=name,
            obj_name=obj_name,
        )

        self.rotation = {}
        self.rotation_axis = None