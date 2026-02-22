# Watercolor Dissolution Aesthetics MCP Server

A medium transformation domain for mapping photographic fidelity to painterly abstraction through watercolor-specific dissolution behaviors.

Unlike subject domains (heraldry, cocktails, botanical growth) that describe *what* is depicted, this is a **process domain** — it describes *how* one visual regime dissolves into another. Structurally analogous to `film_color_grading`, it operates as a modifier layer applicable to any subject matter.

## Origin

This domain emerged from analyzing a digital watercolor treatment of an urban mural and discovering that the phenomena making the image distinctive — selective fidelity fields, pigment hydrology, edge negotiation typology, substrate assertion — had no vocabulary anywhere in a 16-domain aesthetic ecosystem. Cross-ecosystem keyword search returned only tangential matches. The gap was real.

## 5D Parameter Space

| Axis | 0.0 | 1.0 |
|------|-----|-----|
| `dissolution_rate` | Full photographic fidelity | Complete painterly abstraction |
| `edge_coherence` | All edges feathered/bled | All edges architecturally sharp |
| `substrate_visibility` | Paper/ground completely hidden | Paper is dominant visual element |
| `pigment_hydrology` | Dry brush, controlled marks | Flooding wet-on-wet, maximum water |
| `anchor_density` | Pure abstraction, no recognizable objects | Dense photographic anchors throughout |

**Validation:** Round-trip error 0.0087, symmetry 0.994. Decomposition accuracy 100% (6/6 types correctly recovered), mean reconstruction error 0.0042.

## Visual Types

### Editorial Wash
`(0.15, 0.85, 0.10, 0.20, 0.90)`

Watercolor as decorative accent on editorial photography. Sharp subject retention with selective background washes. Magazine illustration aesthetic — the medium enhances without overriding.

### Contested Boundary
`(0.50, 0.50, 0.35, 0.50, 0.50)`

Equal tension between photographic and painterly regimes. Multiple edge types coexist: architectural hard edges alongside cauliflower backruns alongside feathered bleeds. The viewer oscillates between reading photograph and painting. This is where the source image lives.

### Full Dissolution
`(0.85, 0.15, 0.75, 0.85, 0.10)`

The watercolor medium dominates completely. Paper texture prominent, pigment behavior (blooms, backruns, granulation) is primary visual interest. Original content survives only as vague shapes or color memory.

### Ghost Impression
`(0.65, 0.75, 0.50, 0.10, 0.20)`

The paradoxical type: high dissolution WITH high edge coherence. Content faded but structural edges remain crisp — dry technique. Blueprint washed with tea. Architectural and cartographic palimpsest aesthetic.

### Substrate Emergence
`(0.70, 0.30, 0.85, 0.40, 0.30)`

Paper itself as primary subject. Deliberate restraint — vast white spaces carry compositional weight equal to painted areas. Japanese *ma* (間) aesthetic applied to watercolor.

### Chromatic Flood
`(0.90, 0.20, 0.50, 0.95, 0.15)`

Maximum wet-on-wet saturation. Pigment hydrology drives everything — blooms, runs, capillary action, gravity-fed drips. Backruns and blooms become the content itself. Abstract expressionist watercolor.

## Supplementary Taxonomies

### Edge Modes (6)
The domain identifies six distinct boundary-resolution strategies that coexist within a single image:

- **Architectural Hard** — sharp geometric edges persisting through dissolution (brick mortar, rooflines)
- **Cauliflower Backrun** — fractal bloom patterns where wet pigment meets damp pigment
- **Feathered Bleed** — soft gradient diffusion into wet paper, no hard stop
- **Silhouette Cut** — high-contrast shape recognition through value rather than line
- **Granulation Boundary** — stippled transition where heavy pigment particles separate
- **Wet Lift** — negative-space edge created by removing pigment from wet surface

### Hydrology States (5)
Pigment-water behavior from dry to flooding: `dry_brush`, `controlled_wash`, `wet_on_dry`, `wet_on_wet`, `flooding`.

### Substrate Types (5)
Paper surface properties: `hot_press` (smooth), `cold_press` (standard), `rough`, `yupo` (synthetic non-absorbent), `masa` (Japanese absorbent).

### Color Harmony Modes (5)
`source_inherited`, `analogous_warm`, `complementary_tension`, `monochromatic_value`, `desaturated_ghost`.

### Contrast Curves (6)
`photographic_preserved`, `lifted_wash`, `high_key_dissolution`, `anchor_contrast`, `granulation_curve`, `flood_flat`.

## Three-Layer Architecture

| Layer | Purpose | Cost |
|-------|---------|------|
| **Layer 1** | Pure taxonomy retrieval — enumerate styles, types, states, presets | 0 tokens |
| **Layer 2** | Deterministic computation — classify, decompose, map, interpolate, validate | 0 tokens |
| **Layer 3** | Claude synthesis interface — structured data ready for LLM prompt generation | 1 LLM call |

## Tools (25)

### Layer 1 — Taxonomy (12 tools)
| Tool | Returns |
|------|---------|
| `get_server_info` | Server metadata, architecture overview |
| `list_dissolution_styles` | All 6 visual types with centers |
| `get_dissolution_style_details` | Complete spec for one style |
| `get_dissolution_visual_types` | Types with keywords and optical properties |
| `get_dissolution_canonical_states` | All 10 canonical states with coordinates |
| `list_edge_modes` | 6 edge negotiation modes |
| `list_hydrology_states` | 5 pigment hydrology states |
| `list_substrate_types` | 5 paper/substrate types |
| `list_color_harmony_modes` | 5 color harmony modes |
| `list_contrast_curves` | 6 contrast curve types |
| `list_dissolution_rhythmic_presets` | 5 Phase 2.6 rhythmic presets |
| `list_dissolution_attractor_presets` | 7 attractor presets with basin radii |

### Layer 2 — Computation (12 tools)
| Tool | Function |
|------|----------|
| `classify_dissolution_intent` | Keyword-match user description → style + hydrology + substrate |
| `decompose_dissolution_from_description` | Inverse pipeline: text → 5D coordinates |
| `map_dissolution_parameters` | Style → complete visual parameters with edge/hydrology/contrast |
| `extract_dissolution_visual_vocabulary` | Coordinates → interpolated vocabulary by category |
| `compute_dissolution_distance` | Euclidean distance between any two states |
| `compute_dissolution_trajectory` | Smooth interpolation path between states |
| `generate_dissolution_attractor_prompt` | State → image generation prompt (composite/split/sequence) |
| `generate_dissolution_rhythmic_sequence` | Custom oscillation between two states |
| `apply_dissolution_rhythmic_preset` | Apply curated rhythmic pattern |
| `generate_dissolution_sequence_prompts` | Rhythmic preset → keyframe prompts |
| `get_dissolution_domain_registry_config` | Tier 4D integration config |
| `validate_dissolution_decomposition_round_trip` | Self-test: keywords → decompose → verify |

### Layer 3 — Synthesis (1 tool)
| Tool | Function |
|------|----------|
| `enhance_dissolution_prompt` | Full pipeline: intent → classification → parameters → prompt |

## Rhythmic Presets

| Preset | Endpoints | Period | Character |
|--------|-----------|--------|-----------|
| `fidelity_breathing` | editorial_wash ↔ full_dissolution | 20 | Photography slowly dissolving into paint and reforming |
| `hydrology_pulse` | ghost_impression ↔ chromatic_flood | 16 | Skeletal dryness flooding into saturated color |
| `substrate_tide` | chromatic_flood ↔ substrate_emergence | 18 | Paper surface breathing through pigment coverage |
| `edge_negotiation` | editorial_wash ↔ contested_boundary | 22 | Edges softening and re-sharpening |
| `dissolution_sweep` | editorial_wash ↔ chromatic_flood | 24 | Full journey from editorial control to abstract flood |

## Compositional Potential

As a process/modifier domain, watercolor dissolution composes naturally with:

- **film_color_grading** — chromatic treatment applied to the watercolor palette
- **patina_weathering** — aging effects on the paper substrate itself
- **powers_of_ten** — scale-dependent dissolution (macro = photographic, micro = painterly)
- **botanical_growth** — organic growth patterns influencing bleed directions
- **stage_lighting** — light behavior through translucent wash layers

## Installation

### FastMCP Cloud
Entry point: `watercolor_dissolution_mcp.py:mcp`

The `main()` function returns the server object for cloud deployment.

### Local
```bash
pip install fastmcp
python __main__.py
```

## Quick Start

```python
# Classify what kind of dissolution treatment the user wants
classify_dissolution_intent("loose painterly watercolor with blooming wet effects")
# → full_dissolution, hydrology: flooding, confidence: 1.0

# Decompose an existing image description back to coordinates
decompose_dissolution_from_description("warm amber washes bleeding over brick...")
# → coordinates, nearest_type, confidence

# Get complete enhancement for prompt synthesis
enhance_dissolution_prompt(
    user_intent="urban mural with contested photo-paint tension",
    intensity="moderate"
)
# → classification + parameters + edge modes + hydrology + contrast + prompt

# Generate oscillating sequence between two aesthetic poles
apply_dissolution_rhythmic_preset("fidelity_breathing")
# → 20-step sinusoidal cycle, editorial_wash ↔ full_dissolution
```

## Validation

Round-trip self-test (`validate_dissolution_decomposition_round_trip`):

```
Nearest type accuracy: 1.0 (6/6)
Mean reconstruction error: 0.0042

  ✓ editorial_wash:      0.0006
  ✓ contested_boundary:  0.0008
  ✓ full_dissolution:    0.0015
  ✓ ghost_impression:    0.0060
  ✓ substrate_emergence: 0.0011
  ✓ chromatic_flood:     0.0152
```
