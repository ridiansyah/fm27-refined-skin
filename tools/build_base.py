"""Build an editable base skin from decompiled FM27 stylesheets."""
import sys, os, re, shutil
SRC, DEST = sys.argv[1], sys.argv[2]
COND = ["TransferDeadlineDay.uss", "UEFASuperCup.uss", "StreamedObjectListStyles.uss"]

def root_vars(text):
    out, f = {}, False
    for line in text.splitlines():
        if line.startswith(":root {"): f = True; continue
        if f and line.startswith("}"): f = False; continue
        if f:
            m = re.match(r'\s*(--[\w-]+)\s*:', line)
            if m: out[m.group(1)] = line
    return out

base = open(os.path.join(SRC, "AlwaysAppliedStyleSheet.uss")).read()
blocks, cur, f = [], [], False
for line in base.splitlines():
    if line.startswith(":root {"): f = True; cur = []; continue
    if f and line.startswith("}"): f = False; blocks.append(cur); continue
    if f: cur.append(line)

guarded = {}
for c in COND:
    for k in root_vars(open(os.path.join(SRC, c)).read()):
        guarded.setdefault(k, c.replace(".uss", ""))

os.makedirs(DEST, exist_ok=True)
with open(os.path.join(DEST, "variables.uss"), "w") as o:
    o.write("""/* Native FM27 variables extracted from AlwaysAppliedStyleSheet.
 * Generated file: put personal overrides in custom.uss.
 *
 * Commented declarations:
 *  - "native game asset": image, font, or cursor references kept by the game.
 *  - "overridden by ...": special game styles override these variables.
 *    Leaving them commented preserves competition and event styling.
 */
""")
    for b in blocks:
        o.write("\n:root {\n")
        for line in b:
            m = re.match(r'\s*(--[\w-]+)\s*:', line)
            if m and m.group(1) in guarded:
                o.write("  /* overridden by %s: %s */\n" % (guarded[m.group(1)], line.strip()))
            else:
                o.write(line + "\n")
        o.write("}\n")

ref = os.path.join(DEST, "reference")
os.makedirs(ref, exist_ok=True)
for fn in sorted(os.listdir(SRC)):
    if fn.endswith(".uss"):
        shutil.copy(os.path.join(SRC, fn), os.path.join(ref, fn))
print("root blocks:", [len(b) for b in blocks], "guarded:", len(guarded))
