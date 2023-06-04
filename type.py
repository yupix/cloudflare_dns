from typing import Any, Generic, Literal, TypeVar, TypedDict

T = TypeVar("T")

PERMISSIONS = Literal[
    "#integration:edit",
    "#integration:read",
    "#integration:install",
    "#waitingroom:read",
    "#waitingroom:edit",
    "#magic:read",
    "#magic:edit",
    "#organization:read",
    "#organization:edit",
    "#waf:read",
    "#waf:edit",
    "#dex:read",
    "#analytics:read",
    "#dex:edit",
    "#zone_settings:read",
    "#zone_settings:edit",
    "#dns_records:read",
    "#dns_records:edit",
    "#worker:edit",
    "#zone_versioning:read",
    "#zone_versioning:edit",
    "#ssl:edit",
    "#zaraz:publish",
    "#ssl:read",
    "#worker:read",
    "#logs:edit",
    "#billing:read",
    "#fbm:edit",
    "#fbm:read",
    "#fbm_acc:edit",
    "#logs:read",
    "#http_applications:read",
    "#http_applications:edit",
    "#lb:edit",
    "#blocks:read",
    "#blocks:edit",
    "#zaraz:edit",
    "#zaraz:read",
    "#stream:read",
    "#stream:edit",
    "#teams:read",
    "#teams:edit",
    "#healthchecks:read",
    "#lb:read",
    "#web3:read",
    "#web3:edit",
    "#access:read",
    "#access:edit",
    "#image:read",
    "#image:edit",
    "#healthchecks:edit",
    "#dash_sso:edit",
    "#dash_sso:read",
    "#teams:pii",
    "#zone:edit",
    "#zone:read",
    "#billing:edit",
    "#teams:report",
    "#subscription:edit",
    "#app:edit",
    "#subscription:read",
    "#cache_purge:edit",
    "#auditlogs:read",
    "#member:edit",
    "#member:read",
    "#legal:read",
    "#legal:edit",
]


class IPlan(TypedDict):
    id: str
    name: str
    price: int
    currency: str
    frequency: str
    is_subscribed: bool
    can_subscribe: bool
    legacy_id: str
    legacy_discount: bool
    externally_managed: bool


class ITenantUnit(TypedDict):
    id: str | None


class ITenant(TypedDict):
    id: str | None
    name: str | None


class IAccount(TypedDict):
    id: str
    name: str


class IOwner(TypedDict):
    id: str | None
    type: str
    email: str | None


class IMeta(TypedDict):
    step: int
    custom_certificate_quota: int
    page_rule_quota: int
    phishing_detected: bool
    multiple_railguns_allowed: bool


class IZone(TypedDict):
    id: str
    name: str
    status: str
    paused: bool
    type: str
    development_mode: int
    name_servers: list[str]
    original_name_servers: list[str]
    original_registrar: str
    original_dnshost: str | None
    modified_on: str  # datetime
    created_on: str  # datetime
    activated_on: str  # datetime
    meta: IMeta
    owner: IOwner
    account: IAccount
    tenant: ITenant
    tenant_units: ITenantUnit
    permissions: list[PERMISSIONS]
    plan: IPlan


class IResultInfo(TypedDict):
    page: int
    per_page: int
    total_pages: int
    count: int
    total_count: int


class IDNSRecordMeta(TypedDict):
    auto_added: bool
    source: str


class IDNSRecord(TypedDict):
    content: str
    name: str
    proxied: bool
    type: str
    comment: str
    created_on: str  # datetime
    id: str
    locked: bool
    meta: IDNSRecordMeta
    modified_on: str  # datetime
    proxiable: bool
    tags: list[str]
    ttl: int
    zone_id: str
    zone_name: str


class IResponse(TypedDict, Generic[T]):
    result: T
    result_info: IResultInfo
    success: bool
    errors: list[Any]
    messages: list[Any]


class ICustomZone(TypedDict):
    zone_id: str
    domain: str
