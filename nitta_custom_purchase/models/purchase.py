from odoo import api, fields, models, _


class NittaPurchaseOrder1(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('draft_po', 'Draft PO'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def button_draft_po(self):
        self.ensure_one()
        # if self.order_sequence:
        #     raise UserError(_("Only quotation can convert to order"))
        purchase_order = self.copy(self._prepare_order_from_rfq())
        purchase_order.order_sequence = True
        purchase_order.button_confirm()
        # Reference from this RFQ to Purchase Order
        self.purchase_order_id = purchase_order.id
        self.purchase_order_id.quote_id.state = 'done'
        purchase_order.state = 'draft_po'
        if self.state == "draft":
            self.button_done()
        return self.with_context(order_sequence=True).open_duplicated_purchase_order()

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft_po']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True
