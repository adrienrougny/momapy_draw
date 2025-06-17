import momapy.core
import momapy.builder
import momapy.geometry
import momapy.positioning
import momapy.rendering.skia
import momapy.rendering.svg_native
import momapy.rendering.core

_layout_elements = []

DEFAULT_NODE_WIDTH = 80
DEFAULT_NODE_HEIGHT = 40


def init():
    global _layout_elements
    _layout_elements = []


def render(output_file_path, renderer="skia", format_="pdf", xsep=10, ysep=10):
    layout = momapy.core.LayoutBuilder()
    bbox = momapy.positioning.fit(_layout_elements)
    layout.width = bbox.width + xsep
    layout.height = bbox.height + ysep
    layout.position = bbox.position
    layout.layout_elements = _layout_elements
    momapy.rendering.core.render_layout_element(
        layout,
        output_file=output_file_path,
        to_top_left=False,
        renderer=renderer,
        format_=format_,
    )


def text(text, position=None, font_size=None):
    text_layout = momapy.builder.new_builder_object(momapy.core.TextLayout)
    if position is None:
        position = momapy.geometry.Point(0, 0)
    text_layout.position = position
    text_layout.text = text
    if font_size is not None:
        text_layout.font_size = font_size
    _layout_elements.append(text_layout)
    return text_layout


def node(
    cls: momapy.core.Node,
    position=None,
    width=None,
    height=None,
    text=None,
    font_size=None,
    text_fill=None,
    stroke=None,
    fill=None,
    fit_label=True,
    anchor=None,
):
    node = momapy.builder.new_builder_object(cls)
    if position is None:
        position = momapy.geometry.Point(0, 0)
    elif isinstance(position, tuple):
        position = momapy.geometry.Point.from_tuple(position)
    momapy.positioning.set_position(node, position, anchor)
    if width:
        node.width = width
    if height:
        node.height = height
    if text is not None:
        label = momapy.builder.new_builder_object(momapy.core.TextLayout)
        label.position = node.label_center()
        label.text = text
        if font_size is not None:
            label.font_size = font_size
        if text_fill:
            if isinstance(text_fill, str):
                text_fill = getattr(momapy.coloring, text_fill)
                if text_fill is None:
                    raise ValueError("provided fill color does not exist")
            label.fill = text_fill
        node.label = label
        if fit_label:
            label_bbox = label.ink_bbox()
            width = label_bbox.width + 0.05 * label_bbox.width
            height = label_bbox.height + 0.05 * label_bbox.height
            if width > node.width:
                node.width = width
            if height > node.height:
                node.height = height
    if stroke is not None:
        if isinstance(stroke, str):
            stroke = getattr(momapy.coloring, stroke)
            if stroke is None:
                raise ValueError("provided stroke color does not exist")
        node.stroke = stroke
    if fill is not None:
        if isinstance(fill, str):
            fill = getattr(momapy.coloring, fill)
            if fill is None:
                raise ValueError("provided fill color does not exist")
        node.fill = fill
    _layout_elements.append(node)
    return node


def arc(
    cls: momapy.core.SingleHeadedArc | momapy.core.DoubleHeadedArc,
    source=None,
    target=None,
    points=None,
):
    arc = momapy.builder.new_builder_object(cls)
    if source is None and target is None and points is None:
        raise ValueError(
            "you must provide a source and a target, or a source and points, or a target and points"
        )
    if points is None:
        points = []
    if source is not None:
        arc.source = source
        if target is not None:
            reference_point = target.center()
        else:
            reference_point = points[0]
        start_point = source.border(reference_point)
        points = [start_point] + points
    if target is not None:
        arc.target = target
        if source is not None:
            reference_point = source.center()
        else:
            reference_point = points[-1]
        end_point = target.border(reference_point)
        points = points + [end_point]
    segments = []
    for start_point, end_point in zip(points[:-1], points[1:]):
        segment = momapy.geometry.Segment(start_point, end_point)
        segments.append(segment)
    arc.segments = segments
    _layout_elements.append(arc)
    return arc
