# This piece of code was written by rdb. It is reproduced here with
# permission, or rather, to quote him directly, "Consider it public
# domain. Credit rdb if you like."
# It is a bit too involved for me to grok quite yet. If you want to
# adapt it to any use case, godspeed.

from panda3d.core import CharacterJoint, CharacterSlider, CharacterVertexSlider
from panda3d.core import AnimBundle, AnimGroup, AnimChannelScalarDynamic
from panda3d.core import AnimChannelMatrixXfmTable, AnimChannelScalarTable
from panda3d.core import PTA_float


class MotionCapture:
    def __init__(self, actor, part_name="modelRoot", lod_name="lodRoot"):
        self.part_bundle = actor.get_part_bundle(part_name, lod_name)
        self.joint_tables = {}
        self.slider_tables = {}
        self.num_frames = 0

        for joint in actor.get_joints(partName=part_name, lodName=lod_name):
            if isinstance(joint, CharacterJoint):
                self.joint_tables[joint] = [PTA_float(), PTA_float(), PTA_float(), PTA_float(), PTA_float(), PTA_float(), PTA_float(), PTA_float(), PTA_float(), PTA_float(), PTA_float(), PTA_float()]
            elif isinstance(joint, CharacterSlider):
                self.slider_tables[joint] = PTA_float()

    def capture_frame(self):
        self.part_bundle.force_update()
        self.num_frames += 1

        for joint, tables in self.joint_tables.items():
            transform = joint.get_transform_state()

            scale = transform.get_scale()
            tables[0].push_back(scale.x)
            tables[1].push_back(scale.y)
            tables[2].push_back(scale.z)

            shear = transform.get_shear()
            tables[3].push_back(shear.x)
            tables[4].push_back(shear.y)
            tables[5].push_back(shear.z)

            hpr = transform.get_hpr()
            tables[6].push_back(hpr.x)
            tables[7].push_back(hpr.y)
            tables[8].push_back(hpr.z)

            pos = transform.get_pos()
            tables[ 9].push_back(pos.x)
            tables[10].push_back(pos.y)
            tables[11].push_back(pos.z)

        for slider, table in self.slider_tables.items():
            channel = slider.get_forced_channel()
            if channel and isinstance(channel, AnimChannelScalarDynamic):
                value_node = channel.value_node
                if value_node:
                    value = value_node.get_transform().get_pos()[0]
                else:
                    value = channel.value
            else:
                value = CharacterVertexSlider(slider).get_slider()
            table.push_back(value)

    def make_anim_bundle(self, name, fps):
        bundle = AnimBundle(name, fps, self.num_frames)

        for child in self.part_bundle.children:
            self._make_anim_group(bundle, child)

        return bundle

    def _make_anim_group(self, parent, part_group):
        joint_tables = self.joint_tables.get(part_group)
        slider_table = self.slider_tables.get(part_group)
        if joint_tables:
            group = AnimChannelMatrixXfmTable(parent, part_group.name)
            for i, table in enumerate(joint_tables):
                group.set_table('ijkabchprxyz'[i], table)

        elif slider_table:
            group = AnimChannelScalarTable(parent, part_group.name)
            group.set_table(slider_table)

        else:
            group = AnimGroup(parent, part_group.name)

        for child in part_group.children:
            self._make_anim_group(group, child)
