/** Explicit approved Phase A ancestry for every Phase B functional specimen. */
export const PHASE_A_LINEAGE = Object.freeze({
  "B-DS01": ["FC01", "PO01", "PO02"],
  "B-DS02": ["SH01", "SH02", "SH03", "QC01", "QC02", "QC03"],
  "B-DS03": ["FS02", "HL01", "HL02"],
  "B-DS04": ["ES02", "IC01", "IC02", "IC03"],
  "B-DS05": ["FS01", "FC01", "FC02", "PO01", "PO02"],
  "B-DS06": ["FS01"],
  "B-DS07": ["PO01"],
  "B-DS08": ["BO01", "BO02", "QF01"],

  "B-FT01": ["ES02", "EX02"],
  "B-FT02": ["HL01", "HL02", "EX02"],
  "B-FT03": ["QF01", "SG01"],
  // Historical Round 02/03 evidence. Killed specimens are absent from the
  // active Round 04 definitions but their reviewed lineage remains preserved.
  "B-FT04": ["QC01", "QF01"],
  "B-FT05": ["QF01"],
  "B-FT06": ["IC01"],
  "B-FT07": ["FC01", "PO01"],
  "B-FT08": ["ES02", "ES04"],
  "B-FT09": ["QF03"],
  "B-FT10": ["EX02"],

  "B-PR01": ["SG01", "FC01"],
  "B-PR02": ["FC01", "PO02"],
  "B-PR03": ["FC02"],
  "B-PR04": ["PO01", "PO02"],
  "B-PR05": ["FC01"],
  "B-PR06": ["QF01"],
  "B-PR07": ["FS01"],
  "B-PR08": ["BO01", "BO02"],
  "B-PR09": ["QC02"],
  "B-PR10": ["FS02", "FC01", "FC02"],

  "B-CK01": ["SG01", "QF01"],
  "B-CK02": ["FC02"],
  "B-CK03": ["QF03"],
  "B-CK04": ["SG01"],
  "B-CK05": ["QC03"],
  "B-CK06": ["QC01"],
  "B-CK07": ["BO01"],
  "B-CK08": ["BO02"],

  "B-BU01": ["ST01", "ST02", "BX01", "BX02"],
  "B-BU02": ["BX01", "SG01"],
  "B-BU03": ["ST01", "ST02"],
  "B-BU04": ["FN01", "BX01", "BX02"],
  "B-BU05": ["SG01"],
  "B-BU06": ["PO01", "PO02"],
  "B-BU07": ["ST01"],
  "B-BU08": ["BO01", "BO02"],

  "B-MB01": ["QC04", "ES04", "HL04", "QF03", "PO01", "PO02"],
  "B-MB02": ["HL04", "FC01"],
  "B-MB03": ["QF03", "SG01"],
  "B-MB04": ["BO01", "PO02"],
});

export const approvedPhaseAIds = Object.freeze([...new Set(Object.values(PHASE_A_LINEAGE).flat())].sort());

export function phaseALineageFor(specimenId) {
  return PHASE_A_LINEAGE[specimenId] || [];
}
