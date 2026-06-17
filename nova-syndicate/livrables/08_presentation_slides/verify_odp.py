import zipfile, re

z = zipfile.ZipFile(r"Z:\NOVA SYNDICATE V2\livrables\08_presentation_slides\Nova_Syndicate_Soutenance.odp", "r")
c = z.read("content.xml").decode("utf-8")
z.close()

pages = re.findall(r"<draw:page\s.*?</draw:page>", c, re.DOTALL)
print(f"Total slides: {len(pages)}")
for i, p in enumerate(pages):
    name_m = re.search(r'draw:name="([^"]+)"', p)
    spans = re.findall(r"<text:span[^>]*>([^<]+)</text:span>", p)
    name_str = name_m.group(1) if name_m else "?"
    texts = [s.strip() for s in spans if s.strip()]
    print(f"  Slide {i+1} ({name_str}): {texts[:5]}")
