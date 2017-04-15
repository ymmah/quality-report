"""
Copyright 2012-2017 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import logging

from typing import cast, List, Tuple, Set, Type, Optional

from .document import Document
from .environment import Environment
from .product import Product
from .requirement import RequirementSubject, Requirement
from .team import Team
from ..measurement import metric_source, measurable
from ..measurement.metric_source import MetricSource
from ..measurement.metric_sources import MetricSources
from ..base import DomainObject


class Project(RequirementSubject, measurable.MeasurableObject):
    """ Class representing a software development/maintenance project. """

    def __init__(self, organization: str='Unnamed organization', metric_sources=None, *args, **kwargs) -> None:
        self.__short_section_names = {'MM', 'PC', 'PD'}  # Two letter abbreviations used, must be unique
        self.__organization = organization
        self.__metric_sources = MetricSources(metric_sources or dict())
        self.__products: List[Product] = []
        self.__teams: List[Team] = []
        self.__documents: List[Document] = []
        self.__environments: List[Environment] = []
        self.__dashboard: Tuple[List, List] = ([], [])  # rows, columns
        super().__init__(*args, **kwargs)

    @staticmethod
    def optional_requirements() -> Set[Type[Requirement]]:
        from ... import requirement  # Run time import to prevent circular dependency.
        return {requirement.TrackActions, requirement.TrackBugs,  requirement.TrackManualLTCs,
                requirement.TrackReadyUS, requirement.TrackRisks, requirement.TrackSecurityAndPerformanceRisks,
                requirement.TrustedProductMaintainability, requirement.TrackTechnicalDebt}

    def organization(self) -> str:
        """ Return the name of the organization. """
        return self.__organization

    def metric_source(self, metric_source_class: Type[MetricSource]) -> MetricSource:
        """ Return the metric source instance for the metric source class. """
        return self.__metric_sources.get(metric_source_class, metric_source.MissingMetricSource())

    def metric_source_classes(self) -> List[Type[MetricSource]]:
        """ Return a set of all metric source classes. """
        return list(self.__metric_sources.keys())

    def domain_object_classes(self) -> Set[Type[DomainObject]]:
        """ Return a set of all the domain object classes used. """
        domain_objects = self.products() + self.teams() + self.documents() + self.environments()
        return {cast(Type[DomainObject], domain_object.__class__) for domain_object in domain_objects}

    def add_product(self, product: Product) -> None:
        """ Add a product to the project. """
        self.__check_short_section_name(product.short_name())
        self.__products.append(product)

    def products(self) -> List[Product]:
        """ Return the products of the project. """
        return self.__products

    def get_product(self, name: str) -> Optional[Product]:
        """ Find a product by name. """
        matches = [product for product in self.__products if product.name() == name]
        return matches[0] if matches else None

    def add_team(self, team: Team) -> None:
        """ Add a team to the project. """
        self.__check_short_section_name(team.short_name())
        self.__teams.append(team)

    def teams(self) -> List[Team]:
        """ Return the teams that work on the project. """
        return self.__teams

    def add_document(self, document: Document) -> None:
        """ Add a document to the project. """
        self.__documents.append(document)

    def documents(self) -> List[Document]:
        """ Return the documents of the project. """
        return self.__documents

    def add_environment(self, environment: Environment) -> None:
        """ Add an environment to the project. """
        self.__environments.append(environment)

    def environments(self) -> List[Environment]:
        """ Return the environments of the project """
        return self.__environments

    def set_dashboard(self, dashboard_columns, dashboard_rows):
        """ Set the dashboard layout for the project. """
        self.__dashboard = (dashboard_columns, dashboard_rows)

    def dashboard(self):
        """ Return the dashboard layout for the project. """
        return self.__dashboard

    def __check_short_section_name(self, name: str) -> None:
        """ Raise an exception when the short section name is already in use. """
        if name in self.__short_section_names:
            logging.error('Section abbreviation must be unique: %s already used: %s',
                          name, self.__short_section_names)
            raise ValueError('Section abbreviation {0!s} is not unique'.format(name))
        else:
            self.__short_section_names.add(name)
