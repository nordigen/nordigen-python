from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, TypedDict


class TokenType(TypedDict):
    access: str
    refresh: str
    access_expires: int
    refresh_expires: int


class Institutions(TypedDict):
    id: str
    name: str
    bic: str
    transaction_total_days: str
    countries: List[str]
    logo: str


class EnduserAgreement(TypedDict):
    id: str
    created: str
    enduser_id: str
    institution_id: str
    accepted: Optional[str]
    access_scope: List[str]
    max_historical_days: int
    access_valid_for_days: int


class AgreementsList(TypedDict):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[EnduserAgreement]


class Requisition(TypedDict):
    id: str
    created: str
    redirect: str
    status: str
    agreements: List[str]
    accounts: List[str]
    reference: str
    enduser_id: str
    user_language: Optional[str]
    results: List[Dict[str, str]]


class RequisitionList(AgreementsList):
    results: List[Requisition]


@dataclass
class RequisitionDto:
    link: str
    requisition_id: str


class Balances(TypedDict):
    amount: str
    currency: str


class AccountBalances(TypedDict):
    balances: Balances
    balanceType: str
    creditLimitIncluded: Optional[bool]
    lastChangeDateTime: Optional[datetime]
    referenceDate: Optional[datetime]
    lastCommittedTransaction: Optional[str]


class AccountData(TypedDict):
    id: str
    created: datetime
    lastAccessed: datetime
    iban: str
    aspspIdentifier: str
    status: str


class AccountInfo(TypedDict):
    resource_id: str
    iban: str
    currency: str
    ownerName: str


class AccountDetails(TypedDict):
    account: AccountInfo
