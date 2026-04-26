# -*- coding: utf-8 -*-
{
    'name': "Indoguna (SAP LS)- Business partner ",

    'summary': """
       Indoguna (SAP LS)- Business partner""",

    'description': """
       Indoguna (SAP LS)- Business partner
    """,

    'author': "Indoguna Group, Andy Utomo",
    'website': "http://www.indoguna.com",

 
    'category': 'others',
    'version': '0.1', 
    'application':True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'master_views/mpartner_customer_views.xml',    
        'master_views/mpartner_nnm1_views.xml',    
        'master_views/mpartner_ocrg_views.xml',    
        'master_views/mpartner_octg_views.xml',    
        'master_views/mpartner_sales_views.xml',   
        'security/user_groups.xml',    
        'menu/menu.xml', 
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}