# QWeb Report Analyzer

**Free & Open Source Odoo addon** — Analyze any QWeb report and get a complete dependency tree of all views, t-calls, XPaths, and inherited views.

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL%20v3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo 16](https://img.shields.io/badge/Odoo-16-purple)](https://github.com/JoseAleBerto/qweb-report-analyzer/tree/16.0)
[![Free](https://img.shields.io/badge/price-free-brightgreen)](https://apps.odoo.com)

---

## What it does

Select any report in Odoo → **⚙ Gear → Analyze Report Views** → download a `.txt` file with:

- 📄 **Dependency Tree** — full hierarchy from entry point to every view
- 🔗 **T-Call references** — every template called via `t-call`
- 🛠️ **XPath expressions** — where each inherited view injects its code
- 📦 **Module tracking** — which module owns each view
- 👥 **Sibling views** — related views sharing the same key prefix

Everything runs **locally inside Odoo** — no internet, no server, no API key.

---

## Installation

### From Odoo App Store
Search for **"QWeb Report Analyzer"** on [apps.odoo.com](https://apps.odoo.com) — it's free.

### From GitHub
```bash
# Clone the branch matching your Odoo version
git clone -b 16.0 https://github.com/JoseAleBerto/qweb-report-analyzer.git

# Copy to your addons path
cp -r qweb-report-analyzer/qweb_report_analyzer /path/to/your/addons/

# Update apps list and install "QWeb Report Analyzer"
```

---

## Usage

1. Enable **Developer Mode** (Settings → Activate Developer Mode)
2. Go to **Settings → Technical → Reporting → Reports**
3. Select any report from the list
4. Click the **gear icon (⚙) → Analyze Report Views**
5. A `.txt` file downloads automatically

### Sample output

```
================================================================================
========================= VIEW DEPENDENCY TREE =================================
================================================================================

[REPORT] stock.report_delivery_document
    Module: stock

+-- stock.report_delivery_document_content
    Module: stock
    <t-call> stock.report_delivery_document_line
    <t-call> web.external_layout

    +-- my_custom_module.report_delivery_custom
        Module: my_custom_module
        <inherits> stock.report_delivery_document_content
        <xpath> //div[@class='page']
```

---

## Compatibility

| Branch | Odoo Version | Status |
|--------|-------------|--------|
| `19.0` | Odoo 16 — Community, Enterprise, Odoo Online | ✅ Maintained |

---

## Contributing

Pull requests are welcome! Please open an issue first to discuss what you'd like to change.

```bash
git clone -b 16.0 https://github.com/JoseAleBerto/qweb-report-analyzer.git
cd qweb-report-analyzer
git checkout -b feature/your-feature-name
# make your changes
git push origin feature/your-feature-name
# open a pull request
```

---

## License

[LGPL-3](LICENSE) — Free to use, modify, and distribute. Attribution appreciated.

---

## Author

**José Bertorelli**
- Email: josealebertorelli@gmail.com
- GitHub: [@JoseAleBerto](https://github.com/JoseAleBerto)

---

*If this addon saved you time, consider leaving a ⭐ on GitHub or a review on the Odoo App Store!*
