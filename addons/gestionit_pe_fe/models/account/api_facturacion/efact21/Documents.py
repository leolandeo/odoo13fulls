from xml.dom import minidom

from . import BasicGlobal, InvoiceLine
from . import BillingReference
from . import DiscrepancyResponse
from . import General
from .CustomerParty import AccountingCustomerParty, DeliveryCustomerParty
from .DespatchLine import DespatchLine
from .Shipment import Shipment
from .SupplierParty import AccountingSupplierParty, DespatchSupplierParty, SellerSupplierParty
from .DocumentReference import AdditionalDocumentReference, DespatchDocumentReference
from .MonetaryTotal import LegalMonetaryTotal, RequestedMonetaryTotal
from .OrderReference import OrderReference
from .PrepaidPayment import PrepaidPayment
from .Signature import Signature
from .SummaryDocumentsLine import SummaryDocumentsLine
from .VoidedDocumentsLine import VoidedDocumentsLine
from .TaxTotal import TaxTotal
from .util import Xmleable, default_document
from . import CreditNoteLine, DebitNoteLine
from .AllowanceCharge import AllowanceCharge

import logging
_logger = logging.getLogger(__name__)


class Factura(Xmleable):
    def __init__(self, ubl_extensions=None, ubl_version="2.1", id=None,
                 issue_date=None, issue_time=None, due_date=None,
                 invoice_type_code=None, document_currency_code=None, customization="2.0",
                 despatch_document_reference=None, additional_document_reference=None, signature=None,
                 accounting_supplier_party=None, accounting_customer_party=None,
                 legal_monetary_total=None, tax_total=None, descuento_global=None):
        self.invoice_lines = []
        self.notes = []
        self.tax_total = tax_total
        self.prepaid_payments = []
        self.ubl_extensions = ubl_extensions
        self.ubl_version = ubl_version
        self.customization = customization
        self.id = id
        self.issue_date = issue_date
        self.issue_time = issue_time
        self.due_date = due_date
        self.invoice_type_code = invoice_type_code
        self.document_currency_code = document_currency_code
        self.despatch_document_reference = despatch_document_reference
        self.additional_document_reference = additional_document_reference
        self.signature = signature
        self.accounting_supplier_party = accounting_supplier_party
        self.accounting_customer_party = accounting_customer_party
        self.legal_monetary_total = legal_monetary_total
        self.file_name = None
        self.line_count_numeric = 0
        self.descuento_global = descuento_global

    def set_file_name(self, name):
        self.file_name = name

    def add_prepaid_payment(self, prepaid_payment):
        if type(prepaid_payment) != PrepaidPayment:
            raise Exception("Bad type")
        self.prepaid_payments.append(prepaid_payment)
        prepaid_payment.ord = len(self.prepaid_payments)

    def add_invoice_line(self, invoice_line):
        if type(invoice_line) != InvoiceLine.InvoiceLine:
            raise Exception("Bad type")
        self.invoice_lines.append(invoice_line)
        invoice_line.ord = len(self.invoice_lines)

    def add_note(self, note):
        if type(note) == str:
            note = BasicGlobal.Note(note)
        if type(note) != BasicGlobal.Note:
            raise Exception("Bad type")
        self.notes.append(note)

    def fix_values(self):
        if not self.ubl_extensions:
            self.ubl_extensions = BasicGlobal.UBLExtensions()
        if type(self.ubl_version) == str:
            self.ubl_version = BasicGlobal.UBLVersion(self.ubl_version)
        if type(self.customization) == str:
            self.customization = BasicGlobal.CustomizationID(
                self.customization)
        if type(self.id) == str:
            self.id = BasicGlobal.SummaryId(self.id)
        if type(self.issue_date) == str:
            self.issue_date = General.IssueDate(self.issue_date)
        if type(self.issue_time) == str:
            self.issue_time = BasicGlobal.IssueTime(self.issue_time)
        if type(self.due_date) == str:
            self.due_date = General.DueDate(self.due_date)
        if type(self.invoice_type_code) == str:
            self.invoice_type_code = BasicGlobal.InvoiceTypeCode(
                self.invoice_type_code)
        if type(self.document_currency_code) == str:
            self.document_currency_code = BasicGlobal.DocumentCurrencyCode(
                self.document_currency_code)
        self.line_count_numeric = BasicGlobal.LineCountNumeric(
            len(self.invoice_lines))

    def validate(self, errs, obs):
        assert type(self.ubl_extensions) == BasicGlobal.UBLExtensions
        assert type(self.customization) == BasicGlobal.CustomizationID
        assert type(self.id) == BasicGlobal.SummaryId
        assert type(self.issue_date) == General.IssueDate
        assert self.issue_time is None or type(
            self.issue_time) == BasicGlobal.IssueTime
        assert self.due_date is None or type(self.due_date) == General.DueDate
        assert type(self.invoice_type_code) == BasicGlobal.InvoiceTypeCode
        assert type(
            self.document_currency_code) == BasicGlobal.DocumentCurrencyCode
        assert self.additional_document_reference is None or \
            type(self.additional_document_reference) == AdditionalDocumentReference
        assert type(self.accounting_supplier_party) == AccountingSupplierParty
        assert type(self.legal_monetary_total) == LegalMonetaryTotal
        assert type(self.accounting_customer_party) == AccountingCustomerParty
        assert self.despatch_document_reference is None or \
            type(self.despatch_document_reference) == DespatchDocumentReference
        assert self.descuento_global is None or \
            type(self.descuento_global) == AllowanceCharge

    def generate_root(self):
        self.doc = default_document.createElement("Invoice")
        self.doc.setAttribute(
            "xmlns", "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2")
        self.doc.setAttribute(
            "xmlns:cac", "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2")
        self.doc.setAttribute(
            "xmlns:cbc", "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2")
        self.doc.setAttribute(
            "xmlns:ccts", "urn:un:unece:uncefact:documentation:2")
        self.doc.setAttribute("xmlns:ds", "http://www.w3.org/2000/09/xmldsig#")
        self.doc.setAttribute(
            "xmlns:ext", "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2")
        self.doc.setAttribute(
            "xmlns:qdt", "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2")
        self.doc.setAttribute("xmlns:udt",
                              "urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2")
        self.doc.setAttribute(
            "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

    def generate_doc(self):
        self.generate_root()

        self.doc.appendChild(self.ubl_extensions.get_document())

        # Datos de la factura
        self.doc.appendChild(self.ubl_version.get_document())
        self.doc.appendChild(self.customization.get_document())
        self.doc.appendChild(self.id.get_document())

        # Fecha de Emisi??n
        self.doc.appendChild(self.issue_date.get_document())

        # Hora de Emisi??n
        if self.issue_time:
            self.doc.appendChild(self.issue_time.get_document())

        # Fecha de Vencimiento
        if self.due_date:
            self.doc.appendChild(self.due_date.get_document())

        # Tipo de Documento
        self.doc.appendChild(self.invoice_type_code.get_document())

        # Informacion adicional
        for note in self.notes:
            self.doc.appendChild(note.get_document())

        # Moneda
        self.doc.appendChild(self.document_currency_code.get_document())

        # Cantidad de Items de la factura
        self.doc.appendChild(self.line_count_numeric.get_document())

        # despatch_document_reference
        if self.despatch_document_reference:
            self.doc.appendChild(
                self.despatch_document_reference.get_document())

        # Documentos de referencia
        if self.additional_document_reference:
            self.doc.appendChild(
                self.additional_document_reference.get_document())

        # Datos de la firma
        if self.signature:
            self.doc.appendChild(self.signature.get_document())

        # Datos del emisor
        self.doc.appendChild(self.accounting_supplier_party.get_document())
        # Falta Delivery

        # Datos del receptor
        self.doc.appendChild(self.accounting_customer_party.get_document())

        # Descuento Global
        if self.descuento_global:
            self.doc.appendChild(self.descuento_global.get_document())

        # Datos del comprador: falta

        # Total de Impuestos de la factura
        self.doc.appendChild(self.tax_total.get_document())

        # Informacion adicional: anticipos
        for prepaid_payment in self.prepaid_payments:
            self.doc.appendChild(prepaid_payment.get_document())

        self.doc.appendChild(self.legal_monetary_total.get_document())

        # Items de la factura
        for line in self.invoice_lines:
            self.doc.appendChild(line.get_document())

    def get_document(self):
        self.fix_values()
        self.generate_doc()

        xml_doc = minidom.Document()
        xml_doc.appendChild(self.doc)
        return xml_doc


class ResumenDiario(Xmleable):
    def __init__(self, ubl_version="2.0", customization_id="1.1", doc_id=None,
                 issue_date=None, reference_date=None, accounting_supplier_party=None,
                 signature=None, ubl_extensions=None):
        self.ubl_version = ubl_version
        self.customization_id = customization_id
        self.doc_id = doc_id
        self.issue_date = issue_date
        self.reference_date = reference_date
        self.accounting_supplier_party = accounting_supplier_party
        self.signature = signature
        self.ubl_extensions = ubl_extensions
        self.documents_line = []
        self.notes = []
        self.file_name = None

    def set_file_name(self, name):
        self.file_name = name

    def fix_values(self):
        if type(self.ubl_version) == str:
            self.ubl_version = BasicGlobal.UBLVersion(self.ubl_version)
        if type(self.customization_id) == str:
            self.customization_id = BasicGlobal.CustomizationID(
                self.customization_id)
        if type(self.doc_id) == str:
            self.doc_id = BasicGlobal.SummaryId(self.doc_id)
        if type(self.reference_date) == str:
            self.reference_date = General.ReferenceDate(self.reference_date)
        if self.ubl_extensions is None:
            self.ubl_extensions = BasicGlobal.UBLExtensions()
        if type(self.issue_date) == str:
            self.issue_date = General.IssueDate(self.issue_date)

    def validate(self, errs, obs):
        assert type(self.ubl_version) == BasicGlobal.UBLVersion
        assert type(self.customization_id) == BasicGlobal.CustomizationID
        assert type(self.doc_id) == BasicGlobal.SummaryId
        assert type(self.issue_date) == General.IssueDate
        assert type(self.reference_date) == General.ReferenceDate
        assert type(self.accounting_supplier_party) == AccountingSupplierParty
        assert self.signature is None or type(self.signature) == Signature
        assert type(self.ubl_extensions) == BasicGlobal.UBLExtensions

    def generate_root(self):
        self.doc = default_document.createElement("SummaryDocuments")
        self.doc.setAttribute(
            "xmlns", "urn:sunat:names:specification:ubl:peru:schema:xsd:SummaryDocuments-1")
        self.doc.setAttribute(
            "xmlns:cac", "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2")
        self.doc.setAttribute(
            "xmlns:cbc", "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2")
        self.doc.setAttribute("xmlns:ds", "http://www.w3.org/2000/09/xmldsig#")
        self.doc.setAttribute(
            "xmlns:ccts", "urn:un:unece:uncefact:documentation:2")
        self.doc.setAttribute(
            "xmlns:qdt", "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2")
        self.doc.setAttribute("xmlns:udp",
                              "urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2")
        self.doc.setAttribute(
            "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        self.doc.setAttribute(
            "xmlns:ext", "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2")
        self.doc.setAttribute("xmlns:sac",
                              "urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1")

    def add_summary_document_line(self, doc_line):
        assert type(doc_line) == SummaryDocumentsLine
        self.documents_line.append(doc_line)
        doc_line.line_id = len(self.documents_line)

    def add_note(self, note):
        if type(note) == str:
            note = BasicGlobal.Note(note)
        assert type(note) == BasicGlobal.Note
        self.notes.append(note)

    def generate_doc(self):
        self.generate_root()

        self.doc.appendChild(self.ubl_extensions.get_document())

        # Datos del resumen
        self.doc.appendChild(self.ubl_version.get_document())
        self.doc.appendChild(self.customization_id.get_document())
        self.doc.appendChild(self.doc_id.get_document())
        self.doc.appendChild(self.reference_date.get_document())
        self.doc.appendChild(self.issue_date.get_document())

        if self.signature:
            self.doc.appendChild(self.signature.get_document())

        self.doc.appendChild(self.accounting_supplier_party.get_document())

        # Notes
        for note in self.notes:
            self.doc.appendChild(note.get_document())

        # Docs Lines
        for doc_line in self.documents_line:
            self.doc.appendChild(doc_line.get_document())

    def get_document(self):
        self.fix_values()
        self.generate_doc()

        xml_doc = minidom.Document()
        xml_doc.appendChild(self.doc)
        return xml_doc


class ComunicacionBaja(Xmleable):
    def __init__(self, ubl_version="2.0", customization_id="1.0", doc_id=None,
                 issue_date=None, reference_date=None, accounting_supplier_party=None,
                 signature=None, ubl_extensions=None):
        self.ubl_version = ubl_version
        self.customization_id = customization_id
        self.doc_id = doc_id
        self.issue_date = issue_date
        self.reference_date = reference_date
        self.accounting_supplier_party = accounting_supplier_party
        self.signature = signature
        self.ubl_extensions = ubl_extensions
        self.documents_line = []
        self.notes = []
        self.file_name = None

    def set_file_name(self, name):
        self.file_name = name

    def fix_values(self):
        if type(self.ubl_version) == str:
            self.ubl_version = BasicGlobal.UBLVersion(self.ubl_version)
        if type(self.customization_id) == str:
            self.customization_id = BasicGlobal.CustomizationID(
                self.customization_id)
        if type(self.doc_id) == str:
            self.doc_id = BasicGlobal.SummaryId(self.doc_id)
        if type(self.reference_date) == str:
            self.reference_date = General.ReferenceDate(self.reference_date)
        if self.ubl_extensions is None:
            self.ubl_extensions = BasicGlobal.UBLExtensions()
        if type(self.issue_date) == str:
            self.issue_date = General.IssueDate(self.issue_date)

    def validate(self, errs, obs):
        assert type(self.ubl_version) == BasicGlobal.UBLVersion
        assert type(self.customization_id) == BasicGlobal.CustomizationID
        assert type(self.doc_id) == BasicGlobal.SummaryId
        assert type(self.issue_date) == General.IssueDate
        assert type(self.reference_date) == General.ReferenceDate
        assert type(self.accounting_supplier_party) == AccountingSupplierParty
        assert self.signature is None or type(self.signature) == Signature
        assert type(self.ubl_extensions) == BasicGlobal.UBLExtensions

    def generate_root(self):
        self.doc = default_document.createElement("VoidedDocuments")
        self.doc.setAttribute(
            'xmlns', 'urn:sunat:names:specification:ubl:peru:schema:xsd:VoidedDocuments-1')
        self.doc.setAttribute(
            'xmlns:cac', 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2')
        self.doc.setAttribute(
            'xmlns:cbc', 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2')
        self.doc.setAttribute('xmlns:ds', 'http://www.w3.org/2000/09/xmldsig#')
        self.doc.setAttribute(
            'xmlns:ext', 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2')
        self.doc.setAttribute(
            'xmlns:sac', 'urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1')
        self.doc.setAttribute(
            'xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

    def add_voided_document_line(self, doc_line):
        assert type(doc_line) == VoidedDocumentsLine
        self.documents_line.append(doc_line)
        doc_line.line_id = len(self.documents_line)

    def generate_doc(self):
        self.generate_root()

        self.doc.appendChild(self.ubl_extensions.get_document())

        # Datos del resumen
        self.doc.appendChild(self.ubl_version.get_document())
        self.doc.appendChild(self.customization_id.get_document())
        self.doc.appendChild(self.doc_id.get_document())
        self.doc.appendChild(self.reference_date.get_document())
        self.doc.appendChild(self.issue_date.get_document())

        if self.signature:
            self.doc.appendChild(self.signature.get_document())

        self.doc.appendChild(self.accounting_supplier_party.get_document())

        # Docs Lines
        for doc_line in self.documents_line:
            self.doc.appendChild(doc_line.get_document())

    def get_document(self):
        self.fix_values()
        self.generate_doc()

        xml_doc = minidom.Document()
        xml_doc.appendChild(self.doc)
        return xml_doc


class CreditNote(Xmleable):
    def __init__(self, ubl_extensions=None, ubl_version="2.1", id=None,
                 issue_date=None, issue_time=None, document_currency_code=None, customization="2.0",
                 discrepancy_response=None, billing_reference=None,
                 signature=None, accounting_supplier_party=None, accounting_customer_party=None,
                 tax_total=None, legal_monetary_total=None):

        self.credit_note_lines = []
        self.notes = []
        self.file_name = None

        self.ubl_extensions = ubl_extensions
        self.ubl_version = ubl_version
        self.customization = customization
        self.id = id
        self.issue_date = issue_date
        self.issue_time = issue_time
        self.document_currency_code = document_currency_code
        self.discrepancy_response = discrepancy_response
        self.billing_reference = billing_reference
        self.signature = signature
        self.accounting_supplier_party = accounting_supplier_party
        self.accounting_customer_party = accounting_customer_party
        self.legal_monetary_total = legal_monetary_total
        self.tax_total = tax_total

    def set_file_name(self, name):
        self.file_name = name

    def add_credit_note_line(self, credit_note_line):
        assert type(credit_note_line) == CreditNoteLine.CreditNoteLine
        self.credit_note_lines.append(credit_note_line)
        credit_note_line.ord = len(self.credit_note_lines)

    def add_note(self, note):
        if type(note) == str:
            note = BasicGlobal.Note(note)
        assert type(note) == BasicGlobal.Note
        self.notes.append(note)

    def fix_values(self):
        if not self.ubl_extensions:
            self.ubl_extensions = BasicGlobal.UBLExtensions()
        if type(self.ubl_version) == str:
            self.ubl_version = BasicGlobal.UBLVersion(self.ubl_version)
        if type(self.customization) == str:
            self.customization = BasicGlobal.CustomizationID(
                self.customization)
        if type(self.id) == str:
            self.id = BasicGlobal.SummaryId(self.id)
        if type(self.issue_date) == str:
            self.issue_date = General.IssueDate(self.issue_date)
        if type(self.issue_time) == str:
            self.issue_time = BasicGlobal.IssueTime(self.issue_time)
        if type(self.document_currency_code) == str:
            self.document_currency_code = BasicGlobal.DocumentCurrencyCode(
                self.document_currency_code)

    def validate(self, errs, obs):
        assert type(self.ubl_extensions) == BasicGlobal.UBLExtensions
        assert type(self.customization) == BasicGlobal.CustomizationID
        assert type(self.id) == BasicGlobal.SummaryId
        assert type(self.issue_date) == General.IssueDate
        assert self.issue_time is None or type(
            self.issue_time) == BasicGlobal.IssueTime
        assert type(
            self.discrepancy_response) == DiscrepancyResponse.DiscrepancyResponse
        assert type(self.billing_reference) == BillingReference.BillingReference
        assert type(
            self.document_currency_code) == BasicGlobal.DocumentCurrencyCode
        assert type(self.accounting_supplier_party) == AccountingSupplierParty
        assert type(self.tax_total) == TaxTotal
        assert type(self.legal_monetary_total) == LegalMonetaryTotal
        assert type(self.accounting_customer_party) == AccountingCustomerParty

    def generate_root(self):
        self.doc = default_document.createElement("CreditNote")
        self.doc.setAttribute(
            "xmlns", "urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2")
        self.doc.setAttribute(
            "xmlns:cac", "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2")
        self.doc.setAttribute(
            "xmlns:cbc", "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2")
        self.doc.setAttribute(
            "xmlns:ccts", "urn:un:unece:uncefact:documentation:2")
        self.doc.setAttribute("xmlns:ds", "http://www.w3.org/2000/09/xmldsig#")
        self.doc.setAttribute(
            "xmlns:ext", "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2")
        self.doc.setAttribute(
            "xmlns:qdt", "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2")
        self.doc.setAttribute("xmlns:sac",
                              "urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1")
        self.doc.setAttribute("xmlns:udt",
                              "urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2")
        self.doc.setAttribute(
            "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

    def generate_doc(self):
        self.generate_root()

        self.doc.appendChild(self.ubl_extensions.get_document())

        # Datos de la factura
        self.doc.appendChild(self.ubl_version.get_document())
        self.doc.appendChild(self.customization.get_document())
        self.doc.appendChild(self.id.get_document())

        # Fecha de Emisi??n
        self.doc.appendChild(self.issue_date.get_document())

        # Hora de Emisi??n
        if self.issue_time:
            self.doc.appendChild(self.issue_time.get_document())

        # Moneda
        self.doc.appendChild(self.document_currency_code.get_document())

        # Informacion adicional
        for note in self.notes:
            self.doc.appendChild(note.get_document())

            # Discrepancy Response
        self.doc.appendChild(self.discrepancy_response.get_document())

        # Billing reference
        self.doc.appendChild(self.billing_reference.get_document())

        # Datos de la firma
        if self.signature:
            self.doc.appendChild(self.signature.get_document())

        # Datos del emisor
        self.doc.appendChild(self.accounting_supplier_party.get_document())

        # Datos del receptor
        self.doc.appendChild(self.accounting_customer_party.get_document())

        # Total de Impuestos de la factura
        self.doc.appendChild(self.tax_total.get_document())

        self.doc.appendChild(self.legal_monetary_total.get_document())

        # Items de la factura
        for line in self.credit_note_lines:
            self.doc.appendChild(line.get_document())

    def get_document(self):
        self.fix_values()
        self.generate_doc()

        xml_doc = minidom.Document()
        xml_doc.appendChild(self.doc)
        return xml_doc


class DebitNote(Xmleable):
    def __init__(self, ubl_extensions=None, ubl_version="2.1", doc_id=None,
                 issue_date=None, issue_time=None, document_currency_code=None, customization="2.0",
                 discrepancy_response=None, billing_reference=None,
                 signature=None, accounting_supplier_party=None, accounting_customer_party=None,
                 tax_total=None, requested_monetary_total=None):

        self.credit_note_lines = []
        self.notes = []
        self.file_name = None

        self.ubl_extensions = ubl_extensions
        self.ubl_version = ubl_version
        self.customization = customization
        self.doc_id = doc_id
        self.issue_date = issue_date
        self.issue_time = issue_time
        self.document_currency_code = document_currency_code
        self.discrepancy_response = discrepancy_response
        self.billing_reference = billing_reference
        self.signature = signature
        self.accounting_supplier_party = accounting_supplier_party
        self.accounting_customer_party = accounting_customer_party
        self.tax_total = tax_total
        self.requested_monetary_total = requested_monetary_total

    def set_file_name(self, name):
        self.file_name = name

    def add_credit_note_line(self, credit_note_line):
        assert type(credit_note_line) == DebitNoteLine.DebitNoteLine
        self.credit_note_lines.append(credit_note_line)
        credit_note_line.ord = len(self.credit_note_lines)

    def add_note(self, note):
        if type(note) == str:
            note = BasicGlobal.Note(note)
        assert type(note) == BasicGlobal.Note
        self.notes.append(note)

    def fix_values(self):
        if not self.ubl_extensions:
            self.ubl_extensions = BasicGlobal.UBLExtensions()
        if type(self.ubl_version) == str:
            self.ubl_version = BasicGlobal.UBLVersion(self.ubl_version)
        if type(self.customization) == str:
            self.customization = BasicGlobal.CustomizationID(
                self.customization)
        if type(self.doc_id) == str:
            self.doc_id = BasicGlobal.ID(self.doc_id)
        if type(self.issue_date) == str:
            self.issue_date = General.IssueDate(self.issue_date)
        if type(self.issue_time) == str:
            self.issue_time = BasicGlobal.IssueTime(self.issue_time)
        if type(self.document_currency_code) == str:
            self.document_currency_code = BasicGlobal.DocumentCurrencyCode(
                self.document_currency_code)

    def validate(self, errs, obs):
        assert type(self.ubl_extensions) == BasicGlobal.UBLExtensions
        assert type(self.customization) == BasicGlobal.CustomizationID
        assert type(self.doc_id) == BasicGlobal.ID
        assert type(self.issue_date) == General.IssueDate
        assert self.issue_time is None or type(
            self.issue_time) == BasicGlobal.IssueTime
        assert type(
            self.discrepancy_response) == DiscrepancyResponse.DiscrepancyResponse
        assert type(self.billing_reference) == BillingReference.BillingReference
        assert type(
            self.document_currency_code) == BasicGlobal.DocumentCurrencyCode
        assert type(self.accounting_supplier_party) == AccountingSupplierParty
        assert type(self.tax_total) == TaxTotal
        assert type(self.requested_monetary_total) == RequestedMonetaryTotal
        assert type(self.accounting_customer_party) == AccountingCustomerParty

    def generate_root(self):
        self.doc = default_document.createElement("DebitNote")
        self.doc.setAttribute(
            "xmlns", "urn:oasis:names:specification:ubl:schema:xsd:DebitNote-2")
        self.doc.setAttribute(
            "xmlns:cac", "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2")
        self.doc.setAttribute(
            "xmlns:cbc", "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2")
        self.doc.setAttribute(
            "xmlns:ccts", "urn:un:unece:uncefact:documentation:2")
        self.doc.setAttribute("xmlns:ds", "http://www.w3.org/2000/09/xmldsig#")
        self.doc.setAttribute(
            "xmlns:ext", "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2")
        self.doc.setAttribute(
            "xmlns:qdt", "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2")
        self.doc.setAttribute(
            "xmlns:sac", "urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1")
        self.doc.setAttribute(
            "xmlns:udt", "urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2")
        self.doc.setAttribute(
            "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

    def generate_doc(self):
        self.generate_root()

        self.doc.appendChild(self.ubl_extensions.get_document())

        # Datos de la factura
        self.doc.appendChild(self.ubl_version.get_document())
        self.doc.appendChild(self.customization.get_document())
        self.doc.appendChild(self.doc_id.get_document())

        # Fecha de Emisi??n
        self.doc.appendChild(self.issue_date.get_document())

        # Hora de Emisi??n
        if self.issue_time:
            self.doc.appendChild(self.issue_time.get_document())

        # Moneda
        self.doc.appendChild(self.document_currency_code.get_document())

        # Informacion adicional
        for note in self.notes:
            self.doc.appendChild(note.get_document())

            # Discrepancy Response
        self.doc.appendChild(self.discrepancy_response.get_document())

        # Billing reference
        self.doc.appendChild(self.billing_reference.get_document())

        # Datos de la firma
        if self.signature:
            self.doc.appendChild(self.signature.get_document())

        # Datos del emisor
        self.doc.appendChild(self.accounting_supplier_party.get_document())

        # Datos del receptor
        self.doc.appendChild(self.accounting_customer_party.get_document())

        # Total de Impuestos de la factura
        self.doc.appendChild(self.tax_total.get_document())

        self.doc.appendChild(self.requested_monetary_total.get_document())

        # Items de la factura
        for line in self.credit_note_lines:
            self.doc.appendChild(line.get_document())

    def get_document(self):
        self.fix_values()
        self.generate_doc()

        xml_doc = minidom.Document()
        xml_doc.appendChild(self.doc)
        return xml_doc


class DespatchAdvice(Xmleable):
    def __init__(self, ubl_extensions=None, ubl_version="2.1", doc_id=None, customization="2.0",
                 issue_date=None, issue_time=None, despatch_advice_type_code=None,
                 order_reference=None, additional_document_reference=None, signature=None,
                 despatch_supplier_party=None, delivery_customer_party=None,
                 shipment=None, seller_supplier_party=None):

        self.guia_lines = []
        self.notes = []
        self.file_name = None

        self.ubl_extensions = ubl_extensions
        self.ubl_version = ubl_version
        self.customization = customization
        self.doc_id = doc_id
        self.issue_date = issue_date
        self.issue_time = issue_time
        self.despatch_advice_type_code = despatch_advice_type_code
        self.order_reference = order_reference
        self.additional_document_reference = additional_document_reference
        self.signature = signature
        self.despatch_supplier_party = despatch_supplier_party
        self.delivery_customer_party = delivery_customer_party
        self.seller_supplier_party = seller_supplier_party
        self.shipment = shipment

    def set_file_name(self, name):
        self.file_name = name

    def add_guia_line(self, credit_note_line):
        assert type(credit_note_line) == DespatchLine
        self.guia_lines.append(credit_note_line)
        credit_note_line.ord = len(self.guia_lines)

    def add_note(self, note):
        if type(note) == str:
            note = BasicGlobal.Note(note)
        assert type(note) == BasicGlobal.Note
        self.notes.append(note)

    def fix_values(self):
        if not self.ubl_extensions:
            self.ubl_extensions = BasicGlobal.UBLExtensions()
        if type(self.ubl_version) == str:
            self.ubl_version = BasicGlobal.UBLVersion(self.ubl_version)
        if type(self.customization) == str:
            self.customization = BasicGlobal.CustomizationID(
                self.customization)
        if type(self.doc_id) == str:
            self.doc_id = BasicGlobal.ID(self.doc_id)
        if type(self.issue_date) == str:
            self.issue_date = General.IssueDate(self.issue_date)
        if type(self.issue_time) == str:
            self.issue_time = BasicGlobal.IssueTime(self.issue_time)
        if type(self.despatch_advice_type_code) == str:
            self.despatch_advice_type_code = BasicGlobal.DespatchAdviceTypeCode(
                self.despatch_advice_type_code)

    def validate(self, errs, obs):
        assert type(self.ubl_extensions) == BasicGlobal.UBLExtensions
        assert type(self.customization) == BasicGlobal.CustomizationID
        assert type(self.doc_id) == BasicGlobal.ID
        assert type(self.issue_date) == General.IssueDate
        assert self.issue_time is None or type(
            self.issue_time) == BasicGlobal.IssueTime
        assert type(
            self.despatch_advice_type_code) is BasicGlobal.DespatchAdviceTypeCode
        assert self.order_reference is None or type(
            self.order_reference) == OrderReference
        assert self.additional_document_reference is None or \
            type(self.additional_document_reference) == AdditionalDocumentReference
        assert type(self.despatch_supplier_party) == DespatchSupplierParty
        assert type(self.delivery_customer_party) is DeliveryCustomerParty
        assert self.seller_supplier_party is None or type(
            self.seller_supplier_party) is SellerSupplierParty
        assert type(self.shipment) == Shipment

    def generate_root(self):
        self.doc = default_document.createElement("DespatchAdvice")
        self.doc.setAttribute(
            "xmlns", "urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2")
        self.doc.setAttribute(
            "xmlns:cac", "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2")
        self.doc.setAttribute(
            "xmlns:cbc", "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2")
        self.doc.setAttribute(
            "xmlns:ccts", "urn:un:unece:uncefact:documentation:2")
        self.doc.setAttribute("xmlns:ds", "http://www.w3.org/2000/09/xmldsig#")
        self.doc.setAttribute(
            "xmlns:ext", "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2")
        self.doc.setAttribute(
            "xmlns:qdt", "urn:oasis:names:specification:ubl:schema:xsd:QualifiedDatatypes-2")
        self.doc.setAttribute("xmlns:sac",
                              "urn:sunat:names:specification:ubl:peru:schema:xsd:SunatAggregateComponents-1")
        self.doc.setAttribute("xmlns:udt",
                              "urn:un:unece:uncefact:data:specification:UnqualifiedDataTypesSchemaModule:2")
        self.doc.setAttribute(
            "xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")

    def generate_doc(self):
        self.generate_root()

        self.doc.appendChild(self.ubl_extensions.get_document())

        # Datos de la guia
        self.doc.appendChild(self.ubl_version.get_document())
        self.doc.appendChild(self.customization.get_document())
        self.doc.appendChild(self.doc_id.get_document())

        # Fecha de Emisi??n
        self.doc.appendChild(self.issue_date.get_document())

        # Hora de Emisi??n
        if self.issue_time:
            self.doc.appendChild(self.issue_time.get_document())

        self.doc.appendChild(self.despatch_advice_type_code.get_document())

        # Informacion adicional
        for note in self.notes:
            self.doc.appendChild(note.get_document())

        if self.order_reference:
            self.doc.appendChild(self.order_reference.get_document())
        if self.additional_document_reference:
            self.doc.appendChild(
                self.additional_document_reference.get_document())

        # Datos de la firma
        if self.signature:
            self.doc.appendChild(self.signature.get_document())

        self.doc.appendChild(self.despatch_supplier_party.get_document())
        self.doc.appendChild(self.delivery_customer_party.get_document())
        if self.seller_supplier_party:
            self.doc.appendChild(self.seller_supplier_party.get_document())

        # Datos del envio
        self.doc.appendChild(self.shipment.get_document())

        # Items de la fguia
        for line in self.guia_lines:
            self.doc.appendChild(line.get_document())

    def get_document(self):
        self.fix_values()
        self.generate_doc()

        xml_doc = minidom.Document()
        xml_doc.appendChild(self.doc)
        return xml_doc
