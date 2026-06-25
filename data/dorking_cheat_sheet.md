# 🛰️ Dorking Cheat Sheet

A field reference for crafting precise Google dork queries. Use responsibly and
only against targets you are authorised to test.

---

## Core Operators

| Operator | Purpose | Example |
| --- | --- | --- |
| `site:` | Limit results to one domain | `site:example.com` |
| `filetype:` | Match a file extension | `filetype:pdf` |
| `intitle:` | Word in the page title | `intitle:"admin login"` |
| `allintitle:` | All words in the title | `allintitle:index of backup` |
| `inurl:` | Word in the URL | `inurl:admin` |
| `allinurl:` | All words in the URL | `allinurl:auth login` |
| `intext:` | Word in the body text | `intext:"confidential"` |
| `cache:` | Google's cached copy | `cache:example.com` |
| `related:` | Sites similar to a URL | `related:example.com` |
| `ext:` | Alias for `filetype:` | `ext:sql` |

## Logical Modifiers

| Syntax | Meaning | Example |
| --- | --- | --- |
| `" "` | Exact phrase | `"parent directory"` |
| `-` | Exclude a term | `-www` |
| `OR` / `\|` | Match either term | `filetype:pdf OR filetype:doc` |
| `( )` | Group terms | `(admin OR root) login` |
| `*` | Wildcard placeholder | `"index of *"` |
| `..` | Numeric range | `salary 50000..90000` |

---

## Recipes by Objective

### 📄 Find documents
```text
site:example.com filetype:pdf "annual report"
intitle:"report" (filetype:pdf OR filetype:docx) -template
```

### 📚 Download books
```text
intitle:"index of" +(epub|pdf|mobi) "book title"
"book title" filetype:pdf -site:amazon.com
```

### 🔐 Find login / admin panels
```text
inurl:admin intitle:login
site:example.com (inurl:admin OR inurl:login OR inurl:portal)
intitle:"dashboard" inurl:admin -intext:"forgot password"
```

### 🗂️ Explore exposed directories
```text
intitle:"index of" "parent directory"
intitle:"index of" "last modified" -inurl:(html|htm|php)
```

---

## 🕳️ Open Directory Power Pattern

The classic high-signal open-directory query strips rendered web pages and
known fake-index link farms:

```text
<keywords> +(mp3|flac|m4a) -inurl:(jsp|pl|php|html|aspx|htm|cf|shtml)
intitle:index.of -inurl:(listen77|mp3raid|mp3toss|mp3drug|index_of|index-of|wallywashis|downloadmana)
```

### Handy filetype bundles

| Bundle | Extensions |
| --- | --- |
| Documents | `pdf doc docx xls xlsx ppt pptx csv txt rtf odt` |
| Books | `MOBI CBZ CBR CHM EPUB FB2 LIT PDF PRC RTF DOC DOCX` |
| Music | `mp3 wav ac3 ogg flac wma m4a aac mod` |
| Video | `mkv mp4 avi mov mpg wmv divx mpeg` |
| Software | `exe iso dmg tar 7z bz2 gz rar zip apk` |
| Images | `jpg png bmp gif tif tiff psd` |
| Config / secrets | `env conf cfg ini yml yaml json xml log sql bak` |

---

## ⚠️ Sensitive-Exposure Patterns (defensive use only)

```text
intitle:"index of" "*.env"
filetype:log intext:password
filetype:sql "INSERT INTO" "password"
inurl:"/.git/config"
```

> Use these to **audit your own** assets and find leaks before attackers do.

---

## Tips

- Stack operators for precision, but too many can zero out results — start broad, then narrow.
- Quote multi-word phrases so Google treats them as a unit.
- `OR` must be uppercase; `|` works the same inside groups.
- Combine `site:` with `-www` to surface subdomains.
- Rotate keywords and synonyms — indexes differ across phrasings.
