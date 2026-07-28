export * from "./mz-core.js";
export * from "./version.js";

export const MANIFEST_URL = new URL("../manifest.json", import.meta.url);
export async function getPackageManifest() {
  const response = await fetch(MANIFEST_URL);
  if (!response.ok) throw new Error("Mez package manifest unavailable");
  return response.json();
}
