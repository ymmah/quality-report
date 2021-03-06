/* Copyright 2012-2017 Ministerie van Sociale Zaken en Werkgelegenheid
 *
 * Licensed under the Apache License, Version 2.0 (the "License")
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React from 'react';
import {Menu, MenuItem} from 'widgets/menu.js';


class MetricsMenu extends React.Component {
    render() {
        let section_menu_items = [];
        this.props.sections.forEach(function(section) {
            let id = section["id"], title = section["title"];
            section_menu_items.push(
                <MenuItem key={id} className={"link_section_" + id} href={"section_" + id} title={title} />
            );
        });
        return (
            <Menu id="navigation_menu" title="Metrieken" hide={this.props.tab !== 'metrics_tab'}>
                <MenuItem href="section_dashboard" icon="dashboard" title="Dashboard"
                          hide={!this.props.show_dashboard} />
                {section_menu_items}
            </Menu>
        );
    }
}

class FilterMenu extends React.Component {
    render() {
        return (
            <Menu id="toon_menu" title="Toon" hide={this.props.tab !== 'metrics_tab'}>
                <MenuItem id="show_dashboard" title="Dashboard"
                          check={this.props.show_dashboard}
                          onClick={this.props.on_toggle_dashboard} />
                <MenuItem id="show_multiple_tables" title="Tabel per product/team"
                          check={!this.props.show_one_table}
                          onClick={this.props.on_toggle_one_table} />
                <li role="separator" className="divider"></li>
                <MenuItem id="filter_all" title="Alle statussen"
                          check={this.props.filter.filter_all}
                          onClick={this.props.on_filter} />
                <MenuItem id="filter_color_red" title="Actie vereist"
                          check={this.props.filter.filter_color_red}
                          onClick={this.props.on_filter} />
                <MenuItem id="filter_color_yellow" title="Bijna goed"
                          check={this.props.filter.filter_color_yellow}
                          onClick={this.props.on_filter} />
                <MenuItem id="filter_color_green" title="Goed"
                          check={this.props.filter.filter_color_green}
                          onClick={this.props.on_filter} />
                 <MenuItem id="filter_color_perfect" title="Perfect"
                          check={this.props.filter.filter_color_perfect}
                          onClick={this.props.on_filter} />
                <MenuItem id="filter_color_grey" title="Technische schuld"
                          check={this.props.filter.filter_color_grey}
                          onClick={this.props.on_filter} />
                <MenuItem id="filter_color_missing_source" title="Bron niet geconfigureerd"
                          check={this.props.filter.filter_color_missing_source}
                          onClick={this.props.on_filter} />
                <MenuItem id="filter_color_missing" title="Bron niet beschikbaar"
                          check={this.props.filter.filter_color_missing}
                          onClick={this.props.on_filter} />
                <MenuItem id="filter_status_week" title="Langer dan een week dezelfde status"
                          check={this.props.filter.filter_status_week}
                          onClick={this.props.on_filter} />
                <li role="separator" className="divider"></li>
                <MenuItem id="hidden_metrics" title="Verborgen metrieken"
                          disabled={this.props.filter.hidden_metrics.length === 0}
                          onClick={this.props.on_filter} />
            </Menu>
        );
    }
}

class TrendMenu extends React.Component {
    render() {
        return (
            <Menu id="trend_navigation_menu" title="Trend" hide={this.props.tab !== 'trend_tab'}>
                <MenuItem href="meta_metrics_history_absolute_graph" title="Aantal metrieken per status" />
                <MenuItem href="meta_metrics_history_relative_graph" title="Percentage metrieken per status" />
            </Menu>
        );
    }
}

class HelpMenu extends React.Component {
    render() {
        return (
            <Menu id="help_tab_menu" title="Help" hide={this.props.tab !== 'help_tab'}>
                <MenuItem href="help_about" title="Over HQ" icon="info-sign" />
                <MenuItem href="help_on_metrics" title="Metrieken" icon="tasks" />
                <MenuItem href="help_on_metric_sources" title="Metriekbronnen" icon="open" />
                <MenuItem href="help_on_requirements" title="Eisen" icon="check" />
                <MenuItem href="help_on_domain_objects" title="Domeinobjecten" icon="file" />
                <MenuItem href="help_on_configuration" title="Configuratie" icon="wrench" />
            </Menu>
        );
    }
}

class Menus extends React.Component {
    render() {
        return (
            <ul className="nav navbar-nav">
                <MenuItem id="metrics_tab" onClick={this.props.on_tab} title="Metrieken"
                          hide={this.props.tab === 'metrics_tab'} />
                <MetricsMenu {...this.props} />
                <MenuItem title="Toon" hide={this.props.tab === 'metrics_tab'} disabled={true} />
                <FilterMenu {...this.props} />
                <MenuItem id="trend_tab" onClick={this.props.on_tab} title="Trend"
                          hide={this.props.tab === 'trend_tab'} />
                <TrendMenu tab={this.props.tab} />
                <MenuItem id="help_tab" onClick={this.props.on_tab} title="Help"
                          hide={this.props.tab === 'help_tab'} />
                <HelpMenu tab={this.props.tab} />
            </ul>
        );
    }
}

export {Menus, MetricsMenu, FilterMenu, TrendMenu, HelpMenu};
