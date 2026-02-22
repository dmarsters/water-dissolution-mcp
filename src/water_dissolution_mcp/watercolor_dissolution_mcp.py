"""
Watercolor Dissolution Aesthetics MCP Server

Medium transformation domain: maps photographic fidelity → painterly abstraction
through watercolor-specific dissolution behaviors.

Three-layer architecture:
  Layer 1 — Pure taxonomy retrieval (0 LLM tokens)
  Layer 2 — Deterministic computation (0 LLM tokens)
  Layer 3 — Claude synthesis interface (structured data for LLM)

5D Parameter Space:
  dissolution_rate:     0.0 (full photographic fidelity) → 1.0 (complete painterly abstraction)
  edge_coherence:       0.0 (all edges feathered/bled) → 1.0 (all edges architecturally sharp)
  substrate_visibility: 0.0 (paper/ground hidden) → 1.0 (paper is dominant visual element)
  pigment_hydrology:    0.0 (dry brush, controlled marks) → 1.0 (flooding wet-on-wet, max water)
  anchor_density:       0.0 (pure abstraction) → 1.0 (dense photographic anchors throughout)
"""

from fastmcp import FastMCP
import json
import math
from typing import Optional

mcp = FastMCP("Watercolor Dissolution")

# ─────────────────────────────────────────────────────────────────────
# TAXONOMY DATA — Layer 1 (pure reference, 0 tokens)
# ─────────────────────────────────────────────────────────────────────

PARAMETER_NAMES = [
    "dissolution_rate",
    "edge_coherence",
    "substrate_visibility",
    "pigment_hydrology",
    "anchor_density",
]

VISUAL_TYPES = {
    "editorial_wash": {
        "name": "Editorial Wash",
        "description": (
            "Watercolor as decorative accent on editorial photography. Strong "
            "compositional discipline from the photographic substrate. Controlled, "
            "selective color washes applied to backgrounds or secondary elements "
            "while subjects remain sharp. Magazine illustration aesthetic — the "
            "medium enhances without overriding."
        ),
        "center": {
            "dissolution_rate": 0.15,
            "edge_coherence": 0.85,
            "substrate_visibility": 0.10,
            "pigment_hydrology": 0.20,
            "anchor_density": 0.90,
        },
        "keywords": [
            "controlled color accent on photographic base",
            "selective background wash with sharp subject retention",
            "editorial substrate preserved through disciplined pigment",
            "sharp subject silhouette against soft color field",
            "magazine illustration quality watercolor atmosphere",
            "decorative watercolor border framing photographic content",
            "minimal dissolution preserving compositional hierarchy",
            "restrained wash enhancing without overriding source",
        ],
        "optical": {
            "finish": "matte_photographic",
            "scatter": "minimal_scatter",
            "transparency": "opaque_to_translucent",
        },
        "color_associations": [
            "muted editorial palette",
            "controlled accent hue",
            "neutral substrate",
            "photographic skin tones retained",
        ],
    },
    "contested_boundary": {
        "name": "Contested Boundary",
        "description": (
            "Equal tension between photographic and painterly regimes — neither "
            "wins. Multiple edge types coexist: architectural hard edges alongside "
            "cauliflower backruns alongside feathered bleeds. The defining "
            "characteristic is unresolved tension — the viewer oscillates between "
            "reading the image as a photograph and as a painting."
        ),
        "center": {
            "dissolution_rate": 0.50,
            "edge_coherence": 0.50,
            "substrate_visibility": 0.35,
            "pigment_hydrology": 0.50,
            "anchor_density": 0.50,
        },
        "keywords": [
            "competing visual regimes in unresolved tension",
            "coexisting edge types from architectural to cauliflower backrun",
            "selective dissolution frozen mid-process",
            "neither photograph nor painting but oscillating between",
            "mural-wall boundary bleeding across media regimes",
            "figure silhouette cutting through wash field",
            "photographic anchors amid painterly dissolution zones",
            "cauliflower backrun against architectural hard edge",
        ],
        "optical": {
            "finish": "mixed_finish",
            "scatter": "localized_halation",
            "transparency": "variable_transparency",
        },
        "color_associations": [
            "source-inherited warm palette",
            "analogous ambient temperature",
            "localized chroma variation",
            "pigment and photographic color coexisting",
        ],
    },
    "full_dissolution": {
        "name": "Full Dissolution",
        "description": (
            "The watercolor medium dominates completely. Paper texture is prominent "
            "— white space carries compositional weight. Pigment behavior (blooms, "
            "backruns, granulation) becomes the primary visual interest. Original "
            "photographic content survives only as vague shapes or color memory. "
            "Classic loose watercolor aesthetic."
        ),
        "center": {
            "dissolution_rate": 0.85,
            "edge_coherence": 0.15,
            "substrate_visibility": 0.75,
            "pigment_hydrology": 0.85,
            "anchor_density": 0.10,
        },
        "keywords": [
            "complete painterly takeover of photographic source",
            "paper texture as co-subject with pigment behavior",
            "pigment bloom dominant over representational content",
            "backrun cauliflower edges defining all boundaries",
            "granulation revealing paper tooth through diluted wash",
            "wet-on-wet diffusion fields replacing hard detail",
            "vague photographic memory beneath loose watercolor",
            "white paper breathing through composition as active element",
        ],
        "optical": {
            "finish": "paper_matte",
            "scatter": "diffuse_scatter",
            "transparency": "translucent_wash",
        },
        "color_associations": [
            "diluted source palette",
            "pigment granulation separating warm and cool",
            "paper white as active color",
            "watercolor-specific pigment interaction",
        ],
    },
    "ghost_impression": {
        "name": "Ghost Impression",
        "description": (
            "The paradoxical type: high dissolution WITH high edge coherence. "
            "Content has faded away but structural edges remain crisp because the "
            "technique was dry. Like a watercolor left in the sun, or a blueprint "
            "washed with tea. Minimal pigment, visible paper, but the drawing "
            "persists through the dissolution."
        ),
        "center": {
            "dissolution_rate": 0.65,
            "edge_coherence": 0.75,
            "substrate_visibility": 0.50,
            "pigment_hydrology": 0.10,
            "anchor_density": 0.20,
        },
        "keywords": [
            "faded dry-technique dissolution preserving edge structure",
            "crisp edges persisting despite dissolved content fill",
            "blueprint through tea wash palimpsest aesthetic",
            "architectural ghost drawing on aged paper",
            "cartographic palimpsest with structural traces",
            "minimal pigment with maximum structural retention",
            "sun-bleached watercolor memory of former content",
            "skeletal framework visible through translucent wash field",
        ],
        "optical": {
            "finish": "dry_matte",
            "scatter": "no_scatter",
            "transparency": "semi_transparent_dry",
        },
        "color_associations": [
            "faded tertiary palette",
            "desaturated earth memory",
            "parchment and iron-gall",
            "tea-stained substrate",
        ],
    },
    "substrate_emergence": {
        "name": "Substrate Emergence",
        "description": (
            "The paper itself becomes the primary subject. Deliberate restraint — "
            "vast white spaces carry as much compositional weight as painted areas. "
            "Negative space as positive content. Japanese ma aesthetic applied to "
            "watercolor — the intervals between marks matter more than the marks."
        ),
        "center": {
            "dissolution_rate": 0.70,
            "edge_coherence": 0.30,
            "substrate_visibility": 0.85,
            "pigment_hydrology": 0.40,
            "anchor_density": 0.30,
        },
        "keywords": [
            "paper as primary subject over pigment content",
            "negative space carrying positive compositional weight",
            "deliberate white space as compositional strategy",
            "breath between painted areas defining rhythm",
            "ma aesthetic applied to watercolor intervals",
            "unpainted ground as light source and structure",
            "island marks floating on paper ocean",
            "minimalist wash placement with maximum restraint",
        ],
        "optical": {
            "finish": "paper_dominant",
            "scatter": "zero_scatter",
            "transparency": "ground_as_light_source",
        },
        "color_associations": [
            "paper white dominant",
            "isolated chromatic islands",
            "controlled pigment economy",
            "sparse color against vast ground",
        ],
    },
    "chromatic_flood": {
        "name": "Chromatic Flood",
        "description": (
            "Maximum wet-on-wet saturation. Pigment hydrology drives everything — "
            "blooms, runs, capillary action, gravity-fed drips. The paper is "
            "covered rather than revealed. Color fields override subject matter. "
            "Backruns and blooms become the content itself. Abstract expressionist "
            "watercolor."
        ),
        "center": {
            "dissolution_rate": 0.90,
            "edge_coherence": 0.20,
            "substrate_visibility": 0.50,
            "pigment_hydrology": 0.95,
            "anchor_density": 0.15,
        },
        "keywords": [
            "maximum wet-on-wet saturation flooding surface",
            "pigment hydrology as primary content over subject",
            "gravity-fed drip and capillary action visible",
            "bloom and backrun as subject matter not artifact",
            "color field overriding representational content",
            "saturated wash flooding substrate with pigment",
            "abstract expressionist watercolor energy",
            "uncontrolled pigment interaction creating emergent pattern",
        ],
        "optical": {
            "finish": "wet_satin",
            "scatter": "maximum_scatter",
            "transparency": "saturated_translucent",
        },
        "color_associations": [
            "fully saturated primaries interacting",
            "uncontrolled pigment mixing zones",
            "wet interference patterns",
            "chromatic tide covering substrate",
        ],
    },
}

# 10 canonical states: 6 visual types + 4 interpolated positions
CANONICAL_STATES = {
    "editorial_wash": {
        "name": "Editorial Wash",
        "coordinates": VISUAL_TYPES["editorial_wash"]["center"],
        "source": "visual_type",
    },
    "light_wash": {
        "name": "Light Wash",
        "coordinates": {
            "dissolution_rate": 0.27,
            "edge_coherence": 0.73,
            "substrate_visibility": 0.18,
            "pigment_hydrology": 0.30,
            "anchor_density": 0.77,
        },
        "source": "interpolated",
        "description": "editorial_wash → contested_boundary at 33%",
    },
    "contested_boundary": {
        "name": "Contested Boundary",
        "coordinates": VISUAL_TYPES["contested_boundary"]["center"],
        "source": "visual_type",
    },
    "ghost_impression": {
        "name": "Ghost Impression",
        "coordinates": VISUAL_TYPES["ghost_impression"]["center"],
        "source": "visual_type",
    },
    "advancing_dissolution": {
        "name": "Advancing Dissolution",
        "coordinates": {
            "dissolution_rate": 0.68,
            "edge_coherence": 0.33,
            "substrate_visibility": 0.55,
            "pigment_hydrology": 0.68,
            "anchor_density": 0.30,
        },
        "source": "interpolated",
        "description": "contested_boundary → full_dissolution at 50%",
    },
    "substrate_emergence": {
        "name": "Substrate Emergence",
        "coordinates": VISUAL_TYPES["substrate_emergence"]["center"],
        "source": "visual_type",
    },
    "full_dissolution": {
        "name": "Full Dissolution",
        "coordinates": VISUAL_TYPES["full_dissolution"]["center"],
        "source": "visual_type",
    },
    "saturating_flood": {
        "name": "Saturating Flood",
        "coordinates": {
            "dissolution_rate": 0.88,
            "edge_coherence": 0.18,
            "substrate_visibility": 0.63,
            "pigment_hydrology": 0.90,
            "anchor_density": 0.13,
        },
        "source": "interpolated",
        "description": "full_dissolution → chromatic_flood at 50%",
    },
    "chromatic_flood": {
        "name": "Chromatic Flood",
        "coordinates": VISUAL_TYPES["chromatic_flood"]["center"],
        "source": "visual_type",
    },
    "restrained_study": {
        "name": "Restrained Study",
        "coordinates": {
            "dissolution_rate": 0.68,
            "edge_coherence": 0.53,
            "substrate_visibility": 0.68,
            "pigment_hydrology": 0.25,
            "anchor_density": 0.25,
        },
        "source": "interpolated",
        "description": "substrate_emergence → ghost_impression at 50%",
    },
}

# Contrast curves specific to watercolor dissolution behavior
EDGE_MODES = {
    "architectural_hard": {
        "name": "Architectural Hard Edge",
        "description": "Sharp boundary where built structure meets dissolution field. Brick mortar lines, rooflines, window frames retaining photographic precision.",
        "visual_effect": "Clean geometric cut through painterly atmosphere",
        "dissolution_resistance": 0.95,
        "typical_context": "Building edges, structural elements, geometric objects",
    },
    "cauliflower_backrun": {
        "name": "Cauliflower Backrun",
        "description": "Irregular organic edge where wet pigment meets damp pigment, creating fractal-like bloom patterns. Named for resemblance to cauliflower florets.",
        "visual_effect": "Organic fractal boundary with pigment concentration at rim",
        "dissolution_resistance": 0.15,
        "typical_context": "Wash boundaries, drying fronts, pigment pooling edges",
    },
    "feathered_bleed": {
        "name": "Feathered Bleed",
        "description": "Soft gradient boundary where pigment diffuses into wet paper. No hard stop — color fades gradually into substrate or adjacent wash.",
        "visual_effect": "Smooth gradient transition from saturated to transparent",
        "dissolution_resistance": 0.05,
        "typical_context": "Sky gradients, atmospheric diffusion, background washes",
    },
    "silhouette_cut": {
        "name": "Silhouette Cut",
        "description": "Sharp object boundary maintained by value contrast rather than line. Dark figure against light wash, or vice versa. The photographic substrate asserts through contrast.",
        "visual_effect": "High-contrast shape recognition persisting through dissolution",
        "dissolution_resistance": 0.80,
        "typical_context": "Human figures, strong-silhouette objects (fire hydrants, trees)",
    },
    "granulation_boundary": {
        "name": "Granulation Boundary",
        "description": "Textured edge where heavy pigment particles separate from vehicle, settling into paper tooth. Creates a stippled, grainy transition zone.",
        "visual_effect": "Particulate transition revealing paper micro-texture",
        "dissolution_resistance": 0.30,
        "typical_context": "Earth tones, mineral pigments, textured paper surfaces",
    },
    "wet_lift": {
        "name": "Wet Lift Edge",
        "description": "Boundary created by removing pigment from wet surface. Lighter than surrounding wash. Reveals paper through subtraction rather than addition.",
        "visual_effect": "Negative-space edge — light through dark rather than dark on light",
        "dissolution_resistance": 0.40,
        "typical_context": "Highlights, reflections, light sources, lifted cloud edges",
    },
}

# Pigment hydrology states
HYDROLOGY_STATES = {
    "dry_brush": {
        "name": "Dry Brush",
        "description": "Minimal water — pigment dragged across paper surface. Paper tooth catches pigment on high points, leaving valleys white. Maximum texture revelation.",
        "water_ratio": 0.05,
        "pigment_concentration": 0.90,
        "drying_behavior": "instant",
        "visual_character": "Broken, textured marks showing paper grain",
    },
    "controlled_wash": {
        "name": "Controlled Wash",
        "description": "Balanced water-to-pigment ratio. Even coverage with predictable edges. The workhorse technique — sufficient water for flow, enough pigment for saturation.",
        "water_ratio": 0.40,
        "pigment_concentration": 0.60,
        "drying_behavior": "even_recession",
        "visual_character": "Smooth even coverage with controlled edge quality",
    },
    "wet_on_dry": {
        "name": "Wet on Dry",
        "description": "Wet pigment applied to dry paper or dried wash. Creates hard edges where wet meets dry. Layering technique — each layer dries completely before next.",
        "water_ratio": 0.55,
        "pigment_concentration": 0.45,
        "drying_behavior": "hard_edge_formation",
        "visual_character": "Crisp layered washes with visible overlap edges",
    },
    "wet_on_wet": {
        "name": "Wet on Wet",
        "description": "Wet pigment into wet surface. Colors merge and diffuse unpredictably. Bloom formation. Soft edges everywhere. Requires timing and acceptance of partial control.",
        "water_ratio": 0.75,
        "pigment_concentration": 0.30,
        "drying_behavior": "bloom_formation",
        "visual_character": "Soft diffused edges with pigment migration and bloom",
    },
    "flooding": {
        "name": "Flooding",
        "description": "Excess water carrying dilute pigment. Gravity becomes co-artist — drips, runs, pooling. Capillary action pulls pigment into paper fibers. Maximum unpredictability.",
        "water_ratio": 0.92,
        "pigment_concentration": 0.12,
        "drying_behavior": "gravity_pooling_capillary",
        "visual_character": "Gravity-driven flow with capillary branching and pooling",
    },
}

# Substrate types
SUBSTRATE_TYPES = {
    "hot_press": {
        "name": "Hot Press (Smooth)",
        "description": "Smooth surface. Pigment sits on top rather than settling into valleys. Allows fine detail but washes can be uneven. Colors appear more vivid.",
        "tooth": 0.10,
        "absorbency": 0.30,
        "texture_visibility": 0.15,
        "best_for": "Fine detail, illustration, controlled washes",
    },
    "cold_press": {
        "name": "Cold Press (Medium Texture)",
        "description": "Standard watercolor paper. Moderate tooth provides texture without fighting detail. Most versatile — handles wet and dry techniques. The default.",
        "tooth": 0.50,
        "absorbency": 0.55,
        "texture_visibility": 0.50,
        "best_for": "General purpose, balanced wet and dry techniques",
    },
    "rough": {
        "name": "Rough",
        "description": "Heavy texture with deep valleys and high peaks. Dry brush skips across peaks creating maximum broken-texture effect. Washes settle unevenly, creating granulation.",
        "tooth": 0.85,
        "absorbency": 0.70,
        "texture_visibility": 0.85,
        "best_for": "Expressive texture, dry brush, atmospheric effects",
    },
    "yupo": {
        "name": "Yupo (Non-absorbent Synthetic)",
        "description": "Non-absorbent plastic surface. Pigment floats on top and can be moved indefinitely. Creates unique lifting and pooling effects. No paper grain.",
        "tooth": 0.02,
        "absorbency": 0.02,
        "texture_visibility": 0.05,
        "best_for": "Experimental effects, lifting, extended working time",
    },
    "masa": {
        "name": "Masa (Japanese)",
        "description": "Thin, absorbent Japanese paper. Pigment spreads rapidly through fibers. Very soft feathered edges. Ink-wash aesthetic. Fragile when wet.",
        "tooth": 0.20,
        "absorbency": 0.90,
        "texture_visibility": 0.25,
        "best_for": "Sumi-e aesthetic, rapid feathered diffusion, ink wash",
    },
}

# Rhythmic presets (Phase 2.6)
RHYTHMIC_PRESETS = {
    "fidelity_breathing": {
        "name": "Fidelity Breathing",
        "description": "Slow oscillation between photographic fidelity and painterly dissolution",
        "state_a": "editorial_wash",
        "state_b": "full_dissolution",
        "period": 20,
        "character": "Meditative transition — photography slowly dissolving into paint and reforming",
    },
    "hydrology_pulse": {
        "name": "Hydrology Pulse",
        "description": "Dry/wet cycling between ghost impression and chromatic flood",
        "state_a": "ghost_impression",
        "state_b": "chromatic_flood",
        "period": 16,
        "character": "Dramatic alternation — skeletal dryness flooding into saturated color",
    },
    "substrate_tide": {
        "name": "Substrate Tide",
        "description": "Paper appearing and disappearing beneath pigment",
        "state_a": "chromatic_flood",
        "state_b": "substrate_emergence",
        "period": 18,
        "character": "Tidal rhythm — paper surface breathing through pigment coverage",
    },
    "edge_negotiation": {
        "name": "Edge Negotiation",
        "description": "Edge sharpness cycling between editorial control and contested dissolution",
        "state_a": "editorial_wash",
        "state_b": "contested_boundary",
        "period": 22,
        "character": "Gentle oscillation — edges softening and re-sharpening",
    },
    "dissolution_sweep": {
        "name": "Dissolution Sweep",
        "description": "Full range editorial to chromatic flood",
        "state_a": "editorial_wash",
        "state_b": "chromatic_flood",
        "period": 24,
        "character": "Complete journey from controlled photography through dissolution to abstract flood",
    },
}

# Attractor presets
ATTRACTOR_PRESETS = {
    "editorial_discipline": {
        "name": "Editorial Discipline",
        "description": "Photographic control with watercolor as accent",
        "state": VISUAL_TYPES["editorial_wash"]["center"],
        "basin_radius": 0.25,
    },
    "creative_tension": {
        "name": "Creative Tension",
        "description": "Maximum unresolved regime competition",
        "state": VISUAL_TYPES["contested_boundary"]["center"],
        "basin_radius": 0.20,
    },
    "painterly_freedom": {
        "name": "Painterly Freedom",
        "description": "Complete watercolor dominance",
        "state": VISUAL_TYPES["full_dissolution"]["center"],
        "basin_radius": 0.25,
    },
    "spectral_trace": {
        "name": "Spectral Trace",
        "description": "Faded ghost of former fidelity",
        "state": VISUAL_TYPES["ghost_impression"]["center"],
        "basin_radius": 0.20,
    },
    "breath_of_paper": {
        "name": "Breath of Paper",
        "description": "Substrate as primary compositional element",
        "state": VISUAL_TYPES["substrate_emergence"]["center"],
        "basin_radius": 0.22,
    },
    "saturated_tide": {
        "name": "Saturated Tide",
        "description": "Maximum pigment hydrology",
        "state": VISUAL_TYPES["chromatic_flood"]["center"],
        "basin_radius": 0.25,
    },
    "balanced_study": {
        "name": "Balanced Study",
        "description": "Harmonized restraint between substrate and ghost",
        "state": CANONICAL_STATES["restrained_study"]["coordinates"],
        "basin_radius": 0.18,
    },
}

# Color harmony modes
COLOR_HARMONY_MODES = {
    "source_inherited": {
        "name": "Source Inherited",
        "description": "Watercolor palette derived from photographic source colors — washes in the same hue family as original content",
        "visual_effect": "Natural color continuity between photographic and painterly zones",
    },
    "analogous_warm": {
        "name": "Analogous Warm",
        "description": "Amber-gold-peach-cream palette favored in golden hour dissolution treatments",
        "visual_effect": "Warm harmonious flow unifying dissolution zones",
    },
    "complementary_tension": {
        "name": "Complementary Tension",
        "description": "Opposing hues in photographic vs painterly zones — cool editorial, warm watercolor (or reverse)",
        "visual_effect": "Chromatic regime separation reinforcing medium boundary",
    },
    "monochromatic_value": {
        "name": "Monochromatic Value",
        "description": "Single hue family with dissolution expressed through value and saturation shifts only",
        "visual_effect": "Pure tonal dissolution — medium change without hue change",
    },
    "desaturated_ghost": {
        "name": "Desaturated Ghost",
        "description": "Faded, low-chroma palette as if watercolor has aged or been sun-bleached",
        "visual_effect": "Temporal patina over dissolution — aged document quality",
    },
}

# Contrast curves
CONTRAST_CURVES = {
    "photographic_preserved": {
        "name": "Photographic Preserved",
        "description": "Full tonal range from source image maintained — watercolor as overlay not replacement",
        "toe_compression": 0.05,
        "shoulder_rolloff": 0.05,
        "midtone_contrast": 0.50,
        "visual_effect": "Source dynamic range visible through watercolor treatment",
    },
    "lifted_wash": {
        "name": "Lifted Wash",
        "description": "Raised black point — deepest darks replaced by paper-tone darks. Classic watercolor luminosity.",
        "toe_compression": 0.35,
        "shoulder_rolloff": 0.15,
        "midtone_contrast": 0.30,
        "visual_effect": "Luminous shadows where paper glows through thin pigment",
    },
    "high_key_dissolution": {
        "name": "High Key Dissolution",
        "description": "Majority of tonal range compressed into upper values. Content dissolves into light.",
        "toe_compression": 0.50,
        "shoulder_rolloff": 0.10,
        "midtone_contrast": 0.20,
        "visual_effect": "Content fading into paper white — dissolution as overexposure",
    },
    "anchor_contrast": {
        "name": "Anchor Contrast",
        "description": "Bimodal — strong contrast in anchor elements, flat in dissolution zones. Two tonal regimes coexisting.",
        "toe_compression": 0.10,
        "shoulder_rolloff": 0.10,
        "midtone_contrast": 0.65,
        "visual_effect": "Sharp photographic anchors punching through soft watercolor fields",
    },
    "granulation_curve": {
        "name": "Granulation Curve",
        "description": "Exaggerated midtone separation revealing pigment particle behavior. Shadows and highlights compressed.",
        "toe_compression": 0.25,
        "shoulder_rolloff": 0.25,
        "midtone_contrast": 0.70,
        "visual_effect": "Visible pigment granulation in midtones, compressed extremes",
    },
    "flood_flat": {
        "name": "Flood Flat",
        "description": "Minimal contrast — color fields at similar value. Chromaticity carries the composition instead of luminance.",
        "toe_compression": 0.40,
        "shoulder_rolloff": 0.40,
        "midtone_contrast": 0.15,
        "visual_effect": "Flat color fields where hue difference replaces value contrast",
    },
}


# ─────────────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────────────

def _euclidean_distance(a: dict, b: dict) -> float:
    """Euclidean distance between two states in 5D parameter space."""
    return math.sqrt(sum((a[k] - b[k]) ** 2 for k in PARAMETER_NAMES))


def _lerp_state(a: dict, b: dict, t: float) -> dict:
    """Linear interpolation between two states at parameter t ∈ [0, 1]."""
    return {k: a[k] + t * (b[k] - a[k]) for k in PARAMETER_NAMES}


def _nearest_visual_type(state: dict) -> tuple[str, float]:
    """Find nearest visual type to a given state. Returns (type_id, distance)."""
    best_id = ""
    best_dist = float("inf")
    for tid, tdata in VISUAL_TYPES.items():
        d = _euclidean_distance(state, tdata["center"])
        if d < best_dist:
            best_dist = d
            best_id = tid
    return best_id, best_dist


def _softmax(scores: dict, temperature: float = 1.0) -> dict:
    """Softmax over a dict of scores."""
    max_s = max(scores.values()) if scores else 0
    exp_s = {k: math.exp((v - max_s) / temperature) for k, v in scores.items()}
    total = sum(exp_s.values())
    return {k: v / total for k, v in exp_s.items()} if total > 0 else exp_s


def _interpolate_vocabulary(state: dict, strength: float = 1.0) -> dict:
    """Interpolate visual vocabulary from visual type proximities."""
    distances = {}
    for tid, tdata in VISUAL_TYPES.items():
        distances[tid] = _euclidean_distance(state, tdata["center"])

    # Convert distances to similarity scores (inverse distance)
    scores = {tid: 1.0 / (d + 0.01) for tid, d in distances.items()}
    weights = _softmax(scores, temperature=0.5)

    # Collect weighted vocabulary
    nearest_id = min(distances, key=distances.get)
    nearest = VISUAL_TYPES[nearest_id]

    # Blend keywords from top contributing types
    contributing = sorted(weights.items(), key=lambda x: -x[1])[:3]

    shadow_descriptors = []
    highlight_descriptors = []
    edge_descriptors = []
    substrate_descriptors = []
    hydrology_descriptors = []

    for tid, w in contributing:
        t = VISUAL_TYPES[tid]
        c = t["center"]
        if w > 0.1:
            # Edge character
            if c["edge_coherence"] > 0.7:
                edge_descriptors.append(f"architectural hard edges from {t['name']} regime")
            elif c["edge_coherence"] > 0.4:
                edge_descriptors.append(f"mixed edge negotiation from {t['name']} regime")
            else:
                edge_descriptors.append(f"feathered bleed edges from {t['name']} regime")

            # Substrate character
            if c["substrate_visibility"] > 0.7:
                substrate_descriptors.append(f"paper dominant — {t['name']} aesthetic")
            elif c["substrate_visibility"] > 0.3:
                substrate_descriptors.append(f"paper partially visible — {t['name']} zone")
            else:
                substrate_descriptors.append(f"substrate hidden — {t['name']} coverage")

            # Hydrology character
            if c["pigment_hydrology"] > 0.7:
                hydrology_descriptors.append(f"wet flooding behavior from {t['name']}")
            elif c["pigment_hydrology"] > 0.3:
                hydrology_descriptors.append(f"controlled wash from {t['name']}")
            else:
                hydrology_descriptors.append(f"dry technique from {t['name']}")

    return {
        "nearest_visual_type": nearest_id,
        "distance": distances[nearest_id],
        "keywords": nearest["keywords"],
        "optical_properties": nearest["optical"],
        "color_associations": nearest["color_associations"],
        "nearest_canonical_state": nearest_id,
        "canonical_distance": distances[nearest_id],
        "vocabulary_by_category": {
            "dissolution_character": [
                f"dissolution rate at {state['dissolution_rate']:.0%} — "
                + ("photographic dominant" if state["dissolution_rate"] < 0.3
                   else "mid-dissolution tension" if state["dissolution_rate"] < 0.6
                   else "painterly dominant"),
            ],
            "edge_character": edge_descriptors[:3] if edge_descriptors else ["balanced edge mix"],
            "substrate_character": substrate_descriptors[:3] if substrate_descriptors else ["moderate paper visibility"],
            "hydrology_character": hydrology_descriptors[:3] if hydrology_descriptors else ["controlled wash behavior"],
            "anchor_character": [
                f"anchor density at {state['anchor_density']:.0%} — "
                + ("dense photographic anchors throughout" if state["anchor_density"] > 0.7
                   else "scattered fidelity anchors" if state["anchor_density"] > 0.3
                   else "minimal anchoring — near-abstract")
            ],
        },
        "strength": strength,
        "input_state": state,
    }


# ─────────────────────────────────────────────────────────────────────
# LAYER 1 TOOLS — Pure taxonomy retrieval (0 LLM tokens)
# ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_server_info() -> str:
    """Get information about the Watercolor Dissolution MCP server."""
    return json.dumps({
        "name": "Watercolor Dissolution Aesthetics",
        "version": "1.0.0",
        "domain": "watercolor_dissolution",
        "description": (
            "Medium transformation domain mapping photographic fidelity to "
            "painterly abstraction through watercolor-specific dissolution behaviors. "
            "A process domain (like film_color_grading) rather than a subject domain — "
            "it describes HOW one visual regime dissolves into another."
        ),
        "parameter_space": {
            "dimensions": 5,
            "axes": {
                "dissolution_rate": "0.0 (photographic) → 1.0 (painterly abstraction)",
                "edge_coherence": "0.0 (feathered/bled) → 1.0 (architecturally sharp)",
                "substrate_visibility": "0.0 (paper hidden) → 1.0 (paper dominant)",
                "pigment_hydrology": "0.0 (dry brush) → 1.0 (flooding wet-on-wet)",
                "anchor_density": "0.0 (pure abstraction) → 1.0 (dense photographic anchors)",
            },
        },
        "visual_types": 6,
        "canonical_states": 10,
        "edge_modes": 6,
        "hydrology_states": 5,
        "substrate_types": 5,
        "rhythmic_presets": 5,
        "attractor_presets": 7,
        "color_harmony_modes": 5,
        "contrast_curves": 6,
        "layer_architecture": {
            "layer_1": "Pure taxonomy retrieval (0 tokens)",
            "layer_2": "Deterministic computation (0 tokens)",
            "layer_3": "Claude synthesis interface",
        },
    }, indent=2)


@mcp.tool()
def list_dissolution_styles() -> str:
    """List all 6 visual types with mood, character, and parameter centers.

    LAYER 1: Pure taxonomy enumeration (0 LLM tokens).

    Returns overview of: Editorial Wash, Contested Boundary, Full Dissolution,
    Ghost Impression, Substrate Emergence, Chromatic Flood."""
    styles = []
    for tid, t in VISUAL_TYPES.items():
        styles.append({
            "id": tid,
            "name": t["name"],
            "description": t["description"][:120] + "...",
            "center": t["center"],
        })
    return json.dumps({"styles": styles, "count": len(styles)}, indent=2)


@mcp.tool()
def get_dissolution_style_details(style_id: str) -> str:
    """Get complete specification for a dissolution style including keywords, optical, colors.

    LAYER 1: Pure taxonomy retrieval (0 LLM tokens).

    Args:
        style_id: One of: editorial_wash, contested_boundary, full_dissolution,
                  ghost_impression, substrate_emergence, chromatic_flood"""
    if style_id not in VISUAL_TYPES:
        return json.dumps({"error": f"Unknown style: {style_id}", "valid": list(VISUAL_TYPES.keys())})
    return json.dumps(VISUAL_TYPES[style_id], indent=2)


@mcp.tool()
def get_dissolution_visual_types() -> str:
    """List all 6 dissolution visual types with keywords and optical properties. Layer 1 (0 tokens)."""
    types = {}
    for tid, t in VISUAL_TYPES.items():
        types[tid] = {
            "name": t["name"],
            "center": t["center"],
            "keywords": t["keywords"][:4],
            "optical": t["optical"],
            "color_associations": t["color_associations"],
        }
    return json.dumps({"visual_types": types, "parameter_names": PARAMETER_NAMES}, indent=2)


@mcp.tool()
def get_dissolution_canonical_states() -> str:
    """List all 10 canonical dissolution states with 5D coordinates. Layer 1 (0 tokens)."""
    return json.dumps({"canonical_states": CANONICAL_STATES, "count": len(CANONICAL_STATES)}, indent=2)


@mcp.tool()
def list_edge_modes() -> str:
    """List all 6 watercolor edge negotiation modes. Layer 1 (0 tokens).

    Edge modes: architectural_hard, cauliflower_backrun, feathered_bleed,
    silhouette_cut, granulation_boundary, wet_lift."""
    return json.dumps({"edge_modes": EDGE_MODES, "count": len(EDGE_MODES)}, indent=2)


@mcp.tool()
def list_hydrology_states() -> str:
    """List all 5 pigment hydrology states from dry brush to flooding. Layer 1 (0 tokens)."""
    return json.dumps({"hydrology_states": HYDROLOGY_STATES, "count": len(HYDROLOGY_STATES)}, indent=2)


@mcp.tool()
def list_substrate_types() -> str:
    """List all 5 watercolor substrate types with texture properties. Layer 1 (0 tokens)."""
    return json.dumps({"substrate_types": SUBSTRATE_TYPES, "count": len(SUBSTRATE_TYPES)}, indent=2)


@mcp.tool()
def list_color_harmony_modes() -> str:
    """List all 5 color harmony modes for dissolution treatments. Layer 1 (0 tokens)."""
    return json.dumps({"color_harmony_modes": COLOR_HARMONY_MODES, "count": len(COLOR_HARMONY_MODES)}, indent=2)


@mcp.tool()
def list_contrast_curves() -> str:
    """List all 6 contrast curve types for dissolution treatments. Layer 1 (0 tokens)."""
    return json.dumps({"contrast_curves": CONTRAST_CURVES, "count": len(CONTRAST_CURVES)}, indent=2)


@mcp.tool()
def list_dissolution_rhythmic_presets() -> str:
    """List all 5 Phase 2.6 rhythmic presets for watercolor dissolution.

    Available presets:
        fidelity_breathing (20):    editorial_wash ↔ full_dissolution
        hydrology_pulse (16):       ghost_impression ↔ chromatic_flood
        substrate_tide (18):        chromatic_flood ↔ substrate_emergence
        edge_negotiation (22):      editorial_wash ↔ contested_boundary
        dissolution_sweep (24):     editorial_wash ↔ chromatic_flood"""
    return json.dumps({"rhythmic_presets": RHYTHMIC_PRESETS, "count": len(RHYTHMIC_PRESETS)}, indent=2)


@mcp.tool()
def list_dissolution_attractor_presets() -> str:
    """List all 7 attractor presets for dissolution visualization. Layer 2 (0 tokens)."""
    presets = {}
    for pid, p in ATTRACTOR_PRESETS.items():
        presets[pid] = {
            "name": p["name"],
            "description": p["description"],
            "state": p["state"],
            "basin_radius": p["basin_radius"],
        }
    return json.dumps({"attractor_presets": presets, "count": len(presets)}, indent=2)


# ─────────────────────────────────────────────────────────────────────
# LAYER 2 TOOLS — Deterministic computation (0 LLM tokens)
# ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def classify_dissolution_intent(user_intent: str) -> str:
    """Classify dissolution intent from user description.

    LAYER 2: Deterministic keyword matching (0 LLM tokens).

    Args:
        user_intent: Description of desired dissolution aesthetic"""
    text = user_intent.lower()

    # Score each visual type by keyword match
    type_scores = {}
    matched_keywords = {}

    # Dissolution keywords
    dissolution_terms = {
        "editorial_wash": ["editorial", "magazine", "controlled", "sharp subject", "accent", "selective", "subtle", "restrained"],
        "contested_boundary": ["tension", "between", "both", "neither", "oscillat", "coexist", "compete", "mural", "boundary", "mix"],
        "full_dissolution": ["loose", "dissolve", "painterly", "watercolor", "abstract", "bloom", "backrun", "complete"],
        "ghost_impression": ["ghost", "faded", "blueprint", "trace", "skeleton", "palimpsest", "bleach", "dry", "crisp edge"],
        "substrate_emergence": ["paper", "white space", "negative", "minimal", "restraint", "breath", "ma ", "sparse", "empty"],
        "chromatic_flood": ["flood", "saturated", "wet", "drip", "pour", "expressionist", "bold", "vivid", "maximum", "intense"],
    }

    # Hydrology keywords
    hydrology_terms = {
        "dry": ["dry brush", "dry", "textured", "broken", "scratchy"],
        "controlled": ["controlled", "even", "smooth", "balanced", "standard"],
        "wet_on_dry": ["layered", "crisp layer", "hard edge layer", "glazing"],
        "wet_on_wet": ["wet on wet", "diffuse", "merge", "soft edge", "bloom"],
        "flooding": ["flood", "drip", "gravity", "pour", "capillary", "run"],
    }

    for tid, terms in dissolution_terms.items():
        score = 0
        matches = []
        for term in terms:
            if term in text:
                score += 1
                matches.append(term)
        type_scores[tid] = score
        if matches:
            matched_keywords[tid] = matches

    # Determine primary style
    if max(type_scores.values()) == 0:
        primary = "contested_boundary"  # default to mid-range
        confidence = 0.3
    else:
        primary = max(type_scores, key=type_scores.get)
        confidence = min(1.0, max(type_scores.values()) / 4.0)

    # Detect hydrology preference
    hydrology_match = "controlled_wash"
    for hid, terms in hydrology_terms.items():
        for term in terms:
            if term in text:
                hydrology_match = hid if hid != "dry" else "dry_brush"
                break

    # Detect substrate preference
    substrate_match = "cold_press"
    if any(t in text for t in ["smooth", "fine detail", "illustration"]):
        substrate_match = "hot_press"
    elif any(t in text for t in ["rough", "texture", "expressive"]):
        substrate_match = "rough"
    elif any(t in text for t in ["japanese", "sumi", "ink wash"]):
        substrate_match = "masa"
    elif any(t in text for t in ["experimental", "synthetic", "yupo"]):
        substrate_match = "yupo"

    return json.dumps({
        "primary_style": primary,
        "style_details": {
            "name": VISUAL_TYPES[primary]["name"],
            "description": VISUAL_TYPES[primary]["description"][:150],
        },
        "confidence": confidence,
        "type_scores": type_scores,
        "matched_keywords": matched_keywords,
        "suggested_hydrology": hydrology_match,
        "suggested_substrate": substrate_match,
        "center": VISUAL_TYPES[primary]["center"],
    }, indent=2)


@mcp.tool()
def decompose_dissolution_from_description(description: str) -> str:
    """Decompose a text description into 5D dissolution parameter coordinates.

    LAYER 2: Deterministic keyword matching (0 LLM tokens).

    Inverse of the generative pipeline. Takes an image description and
    recovers the watercolor dissolution coordinates by matching against
    the 6 visual type keyword vocabularies.

    Args:
        description: Image description text (from Claude vision, user text,
                     or any text describing an aesthetic artifact)."""
    text = description.lower()

    # Score each visual type
    type_scores = {}
    matched_fragments = []

    # Keyword fragments to match (partial matching)
    fragment_map = {
        "editorial_wash": [
            "editorial", "magazine", "controlled", "sharp", "accent",
            "selective", "restrain", "subtle", "disciplin", "photographic",
        ],
        "contested_boundary": [
            "tension", "between", "neither", "oscillat", "coexist",
            "compete", "boundary", "unresolved", "both", "mural",
        ],
        "full_dissolution": [
            "dissolv", "loose", "bloom", "backrun", "granulat",
            "diffus", "abstract", "painterly", "watercolor", "paper texture",
        ],
        "ghost_impression": [
            "ghost", "faded", "blueprint", "palimpsest", "trace",
            "skeleton", "bleach", "dry", "parchment", "iron-gall",
        ],
        "substrate_emergence": [
            "paper", "white space", "negative space", "minimal",
            "restraint", "breath", "ma ", "sparse", "empty", "unpaint",
        ],
        "chromatic_flood": [
            "flood", "saturat", "wet-on-wet", "drip", "capillary",
            "pour", "expressionist", "bold color", "vivid", "chromatic",
        ],
    }

    # Also match optical/color terms
    optical_map = {
        "editorial_wash": ["matte", "opaque", "photographic"],
        "contested_boundary": ["mixed", "variable", "halation"],
        "full_dissolution": ["translucent", "diffuse", "paper matte"],
        "ghost_impression": ["dry matte", "semi transparent", "no scatter"],
        "substrate_emergence": ["paper dominant", "zero scatter", "ground"],
        "chromatic_flood": ["wet satin", "maximum scatter", "saturated"],
    }

    color_map = {
        "editorial_wash": ["neutral", "muted", "editorial"],
        "contested_boundary": ["warm", "analogous", "amber"],
        "full_dissolution": ["diluted", "granulation", "paper white"],
        "ghost_impression": ["faded", "earth", "parchment", "tea"],
        "substrate_emergence": ["white dominant", "sparse", "chromatic island"],
        "chromatic_flood": ["saturated", "vivid", "intense", "bright"],
    }

    for tid in VISUAL_TYPES:
        score = 0
        for frag in fragment_map.get(tid, []):
            if frag in text:
                score += 1
                matched_fragments.append(frag)
        for frag in optical_map.get(tid, []):
            if frag in text:
                score += 0.5
                matched_fragments.append(frag)
        for frag in color_map.get(tid, []):
            if frag in text:
                score += 0.5
                matched_fragments.append(frag)
        type_scores[tid] = score

    # Softmax to weights
    weights = _softmax(type_scores, temperature=1.0)

    # Weighted average of centers
    coordinates = {k: 0.0 for k in PARAMETER_NAMES}
    for tid, w in weights.items():
        center = VISUAL_TYPES[tid]["center"]
        for k in PARAMETER_NAMES:
            coordinates[k] += w * center[k]

    # Confidence: how much domain vocabulary is present
    total_matches = sum(type_scores.values())
    confidence = min(1.0, total_matches / 8.0)

    nearest_id, nearest_dist = _nearest_visual_type(coordinates)

    # Optical match from nearest type
    optical_match = VISUAL_TYPES[nearest_id]["optical"]
    color_matches = VISUAL_TYPES[nearest_id]["color_associations"]

    return json.dumps({
        "domain_id": "watercolor_dissolution",
        "coordinates": {k: round(v, 4) for k, v in coordinates.items()},
        "confidence": round(confidence, 4),
        "nearest_type": nearest_id,
        "nearest_type_distance": round(nearest_dist, 4),
        "type_scores": {k: round(v, 2) for k, v in type_scores.items()},
        "type_weights": {k: round(v, 4) for k, v in weights.items()},
        "matched_fragments": sorted(set(matched_fragments)),
        "optical_match": optical_match,
        "color_matches": color_matches,
        "detected": total_matches > 0,
    }, indent=2)


@mcp.tool()
def map_dissolution_parameters(
    style_id: str,
    intensity: str = "moderate",
    emphasis: str = "balanced",
    substrate: Optional[str] = None,
) -> str:
    """Map dissolution style to complete visual parameters.

    Layer 2: Deterministic operation (0 tokens).

    Args:
        style_id: Dissolution style ID
        intensity: subtle, moderate, or dramatic
        emphasis: dissolution, edge, substrate, hydrology, or balanced
        substrate: Optional substrate type to apply"""
    if style_id not in VISUAL_TYPES:
        return json.dumps({"error": f"Unknown style: {style_id}", "valid": list(VISUAL_TYPES.keys())})

    t = VISUAL_TYPES[style_id]
    state = dict(t["center"])

    # Intensity scaling
    intensity_scale = {"subtle": 0.6, "moderate": 1.0, "dramatic": 1.4}.get(intensity, 1.0)

    # Emphasis shifts
    emphasis_shifts = {
        "dissolution": {"dissolution_rate": 0.1, "anchor_density": -0.1},
        "edge": {"edge_coherence": 0.15},
        "substrate": {"substrate_visibility": 0.15},
        "hydrology": {"pigment_hydrology": 0.15},
        "balanced": {},
    }
    shifts = emphasis_shifts.get(emphasis, {})

    # Apply intensity and emphasis
    midpoint = {k: 0.5 for k in PARAMETER_NAMES}
    for k in PARAMETER_NAMES:
        deviation = (state[k] - midpoint[k]) * intensity_scale
        state[k] = max(0.0, min(1.0, midpoint[k] + deviation + shifts.get(k, 0.0)))

    nearest_id, nearest_dist = _nearest_visual_type(state)

    # Determine appropriate edge modes
    edge_modes = []
    if state["edge_coherence"] > 0.6:
        edge_modes.extend(["architectural_hard", "silhouette_cut"])
    if 0.3 <= state["edge_coherence"] <= 0.7:
        edge_modes.extend(["cauliflower_backrun", "granulation_boundary"])
    if state["edge_coherence"] < 0.4:
        edge_modes.extend(["feathered_bleed", "wet_lift"])

    # Determine hydrology state
    if state["pigment_hydrology"] < 0.15:
        hydrology = "dry_brush"
    elif state["pigment_hydrology"] < 0.35:
        hydrology = "controlled_wash"
    elif state["pigment_hydrology"] < 0.55:
        hydrology = "wet_on_dry"
    elif state["pigment_hydrology"] < 0.8:
        hydrology = "wet_on_wet"
    else:
        hydrology = "flooding"

    # Determine contrast curve
    if state["anchor_density"] > 0.7:
        contrast = "anchor_contrast"
    elif state["dissolution_rate"] > 0.8 and state["pigment_hydrology"] > 0.8:
        contrast = "flood_flat"
    elif state["dissolution_rate"] > 0.6:
        contrast = "high_key_dissolution"
    elif state["substrate_visibility"] > 0.6:
        contrast = "lifted_wash"
    else:
        contrast = "photographic_preserved"

    # Substrate
    substrate_data = None
    if substrate and substrate in SUBSTRATE_TYPES:
        substrate_data = SUBSTRATE_TYPES[substrate]

    # Build characteristics
    characteristics = []
    if state["dissolution_rate"] < 0.3:
        characteristics.append("photographic fidelity dominant with watercolor accents")
    elif state["dissolution_rate"] < 0.6:
        characteristics.append("contested territory between photographic and painterly regimes")
    else:
        characteristics.append("painterly dissolution overriding photographic source")

    if state["edge_coherence"] > 0.6:
        characteristics.append("sharp architectural edges persisting through dissolution")
    elif state["edge_coherence"] < 0.3:
        characteristics.append("all edges softened into feathered bleeds and backruns")

    if state["substrate_visibility"] > 0.6:
        characteristics.append("paper surface breathing through as compositional element")

    if state["pigment_hydrology"] > 0.7:
        characteristics.append("wet-on-wet pigment behavior driving visual texture")
    elif state["pigment_hydrology"] < 0.2:
        characteristics.append("dry technique preserving structural marks")

    if state["anchor_density"] > 0.6:
        characteristics.append("dense photographic anchors maintaining recognizability")
    elif state["anchor_density"] < 0.2:
        characteristics.append("near-abstract with minimal fidelity anchors")

    return json.dumps({
        "style_id": style_id,
        "style_name": t["name"],
        "intensity": intensity,
        "emphasis": emphasis,
        "weight": 1.0,
        "state": {k: round(v, 4) for k, v in state.items()},
        "nearest_visual_type": nearest_id,
        "visual_distance": round(nearest_dist, 4),
        "active_edge_modes": edge_modes,
        "edge_mode_details": {eid: EDGE_MODES[eid] for eid in edge_modes},
        "hydrology_state": hydrology,
        "hydrology_details": HYDROLOGY_STATES.get(hydrology, {}),
        "contrast_curve": contrast,
        "contrast_curve_details": CONTRAST_CURVES.get(contrast, {}),
        "substrate": substrate_data,
        "characteristics": characteristics,
        "optical_properties": t["optical"],
        "keywords": t["keywords"],
        "color_associations": t["color_associations"],
        "full_vocabulary": _interpolate_vocabulary(state)["vocabulary_by_category"],
    }, indent=2)


@mcp.tool()
def extract_dissolution_visual_vocabulary(
    state: Optional[dict] = None,
    dissolution_id: Optional[str] = None,
    strength: float = 1.0,
) -> str:
    """Extract visual vocabulary from dissolution parameter coordinates. Layer 2 (0 tokens).

    Provide either state (5D coordinates) or dissolution_id (canonical state name)."""
    if dissolution_id and dissolution_id in CANONICAL_STATES:
        state = CANONICAL_STATES[dissolution_id]["coordinates"]
    elif dissolution_id and dissolution_id in VISUAL_TYPES:
        state = VISUAL_TYPES[dissolution_id]["center"]
    elif state is None:
        return json.dumps({"error": "Provide either state dict or dissolution_id"})

    result = _interpolate_vocabulary(state, strength)
    return json.dumps(result, indent=2)


@mcp.tool()
def compute_dissolution_distance(id_1: str, id_2: str) -> str:
    """Compute distance between two dissolution states in 5D parameter space. Layer 2 (0 tokens)."""
    def _resolve(sid):
        if sid in CANONICAL_STATES:
            return CANONICAL_STATES[sid]["coordinates"]
        if sid in VISUAL_TYPES:
            return VISUAL_TYPES[sid]["center"]
        if sid in ATTRACTOR_PRESETS:
            return ATTRACTOR_PRESETS[sid]["state"]
        return None

    s1 = _resolve(id_1)
    s2 = _resolve(id_2)
    if s1 is None:
        return json.dumps({"error": f"Unknown id: {id_1}"})
    if s2 is None:
        return json.dumps({"error": f"Unknown id: {id_2}"})

    dist = _euclidean_distance(s1, s2)
    diff = {k: round(s2[k] - s1[k], 4) for k in PARAMETER_NAMES}

    return json.dumps({
        "id_1": id_1,
        "id_2": id_2,
        "distance": round(dist, 4),
        "per_axis_difference": diff,
        "dominant_axis": max(diff, key=lambda k: abs(diff[k])),
    }, indent=2)


@mcp.tool()
def compute_dissolution_trajectory(
    start_id: str,
    end_id: str,
    num_steps: int = 20,
) -> str:
    """Compute smooth trajectory between two dissolution states. Layer 2 (0 tokens)."""
    def _resolve(sid):
        if sid in CANONICAL_STATES:
            return CANONICAL_STATES[sid]["coordinates"]
        if sid in VISUAL_TYPES:
            return VISUAL_TYPES[sid]["center"]
        if sid in ATTRACTOR_PRESETS:
            return ATTRACTOR_PRESETS[sid]["state"]
        return None

    start = _resolve(start_id)
    end = _resolve(end_id)
    if start is None:
        return json.dumps({"error": f"Unknown id: {start_id}"})
    if end is None:
        return json.dumps({"error": f"Unknown id: {end_id}"})

    trajectory = []
    for i in range(num_steps + 1):
        t = i / num_steps
        state = _lerp_state(start, end, t)
        nearest_id, nearest_dist = _nearest_visual_type(state)
        trajectory.append({
            "step": i,
            "t": round(t, 4),
            "state": {k: round(v, 4) for k, v in state.items()},
            "nearest_type": nearest_id,
            "type_distance": round(nearest_dist, 4),
        })

    return json.dumps({
        "start_id": start_id,
        "end_id": end_id,
        "num_steps": num_steps,
        "total_distance": round(_euclidean_distance(start, end), 4),
        "trajectory": trajectory,
    }, indent=2)


@mcp.tool()
def generate_dissolution_attractor_prompt(
    attractor_id: str = "",
    custom_state: Optional[dict] = None,
    mode: str = "composite",
    style_modifier: str = "",
    keyframe_count: int = 4,
) -> str:
    """Generate image generation prompt from attractor state or custom coordinates.

    Modes: composite (single blended), split_view (per category), sequence (keyframes).
    Layer 2: Deterministic prompt synthesis (0 tokens)."""
    # Resolve state
    if custom_state:
        state = custom_state
    elif attractor_id in ATTRACTOR_PRESETS:
        state = ATTRACTOR_PRESETS[attractor_id]["state"]
    elif attractor_id in VISUAL_TYPES:
        state = VISUAL_TYPES[attractor_id]["center"]
    elif attractor_id in CANONICAL_STATES:
        state = CANONICAL_STATES[attractor_id]["coordinates"]
    else:
        state = VISUAL_TYPES["contested_boundary"]["center"]

    nearest_id, nearest_dist = _nearest_visual_type(state)
    vocab = _interpolate_vocabulary(state)

    vt = VISUAL_TYPES[nearest_id]

    # Determine hydrology descriptor
    if state["pigment_hydrology"] < 0.15:
        hydro_desc = "dry brush technique with broken textured marks revealing paper grain"
    elif state["pigment_hydrology"] < 0.35:
        hydro_desc = "controlled wash with even pigment coverage and predictable edges"
    elif state["pigment_hydrology"] < 0.55:
        hydro_desc = "wet-on-dry layered washes with crisp overlap boundaries"
    elif state["pigment_hydrology"] < 0.8:
        hydro_desc = "wet-on-wet diffusion with soft bloom formations and pigment migration"
    else:
        hydro_desc = "flooding technique with gravity-driven drips, capillary branching, and pigment pooling"

    # Determine edge descriptor
    if state["edge_coherence"] > 0.7:
        edge_desc = "architectural hard edges and sharp silhouette cuts persisting through dissolution"
    elif state["edge_coherence"] > 0.4:
        edge_desc = "mixed edge types: cauliflower backruns alongside architectural remnants and granulation boundaries"
    else:
        edge_desc = "feathered bleed edges and soft wet-lift transitions throughout"

    # Determine substrate descriptor
    if state["substrate_visibility"] > 0.7:
        sub_desc = "paper surface as dominant compositional element — white ground breathing through as active negative space"
    elif state["substrate_visibility"] > 0.35:
        sub_desc = "paper partially visible between wash areas, contributing to luminosity"
    else:
        sub_desc = "substrate hidden beneath continuous pigment coverage"

    # Determine anchor descriptor
    if state["anchor_density"] > 0.7:
        anchor_desc = "dense photographic anchors — recognizable objects maintaining sharp fidelity throughout"
    elif state["anchor_density"] > 0.3:
        anchor_desc = "scattered fidelity anchors — select objects retaining photographic clarity amid dissolution"
    else:
        anchor_desc = "minimal anchoring — near-abstract with content surviving only as color memory or vague shape"

    base_prompt = (
        f"Digital watercolor treatment in {vt['name'].lower()} mode. "
        f"{vt['description'][:200]} "
        f"Pigment behavior: {hydro_desc}. "
        f"Edge character: {edge_desc}. "
        f"Substrate: {sub_desc}. "
        f"Anchoring: {anchor_desc}. "
        f"Color palette: {', '.join(vt['color_associations'][:3])}. "
        f"Optical finish: {vt['optical']['finish'].replace('_', ' ')}, "
        f"{vt['optical']['scatter'].replace('_', ' ')}, "
        f"{vt['optical']['transparency'].replace('_', ' ')}."
    )

    if style_modifier:
        base_prompt += f" Style modifier: {style_modifier}."

    if mode == "composite":
        return json.dumps({
            "mode": "composite",
            "prompt": base_prompt,
            "state": {k: round(v, 4) for k, v in state.items()},
            "nearest_type": nearest_id,
            "keywords": vt["keywords"],
        }, indent=2)

    elif mode == "split_view":
        categories = vocab["vocabulary_by_category"]
        views = {}
        for cat, descs in categories.items():
            views[cat] = {
                "prompt_fragment": "; ".join(descs),
                "descriptors": descs,
            }
        return json.dumps({
            "mode": "split_view",
            "base_prompt": base_prompt,
            "category_views": views,
            "state": {k: round(v, 4) for k, v in state.items()},
        }, indent=2)

    elif mode == "sequence":
        # Generate keyframes along trajectory from editorial_wash to current state
        start = VISUAL_TYPES["editorial_wash"]["center"]
        keyframes = []
        for i in range(keyframe_count):
            t = i / max(1, keyframe_count - 1)
            kf_state = _lerp_state(start, state, t)
            kf_nearest, _ = _nearest_visual_type(kf_state)
            kf_vt = VISUAL_TYPES[kf_nearest]
            keyframes.append({
                "keyframe": i + 1,
                "t": round(t, 3),
                "state": {k: round(v, 4) for k, v in kf_state.items()},
                "nearest_type": kf_nearest,
                "prompt_fragment": (
                    f"Keyframe {i+1}: {kf_vt['name']} — "
                    f"{kf_vt['keywords'][0]}. {kf_vt['keywords'][1]}."
                ),
            })
        return json.dumps({
            "mode": "sequence",
            "keyframe_count": keyframe_count,
            "keyframes": keyframes,
        }, indent=2)

    return json.dumps({"error": f"Unknown mode: {mode}"})


@mcp.tool()
def generate_dissolution_rhythmic_sequence(
    state_a_id: str,
    state_b_id: str,
    steps_per_cycle: int = 20,
    num_cycles: int = 3,
    oscillation_pattern: str = "sinusoidal",
    phase_offset: float = 0.0,
) -> str:
    """Generate custom rhythmic oscillation between any two dissolution states. Layer 2 (0 tokens)."""
    def _resolve(sid):
        if sid in CANONICAL_STATES:
            return CANONICAL_STATES[sid]["coordinates"]
        if sid in VISUAL_TYPES:
            return VISUAL_TYPES[sid]["center"]
        if sid in ATTRACTOR_PRESETS:
            return ATTRACTOR_PRESETS[sid]["state"]
        return None

    a = _resolve(state_a_id)
    b = _resolve(state_b_id)
    if a is None:
        return json.dumps({"error": f"Unknown id: {state_a_id}"})
    if b is None:
        return json.dumps({"error": f"Unknown id: {state_b_id}"})

    total_steps = steps_per_cycle * num_cycles
    sequence = []

    for step in range(total_steps):
        phase = (step / steps_per_cycle + phase_offset) * 2 * math.pi

        if oscillation_pattern == "sinusoidal":
            t = 0.5 * (1.0 + math.sin(phase))
        elif oscillation_pattern == "triangle":
            cycle_pos = (step % steps_per_cycle) / steps_per_cycle
            t = 2.0 * cycle_pos if cycle_pos < 0.5 else 2.0 * (1.0 - cycle_pos)
        elif oscillation_pattern == "sawtooth":
            t = (step % steps_per_cycle) / steps_per_cycle
        else:
            t = 0.5 * (1.0 + math.sin(phase))

        state = _lerp_state(a, b, t)
        nearest_id, _ = _nearest_visual_type(state)

        if step % max(1, steps_per_cycle // 4) == 0:
            sequence.append({
                "step": step,
                "t": round(t, 4),
                "state": {k: round(v, 4) for k, v in state.items()},
                "nearest_type": nearest_id,
            })

    return json.dumps({
        "state_a": state_a_id,
        "state_b": state_b_id,
        "oscillation_pattern": oscillation_pattern,
        "steps_per_cycle": steps_per_cycle,
        "num_cycles": num_cycles,
        "total_steps": total_steps,
        "sampled_keyframes": len(sequence),
        "sequence": sequence,
    }, indent=2)


@mcp.tool()
def apply_dissolution_rhythmic_preset(preset_name: str) -> str:
    """Apply a curated dissolution rhythmic pattern preset. Layer 2 (0 tokens)."""
    if preset_name not in RHYTHMIC_PRESETS:
        return json.dumps({"error": f"Unknown preset: {preset_name}", "valid": list(RHYTHMIC_PRESETS.keys())})

    preset = RHYTHMIC_PRESETS[preset_name]
    a_id = preset["state_a"]
    b_id = preset["state_b"]

    a = VISUAL_TYPES[a_id]["center"] if a_id in VISUAL_TYPES else CANONICAL_STATES[a_id]["coordinates"]
    b = VISUAL_TYPES[b_id]["center"] if b_id in VISUAL_TYPES else CANONICAL_STATES[b_id]["coordinates"]

    period = preset["period"]
    sequence = []

    for step in range(period):
        phase = (step / period) * 2 * math.pi
        t = 0.5 * (1.0 + math.sin(phase))
        state = _lerp_state(a, b, t)
        nearest_id, _ = _nearest_visual_type(state)

        sequence.append({
            "step": step,
            "t": round(t, 4),
            "state": {k: round(v, 4) for k, v in state.items()},
            "nearest_type": nearest_id,
        })

    return json.dumps({
        "preset_name": preset_name,
        "preset_details": preset,
        "period": period,
        "state_a": a,
        "state_b": b,
        "sequence": sequence,
    }, indent=2)


@mcp.tool()
def generate_dissolution_sequence_prompts(
    preset_name: str,
    keyframe_count: int = 4,
    style_modifier: str = "",
) -> str:
    """Generate keyframe prompts from a Phase 2.6 rhythmic preset. Layer 2 (0 tokens)."""
    if preset_name not in RHYTHMIC_PRESETS:
        return json.dumps({"error": f"Unknown preset: {preset_name}", "valid": list(RHYTHMIC_PRESETS.keys())})

    preset = RHYTHMIC_PRESETS[preset_name]
    a_id = preset["state_a"]
    b_id = preset["state_b"]

    a = VISUAL_TYPES[a_id]["center"] if a_id in VISUAL_TYPES else CANONICAL_STATES[a_id]["coordinates"]
    b = VISUAL_TYPES[b_id]["center"] if b_id in VISUAL_TYPES else CANONICAL_STATES[b_id]["coordinates"]

    period = preset["period"]
    keyframes = []

    for i in range(keyframe_count):
        phase = (i / keyframe_count) * 2 * math.pi
        t = 0.5 * (1.0 + math.sin(phase))
        state = _lerp_state(a, b, t)
        nearest_id, _ = _nearest_visual_type(state)
        vt = VISUAL_TYPES[nearest_id]

        prompt = (
            f"Keyframe {i+1}/{keyframe_count} — {vt['name']}: "
            f"{vt['keywords'][0]}. {vt['keywords'][1]}. "
            f"Color: {', '.join(vt['color_associations'][:2])}."
        )
        if style_modifier:
            prompt += f" {style_modifier}."

        keyframes.append({
            "keyframe": i + 1,
            "phase_degrees": round((i / keyframe_count) * 360),
            "t": round(t, 4),
            "state": {k: round(v, 4) for k, v in state.items()},
            "nearest_type": nearest_id,
            "prompt": prompt,
        })

    return json.dumps({
        "preset_name": preset_name,
        "character": preset["character"],
        "keyframe_count": keyframe_count,
        "keyframes": keyframes,
    }, indent=2)


@mcp.tool()
def get_dissolution_domain_registry_config() -> str:
    """Get domain config for Tier 4D emergent attractor discovery integration."""
    return json.dumps({
        "domain_id": "watercolor_dissolution",
        "parameter_names": PARAMETER_NAMES,
        "n_visual_types": len(VISUAL_TYPES),
        "visual_type_centers": {
            tid: t["center"] for tid, t in VISUAL_TYPES.items()
        },
        "rhythmic_presets": {
            pid: {
                "state_a": p["state_a"],
                "state_b": p["state_b"],
                "period": p["period"],
            }
            for pid, p in RHYTHMIC_PRESETS.items()
        },
        "attractor_presets": {
            pid: {
                "state": p["state"],
                "basin_radius": p["basin_radius"],
            }
            for pid, p in ATTRACTOR_PRESETS.items()
        },
        "bounds": [0.0, 1.0],
    }, indent=2)


# ─────────────────────────────────────────────────────────────────────
# LAYER 3 TOOL — Claude synthesis interface
# ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def enhance_dissolution_prompt(
    user_intent: str,
    style_override: Optional[str] = None,
    substrate: Optional[str] = None,
    intensity: str = "moderate",
) -> str:
    """Prepare complete dissolution enhancement for Claude synthesis.

    LAYER 3 INTERFACE: Combines Layer 1 & 2 into structured data
    ready for Claude to synthesize into an enhanced image prompt.

    Args:
        user_intent: Description of desired dissolution aesthetic
        style_override: Optional specific style (auto-detected if not provided)
        substrate: Optional substrate type (hot_press, cold_press, rough, yupo, masa)
        intensity: Enhancement intensity (subtle, moderate, dramatic)"""
    # Classify intent
    classification = json.loads(classify_dissolution_intent(user_intent))
    style_id = style_override or classification["primary_style"]

    if style_id not in VISUAL_TYPES:
        style_id = classification["primary_style"]

    # Map parameters
    params = json.loads(map_dissolution_parameters(
        style_id=style_id,
        intensity=intensity,
        substrate=substrate,
    ))

    # Generate prompt
    prompt_data = json.loads(generate_dissolution_attractor_prompt(
        attractor_id=style_id,
        mode="composite",
    ))

    # Get vocabulary
    vocab = json.loads(extract_dissolution_visual_vocabulary(dissolution_id=style_id))

    return json.dumps({
        "classification": {
            "detected_style": classification["primary_style"],
            "applied_style": style_id,
            "confidence": classification["confidence"],
            "matched_keywords": classification["matched_keywords"],
        },
        "parameters": {
            "state": params["state"],
            "intensity": intensity,
            "style_name": params["style_name"],
        },
        "active_edge_modes": params["active_edge_modes"],
        "hydrology": {
            "state": params["hydrology_state"],
            "details": params["hydrology_details"],
        },
        "contrast": {
            "curve": params["contrast_curve"],
            "details": params["contrast_curve_details"],
        },
        "substrate": params.get("substrate"),
        "prompt": prompt_data["prompt"],
        "keywords": params["keywords"],
        "optical": params["optical_properties"],
        "color_associations": params["color_associations"],
        "characteristics": params["characteristics"],
        "vocabulary": vocab["vocabulary_by_category"],
    }, indent=2)


@mcp.tool()
def validate_dissolution_decomposition_round_trip() -> str:
    """Test decomposition fidelity by round-tripping through visual types.

    LAYER 2: Deterministic self-test (0 LLM tokens).

    For each visual type, uses its own keywords as the description,
    decomposes back to coordinates, and measures reconstruction error."""
    results = {}
    total_error = 0.0
    correct_nearest = 0

    for tid, t in VISUAL_TYPES.items():
        # Use keywords as description
        description = " ".join(t["keywords"])
        decomposed = json.loads(decompose_dissolution_from_description(description))

        # Measure error
        original = t["center"]
        recovered = decomposed["coordinates"]
        error = math.sqrt(sum(
            (original[k] - recovered[k]) ** 2 for k in PARAMETER_NAMES
        ))
        total_error += error

        nearest_correct = decomposed["nearest_type"] == tid

        if nearest_correct:
            correct_nearest += 1

        results[tid] = {
            "original_center": original,
            "recovered_coordinates": recovered,
            "reconstruction_error": round(error, 4),
            "nearest_type_correct": nearest_correct,
            "recovered_nearest": decomposed["nearest_type"],
            "confidence": decomposed["confidence"],
        }

    n = len(VISUAL_TYPES)
    return json.dumps({
        "test": "round_trip_decomposition_fidelity",
        "n_types_tested": n,
        "nearest_type_accuracy": round(correct_nearest / n, 4),
        "mean_reconstruction_error": round(total_error / n, 4),
        "per_type_results": results,
    }, indent=2)


# ─────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────

def main():
    """Entry point for FastMCP Cloud deployment. Returns server object."""
    return mcp
