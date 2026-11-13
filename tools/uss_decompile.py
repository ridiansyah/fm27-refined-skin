"""Decompile Unity UI Toolkit StyleSheet assets from asset bundles into .uss text."""
import sys, os, re, UnityPy

REF = sys.argv[1]          # dir with Unity reference .cs files
OUT = sys.argv[2]          # output dir
BUNDLES = sys.argv[3:]

GROUPS = {"Inherited":1,"Layout":2,"Rare":3,"Shorthand":4,"Transform":5,"Transition":6,"Visual":7}
src = open(os.path.join(REF, "StylePropertyEnums.cs")).read()
off_m = re.search(r'k_GroupOffset\s*=\s*(\d+)', open(os.path.join(REF, "StylePropertyUtil.cs")).read())
OFFSET = int(off_m.group(1)) if off_m else 16
enum_ids = {}
for name, grp, idx in re.findall(r'(\w+) = StylePropertyGroup\.(\w+) << k_GroupOffset \| (\d+)', src):
    enum_ids[name] = (GROUPS[grp] << OFFSET) | int(idx)
util = open(os.path.join(REF, "StylePropertyUtil.cs")).read()
nm = util[util.index("s_NameToId"):]
nm = nm[:nm.index("};")]
ID2NAME = {}
for css, enum in re.findall(r'\{"([^"]+)", StylePropertyId\.(\w+)\}', nm):
    ID2NAME.setdefault(enum_ids[enum], css)

KEYWORDS = ["inherit","initial","auto","unset","true","false","none","cover","contain"]
FUNCS = ["unknown","var","env","linear-gradient","none","custom","tint","opacity","invert","grayscale","sepia","blur","contrast","hue-rotate","material-property"]
UNITS = ["","px","%","s","ms","deg","grad","rad","turn"]

def num(v):
    s = ("%.4f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s

def color(c):
    r,g,b,a = (round(c[k]*255) for k in "rgba")
    return "#%02X%02X%02X" % (r,g,b) if a == 255 else "rgba(%d, %d, %d, %s)" % (r,g,b,num(c["a"]))

class Sheet:
    def __init__(self, tt, asset_names):
        self.tt, self.asset_names = tt, asset_names
        self.unresolved = 0
    def val(self, h):
        t, i = h["m_ValueType"], h["valueIndex"]
        tt = self.tt
        if t == 1: return KEYWORDS[i] if i < len(KEYWORDS) else "/*kw%d*/" % i
        if t == 2: return num(tt["floats"][i])
        if t == 3:
            d = tt["dimensions"][i]; return num(d["value"]) + UNITS[d["unit"]]
        if t == 4: return color(tt["colors"][i])
        if t == 5: return 'resource("%s")' % tt["strings"][i]
        if t in (6, 13):
            self.unresolved += 1
            a = tt["assets"][i]
            return None, self.asset_names.get(a["m_PathID"], "asset")
        if t in (7, 8): return tt["strings"][i]
        if t == 9: return '"%s"' % tt["strings"][i].replace('"', '\\"')
        if t == 11: return ","
        if t == 12:
            self.unresolved += 1
            return None, "scalable-image"
        return "/*type%d*/" % t
    def values(self, hs):
        try:
            pos = [0]
            s = self._seq(hs, pos, -1)
            return s, None
        except _Bad as e:
            return None, str(e)
    def _seq(self, hs, pos, count):
        out = ""
        while pos[0] < len(hs) and count != 0:
            h = hs[pos[0]]; pos[0] += 1
            if h["m_ValueType"] == 10:
                fn = FUNCS[h["valueIndex"]]
                n = int(self.tt["floats"][hs[pos[0]]["valueIndex"]]); pos[0] += 1
                out += "%s(%s)" % (fn, self._seq(hs, pos, n))
            elif h["m_ValueType"] == 11:
                out += ","
            else:
                v = self.val(h)
                if isinstance(v, tuple): raise _Bad(v[1])
                out += v
            if pos[0] < len(hs) and hs[pos[0]]["m_ValueType"] != 11 and count != 1:
                out += " "
            count -= 1
        return out.replace(",", ", ").replace(",  ", ", ")

class _Bad(Exception): pass

def selector(cs):
    out = ""
    for sel in cs["m_Selectors"]:
        rel = sel["m_PreviousRelationship"]
        if out: out += " > " if rel == 1 else " "
        for p in sel["m_Parts"]:
            t, v = p["m_Type"], p["m_Value"]
            out += {1:"*", 2:v, 3:"."+v, 4:":"+v, 5:":"+v, 6:"#"+v}.get(t, "/*sel%d:%s*/" % (t, v))
    return out

os.makedirs(OUT, exist_ok=True)
summary = []
for b in BUNDLES:
    env = UnityPy.load(b)
    names = {}
    for o in env.objects:
        try: names[o.path_id] = o.peek_name() or o.type.name
        except Exception: pass
    for o in env.objects:
        if o.type.name != "MonoBehaviour": continue
        tt = o.read_typetree()
        if "m_Rules" not in tt: continue
        sh = Sheet(tt, names)
        lines, nprop, skipped = [], 0, 0
        for r in tt["m_Rules"]:
            sels = ",\n".join(selector(cs) for cs in r["m_ComplexSelectors"])
            if not sels: continue
            body = []
            for p in r["m_Properties"]:
                name = p["m_CustomName"] if p["m_Id"] == -1 else ID2NAME.get(p["m_Id"], "/*prop%d*/" % p["m_Id"])
                s, bad = sh.values(p["m_Values"])
                if bad:
                    body.append("  /* %s: native game asset (%s), cannot be represented as text */" % (name, bad)); skipped += 1
                else:
                    body.append("  %s: %s;" % (name, s)); nprop += 1
            lines.append("%s {\n%s\n}\n" % (sels, "\n".join(body)))
        bname = os.path.basename(b).replace(".bundle", "")
        fn = "%s.uss" % tt["m_Name"]
        with open(os.path.join(OUT, fn), "w") as f:
            f.write("/* Extracted from native FM27 stylesheet: %s (bundle %s). Personal use only. */\n\n" % (tt["m_Name"], bname))
            f.write("\n".join(lines))
        summary.append((fn, bname, len(tt["m_Rules"]), nprop, skipped))
for s in sorted(summary, key=lambda x: -x[2]): print("%-45s %-35s rules=%-5d props=%-6d asset-skip=%d" % s)
unknown = set()
