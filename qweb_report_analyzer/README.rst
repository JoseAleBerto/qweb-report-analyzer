=======================
QWeb Report Analyzer
=======================

.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0.html
   :alt: License: LGPL-3

.. image:: https://img.shields.io/badge/Odoo-18-purple.svg
   :alt: Odoo 18

.. image:: https://img.shields.io/badge/free-%E2%9C%94-brightgreen.svg
   :alt: Free & Open Source

Free and open source tool for Odoo developers and consultants. Instantly
understand **any** QWeb report — base views, inherited views, t-calls, XPaths,
and module origins. One click. No server. **100% free.**

**Key Features**
----------------

* **Dependency Tree** — full hierarchy from entry point to every view
* **Inherited Views** — see every module that modifies the report
* **T-Call References** — every template called via ``t-call``
* **XPath Detection** — exactly where each inherited view injects its code
* **Module Tracking** — which module owns each view
* **One-Click Export** — downloads a ``.txt`` file instantly, no popups
* **Fully Local** — runs entirely inside Odoo, no internet or API key needed

**Usage**
---------

1. Enable **Developer Mode** (Settings → Activate Developer Mode)
2. Go to **Settings → Technical → Reporting → Reports**
3. Select any report from the list
4. Click the **gear icon (⚙) → Analyze Report Views**
5. A ``.txt`` file downloads automatically with the complete analysis

**Compatibility**
-----------------

* Odoo 18.0 — Community, Enterprise, and Odoo Online

**Installation**
----------------

From the **Odoo App Store** (recommended):
Search for *QWeb Report Analyzer* on `apps.odoo.com <https://apps.odoo.com>`_ — it's free.

From **GitHub**::

    git clone -b 19.0 https://github.com/JoseAleBerto/qweb-report-analyzer.git
    cp -r qweb-report-analyzer/qweb_report_analyzer /path/to/your/addons/

Then update the apps list and install *QWeb Report Analyzer*.

**Source Code**
---------------

https://github.com/JoseAleBerto/qweb-report-analyzer

**Author**
----------

José Bertorelli — josealebertorelli@gmail.com

**License**
-----------

LGPL-3 (GNU Lesser General Public License v3).

Copyright (C) 2026 José Bertorelli
