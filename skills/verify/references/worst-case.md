# Worst-case data

Read when a change renders data on screen. Demo and seed data is kind by accident: names fit on one line, counts are plural, optional fields are filled. The **worst case** undoes that, one rendered value at a time. Adapted from the MIT-licensed `break-ui` skill by Emil Kowalski.

## Build it

1. **Map the surface.** List every value the change renders and its source field: names, emails, titles, badges, status text, counts in headers, timestamps, avatars, optional fields, and the length of each list. Done when every rendered value has a source.
2. **Pick values.** For each field, take rows from the tables below. Every value is **realistic**: a pattern a real user produces, or the longest value the backend accepts. A value like `aaaaaaaaaaaa` proves nothing and gets dismissed.
3. **Seed through the boundary.** Create the records through the API or the normal UI, in the test instance's own database. Never edit markup, CSS, or the rendered DOM to produce a break.
4. **Spread the failures.** Put a different worst case in each of the first visible rows (row 1 the long name, row 2 the unbreakable email, row 3 the two-letter name, row 4 the missing optional field). One screenshot then covers many rows of the tables.
5. **Cover the counts.** Empty (zero items), exactly one (singular copy), and the realistic upper bound (1,000+ rows when the list does not paginate). Each is a separate state to screenshot.

Use `example.com` or `.test` domains so no fixture points at a real inbox. Keep a list of what you create, and remove it at cleanup.

## Values

### People

| Value | Breaks |
| --- | --- |
| `Aleksandra Wiśniewska-Kowalczyk` | Long, hyphenated, diacritics; wraps, and the hyphen is a break point |
| `Christopher Alexander Montgomery III` | Suffix; first-plus-last initials come out wrong |
| `Jo` | Two letters; column looks empty, one-letter initials |
| `Đặng Thị Ngọc Hân` | Stacked diacritics; clipped by tight line height with hidden overflow |
| `王秀英` | No spaces; word-based initials and wrapping logic |
| `Seán O'Brien` | Apostrophe; escaping, search, initials |
| `🦊 Fox` | Emoji first; `charAt(0)` returns half a character |
| `  Sam   Lee ` | Extra spaces; empty words in initials, odd gaps |
| *(no name, only an email)* | The fallback display |

### Identifiers and links

| Value | Breaks |
| --- | --- |
| `bartholomew.fitzgerald@northwind-industries-holdings.example.com` | No break points; pushes trailing actions off the row |
| `a@b.co` | Shortest; layouts that assumed length |
| `first.last+billing@example.com` | Plus sign; validation, and truncation hides the meaningful part |
| A 120-character URL with a query string | Overflow; end truncation hides the part that differs |
| `Q3 Board Deck - FINAL (revised) v12.pdf` | End truncation hides version and extension |

### Labels and copy

| Value | Breaks |
| --- | --- |
| `Senior Product Design Engineer, Platform Infrastructure` | Wraps to three lines in a secondary slot |
| `Invitation expired 12 days ago` | Long badge; wraps or squeezes the name column |
| `Benachrichtigungseinstellungen` | Long word with no spaces |
| Twelve tags on one item | Tag rows become a wall; needs an overflow count |
| One tag of 45 characters | Wider than its container |
| Empty string or only spaces | Collapsed heading, zero-height row |
| `<b>bold</b>`, `&amp;`, `**bold**` | Must render as literal text |
| A title with a line break inside | Doubles row height or vanishes |
| A 2,000-character pasted description | Clamping, "show more", text area growth |

### Numbers

| Value | Breaks |
| --- | --- |
| `0` | "0 items", empty bars, division by zero in percentages |
| `1` | Plurals: "1 members", "1 days ago" |
| `1284` | Needs a thousands separator |
| `1000000` | Badge width |
| `-42.5` | Sign, color logic |
| `0.1 + 0.2` | `0.30000000000000004` shown raw |
| `142%`, `-3%` | Bars and meters past their bounds |
| `null`, missing | Renders `null`, `undefined`, or `NaN` |
| A count that changes live (`99` to `100`) | Width jump without tabular figures |

### Collections

| Value | Breaks |
| --- | --- |
| 0 items | Whether an empty state exists |
| 1 item | Grids that look broken with one card; "1 of 1" |
| Page size, and page size + 1 | Off-by-one copy, empty last page |
| 1,000+ items unpaginated | Scroll and render performance |
| One item ten times taller | Rows stretch to the tallest item |
| Two items with the same name | Lists where the name is the only distinguishing field |

### Time

| Value | Breaks |
| --- | --- |
| Now | "0 seconds ago" |
| 12 days, 11 months, 3 years ago | Relative-time thresholds |
| A future date | "-3 days ago" |
| `1970-01-01` | A zero timestamp shown as real |
| 23:30 in the user's zone, next day in UTC | Wrong calendar day |
| A 1,284-hour duration | No roll-up to days |

### Images

| Value | Breaks |
| --- | --- |
| An avatar URL that returns 404 | Broken-image icon instead of the fallback |
| No avatar | The fallback's size parity |
| A 4000×200 or 200×4000 image | Distortion or a blown-out card |
| A transparent logo | Invisible on the background |

### States

| Value | Breaks |
| --- | --- |
| Partial data | Some optional fields filled, others not, in one list; misaligned rows |
| Every status at once | Badge widths vary |
| No permission | Disabled actions and row layout |
| The current user in the list | "You" labels, actions that do not apply to yourself |
