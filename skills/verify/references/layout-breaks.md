# Layout breaks

Read when a screenshot shows a layout break and you diagnose or fix it. Each symptom has one usual cause. Confirm the cause in the computed styles before the fix, and use the project's existing classes and tokens. Adapted from the MIT-licensed `break-ui` skill by Emil Kowalski.

| Symptom | Usual cause | Fix |
| --- | --- | --- |
| Avatar or icon squished into an oval | Flex child shrinks | `flex-shrink: 0` on fixed-size boxes |
| Text overflows instead of wrapping or truncating | Flex or grid child has `min-width: auto` | `min-width: 0` on the text column; `minmax(0, 1fr)` in grid |
| Email or URL runs past the edge | No break points in the string | `overflow-wrap: anywhere` on that element |
| Trailing action pushed off-screen | Middle content takes all the space | `min-width: 0` on the middle, `flex-shrink: 0` on the action |
| Badge wraps onto two lines | Badge can shrink | `white-space: nowrap; flex-shrink: 0`, and choose what yields |
| Avatar adrift beside a three-line name | `align-items: center` on rows of varying height | Top-align once text can wrap |
| Last row cut mid-glyph at a hard edge | Fixed height with no scroll affordance | Visible scroll or a fade; confirm the overflow is intended |
| A heading word broken mid-word | `word-break: break-all` | `overflow-wrap: anywhere` |
| Wrong initials (`J` for "Jo", `�` for an emoji name) | `split(' ')[0][0]`-style code | Grapheme-safe initials, first and last word, fallback icon |
| Orphaned dash or blank line for a missing field | Placeholder for an empty optional field | Omit the line, or reserve its height on purpose |
| "1 members", "0 member" | Hardcoded plural | `Intl.PluralRules` or a string per count |
| Numbers jitter or columns misalign | Proportional figures | `font-variant-numeric: tabular-nums` |
| `1284`, long decimals, `NaN`, `undefined` | Raw number rendered | `Intl.NumberFormat`; guard missing values |
| Button label overflows | Fixed-width button | Width from content with a `min-width` |
| Diacritics clipped top or bottom | Tight line height with hidden overflow | Looser line height, or no clipping on text |
| Broken-image icon | No error fallback | Fall back to initials; `object-fit: cover` |
| Truncated text with no way to read it | Ellipsis only | `title` or tooltip, and the full value elsewhere |
| 1,000 rows stutter on scroll | Every row rendered | Virtualize or paginate |
| Literal `<b>` or `&amp;` shown | Escaped twice or at the wrong layer | Escape once, at render |

## Truncate, wrap, or clamp

Decide per field. A choice between these is a product decision when the issue does not settle it; report it with a recommendation.

- **Wrap** values the user needs in full to identify something: names, titles in a detail view.
- **Truncate at the end** for secondary metadata whose start carries the meaning. Pair it with a way to read the full value.
- **Truncate in the middle** when items differ at the end: file names, paths, emails on a shared domain.
- **Clamp** multi-line previews in cards so card heights stay even.
- **Never truncate** numbers, amounts, dates, or anything the user compares.
