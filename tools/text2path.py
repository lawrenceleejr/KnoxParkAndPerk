"""Shape text with harfbuzz and emit SVG path data (y-down, baseline at y=0)."""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

class Face:
    def __init__(self, path):
        if path.endswith('.woff2'):
            import os, tempfile
            ttf_path = os.path.join(tempfile.gettempdir(),
                                    os.path.basename(path).replace('.woff2', '.ttf'))
            if not os.path.exists(ttf_path):
                f = TTFont(path)
                f.flavor = None
                f.save(ttf_path)
            path = ttf_path
        blob = hb.Blob.from_file_path(path)
        face = hb.Face(blob)
        self.hbfont = hb.Font(face)
        self.tt = TTFont(path)
        self.upem = face.upem
        self.glyphset = self.tt.getGlyphSet()
        self.order = self.tt.getGlyphOrder()

    def shape(self, text, size, letterspacing=0.0, features=None):
        """Return (path_d, advance_width) at given px size."""
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbfont, buf, features or {})
        scale = size / self.upem
        ls = letterspacing * size  # em units -> px
        x = 0.0
        parts = []
        for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
            gname = self.order[info.codepoint]
            pen = SVGPathPen(self.glyphset)
            t = Transform(scale, 0, 0, -scale, x + pos.x_offset*scale, -pos.y_offset*scale)
            tpen = TransformPen(pen, t)
            self.glyphset[gname].draw(tpen)
            d = pen.getCommands()
            if d:
                parts.append(d)
            x += pos.x_advance*scale + ls
        if letterspacing:
            x -= ls  # no trailing space
        return " ".join(parts), x
