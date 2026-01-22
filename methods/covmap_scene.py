import bpy

class COVMAP_SCENE(bpy.types.Operator):

    bl_label = "CovmapScene"
    bl_idname = "object.covmapscene"
    
    def execute(self, context):

        # Find the 3D View area and its region
        view3d_area = None
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                view3d_area = area
                break

        if view3d_area:
            # Create an override context for the operators
            # This allows the script to run viewport commands from the text editor
            ctx = bpy.context.copy()
            ctx['area'] = view3d_area
            ctx['region'] = view3d_area.regions[-1]

            # 1. Set Viewport to Top Orthographic
            bpy.ops.view3d.view_axis(ctx, type='TOP')
            
            # 2. Rotate 90 degrees (Numpad 6, six times)
            # 15 degrees = 0.261799 radians
            for _ in range(6):
                bpy.ops.view3d.view_orbit(ctx, angle=0.261799, type='ORBITRIGHT')

        # 3. Create the Plane
        bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
        plane = bpy.context.active_object

        # 4. Apply Scaling
        plane.scale[0] = 21.5   # X
        plane.scale[1] = 32.25  # Y

        # 5. Global Scale by (1 / 0.9)
        plane.scale *= (1 / 0.9)

        # Update the view to show changes
        bpy.context.view_layer.update()   
        
        return{"FINISHED"}