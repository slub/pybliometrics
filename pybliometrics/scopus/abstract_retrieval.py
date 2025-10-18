from typing import Union

from pybliometrics.superclasses import Retrieval
from pybliometrics.utils import check_parameter_value, detect_id_type, VIEWS


class Affiliation(NamedTuple):
    id: int | None
    name: str | None
    city: str | None
    country: str | None


class AuthorGroup(NamedTuple):
    affiliation_id: int | None
    collaboration_id: str | None
    dptid: int | None
    organization: str | None
    city: str | None
    postalcode: str | None
    addresspart: str | None
    country: str | None
    auid: int | None
    orcid: str | None
    indexed_name: str | None
    surname: str | None
    given_name: str | None


class Author(NamedTuple):
    auid: int
    indexed_name: str | None
    surname: str | None
    given_name: str | None
    affiliation: str | None


class Chemical(NamedTuple):
    source: str
    chemical_name: str
    cas_registry_number: str | None


class Contributor(NamedTuple):
    given_name: str | None
    initials: str | None
    surname: str | None
    indexed_name: str | None
    role: str | None


class Correspondence(NamedTuple):
    surname: str | None
    initials: str | None
    organization: str | None
    country: str | None
    city_group: str | None


class Funding(NamedTuple):
    agency: str | None
    agency_id: str | None
    string: str | None
    funding_id: list[str] | None
    acronym: str | None
    country: str | None


class ISSN(NamedTuple):
    print: str | None = None
    electronic: str | None = None


class Reference(NamedTuple):
    position: str | None
    id: str | None
    doi: str | None
    title: str | None
    authors: str | None
    authors_auid: str | None
    authors_affiliationid: str | None
    sourcetitle: str | None
    publicationyear: str | None
    coverDate: str | None
    volume: str | None
    issue: str | None
    first: str | None
    last: str | None
    citedbycount: str | None
    type: str | None
    text: str | None
    fulltext: str | None


class Sequencebank(NamedTuple):
    name: str
    sequence_number: str
    type: str


class Area(NamedTuple):
    area: str
    abbreviation: str
    code: int


class AbstractRetrieval(Retrieval):

    def __init__(self,
                 identifier: int | str | None = None,
                 refresh: bool | int = False,
                 view: str = 'META_ABS',
                 id_type: str | None = None,
                 **kwds: str
                 ) -> None:
        """Interaction with the Abstract Retrieval API.

        :param identifier: The identifier of a document.  Can be the Scopus EID
                           , the Scopus ID, the PII, the Pubmed-ID or the DOI.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param id_type: The type of used ID. Allowed values: None, 'eid', 'pii',
                        'scopus_id', 'pubmed_id', 'doi'.  If the value is None,
                        the function tries to infer the ID type itself.
        :param view: The view of the file that should be downloaded.  Allowed
                     values: META, META_ABS, REF, FULL, ENTITLED, where FULL includes all
                     information of META_ABS view and META_ABS includes all
                     information of the META view.  For details see
                     https://dev.elsevier.com/sc_abstract_retrieval_views.html.
                     Note: `ENTITLED` view only contains the `document_entitlement_status`.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values listed in the API specification at
                     https://dev.elsevier.com/documentation/AbstractRetrievalAPI.wadl.

        Raises
        ------
        ValueError
            If any of the parameters `id_type`, `refresh` or `view` is not
            one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/{view}/{identifier}`,
        where `path` is specified in your configuration file.  In case
        `identifier` is a DOI, an underscore replaces the forward slash.
        """
        # Checks
        identifier = str(identifier)
        check_parameter_value(view, VIEWS['AbstractRetrieval'], "view")
        if id_type is None:
            id_type = detect_id_type(identifier)
        else:
            allowed_id_types = ('eid', 'pii', 'scopus_id', 'pubmed_id', 'doi')
            check_parameter_value(id_type, allowed_id_types, "id_type")

        # Load xml
        self._view = view
        self._refresh = refresh
        Retrieval.__init__(self, identifier=identifier, id_type=id_type, **kwds)
