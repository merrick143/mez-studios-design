# Mez Systems canonical cutover

Cutover ID: `CUTOVER-2026-07-21-01`  
Active migration snapshot: `0.1.0-alpha.1`  
Authority state: `canonical-active`

The activation is a two-phase handshake. The internal pack remains rank-one until its transfer record and this authority manifest share the cutover ID and this manifest is `canonical-active`. After activation, all new design-system work happens in `brand-kit/`; the old internal pack is a pinned archive and consumer reference.
