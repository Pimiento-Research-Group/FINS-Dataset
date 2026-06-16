import pandas as pd
from docx import Document

f = '/Volumes/External_memory/Dropbox/Kristina_PhD_K_version/Manuscripts/Descriptor/For_submission/Global Ecology and Biogeography/R1/'
df = pd.read_csv(f + "Data_S4.csv")

def parse_authors(raw_authors: str):
    if not raw_authors:
        return []

    s = raw_authors.strip().strip(",")

    if "&" in s:
        # Normalize spaces around &
        s_norm = s.replace(" & ", "|||").replace("&", "|||")
        parts = [p.strip().strip(",") for p in s_norm.split("|||") if p.strip().strip(",")]
        return parts

    parts = [p.strip().strip(",") for p in s.split(",") if p.strip().strip(",")]
    return parts

def format_authors_apa6(raw_authors: str) -> str:
    authors = parse_authors(raw_authors)

    if not authors:
        return ""

    n = len(authors)

    if n == 1:
        return authors[0]
    elif 2 <= n <= 7:
        return ", ".join(authors[:-1]) + ", & " + authors[-1]
    else:
        first_six = ", ".join(authors[:6])
        last = authors[-1]
        return f"{first_six}, ... {last}"

doc = Document()

for _, row in df.iterrows():
    raw_authors = str(row.get("author", "")).strip().rstrip(",")
    year = str(row.get("year", "")).strip()
    title = str(row.get("title", "")).strip().rstrip(".")
    journal = str(row.get("journal_detail", "")).strip().rstrip(".")
    doi = str(row.get("DOI", "")).strip()

    authors_str = format_authors_apa6(raw_authors)

    parts = []

    if authors_str:
        if year:
            parts.append(f"{authors_str} ({year}).")
        else:
            parts.append(f"{authors_str}.")
    elif year:
        parts.append(f"({year}).")

    if title:
        parts.append(f"{title}.")

    if journal:
        parts.append(f"{journal}.")

    # Only add DOI if non-empty and not nan
    if doi and doi.lower() != "nan":
        parts.append(f"DOI: {doi}.")

    # Join all parts with spaces
    ref_line = " ".join(parts).strip()

    # Add to document (empty lines will be skipped)
    if ref_line:
        doc.add_paragraph(ref_line)


doc.save(f + "Appendix_1.docx")



# == TEMP - Add journal details ==

fins = ("/Volumes/External_memory/Dropbox/FINS_dataset/Data/Master_files/fins.xlsx")
refs = pd.read_excel(fins, "References")

pbdb_refs = pd.read_csv('/Volumes/External_memory/Downloads/pbdb_data(10).csv')


def build_pagestring(row):
    parts = []

    # pubtitle always first if present
    if pd.notna(row['pubtitle']) and row['pubtitle'] != "":
        parts.append(str(row['pubtitle']).strip())

    # pubvol + pubno formatting
    vol = str(row['pubvol']).strip() if pd.notna(row['pubvol']) else ""
    no = str(row['pubno']).strip() if pd.notna(row['pubno']) else ""

    if vol:
        if no:
            parts.append(f"{vol} ({no})")
        else:
            parts.append(f"{vol}")

    # pages: first-last
    first = str(row['firstpage']).strip() if pd.notna(row['firstpage']) else ""
    last = str(row['lastpage']).strip() if pd.notna(row['lastpage']) else ""

    if first:
        if last:
            parts.append(f"{first}-{last}")
        else:
            parts.append(f"{first}")

    # Join: ", " between main parts, ": " before pages
    if len(parts) >= 3:
        return f"{parts[0]}, {parts[1]}: {parts[2]}"
    elif len(parts) == 2:
        return f"{parts[0]}, {parts[1]}"
    elif len(parts) == 1:
        return parts[0]
    else:
        return ""


vals = []

for i, author in enumerate(refs["author1"]):
    if refs["journal_detail"].values[i] != 0:
        vals.append("")
        continue

    pagestr = 0

    for idx, auth in pbdb_refs["author1last"].items():
        if (
            author == auth and
            refs["year"].values[i] == pbdb_refs["pubyr"].values[idx] and
            refs["journal"].values[i] == pbdb_refs["pubtitle"].values[idx]
        ):
            row = pbdb_refs.loc[idx]
            pagestr = build_pagestring(row)
            break

    vals.append(pagestr)

refs["journal_detail_new"] = vals

refs.to_csv("/Volumes/External_memory/Dropbox/temp/refs_new_journal_details.csv")






