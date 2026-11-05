# Changelog

## [3.8.0] - 2026-11-05

### Changed
- The parcel dropdown now lists the same 59 numbers on every map. The map choice (working model, 1824 Stewart plan, 1841 tithe map of Landough, Cogan and Leckwith) changes which records show beneath a number, never the list; the tithe map no longer swaps in its own plot-number list. The list is always the 1824 Stewart plan figures; the tithe map's own plot numbers appear inside each record, never in the list. Legacy ?plot=N links open the parcel the plot is linked to.
- The native select is replaced by a custom dropdown (button plus listbox, with keyboard support), because browsers do not reliably colour native options. Each row carries a real CSS status dot plus a status word, so colour is never the only cue: green "concrete", amber "ambiguous", red "none". The same CSS dots restate the meanings in the key.
- Status colours follow the site's own per-parcel index and 1824 reading record: green only where the parcel's figure is clearly read in that record (the parcel-by-year sheet, tab 1824, "Number read?" = yes, outside the two-ways 30-39 / 50-59 band) and the parcel is placed, with its record (23 numbers); amber where something is held even if ambiguous (31: the homestead group 1-4, the unread figure 18, figures read unclearly or two ways, and the whole unsettled 30-39 / 50-59 band); red where nothing is held for that number yet (46-49 and 51). A tithe row linked via the site's reading never by itself makes a number green.
- Each number now carries its core identifying trait in brackets, taken only from the site's own index: an 1841 field name or land use with its tithe plot (Parsonage, Salt marsh, Cottage & garden, Old land, orchard, wood), the homestead-group note for 1-4, the unread-figure note for 18, and the paired reading for 50-59. Every tithe-derived bracket is marked as the site's own reading in place (e.g. "meadow, tithe plots 217/262 - site's reading"), and where a figure or pairing is unresolved the bracket says so too (e.g. "arable (use word unsettled), tithe plot 223 - site's reading - 33/53 unsettled", "figure unclear"), not only in a buried note. No trait is invented; where nothing is held the bracket says so.
- Working model: the 59 parcels head the list and the model's own lines (A+B, A, B, SA1-SA3, SA3+B) and data-file labels (A1-A3) sit in a separate group, marked as not matched to parcel numbers. Picking a parcel under the model explains that the ring's labels are not matched to Stewart numbers (open research) and what is held for the number.


## [3.7.0] - 2026-11-05

### Added
- A "Map" dropdown above the parcel dropdown, three entries: the working model of the title lines (not a survey map), the 1824 Stewart plan of Cedfin (parcels 1-59) and the 1841 tithe map (only the plots this page links to Stewart parcels, not every plot). The second dropdown refills for the chosen map and the text for the selection appears under the diagram.
- Working model: the ring's own lines (whole farm A+B, A, B, SA1, SA2, SA3, SA3+B) each draw on pick. The data file's labels A1, A2 and A3 are listed apart and draw nothing, because which ring line each matches has not been established.
- Stewart parcels and tithe plots: the circle shows only what the records tie to the pick (the 1841 listed owner and occupier, then a dashed unknown). Tithe landowner and occupier entries are shown as listings as written, not proof of title; replay, narration and node taps are off in these views so the farm-level chain does not appear. No journey is drawn where no transfer is tied to the number.
- Deep links: `?map=stewart&parcel=N`, `?map=tithe&plot=N`, `?map=model&p=KEY`.

### Changed
- The record sheet for a parcel is now text under the diagram, not a pop-up. The farm-level chain stays in a collapsed block, labelled as not tied to the number.
- 1987 is described as an application to merge titles, not a confirmed merger.
- Tithe plot 223: the earlier open note about an unnumbered 8a row is replaced by a source note. On page 12 of the library apportionment the 8a 0r 30p line sits against plot 223 (one-line offset); the land-use word is read by alignment and is not settled independently. Stewart plan figures are described as read from a phone photograph, not the archive image.

## [3.6.1] - 2026-11-05

### Changed
- App-first first screen: on load, only the header, the parcel dropdown and the diagram show. The introduction, the note on the 1824 Stewart plan parcel figures (including the unsettled 30-39 / 50-59 readings) and the title-chain link moved into a collapsed section under the diagram (steps list and caption likewise; replay opens the steps). Wording unchanged. The diagram is capped to the screen height. The shared Garden banner is not loaded on this page only (a page flag the banner script already honours); header and navigation unchanged.

## [3.6.0] - 2026-11-04

### Added
- A parcel dropdown, numbered 1-59, replacing the line-picker chips. Numbers are the parcel figures read on the 1824 Stewart plan of Cedfin (Tŷ Mawr). Each number opens a record sheet: the figure reading, the matching 1841 tithe plot with its entries as transcribed in the site's Tithe H3 index (land use, area, landowner, occupier), OS grid reference and traced area. Numbers 1-4 and 18 note the unread figures and the homestead group.
- The 30-39 / 50-59 readings are presented as unsettled: several southern figures can be read either way (old-style 3 or 5), so both readings are listed and numbers 46-59 stay in the dropdown with the ambiguity stated rather than a categorical exclusion. Parcel 33 carries the open unnumbered-8a-row conflict from the research register.
- Each sheet links the farm's documented chain (Bute -> Mountjoy -> Western Ground Rents -> BP Pension Trust -> BP Properties -> 1982/83 first registrations -> 1986/87 judgment) with a link to /title-chain/, scoped as farm-level, not parcel-tied.
- Record sheets now trap keyboard focus and make the background inert while open; the dropdown keeps the picked parcel selected; ?parcel=N deep links open the sheet directly.
- `public/data/stewart-parcels.json`: the per-parcel data, from the site's own Tithe H3 parcel table (`/tithe-h3/data/stewart-parcels.csv`); which plan parcel matches which tithe plot remains our reading, and the tithe records occupation, not ownership.
- `?parcel=N` opens a parcel's record directly.

### Changed
- The ring now draws every line on load; narration starts from the replay button. The line-filter chips are removed in favour of the parcel dropdown. Audio and animation paths unchanged (3.3.3).

## [3.5.0] - 2026-10-27

### Changed
- Parcel A in three parts, from the family's boundary plan: A1 the north wood (OS 1900 field 45), A2 the farmhouse, yard and buildings (south part of field 70), A3 the garden and orchard (north part of field 70, with the strip west to the road as its access). A3 is marked "title not traced"; the 1959 offer and the 1962 possession order name the garden with the farmhouse and buildings. The green keeps its own entry outside Parcel A, and its labels no longer call it A3. Animation paths and narration audio unchanged (3.3.3).

## [3.4.1] - 2026-10-27

### Fixed
- Parcel A boundary: Parcel A is the farmhouse, yard, buildings and woodland. On the family's boundary plan the Parcel A line ends before the green begins, so the green is no longer shown as a third of Parcel A. The green (village green VG41, registered by Glamorgan County Council in 1970) is shown as separate ground, outside Parcel A. A1/A2 now read "north part" / "south part"; A3 is relabelled "The green · VG41 (outside Parcel A)". Narration audio unchanged.

## [3.4.0] - 2026-10-25

### Added
- `title-chain/`: an animated, step-by-step title chain (Bute → Mountjoy → Western Ground Rents 1938 → BP 1969 → first registration 1982/83) beside the Williams occupation line, the twelve-year pairs (stacked from a common start) and the parcels taken. It reads the “title-chain” layer from the Cedwyn catalogue database (fallback: /research/layer.json); every step links to its catalogue ID. The courts’ view is shown first.
- A link to it above the circle diagram.

## [3.3.3] - 2026-10-24

### Fixed
- Align the embedded data, animation-path and audio cache version markers at `3.3.3` (they were inconsistent).
- Describe the 1877 Parcel A/B division as a proposed model pending a site-matched instrument, rather than a conclusively established split.
- Keep the known 1877 Clyde Street, Roath lease excluded from the Great House Farm title chain.

### Reviewed
- Preserved the existing case model and its cited records; this is a presentation/provenance clarification, not a legal finding.
