# SarcomaHub website

Static website for [sarcomahub.com](https://www.sarcomahub.com), hosted on Cloudflare Pages. Plain HTML and CSS: no build step.

## Pages

| Address | File |
| --- | --- |
| `/` | `index.html` |
| `/understanding-sarcoma/` | `understanding-sarcoma/index.html` |
| `/for-parents/` | `for-parents/index.html` |
| `/stories/` | `stories/index.html` |
| `/about/` | `about/index.html` |
| `/contact/` | `contact/index.html` |

Shared styles are in `assets/style.css` and scripts in `assets/site.js`. `_redirects` sends the old Wix addresses (`/ourpurpose`, `/ourlogo`, `/ourthoughts`) to their new pages.

## Cloudflare Pages settings

- Framework preset: None
- Build command: (leave empty)
- Build output directory: `/`

## Contact form

The form posts to Formspree. Replace `YOUR_FORM_ID` in `contact/index.html` with the form ID from formspree.io.

## Before launch

- Review all medical text
- Fill the dashed placeholder boxes (team, contact details, parents' practical support, stories)
- Replace the drawn logo with the real logo file
