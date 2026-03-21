# -*- coding: utf-8 -*-
"""
QWeb Report Analyzer - Odoo Module
Author: José Bertorelli
Email: josealebertorelli@gmail.com
GitHub: https://github.com/josebertorelli/qweb-report-analyzer

Free and open source. No license server required.
"""

import re
import logging

from odoo import api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class QWebAnalyzer:
    """
    Core analysis engine — runs locally inside Odoo.
    No external server or license required.
    """

    def __init__(self, report_data, views_data, inherited_map, entry_point):
        self.report = report_data
        self.views = views_data
        self.inherited_map = inherited_map
        self.entry_point = entry_point

        # Build key -> id mapping
        self.key_to_id = {}
        for vid, vdata in self.views.items():
            if vdata.get('key'):
                self.key_to_id[vdata['key']] = vid

    def _get_view_by_key(self, key):
        """Get view data by key or name."""
        vid = self.key_to_id.get(key)
        if vid:
            return self.views.get(str(vid))
        for vid, vdata in self.views.items():
            if vdata.get('name') == key:
                return vdata
        return None

    def _extract_tcalls(self, arch):
        """Extract t-call references from view architecture."""
        if not arch:
            return []
        tcalls = []
        pattern = r't-call=["\']([^"\']+)["\']'
        matches = re.findall(pattern, arch)
        for match in matches:
            if not match.startswith('{{'):
                tcalls.append(match)
        return tcalls

    def _get_siblings(self, key):
        """Get sibling views (same key prefix, different suffix)."""
        if not key or '.' not in key:
            return []
        prefix = key.rsplit('.', 1)[0]
        siblings = []
        for vid, vdata in self.views.items():
            vkey = vdata.get('key', '')
            if vkey and vkey.startswith(prefix + '.') and vkey != key:
                siblings.append(vkey)
        return siblings

    def _extract_xpaths(self, arch):
        """Extract XPath expressions from inherited views."""
        if not arch:
            return []
        xpaths = []
        pattern = r'<xpath\s+expr=["\']([^"\']+)["\']'
        matches = re.findall(pattern, arch)
        xpaths.extend(matches)
        return xpaths

    def _get_module_from_key(self, key):
        """Extract module name from view key (e.g. 'sale.report_saleorder' → 'sale')."""
        if key and '.' in key:
            return key.split('.')[0]
        return 'unknown'

    def analyze(self):
        """
        Perform the full analysis locally and return the report as a string.
        """
        output = []

        # ── Header ──────────────────────────────────────────────────────────
        output.append("=" * 80)
        output.append(" QWEB REPORT ANALYZER - Analysis Results ".center(80, "="))
        output.append("=" * 80)
        output.append("")
        output.append(f"Report:      {self.report.get('name', 'Unknown')}")
        output.append(f"Model:       {self.report.get('model', 'Unknown')}")
        output.append(f"Report name: {self.report.get('report_name', 'Unknown')}")
        output.append(f"Entry point: {self.entry_point}")
        output.append("")

        # ── Build dependency tree ────────────────────────────────────────────
        output.append("=" * 80)
        output.append(" VIEW DEPENDENCY TREE ".center(80, "="))
        output.append("=" * 80)
        output.append("")

        visited = set()
        tree_nodes = {}

        def build_tree(key, depth=0):
            if key in visited or depth > 20:
                return
            visited.add(key)

            view = self._get_view_by_key(key)
            if not view:
                return

            node = {
                'key': key,
                'name': view.get('name', ''),
                'module': self._get_module_from_key(key),
                'inherit_id': view.get('inherit_id'),
                'inherit_key': view.get('inherit_key'),
                'tcalls': self._extract_tcalls(view.get('arch', '')),
                'xpaths': self._extract_xpaths(view.get('arch', '')),
                'siblings': self._get_siblings(key),
                'children': [],
            }

            # Collect inherited child views
            view_id = str(view.get('id', ''))
            if view_id in self.inherited_map:
                for child_id in self.inherited_map[view_id]:
                    child_view = self.views.get(str(child_id))
                    if child_view and child_view.get('key'):
                        node['children'].append(child_view['key'])

            tree_nodes[key] = node

            # Recurse into t-calls
            for tcall in node['tcalls']:
                build_tree(tcall, depth + 1)

            # Recurse into children (inherited views)
            for child_key in node['children']:
                build_tree(child_key, depth + 1)

        build_tree(self.entry_point)

        def print_tree(key, depth=0):
            if key not in tree_nodes:
                return []

            node = tree_nodes[key]
            lines = []
            indent = "    " * depth

            if depth == 0:
                lines.append(f"{indent}[REPORT] {key}")
            else:
                lines.append(f"{indent}+-- {key}")

            lines.append(f"{indent}    Module: {node['module']}")

            if node['inherit_key']:
                lines.append(f"{indent}    <inherits> {node['inherit_key']}")
            elif node['inherit_id']:
                lines.append(f"{indent}    <inherits id={node['inherit_id']}>")

            for xpath in node['xpaths']:
                lines.append(f"{indent}    <xpath> {xpath}")

            for tc in node['tcalls']:
                lines.append(f"{indent}    <t-call> {tc}")

            for sib in node['siblings'][:5]:
                lines.append(f"{indent}    <sibling> {sib}")

            lines.append("")

            # Recurse t-calls (skip generic web/base templates)
            for tc in node['tcalls']:
                if tc in tree_nodes and not tc.startswith(('web.', 'base.')):
                    lines.extend(print_tree(tc, depth + 1))

            return lines

        output.extend(print_tree(self.entry_point))

        # ── Inherited views section ──────────────────────────────────────────
        output.append("=" * 80)
        output.append(" INHERITED VIEWS (by module) ".center(80, "="))
        output.append("=" * 80)
        output.append("")

        inherited_by_module = {}
        for key, node in tree_nodes.items():
            if node['children']:
                for child_key in node['children']:
                    child_node = tree_nodes.get(child_key)
                    if child_node:
                        mod = child_node['module']
                        inherited_by_module.setdefault(mod, []).append({
                            'key': child_key,
                            'parent': key,
                            'xpaths': child_node['xpaths'],
                        })

        if inherited_by_module:
            for module, items in sorted(inherited_by_module.items()):
                output.append(f"  [{module}]")
                for item in items:
                    output.append(f"    {item['key']}")
                    output.append(f"      inherits: {item['parent']}")
                    for xp in item['xpaths']:
                        output.append(f"      xpath: {xp}")
                output.append("")
        else:
            output.append("  (no inherited views found)")
            output.append("")

        # ── All t-calls summary ──────────────────────────────────────────────
        output.append("=" * 80)
        output.append(" ALL T-CALLS REFERENCED ".center(80, "="))
        output.append("=" * 80)
        output.append("")

        all_tcalls = set()
        for node in tree_nodes.values():
            all_tcalls.update(node['tcalls'])

        if all_tcalls:
            for tc in sorted(all_tcalls):
                status = "found" if tc in tree_nodes else "NOT FOUND in DB"
                output.append(f"  {tc}  [{status}]")
        else:
            output.append("  (no t-calls found)")
        output.append("")

        # ── Footer ───────────────────────────────────────────────────────────
        output.append("=" * 80)
        output.append(" LEGEND ".center(80, "="))
        output.append("=" * 80)
        output.append("  [REPORT]    = Base report entry-point view")
        output.append("  <t-call>    = Template called with t-call directive")
        output.append("  <inherits>  = Parent view this view extends (inherit_id)")
        output.append("  <xpath>     = XPath expression used for injection")
        output.append("  <sibling>   = Related view sharing the same key prefix")
        output.append("")
        output.append("=" * 80)
        output.append(" Generated by QWeb Report Analyzer - José Bertorelli ".center(80, "="))
        output.append(" https://github.com/josebertorelli/qweb-report-analyzer ".center(80, "="))
        output.append("=" * 80)

        return "\n".join(output)


class ReportAnalyzer(models.AbstractModel):
    _name = 'report.analyzer'
    _description = 'QWeb Report Analyzer'

    def _collect_view_data(self, view):
        """Collect relevant data from a single ir.ui.view record."""
        return {
            'id': view.id,
            'name': view.name,
            'key': view.key,
            'type': view.type,
            'priority': view.priority,
            'arch': view.arch,
            'inherit_id': view.inherit_id.id if view.inherit_id else None,
            'inherit_key': view.inherit_id.key if view.inherit_id else None,
            'inherit_name': view.inherit_id.name if view.inherit_id else None,
        }

    def _collect_all_views_data(self, report):
        """
        Collect all QWeb views and build the inheritance map.
        Everything runs locally — no external call needed.
        """
        views_data = {}
        view_key = report.report_name

        all_qweb_views = self.env['ir.ui.view'].search([('type', '=', 'qweb')])

        for view in all_qweb_views:
            views_data[view.id] = self._collect_view_data(view)

        # Build parent → [children] map
        inherited_map = {}
        for view in all_qweb_views:
            if view.inherit_id:
                parent_id = view.inherit_id.id
                inherited_map.setdefault(parent_id, []).append(view.id)

        return {
            'report': {
                'id': report.id,
                'name': report.name,
                'report_name': report.report_name,
                'model': report.model,
                'report_type': report.report_type,
            },
            'views': views_data,
            'inherited_map': inherited_map,
            'entry_point': view_key,
        }

    def analyze_report(self, report_id):
        """
        Main entry point.
        Collects view data, runs the analysis locally, and returns a
        downloadable .txt attachment.
        """
        report = self.env['ir.actions.report'].browse(report_id)
        if not report.exists():
            raise UserError("Report not found.")

        _logger.info("QWeb Report Analyzer: collecting data for '%s'", report.name)
        collected = self._collect_all_views_data(report)

        _logger.info("QWeb Report Analyzer: running local analysis...")
        analyzer = QWebAnalyzer(
            report_data=collected['report'],
            views_data={str(k): v for k, v in collected['views'].items()},
            inherited_map={str(k): v for k, v in collected['inherited_map'].items()},
            entry_point=collected['entry_point'],
        )
        analysis_content = analyzer.analyze()

        # Sanitise filename
        safe_name = report.name
        for char in r'/\:*?"<>|':
            safe_name = safe_name.replace(char, '_')
        filename = f"{safe_name} - analysis.txt"

        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'raw': analysis_content.encode('utf-8'),
            'mimetype': 'text/plain',
            'res_model': 'ir.actions.report',
            'res_id': report.id,
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }
