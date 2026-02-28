bl_info = {
    "name": "Quick Object Select",
    "author": "Claude",
    "version": (1, 0),
    "blender": (3, 1, 0),
    "location": "3D Viewport > Press Alt+F (or search 'Quick Select Object')",
    "description": "Keyboard-driven object selector with live filtering dropdown",
    "category": "Object",
}

import bpy
import blf
import gpu
from gpu_extras.batch import batch_for_shader

# ─── Configuration ────────────────────────────────────────────────────────────
FONT_SIZE       = 18
PADDING         = 10
ROW_HEIGHT      = 28
MAX_VISIBLE     = 12          # max rows shown in dropdown
BOX_WIDTH       = 400
INPUT_HEIGHT    = 40
CORNER_RADIUS   = 6           # visual only (drawn as rect)

# Colors (R, G, B, A)
COL_BG          = (0.15, 0.15, 0.15, 0.92)
COL_INPUT_BG    = (0.20, 0.20, 0.20, 1.0)
COL_BORDER      = (0.40, 0.40, 0.40, 1.0)
COL_HIGHLIGHT   = (0.25, 0.50, 0.85, 1.0)
COL_TEXT        = (0.95, 0.95, 0.95, 1.0)
COL_DIM_TEXT    = (0.60, 0.60, 0.60, 1.0)
COL_CURSOR      = (0.90, 0.90, 0.90, 1.0)
COL_MATCH       = (0.40, 0.80, 1.00, 1.0)


# ─── Drawing helpers ──────────────────────────────────────────────────────────

def draw_rect(x, y, w, h, color):
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'TRI_FAN', {"pos": [
        (x,     y),
        (x + w, y),
        (x + w, y + h),
        (x,     y + h),
    ]})
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)


def draw_rect_outline(x, y, w, h, color, thickness=1):
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    verts = [
        (x,         y),           (x + w,     y),
        (x + w,     y),           (x + w,     y + h),
        (x + w,     y + h),       (x,         y + h),
        (x,         y + h),       (x,         y),
    ]
    batch = batch_for_shader(shader, 'LINES', {"pos": verts})
    shader.bind()
    shader.uniform_float("color", color)
    batch.draw(shader)


def draw_text(text, x, y, size=FONT_SIZE, color=COL_TEXT):
    font_id = 0
    blf.size(font_id, size, 72)
    blf.color(font_id, *color)
    blf.position(font_id, x, y, 0)
    blf.draw(font_id, text)


def text_width(text, size=FONT_SIZE):
    font_id = 0
    blf.size(font_id, size, 72)
    return blf.dimensions(font_id, text)[0]


# ─── Operator ─────────────────────────────────────────────────────────────────

class OBJECT_OT_quick_select(bpy.types.Operator):
    """Keyboard-driven object selector  (Alt+F)"""
    bl_idname  = "object.quick_select"
    bl_label   = "Quick Select Object"
    bl_options = {'REGISTER', 'UNDO'}

    # ── state ──────────────────────────────────────────────────────────────
    _handle   = None
    _query    = ""
    _items    = []        # filtered list of object names
    _cursor   = 0         # index in filtered list (highlighted row)
    _scroll   = 0         # first visible row index
    _multi    = False     # whether Shift was held on Enter
    _origin   = (0, 0)   # top-left of the widget

    # ── helpers ────────────────────────────────────────────────────────────
    def _all_objects(self, context):
        return sorted(context.scene.objects.keys())

    def _filter(self, context):
        q = self._query.lower()
        if not q:
            return self._all_objects(context)
        return [n for n in self._all_objects(context) if q in n.lower()]

    def _clamp_cursor(self):
        if not self._items:
            self._cursor = 0
            self._scroll = 0
            return
        self._cursor = max(0, min(self._cursor, len(self._items) - 1))
        visible = min(MAX_VISIBLE, len(self._items))
        if self._cursor < self._scroll:
            self._scroll = self._cursor
        if self._cursor >= self._scroll + visible:
            self._scroll = self._cursor - visible + 1

    def _select_current(self, context):
        if not self._items:
            return
        name = self._items[self._cursor]
        obj  = context.scene.objects.get(name)
        if obj is None:
            return
        if not self._multi:
            # deselect all first
            for o in context.selected_objects:
                o.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj

    # ── widget origin (centered in viewport) ───────────────────────────────
    def _compute_origin(self, context):
        region = context.region
        cx = region.width  // 2 - BOX_WIDTH // 2
        cy = region.height // 2 + (INPUT_HEIGHT + ROW_HEIGHT * min(MAX_VISIBLE, max(1, len(self._items)))) // 2
        return (cx, cy)

    # ── draw callback ──────────────────────────────────────────────────────
    def _draw(self, context):
        visible_count = min(MAX_VISIBLE, len(self._items))
        drop_h  = visible_count * ROW_HEIGHT
        total_h = INPUT_HEIGHT + drop_h
        x, y_top = self._origin
        y_input   = y_top - INPUT_HEIGHT
        y_drop    = y_input - drop_h

        gpu.state.blend_set('ALPHA')

        # ── dropdown background ──
        if self._items:
            draw_rect(x, y_drop, BOX_WIDTH, drop_h, COL_BG)
            draw_rect_outline(x, y_drop, BOX_WIDTH, drop_h, COL_BORDER)

        # ── draw rows ──
        for i in range(visible_count):
            idx  = self._scroll + i
            name = self._items[idx]
            ry   = y_input - (i + 1) * ROW_HEIGHT

            if idx == self._cursor:
                draw_rect(x, ry, BOX_WIDTH, ROW_HEIGHT, COL_HIGHLIGHT)

            # draw name with matched part highlighted
            q = self._query.lower()
            tx = x + PADDING
            ty = ry + (ROW_HEIGHT - FONT_SIZE) // 2 + 2
            if q and q in name.lower():
                lo = name.lower().index(q)
                hi = lo + len(q)
                draw_text(name[:lo],      tx,                           ty, color=COL_TEXT)
                draw_text(name[lo:hi],    tx + text_width(name[:lo]),   ty, color=COL_MATCH)
                draw_text(name[hi:],      tx + text_width(name[:hi]),   ty, color=COL_TEXT)
            else:
                draw_text(name, tx, ty, color=COL_TEXT)

            # object type hint (right-aligned, dim)
            obj = context.scene.objects.get(name)
            if obj:
                hint = obj.type.capitalize()
                hw   = text_width(hint, size=14)
                draw_text(hint, x + BOX_WIDTH - hw - PADDING, ty, size=14, color=COL_DIM_TEXT)

        # ── input box background ──
        draw_rect(x, y_input, BOX_WIDTH, INPUT_HEIGHT, COL_INPUT_BG)
        draw_rect_outline(x, y_input, BOX_WIDTH, INPUT_HEIGHT, COL_HIGHLIGHT)

        # ── prompt + query text ──
        prompt = "🔍 "
        draw_text(prompt + self._query,
                  x + PADDING,
                  y_input + (INPUT_HEIGHT - FONT_SIZE) // 2 + 2)

        # ── blinking cursor (simple: always visible) ──
        cx = x + PADDING + text_width(prompt + self._query) + 2
        cy_line = y_input + (INPUT_HEIGHT - FONT_SIZE) // 2 + 2
        draw_rect(cx, cy_line, 2, FONT_SIZE, COL_CURSOR)

        # ── hint line at bottom ──
        hint_y = y_drop - 20
        draw_text("Enter=select  Shift+Enter=add  Esc=cancel  ↑↓=navigate",
                  x, hint_y, size=13, color=COL_DIM_TEXT)

        gpu.state.blend_set('NONE')

    # ── modal ──────────────────────────────────────────────────────────────
    def modal(self, context, event):
        context.area.tag_redraw()

        if event.type == 'ESC' and event.value == 'PRESS':
            self._finish(context)
            return {'CANCELLED'}

        if event.type in ('RET', 'NUMPAD_ENTER') and event.value == 'PRESS':
            self._multi = event.shift
            self._select_current(context)
            self._finish(context)
            return {'FINISHED'}

        if event.type == 'UP_ARROW' and event.value in ('PRESS', 'REPEAT'):
            self._cursor -= 1
            self._clamp_cursor()
            return {'RUNNING_MODAL'}

        if event.type == 'DOWN_ARROW' and event.value in ('PRESS', 'REPEAT'):
            self._cursor += 1
            self._clamp_cursor()
            return {'RUNNING_MODAL'}

        if event.type == 'PAGE_UP' and event.value in ('PRESS', 'REPEAT'):
            self._cursor = max(0, self._cursor - MAX_VISIBLE)
            self._clamp_cursor()
            return {'RUNNING_MODAL'}

        if event.type == 'PAGE_DOWN' and event.value in ('PRESS', 'REPEAT'):
            self._cursor = min(len(self._items) - 1, self._cursor + MAX_VISIBLE)
            self._clamp_cursor()
            return {'RUNNING_MODAL'}

        if event.type == 'BACK_SPACE' and event.value in ('PRESS', 'REPEAT'):
            if event.ctrl:
                self._query = ""
            else:
                self._query = self._query[:-1]
            self._items  = self._filter(context)
            self._cursor = 0
            self._scroll = 0
            self._origin = self._compute_origin(context)
            return {'RUNNING_MODAL'}

        if event.type == 'TAB' and event.value == 'PRESS':
            # Tab cycles through matches without committing
            if self._items:
                self._cursor = (self._cursor + 1) % len(self._items)
                self._clamp_cursor()
            return {'RUNNING_MODAL'}

        # Printable character
        if event.value == 'PRESS' and event.ascii and event.ascii.isprintable():
            self._query += event.ascii
            self._items  = self._filter(context)
            self._cursor = 0
            self._scroll = 0
            self._origin = self._compute_origin(context)
            return {'RUNNING_MODAL'}

        # Swallow all keyboard events so they don't pass through
        if event.type not in {'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE',
                               'TIMER', 'TIMER_REPORT', 'NONE'}:
            return {'RUNNING_MODAL'}

        return {'PASS_THROUGH'}

    # ── invoke ─────────────────────────────────────────────────────────────
    def invoke(self, context, event):
        if context.area.type != 'VIEW_3D':
            self.report({'WARNING'}, "Run this from the 3D Viewport")
            return {'CANCELLED'}

        self._query  = ""
        self._items  = self._filter(context)
        self._cursor = 0
        self._scroll = 0
        self._origin = self._compute_origin(context)

        self._handle = context.space_data.draw_handler_add(
            self._draw, (context,), 'WINDOW', 'POST_PIXEL')

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def _finish(self, context):
        if self._handle:
            context.space_data.draw_handler_remove(self._handle, 'WINDOW')
            self._handle = None
        context.area.tag_redraw()


# ─── Keymap ───────────────────────────────────────────────────────────────────

addon_keymaps = []

def register():
    bpy.utils.register_class(OBJECT_OT_quick_select)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            OBJECT_OT_quick_select.bl_idname,
            type='F', value='PRESS', alt=True)
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    bpy.utils.unregister_class(OBJECT_OT_quick_select)

if __name__ == "__main__":
    register()