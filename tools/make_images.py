#!/usr/bin/env python3
"""Draw the site's medical illustrations and icons as SVG (black, greys, one yellow accent).
Run from the repo root: python3 tools/make_images.py  -> assets/img/*.svg"""
import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

INK, G1, G2, G3, G4, Y = "#111111", "#3A3A3A", "#6E6E6E", "#D4D4D4", "#F2F2F2", "#FEDC34"

def svg(name, vb, body, title):
    OUT.joinpath(name + ".svg").write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}">'
        f'<title>{title}</title>{body}</svg>')

# ---------- shared shapes ----------
# long bone (femur-like), drawn in a 120 x 300 box
BONE = ("M42 22C40 6 80 6 78 22C96 22 100 48 82 58L76 74V226L82 242C100 252 100 284 82 288"
        "C72 291 66 283 60 283C54 283 48 291 38 288C20 284 20 252 38 242L44 226V74L38 58"
        "C20 48 24 22 42 22Z")
MARROW = "M52 80V220"  # faint centre line

def bone(x=0, y=0, s=1.0, fill=G4, stroke=INK, sw=3):
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="{BONE}" fill="{fill}" stroke="{stroke}" stroke-width="{sw/s:.2f}" stroke-linejoin="round"/>'
            f'<path d="M60 84V216" stroke="{G3}" stroke-width="{10/s:.2f}" stroke-linecap="round"/></g>')

def blob(cx, cy, rx, ry, sw=3, fill=Y):
    # an irregular tumour outline
    k = 0.55
    d = (f"M{cx-rx} {cy}C{cx-rx} {cy-ry*k-ry*.2} {cx-rx*k} {cy-ry} {cx+rx*.1} {cy-ry}"
         f"C{cx+rx*.8} {cy-ry*1.05} {cx+rx*1.1} {cy-ry*.4} {cx+rx} {cy+ry*.1}"
         f"C{cx+rx*.95} {cy+ry*.8} {cx+rx*.3} {cy+ry*1.05} {cx-rx*.2} {cy+ry}"
         f"C{cx-rx*.8} {cy+ry*.95} {cx-rx} {cy+ry*.5} {cx-rx} {cy}Z")
    return f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round"/>'

def label(x, y, text, anchor="start", size=13):
    return (f'<text x="{x}" y="{y}" font-family="Avenir, Nunito Sans, sans-serif" font-size="{size}" '
            f'font-weight="700" fill="{G1}" text-anchor="{anchor}">{text}</text>')

def leader(x1, y1, x2, y2):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{G2}" stroke-width="1.5"/><circle cx="{x1}" cy="{y1}" r="3" fill="{INK}"/>'

# ---------- 1. What is sarcoma: bone tumour ----------
svg("what-bone", "0 0 260 320",
    f'<rect width="260" height="320" rx="16" fill="{G4}"/>'
    + bone(70, 10, 1.0, fill="#fff")
    + blob(130, 228, 34, 30)
    + leader(160, 220, 200, 196) + label(200, 190, "Tumour", "start")
    + leader(130, 120, 200, 104) + label(200, 98, "Bone", "start"),
    "A long bone with a tumour growing near its lower end")

# ---------- 2. What is sarcoma: soft tissue tumour ----------
LIMB = "M70 12C40 40 32 120 40 200C46 260 60 300 70 312H190C200 300 214 260 220 200C228 120 220 40 190 12Z"
svg("what-soft", "0 0 260 320",
    f'<rect width="260" height="320" rx="16" fill="{G4}"/>'
    f'<path d="{LIMB}" fill="#fff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    f'<path d="M60 60C90 90 92 160 70 250M200 60C170 100 168 170 192 250" stroke="{G3}" stroke-width="2" fill="none"/>'
    + bone(98, 18, 0.95, fill=G4)
    + blob(194, 150, 16, 34)
    + leader(194, 128, 232, 40) + label(246, 32, "Tumour", "end")
    + leader(122, 100, 60, 40) + label(24, 32, "Bone", "start"),
    "A thigh with a tumour growing in the muscle beside the bone")

# ---------- 3. small icons for common types (96 x 96) ----------
def mini_bone(fill="#fff"):
    return bone(18, 4, 0.30, fill=fill, sw=2.4)  # occupies about x18-54, y6-92

TYPES = {
    "t-osteo": ("Osteosarcoma: a tumour near the end of a long bone",
                mini_bone() + blob(36, 70, 13, 11, sw=2)),
    "t-ewing": ("Ewing sarcoma: a tumour along the middle of a bone",
                mini_bone() + blob(36, 48, 12, 15, sw=2)),
    "t-chondro": ("Chondrosarcoma: a tumour in cartilage, often in the pelvis",
                  f'<path d="M20 30C20 14 48 10 60 24C72 10 96 14 92 34C90 50 74 54 70 70C66 82 50 82 46 70C42 54 20 48 20 30Z" fill="#fff" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
                  f'<circle cx="57" cy="66" r="7" fill="{G4}" stroke="{INK}" stroke-width="2"/>' + blob(36, 32, 11, 9, sw=2)),
    "t-soft": ("Soft tissue sarcoma: a tumour in the muscle or fat",
               f'<path d="M26 6C16 30 16 66 26 90H70C80 66 80 30 70 6Z" fill="#fff" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
               f'<path d="M48 10V86" stroke="{G3}" stroke-width="7" stroke-linecap="round"/>' + blob(64, 48, 9, 14, sw=2)),
    "t-gct": ("Giant cell tumour: in the bone end next to a joint",
              mini_bone() + blob(36, 86, 11, 6, sw=2)),
    "t-benign": ("Benign bone tumours such as bone cysts",
                 mini_bone() + f'<ellipse cx="36" cy="30" rx="6" ry="11" fill="#fff" stroke="{INK}" stroke-width="2"/>'
                 f'<circle cx="36" cy="70" r="3.5" fill="{Y}" stroke="{INK}" stroke-width="1.6"/>'),
    "t-mets": ("Metastasis: cancer spreading to bone from another organ",
               mini_bone() + f'<circle cx="78" cy="22" r="11" fill="{G4}" stroke="{INK}" stroke-width="2.4"/>'
               f'<path d="M70 32C62 40 54 46 44 50" stroke="{INK}" stroke-width="2" stroke-dasharray="3 3" fill="none"/>'
               f'<path d="M48 44l-6 7 9 1" stroke="{INK}" stroke-width="2" fill="none" stroke-linejoin="round"/>' + blob(36, 56, 7, 8, sw=2)),
    "t-myeloma": ("Myeloma: spots in the bone marrow of the spine",
                  "".join(f'<rect x="30" y="{8+i*17}" width="36" height="13" rx="4" fill="#fff" stroke="{INK}" stroke-width="2.2"/>' for i in range(5))
                  + "".join(f'<circle cx="{cx}" cy="{cy}" r="3.4" fill="{Y}" stroke="{INK}" stroke-width="1.4"/>' for cx, cy in [(42, 14), (56, 31), (40, 48), (54, 65), (46, 82)])),
}
for name, (title, body) in TYPES.items():
    svg(name, "0 0 96 96", f'<rect width="96" height="96" rx="14" fill="{G4}"/>' + body, title)

# ---------- 4. line icons (48 x 48, stroke style) ----------
def icon(name, title, paths, accent=""):
    svg(name, "0 0 48 48",
        f'<rect width="48" height="48" rx="12" fill="{G4}"/>{accent}'
        f'<g fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" transform="translate(12 12)">{paths}</g>', title)

icon("flag", "Warning flag",
     '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/>',
     f'<path d="M16 26.5s1-1 4-1 5 2 8 2 4-1 4-1V15s-1 1-4 1-5-2-8-2-4 1-4 1z" fill="{Y}"/>')
icon("d-consult", "Consultation and examination",
     '<path d="M11 2v2M5 2v2M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/><path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/>')
icon("d-scan", "X-ray and MRI scan",
     '<circle cx="12" cy="10" r="8"/><circle cx="12" cy="10" r="4"/><path d="M2 21h20M6 21v-3h12v3"/>',
     f'<circle cx="24" cy="22" r="4" fill="{Y}"/>')
icon("d-biopsy", "Needle biopsy",
     '<path d="m18 2 4 4M17 7l3-3M19 9 8.7 19.3c-1 1-2.5 1-3.4 0l-.6-.6c-1-1-1-2.5 0-3.4L15 5M9 11l4 4M5 19l-3 3M14 4l6 6"/>')
icon("d-staging", "Staging CT scan of the chest",
     '<path d="M12 3v18"/><path d="M12 6C8 4 4 7 4 12s1 8 4 8 4-3 4-6M12 6c4-2 8 1 8 6s-1 8-4 8-4-3-4-6"/>')
icon("d-board", "Tumour board: the team plans together",
     '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>')
icon("tx-surgery", "Surgery",
     '<path d="M3 21 15 9l3 3L6 21z"/><path d="m15 9 4-4a2.1 2.1 0 0 1 3 3l-4 4"/>')
icon("tx-chemo", "Chemotherapy",
     '<path d="M7 2h10v9a5 5 0 0 1-10 0z"/><path d="M12 16v3a3 3 0 0 0 3 3h3"/><path d="M7 7h10"/>',
     f'<path d="M19 19h10v4a5 5 0 0 1-10 0z" fill="{Y}"/>')
icon("tx-radio", "Radiotherapy",
     '<rect x="7" y="2" width="10" height="5" rx="1"/><path d="M12 7v3M8 10l-3 7M16 10l3 7M12 10v7"/><circle cx="12" cy="20" r="2"/>',
     f'<circle cx="24" cy="32" r="3.5" fill="{Y}"/>')
icon("tx-targeted", "Targeted therapy and clinical trials",
     '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
     f'<circle cx="24" cy="24" r="5" fill="{Y}"/>')

# ---------- 5. biopsy diagram ----------
svg("biopsy", "0 0 320 240",
    f'<rect width="320" height="240" rx="16" fill="{G4}"/>'
    f'<path d="M20 120H300" stroke="{G2}" stroke-width="2" stroke-dasharray="5 5"/>'
    + label(24, 112, "Skin", "start", 12)
    + f'<path d="M30 150H290V210H30Z" fill="#fff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    f'<path d="M40 180H280" stroke="{G3}" stroke-width="10" stroke-linecap="round"/>'
    + blob(200, 168, 44, 26)
    + f'<g transform="rotate(32 120 70)"><rect x="50" y="62" width="170" height="10" rx="3" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
    f'<rect x="20" y="54" width="34" height="26" rx="5" fill="{G1}"/><path d="M220 67H246" stroke="{INK}" stroke-width="3" stroke-linecap="round"/></g>'
    + leader(200, 190, 250, 228) + label(256, 232, "Tumour", "start", 12)
    + label(150, 30, "A thin core of tissue is taken through a small needle", "middle", 12),
    "A needle passing through the skin into a tumour to take a small sample")

# ---------- 6. surgery: curettage vs wide excision ----------
svg("surg-curettage", "0 0 260 300",
    f'<rect width="260" height="300" rx="16" fill="{G4}"/>'
    + bone(70, 4, 0.98, fill="#fff")
    + f'<path d="M110 200C108 182 150 182 150 200C150 222 110 222 110 200Z" fill="#fff" stroke="{INK}" stroke-width="2.5" stroke-dasharray="4 3"/>'
    f'<path d="M150 196l52-40" stroke="{INK}" stroke-width="5" stroke-linecap="round"/><circle cx="151" cy="197" r="6" fill="{Y}" stroke="{INK}" stroke-width="2"/>',
    "Curettage: the tumour is scraped out from inside the bone")
svg("surg-excision", "0 0 260 300",
    f'<rect width="260" height="300" rx="16" fill="{G4}"/>'
    + bone(70, 4, 0.98, fill="#fff")
    + f'<rect x="58" y="150" width="144" height="110" rx="10" fill="none" stroke="{INK}" stroke-width="2.5" stroke-dasharray="7 5"/>'
    + blob(130, 210, 30, 28),
    "Wide excision: the tumour is removed in one piece with a margin of healthy tissue")

# ---------- 7. reconstruction ----------
svg("r-mega", "0 0 200 260",
    f'<rect width="200" height="260" rx="16" fill="{G4}"/>'
    f'<path d="M82 14H118L114 120H86Z" fill="#fff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    f'<rect x="80" y="118" width="40" height="70" rx="6" fill="{G3}" stroke="{INK}" stroke-width="3"/>'
    f'<path d="M64 188H136C140 206 126 220 100 220C74 220 60 206 64 188Z" fill="{G2}" stroke="{INK}" stroke-width="3"/>'
    f'<path d="M66 228H134C128 244 72 244 66 228Z" fill="#fff" stroke="{INK}" stroke-width="3"/>'
    f'<circle cx="100" cy="203" r="5" fill="{Y}" stroke="{INK}" stroke-width="2"/>',
    "A metal megaprosthesis replacing the end of the bone and the knee joint")
svg("r-bio", "0 0 200 260",
    f'<rect width="200" height="260" rx="16" fill="{G4}"/>'
    + bone(40, -10, 0.92, fill="#fff")
    + f'<rect x="72" y="104" width="56" height="70" rx="4" fill="{Y}" fill-opacity=".55" stroke="{INK}" stroke-width="2.5"/>'
    f'<rect x="76" y="100" width="48" height="8" rx="2" fill="{G1}"/><rect x="76" y="170" width="48" height="8" rx="2" fill="{G1}"/>',
    "Biological reconstruction: a segment of treated bone fixed back in place")
svg("r-3d", "0 0 200 260",
    f'<rect width="200" height="260" rx="16" fill="{G4}"/>'
    f'<path d="M50 60C50 30 150 30 150 60C170 70 170 110 150 120L140 200C130 230 70 230 60 200L50 120C30 110 30 70 50 60Z" fill="#fff" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    + "".join(f'<path d="M{x} 70L{x+20} 200" stroke="{G3}" stroke-width="1.6"/>' for x in range(56, 150, 12))
    + "".join(f'<path d="M48 {y}H152" stroke="{G3}" stroke-width="1.6"/>' for y in range(80, 210, 14))
    + f'<path d="M50 60C50 30 150 30 150 60C170 70 170 110 150 120L140 200C130 230 70 230 60 200L50 120C30 110 30 70 50 60Z" fill="none" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    f'<circle cx="152" cy="40" r="10" fill="{Y}" stroke="{INK}" stroke-width="2"/>',
    "A custom 3D-printed implant with a lattice surface that bone can grow into")
print("images written to", OUT)

# ---------- 8. warm illustrations for the families page (320 x 240) ----------
def person(x, y, s=1.0, body=G3, head="#fff", accent=False):
    """A simple figure: round head and rounded shoulders. (x, y) is the top of the head."""
    r = 20 * s
    b = (f'<path d="M{x-34*s} {y+110*s}C{x-34*s} {y+62*s} {x-22*s} {y+48*s} {x} {y+48*s}'
         f'C{x+22*s} {y+48*s} {x+34*s} {y+62*s} {x+34*s} {y+110*s}Z" fill="{Y if accent else body}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
    h = f'<circle cx="{x}" cy="{y+r}" r="{r}" fill="{head}" stroke="{INK}" stroke-width="2.5"/>'
    return b + h

def scene(name, title, body):
    svg(name, "0 0 320 240", f'<rect width="320" height="240" rx="16" fill="{G4}"/>' + body, title)

GROUND = f'<path d="M24 206H296" stroke="{G3}" stroke-width="3" stroke-linecap="round"/>'
HEART = lambda x, y, s=1: (f'<path transform="translate({x} {y}) scale({s})" d="M0 6C0-2 10-4 12 3C14-4 24-2 24 6C24 14 12 20 12 22C12 20 0 14 0 6Z" '
                           f'fill="{Y}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>')

scene("p-family", "A family sitting close together",
      GROUND + person(110, 70, 1.1) + person(210, 66, 1.15) + person(160, 112, .8, accent=True)
      + f'<path d="M136 160C150 170 170 170 184 160" stroke="{INK}" stroke-width="2.5" fill="none" stroke-linecap="round"/>' + HEART(148, 34, 1))
scene("p-talk", "A parent and child talking",
      GROUND + person(110, 60, 1.25) + person(212, 110, .85, accent=True)
      + f'<rect x="150" y="40" width="84" height="40" rx="14" fill="#fff" stroke="{INK}" stroke-width="2.5"/><path d="M172 80l-6 12 16-12" fill="#fff" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
      + "".join(f'<circle cx="{cx}" cy="60" r="4" fill="{G2}"/>' for cx in (176, 192, 208)))
scene("p-dna", "A family tree with one highlighted person",
      f'<path d="M160 70V100M90 100H230M90 100V130M160 100V130M230 100V130" stroke="{G2}" stroke-width="2.5" fill="none"/>'
      f'<path d="M120 50H200" stroke="{G2}" stroke-width="2.5"/>'
      + "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}" stroke="{INK}" stroke-width="2.5"/>'
                for cx, cy, r, f in [(110, 50, 18, "#fff"), (210, 50, 18, "#fff"), (90, 150, 18, "#fff"), (160, 150, 18, Y), (230, 150, 18, "#fff")])
      + label(160, 210, "Very rarely passed down in families", "middle", 13))
scene("p-road", "A winding road with milestones",
      f'<path d="M30 200C110 200 60 120 150 120S210 50 290 46" stroke="{G3}" stroke-width="22" fill="none" stroke-linecap="round"/>'
      f'<path d="M30 200C110 200 60 120 150 120S210 50 290 46" stroke="#fff" stroke-width="2.5" stroke-dasharray="8 8" fill="none"/>'
      + "".join(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{f}" stroke="{INK}" stroke-width="2.5"/>' + label(cx, cy - 16, t, "middle", 12)
                for cx, cy, f, t in [(40, 200, "#fff", "Start"), (104, 160, "#fff", "Chemo"), (160, 118, "#fff", "Surgery"), (222, 76, "#fff", "Chemo"), (286, 46, Y, "Follow-up")]))
WHEEL = lambda cx: f'<circle cx="{cx}" cy="180" r="28" fill="none" stroke="{INK}" stroke-width="3"/><circle cx="{cx}" cy="180" r="3" fill="{INK}"/>'
scene("p-cycle", "A child riding a bicycle",
      GROUND + WHEEL(100) + WHEEL(220)
      + f'<path d="M100 180L140 130H200L220 180M140 130L162 180H100M162 180L200 130M136 118H152M196 120L204 108H216" stroke="{INK}" stroke-width="3" fill="none" stroke-linejoin="round" stroke-linecap="round"/>'
      + f'<circle cx="168" cy="52" r="16" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
      + f'<path d="M166 70L150 124M162 84L204 108M152 122L172 150L162 180" stroke="{Y}" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
      + f'<path d="M166 70L150 124M162 84L204 108M152 122L172 150L162 180" stroke="{INK}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".35"/>'
      + f'<path d="M40 120H70M30 140H64M44 100H66" stroke="{G2}" stroke-width="2.5" stroke-linecap="round"/>')
scene("p-counsel", "Two people talking with speech bubbles",
      GROUND + person(100, 90, 1.0) + person(220, 90, 1.0, accent=True)
      + f'<rect x="60" y="24" width="80" height="40" rx="14" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
      + f'<rect x="180" y="24" width="80" height="40" rx="14" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
      + f'<path d="M80 44H120M200 44H240" stroke="{G2}" stroke-width="3" stroke-linecap="round"/>' + HEART(148, 100, 1))
scene("p-circle", "A small circle of people around the patient",
      f'<circle cx="160" cy="120" r="84" fill="none" stroke="{G2}" stroke-width="2.5" stroke-dasharray="6 6"/>'
      + "".join(f'<circle cx="{cx}" cy="{cy}" r="20" fill="#fff" stroke="{INK}" stroke-width="2.5"/>' for cx, cy in [(160, 36), (76, 120), (244, 120), (160, 204)])
      + f'<circle cx="160" cy="120" r="26" fill="{Y}" stroke="{INK}" stroke-width="2.5"/>')
print("family illustrations written")
