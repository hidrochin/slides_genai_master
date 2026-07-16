# Hybrid OCR + VLM Pipeline for Complex Financial Table Reconstruction

## 1. Motivation

Directly prompting a Vision-Language Model (VLM) such as Qwen3.6-VL to convert a table image into HTML often fails for complex financial tables:

```text
Image
 ↓
Qwen-VL
 ↓
HTML
```

This approach suffers from error propagation:

- OCR errors shift columns.
- Missing cells break row alignment.
- Incorrect rowspan/colspan causes catastrophic HTML failure.
- A single mistake in an early row may invalidate the entire table structure.

This issue becomes particularly severe in financial tables containing:

- hierarchical headers
- merged cells
- sparse text and dense numerical values
- whitespace-based grouping
- irregular column boundaries
- borderless sections
- partially bordered layouts

Therefore, we propose a hybrid pipeline that separates:

1. Text extraction
2. Geometric reasoning
3. Structural reasoning
4. HTML rendering

---

## 2. Proposed Architecture

```text
Financial Table Image
        │
        ▼
┌──────────────────────────────┐
│ OCR Extraction               │
│ (PaddleOCR / Surya / Qwen)   │
└──────────────┬───────────────┘
               │
               ▼
       Text + Bounding Boxes
               │
               ▼
┌──────────────────────────────┐
│ Geometry Construction        │
│ - row clustering             │
│ - column clustering          │
│ - line detection             │
│ - merge candidates           │
└──────────────┬───────────────┘
               │
               ▼
 Image + OCR + Geometry Hints
               │
               ▼
┌──────────────────────────────┐
│ Qwen Structural Reasoning    │
│ Infer logical table layout   │
└──────────────┬───────────────┘
               │
               ▼
        Cell Graph JSON
               │
               ▼
┌──────────────────────────────┐
│ Deterministic HTML Renderer  │
└──────────────────────────────┘
               │
               ▼
          Final HTML
```

---

## 3. Stage 1: OCR Extraction

### Input

```text
table.png
```

### Output

```json
[
    {
        "text": "Revenue",
        "bbox": [102, 45, 253, 78]
    },
    {
        "text": "2024",
        "bbox": [312, 45, 365, 78]
    },
    {
        "text": "2025",
        "bbox": [395, 45, 448, 78]
    }
]
```

### Recommended OCR engines

- PaddleOCR
- Surya OCR
- MinerU OCR
- Qwen OCR (fallback option)

Dedicated OCR engines generally provide more stable bounding boxes than VLM OCR.

---

## 4. Stage 2: Geometry Construction

### 4.1 Row Clustering

For each OCR box:

```text
y_center = (y1 + y2) / 2
```

Two OCR boxes belong to the same row if:

```text
|y_i - y_j| < row_threshold
```

Typical values:

```text
row_threshold = 10 ~ 20 pixels
```

Result:

```json
{
    "row_id": 3
}
```

---

### 4.2 Column Clustering

For each OCR box:

```text
x_center = (x1 + x2) / 2
```

Two OCR boxes belong to the same column if:

```text
|x_i - x_j| < column_threshold
```

Typical values:

```text
column_threshold = 20 ~ 40 pixels
```

Result:

```json
{
    "column_id": 5
}
```

---

### 4.3 Optional Line Detection

Many financial tables contain explicit ruling lines.

OpenCV morphology can detect them:

```python
horizontal_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (50, 1)
)

vertical_kernel = cv2.getStructuringElement(
    cv2.MORPH_RECT,
    (1, 50)
)
```

Output:

```json
{
    "horizontal_lines": [...],
    "vertical_lines": [...]
}
```

---

### 4.4 Merge Candidate Detection

#### Candidate Colspan

Example:

```text
Revenue
2024    2025
```

If:

```text
cell_width >> average_column_width
```

then:

```text
candidate_colspan = True
```

---

#### Candidate Rowspan

If:

```text
cell_height >> average_row_height
```

then:

```text
candidate_rowspan = True
```

---

## 5. Stage 3: Structural Reasoning with Qwen

Qwen receives three inputs:

### Original Image

Provides:

- borders
- whitespace
- indentation
- visual grouping
- alignment

---

### OCR Output

```json
[
    {
        "text": "Revenue",
        "bbox": [102,45,253,78],
        "row_candidate": 0,
        "col_candidate": 1
    }
]
```

---

### Geometry Hints

```json
{
    "rows": [45, 78, 105, 132],
    "cols": [0, 100, 250, 360, 450]
}
```

---

### Prompt

```text
You are given:

1. Original table image.
2. OCR output with bounding boxes.
3. Candidate rows and columns.

Infer:

- row_start
- row_end
- col_start
- col_end

Return JSON only.

Do not generate HTML.
```

---

## 6. Cell Graph Representation

Instead of generating HTML directly, Qwen outputs a structured cell graph:

```json
[
    {
        "text": "Company",
        "row_start": 0,
        "row_end": 1,
        "col_start": 0,
        "col_end": 0
    },
    {
        "text": "Revenue",
        "row_start": 0,
        "row_end": 0,
        "col_start": 1,
        "col_end": 2
    },
    {
        "text": "2024",
        "row_start": 1,
        "row_end": 1,
        "col_start": 1,
        "col_end": 1
    }
]
```

This representation is:

- easier for VLMs to generate
- easier to debug
- deterministic
- independent of HTML syntax

---

## 7. Deterministic HTML Rendering

The renderer converts the cell graph into HTML.

### Conversion rules

```text
rowspan = row_end - row_start + 1
colspan = col_end - col_start + 1
```

Example:

```json
{
    "text": "Company",
    "row_start": 0,
    "row_end": 1,
    "col_start": 0,
    "col_end": 0
}
```

becomes:

```html
<th rowspan="2">Company</th>
```

---

Example:

```json
{
    "text": "Revenue",
    "row_start": 0,
    "row_end": 0,
    "col_start": 1,
    "col_end": 2
}
```

becomes:

```html
<th colspan="2">Revenue</th>
```

---

## 8. Advantages

| Property | Direct Image → HTML | Proposed Pipeline |
|----------|--------------------|-------------------|
| OCR robustness | Low | High |
| HTML validity | Medium | Guaranteed |
| Rowspan accuracy | Low | High |
| Colspan accuracy | Low | High |
| Error propagation | Severe | Limited |
| Debuggability | Poor | Excellent |
| Structural consistency | Medium | High |

---

## 9. Expected Performance

Estimated reconstruction quality for financial tables:

| Method | Estimated Accuracy |
|--------|-------------------|
| Image → HTML | 50-70% |
| OCR → HTML | 70-80% |
| OCR + Image → HTML | 80-90% |
| OCR + Image → Cell Graph → HTML | 90-95% |
| OCR + Geometry + Cell Graph → HTML | 95%+ |

---

## 10. Final Pipeline

```text
Financial Table Image
        │
        ▼
OCR Engine
(PaddleOCR / Surya)
        │
        ▼
Text + Bounding Boxes
        │
        ▼
Geometry Construction
(Row clustering,
 Column clustering,
 Line detection,
 Merge candidates)
        │
        ▼
Image + OCR + Geometry Hints
        │
        ▼
Qwen3.6-VL
        │
        ▼
Cell Graph JSON
        │
        ▼
Deterministic HTML Renderer
        │
        ▼
Complex Financial HTML Table
```

---

## 11. Future Extensions

Possible future improvements include:

- Graph Neural Networks for cell relation prediction
- Multi-page table reconstruction
- Excel export
- LaTeX export
- Tree-based financial hierarchy reconstruction
- Confidence-aware rendering
- Human-in-the-loop correction systems