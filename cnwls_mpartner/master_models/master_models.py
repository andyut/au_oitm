# -*- coding: utf-8 -*-


from odoo import models, fields, api 
from odoo.modules import get_modules, get_module_path
from odoo.exceptions import UserError
from datetime import datetime
import requests
import base64
import pyodbc 
import pytz
import os
import requests 

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

 
 
class CNWLS_MPARTNER_SALES(models.Model):
	_name 			= "cnwls.mpartner.sales"
	_description 	= "SAP Business Partner sales"
	name			= fields.Char("Sales")
	company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.company.id)
	slpcode 		= fields.Char("Sales Code")
	slpname			= fields.Char("Sales Short Name")
	slsempname 		= fields.Char("Sales Full Name")
	no_telp 		= fields.Char("No telp")
	email 			= fields.Char("Email")
	istatus 		= fields.Selection(string="Status", selection=[("update","Update"),("new","New"),("change","Change")], default="new")

class CNWLS_MPARTNER_NNM1(models.Model):
	_name 			= "cnwls.mpartner.nnm1"
	_description 	= "SAP Business Partner Series" 
	company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.company.id)
	name 			= fields.Char("Series ")
	series			= fields.Char("Series Code")

class CNWLS_MPARTNER_OCTG(models.Model):
	_name 			= "cnwls.mpartner.octg"
	_description 	= "SAP Business Partner termofpayment"
	company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.company.id)
	name			= fields.Char("octg ID")
	groupnum 		= fields.Char("Top Code")
	paymentname		= fields.Char("Top Name")
	extradays 		= fields.Integer("TOP Day(s)" , default=0) 
	istatus 		= fields.Selection(string="Status", selection=[("update","Update"),("new","New"),("change","Change")], default="new")


class CNWLS_MPARTNER_OCRG(models.Model):
	_name 			= "cnwls.mpartner.ocrg"
	_description 	= "SAP Business Partner Group"
	company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.company.id)
	name			= fields.Char("Group ID")
	groupcode 		= fields.Char("Group Code")
	groupname		= fields.Char("Group Short Name") 
	istatus 		= fields.Selection(string="Status", selection=[("update","Update"),("new","New"),("change","Change")], default="new")

	

class  CNWLS_MPARTNER_CUST0MER(models.Model):
	_name 			= "cnwls.mpartner.customer"
	_description 	= "SAP Partner Customer"
	company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.company.id)
	iseries 		= fields.Many2one("cnwls.mpartner.nnm1",string="Series", required=True)
	name 			= fields.Char("ID")
	cardcode 		= fields.Char("Customer Code")
	cardname 		= fields.Char("Customer Name", required=True)
	cardfname 		= fields.Char("Foreign Name")
	groupcode 		= fields.Many2one("cnwls.mpartner.ocrg",string="Group  ", required=True)
	salesperson		= fields.Many2one("cnwls.mpartner.sales",string="Sales Person", required=True)
	 
	itextstatus 	= fields.Html("Status Text")


	phone1			= fields.Char("Phone 1")
	phone2			= fields.Char("Phone 2")
	cellular		= fields.Char("Cellular")
	fax 			= fields.Char("Fax")
	email 			= fields.Char("Email")
	website			= fields.Char("Web Site")
	bpactive		= fields.Selection(string="Active",selection=[("A","Active"),("I","Inacive")],default="I")
## Divisi TAX

	npwp			= fields.Char("NPWP", required=True)
	npwpaddress		= fields.Char("NPWP Address", required=True)

	validremarks 	= fields.Char("Valid Remarks")
	frozenremarks	= fields.Char("Frozen Remarks")

## AUDIT
	nik 			= fields.Char("NIK")
	kartukeluarga	= fields.Char("Kartu Keluarga")
	siup			= fields.Char("SIUP")
	tdp 			= fields.Char("TDP")
	skd 			= fields.Char("SKD")
	akte			= fields.Char("Akte Pendirian")
	nib				= fields.Char("NIB")

	## DIVISI AR

	arperson 		= fields.Char("AR Person")
	tukarfaktur		= fields.Char("Catatan Tukar Faktur")
	creditlimit		= fields.Float("Credit Limit",digit=(19,2), default=5000000 )


	paymentgroup	= fields.Many2one("cnwls.mpartner.octg",string="Payment Group", required=True)
	lock_limit		= fields.Integer("Lock Timeout",defaut=2)
	notes 			= fields.Text("Notes")
	lockbp 			= fields.Char("Lock BP")


	istatus 		= fields.Selection(string="Status", selection=[("draft","Draft"),("new","New"),("update","Update"),("change","Change")], default="draft")
 

## relation
	crd1_ids 		= fields.One2many("cnwls.mpartner.customer.crd1","ocrd_id",string="Outlet",required=True)
	ocpr_ids 		= fields.One2many("cnwls.mpartner.customer.ocpr","ocrd_id",string="contact",required=True)
	resulttxt		= fields.Text("Debug")
	resulttxt2		= fields.Text("Debug2")

## SAP INTIDATA

	IDU_SpecialCustomer 	= fields.Char("IDU_SpecialCustomer")
	IDU_Sc_OpenInvoice 		= fields.Char("IDU_Sc_OpenInvoice")
	IDU_AktaTerakhir 		= fields.Char("IDU_AktaTerakhir")
	IDU_StatusTempatUsaha 	= fields.Char("IDU_StatusTempatUsaha")
	IDU_TanggalBerakhirSewa = fields.Date("IDU_TanggalBerakhirSewa")
	IDU_BasedOnTOP 			= fields.Char("IDU_BasedOnTOP") 
	

	@api.model
	def create(self,vals):
		vals["istatus"] ="new"
		return super(CNWLS_MPARTNER_CUST0MER,self).create(vals)
	 
	
	def update2SAP(self):

		#cardcode = self.cardcode if self.cardcode else ""

		self.itextstatus = "<b> <font color='green'> Updating ........ </font> </b>"

		phone1 = self.phone1 if self.phone1 else ""
		phone2 = self.phone2 if self.phone2 else ""
		MobilePhone = self.cellular if self.cellular else "" 
		Fax = self.fax if self.fax else "" 
		E_Mail = self.email if self.email else "" 
 
		outlet =[]
		if self.crd1_ids :
			for line in self.crd1_ids :
				outletline = {

							"AddressName" : line.name ,
							"AddressType" : line.itype ,
							"Street" : line.street  
				}
				outlet.append(outletline)
		contact =[]
		if self.ocpr_ids :
			for line in self.ocpr_ids :
				Position 		= line.position if line.position else ""
				Address 		= line.address if line.address else ""
				LinePhone1 			= line.tel1 if line.tel1 else ""
				linePhone2 			= line.tel2 if line.tel2 else ""
				LineMobilePhone 	= line.selular if line.selular else ""
				LineE_Mail 			= line.email if line.email else ""
				Remarks1 		= line.notes1 if line.notes1 else ""
				U_IGU_NoKTP 	= line.ktp if line.ktp else ""
				U_IGU_noNPWP 	= line.npwp if line.npwp else ""


				contactline = {
							"Name" 			: line.name ,
							"Position" 		: Position,
							"Address" 		: Address ,
							"Phone1" 		: LinePhone1  ,
							"Phone2" 		: linePhone2 ,
							"MobilePhone" 	: LineMobilePhone ,
							"Remarks1" 		: Remarks1  ,
							"E_Mail" 		: LineE_Mail ,
							"U_IGU_NoKTP" 	: U_IGU_NoKTP  ,
							"U_IGU_noNPWP"	: U_IGU_noNPWP
				}
				contact.append(contactline)

		## faktur pajak
	
		businesspartner = { 
							"CardName"			: self.cardname, 
							"GroupCode"			: self.groupcode.groupcode,
							"Address"			: self.npwpaddress,   
							"PayTermsGrpCode" 	: self.paymentgroup.groupnum,
							"CreditLimit" 		: self.creditlimit,
							"SalesPersonCode" 	: self.salesperson.slpcode,
							"Currency"			: "IDR", 
							"Phone1": phone1,
							"Phone2": phone2,
							"Cellular": MobilePhone,
							"EmailAddress": E_Mail, 

							"BPAddresses"		:outlet ,
							"ContactEmployees"	: contact }
		self.resulttxt2 = ""
		self.resulttxt = str(businesspartner)
		self.itextstatus = ""

# INIT SERVICES LAYER
		appSession 	= requests.Session()

		companyDB 	= self.env.user.company_id.db_name
		UserName 	= self.env.user.company_id.sapuser
		Password 	= self.env.user.company_id.sappassword

		url 		= self.env.user.company_id.sapsl

# SERVICES LAYER LOGIN		


		urllogin 	= url + "Login"
		print("LOGIN SL :")


		payload = { "CompanyDB" :companyDB,
					"UserName" : UserName ,
					"Password" : Password
					}
		#print(payload)
		response = appSession.post(urllogin, json=payload,verify=False)

		#print(response.text)


# SERVICES LAYER PATCH 
		urlBP	=	url + "BusinessPartners('" + self.cardcode + "')"

		headers= {"B1S-ReplaceCollectionsOnPatch":"true"}
		response = appSession.patch(urlBP, json=businesspartner,verify=False,headers=headers)
		
		if response.status_code >=400:
			errmsg = str(response.json() ) + "\n" + urlBP

			raise UserError("Error : " + errmsg) 
		else :
			self.resulttxt2  = str(response.status_code) + " " + urlBP
			self.istatus = "update"

		 

		urllogout =  url + "Logout"
		response = appSession.post(urllogout,verify=False)     

		self.itextstatus = ""		


	def create2SAP(self):
		
		self.itextstatus = "<b> <font color='green'> CREATING SAP OBJECT ........ </font> </b>"
		cardcode = self.cardcode if self.cardcode else ""

		if cardcode =="" :
			sap = "new"
		else :
			sap = "update"

		outlet =[]
		if self.crd1_ids :
			for line in self.crd1_ids :
				outletline = {

							"AddressName" : line.name ,
							"AddressType" : line.itype ,
							"Street" : line.street  
				}
				outlet.append(outletline)
		contact =[]
		if self.ocpr_ids :
			for line in self.ocpr_ids :
				Position 	= line.position if line.position else ""
				Address 	= line.address if line.address else ""
				Phone1 		= line.tel1 if line.tel1 else ""
				Phone2 		= line.tel2 if line.tel2 else ""
				MobilePhone = line.selular if line.selular else ""
				E_Mail 		= line.email if line.email else ""
				Remarks1 	= line.notes1 if line.notes1 else ""
				U_IGU_NoKTP 	= line.ktp if line.ktp else ""
				U_IGU_noNPWP 	= line.npwp if line.npwp else ""


				contactline = {
							"Name" 			: line.name ,
							"Position" 		: Position,
							"Address" 		: Address ,
							"Phone1" 		: Phone1  ,
							"Phone2" 		:Phone2 ,
							"MobilePhone" 	: MobilePhone ,
							"Remarks1" 		: Remarks1  ,
							"E_Mail" 		: E_Mail ,
							"U_IGU_NoKTP" 	: U_IGU_NoKTP 
				}
				contact.append(contactline)

# parameter header 
		phone1 			= self.phone1 if self.phone1 else ""
		phone2 			= self.phone2 if self.phone2 else ""
		cellular 		= self.cellular if self.cellular else ""
		fax 			= self.fax if self.fax else ""
		email 			= self.email if self.email else ""
		website 		= self.website if self.website else ""
		npwp 			= self.npwp if self.npwp else ""
		npwpaddress		= self.npwpaddress if self.npwpaddress else ""

		nik 			= self.nik if self.nik else ""
		kartukeluarga	= self.kartukeluarga if self.kartukeluarga else ""
		siup 			= self.siup if self.siup else ""
		tdp 			= self.tdp if self.tdp else ""
		skd 			= self.skd if self.skd else ""
		akte 			= self.akte if self.akte else ""
		nib 			= self.nib if self.nib else ""

## ar dept 
		arperson 		= self.arperson if self.arperson else ""
		tukarfaktur 	= self.tukarfaktur if self.tukarfaktur else ""
		notes 			= self.notes if self.notes else ""
		lockbp 			= self.lockbp if self.lockbp else ""
		validremarks 	= self.validremarks if self.validremarks else ""
		frozenremarks	= self.frozenremarks if self.frozenremarks else ""

## SAP WEB Intidata


		if self.bpactive =="A" :
			Valid = "tNO"
			Frozen = "tYES"
		else:
			Valid = "tYES"
			Frozen = "tNO"

# end of paramater header 
		businesspartner = { 
							"CardName"		: self.cardname,
							"CardType"		: "cCustomer",
							"GroupCode"		: self.groupcode.groupcode,
							"Address"		: self.npwpaddress,   
							"PayTermsGrpCode" 	: self.paymentgroup.groupnum,
							"CreditLimit" 		: self.creditlimit,
							"SalesPersonCode" 	: self.salesperson.slpcode,
							"Currency"		: "IDR",
							"Series"		: self.iseries.series ,
							"BPAddresses"	: outlet ,
							"ContactEmployees"	: contact

						}
		
		self.resulttxt = str(businesspartner)


# INIT SERVICES LAYER
		appSession 	= requests.Session()
		companyDB 	= self.env.user.company_id.db_name
		UserName 	= self.env.user.company_id.sapuser
		Password 	= self.env.user.company_id.sappassword

		url 		= self.env.user.company_id.sapsl

# SERVICES LAYER LOGIN		


		urllogin 	= url + "Login"
		print("LOGIN SL :")


		payload = { "CompanyDB" :companyDB,
					"UserName" 	: UserName ,
					"Password" 	: Password
					}
		#print(payload)
		response = appSession.post(urllogin, json=payload,verify=False)

		#print(response.text)


# SERVICES LAYER PATCH 
		urlBP	=	url + "BusinessPartners"

		headers= {"B1S-ReplaceCollectionsOnPatch":"true"}
		response = appSession.post(urlBP, json=businesspartner,verify=False,headers=headers)
		
		if response.status_code >=400:
			errmsg = str(response.json() )
			raise UserError("Error : " + errmsg)
		else :
			dataresult = response.json()
			self.cardcode = dataresult["CardCode"]
			self.resulttxt2 = str(dataresult)
			self.istatus = "update"

		 

		urllogout 	=  url + "Logout"
		response 	= appSession.post(urllogout,verify=False)     
		self.itextstatus = ""



class  CNWLS_MPARTNER_CUST0MER_CRD1(models.Model):
	_name 			= "cnwls.mpartner.customer.crd1"
	_description 	= "SAP Partner Customer Outlet"
	_order          = "company_id,itype,name" 
	company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.company.id)

	name 			= fields.Char("Outlet")
	outlet			= fields.Char("Outlet Name")
	itype 			= fields.Selection(string="Type", selection=[("bo_ShipTo","Ship To"),("bo_BillTo","Bill To")],default="bo_ShipTo")

	street			= fields.Char("Street")
	billarea		= fields.Char("Bill Area")
	rownum 			= fields.Integer("RowNum",default=0)
	ocrd_id 		= fields.Many2one("cnwls.mpartner.customer",ondelete="cascade")


class  CNWLS_MPARTNER_CUST0MER_OCPR(models.Model):
	_name 			= "cnwls.mpartner.customer.ocpr"
	_description 	= "SAP Partner Customer Contact"
	company_id      = fields.Many2one('res.company', 'Company', required=True, index=True,  default=lambda self: self.env.company.id)

	name 			= fields.Char("Contact name",required=True)
	cardcode		= fields.Char("Cardcode")
	contactcode		= fields.Integer("Contact ID")
	position 		= fields.Char("Position")
	address 		= fields.Char("Address",required=True)
	tel1 			= fields.Char("Tel 1")
	tel2 			= fields.Char("Tel 2")
	selular 		= fields.Char("Selular")
	email 			= fields.Char("email")
	notes1 			= fields.Char("Remarks 1")
	notes2 			= fields.Char("Remarks 2")
	profession		= fields.Char("Profession")
	cityofbirth		= fields.Char("City of Birth")
	ktp 			= fields.Char("ktp")
	npwp 			= fields.Char("npwp")
	internalcode	= fields.Integer("InternalCode",default=0)
	ocrd_id 		= fields.Many2one("cnwls.mpartner.customer",ondelete="cascade")
 