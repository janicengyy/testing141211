# -*- coding: utf-8 -*-
import time
from openerp.osv import fields, osv
from openerp.tools.translate import _
import logging
_logger = logging.getLogger(__name__)

class pl_customer(osv.osv_memory):
    _name = "pl.customer"
    _description = "PL Report"
    def _get_users(self, cr, uid, ids, name, args, context=None):
        sql=""" select user_id from account_invoice GROUP BY user_id"""
        cr.execute(sql)
        lines=[]
        res3={}
        user_obj=self.pool.get('res.users')
        res2=cr.dictfetchall()
        
        for res in res2:
            name=user_obj.browse(cr, uid, res['user_id'], context=context)
            #lines.append((res['user_id'],name))
            res3[ids[0]]=res['user_id']
        return res3
    _columns = {
        'sale_id': fields.many2one('res.users', 'Sales Person'),
        'show': fields.boolean('Show Top100', ),
#        'year': fields.many2one('account.fiscalyear','Fiscal Year'),
        'year_id': fields.many2one('account.fiscalyear','Fiscal Year'),
        'sale_ids1': fields.function(_get_users, string=u"Sales Person", type='selection',selection=[('absent', 'Absent'), ('present', 'Present')],),
    }
    def show_sales(self, cr, uid, ids, context=None):
       # _logger.warning("ids================================================ %s =============", ids)
        datas={}
        sql=""" select user_id from account_invoice GROUP BY user_id"""
        cr.execute(sql)
        res2=cr.dictfetchall()
        for pl_obj in self.browse(cr, uid, ids, context=context):
            datas['year_id'] = pl_obj.year_id.id
            datas['show'] = pl_obj.show
            datas['sale_id'] = pl_obj.sale_id.id
        return {
            'type':'ir.actions.report.xml',
            'datas':datas,
            'report_name':'pl_customer_report',
        }

pl_customer()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
