/* ZIP STORE writer: assets are already compressed PNG/WebP, so no dependency or
 * recompression is needed. Standard CRC-32 and central directory preserve bytes. */
const table = Uint32Array.from({ length: 256 }, (_, value) => {
  for (let bit = 0; bit < 8; bit++) value = (value >>> 1) ^ (value & 1 ? 0xedb88320 : 0);
  return value >>> 0;
});
function crc32(bytes) {
  let crc = 0xffffffff;
  for (const byte of bytes) crc = (crc >>> 8) ^ table[(crc ^ byte) & 255];
  return (crc ^ 0xffffffff) >>> 0;
}
function header(size) {
  const bytes = new Uint8Array(size); const view = new DataView(bytes.buffer);
  return { bytes, u16: (at, value) => view.setUint16(at, value, true), u32: (at, value) => view.setUint32(at, value, true) };
}
export function zipBlob(files) {
  const parts = []; const directory = []; let offset = 0; let count = 0;
  for (const [filename, data] of Object.entries(files)) {
    const name = new TextEncoder().encode(filename); const crc = crc32(data);
    const local = header(30); local.u32(0, 0x04034b50); local.u16(4, 20); local.u16(6, 0x800);
    local.u16(12, 33); local.u32(14, crc); local.u32(18, data.length); local.u32(22, data.length); local.u16(26, name.length);
    parts.push(local.bytes, name, data);
    const central = header(46); central.u32(0, 0x02014b50); central.u16(4, 20); central.u16(6, 20); central.u16(8, 0x800);
    central.u16(14, 33); central.u32(16, crc); central.u32(20, data.length); central.u32(24, data.length);
    central.u16(28, name.length); central.u32(42, offset); directory.push(central.bytes, name);
    offset += local.bytes.length + name.length + data.length; count++;
  }
  const size = directory.reduce((sum, part) => sum + part.length, 0);
  const end = header(22); end.u32(0, 0x06054b50); end.u16(8, count); end.u16(10, count); end.u32(12, size); end.u32(16, offset);
  return new Blob([...parts, ...directory, end.bytes], { type: 'application/zip' });
}
