# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase
from odoo.tests import tagged, Form
from odoo.tests.common import TransactionCase, Form
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError


class TestPurchase(TransactionCase):
    def test_purchase_delivery_status_partial_no_backorder(self):
        print('test_purchase_delivery_status_partial_no_backorder.....')
        po = Form(self.env['purchase.order'])
        partner = self.env['res.partner'].browse(1)
        product_a = self.env['product.product'].search([('detailed_type', '=', 'product')])[0]
        po.partner_id = partner
        with po.order_line.new() as po_line:
            po_line.product_id = product_a
            po_line.product_qty = 20
            po_line.price_unit = 100
        po = po.save()
        po.button_confirm()
        print('po..........', po)
        po.picking_ids[0].move_ids[0].quantity_done = 10
        po.picking_ids[0].button_validate()

        backorder = self.env['stock.backorder.confirmation'].create({'pick_ids': po.picking_ids})
        backorder.with_context(button_validate_picking_ids=po.picking_ids.ids).process_cancel_backorder()
        if po.delivery_status == 'partial_no_backorder':
            print('PARTIAL WITH NO BACKORDER SUCCESS')
        else:
            print('PARTIAL WITH NO BACKORDER FAILED')
            raise UserError(_('PARTIAL WITH NO BACKORDER FAILED'))

    def test_purchase_delivery_status_partial(self):
        print('test_purchase_delivery_status_partial........')
        po = Form(self.env['purchase.order'])
        partner = self.env['res.partner'].browse(1)
        product_a = self.env['product.product'].search([('detailed_type', '=', 'product')])[0]
        po.partner_id = partner
        with po.order_line.new() as po_line:
            po_line.product_id = product_a
            po_line.product_qty = 20
            po_line.price_unit = 100
        po = po.save()
        po.button_confirm()
        print('po..........', po)
        po.picking_ids[0].move_ids[0].quantity_done = 10
        po.picking_ids[0].button_validate()

        backorder = self.env['stock.backorder.confirmation'].create({'pick_ids': po.picking_ids})
        backorder_lines = self.env['stock.backorder.confirmation.line'].create(
            {'backorder_confirmation_id': backorder.id, 'picking_id': po.picking_ids[0].id, 'to_backorder': True})
        backorder.with_context(button_validate_picking_ids=po.picking_ids.ids).process()
        if po.delivery_status == 'partial':
            print('PARTIAL SUCCESS')
        else:
            print('PARTIAL STATUS BACKORDER FAILED')
            raise UserError(_('PARTIAL STATUS BACKORDER FAILED'))

    def test_purchase_delivery_status_nothing(self):
        print('test_purchase_delivery_status_nothing.........')
        po = Form(self.env['purchase.order'])
        partner = self.env['res.partner'].browse(1)
        po.partner_id = partner
        po = po.save()
        po.button_confirm()
        if not po.picking_ids and not po.order_line.filtered(lambda x: x.product_id.type == 'service'):

            if po.delivery_status == 'nothing':
                print('Nothing to Receive Success')
            else:
                print('Nothing to Receive Failed')
                raise UserError(_('Nothing to Receive  FAILED'))

    def test_purchase_delivery_status_receive(self):
        print('test_purchase_delivery_status_receive.........')
        po = Form(self.env['purchase.order'])
        partner = self.env['res.partner'].browse(1)
        product_a = self.env['product.product'].search([('detailed_type', '=', 'product')])[0]
        po.partner_id = partner
        with po.order_line.new() as po_line:
            po_line.product_id = product_a
            po_line.product_qty = 20
            po_line.price_unit = 100
        po = po.save()
        po.button_confirm()
        print('po..........', po)
        po.picking_ids[0].move_ids[0].quantity_done = 20
        po.picking_ids[0].button_validate()
        if all(o.qty_received == o.product_qty for o in po.order_line):
            if po.delivery_status == 'received':
                print('Received Success')
            else:
                print('Received Failed')
                raise UserError(_('Received  FAILED'))

    # def test_purchase_delivery_status_processing(self):
    #     print('test_purchase_delivery_status_processing.........')
    #     po = Form(self.env['purchase.order'])
    #     partner = self.env['res.partner'].browse(1)
    #     product_a = self.env['product.product'].search([('detailed_type', '=', 'product')])[0]
    #     po.partner_id = partner
    #     with po.order_line.new() as po_line:
    #         po_line.product_id = product_a
    #         po_line.product_qty = 20
    #         po_line.price_unit = 100
    #     po = po.save()
    #     po.button_confirm()
    #     print('po..........', po)
    #     po.picking_ids[0].move_ids[0].quantity_done = 10
    #     po.picking_ids[0].state = 'waiting'
    #     print('STATE....',po.picking_ids[0].state)
    #     if any(p.state in ('waiting', 'confirmed') for p in po.picking_ids):
    #         if po.delivery_status == 'processing':
    #             print('Processing Success')
    #         else:
    #             print('Processing Failed')
    #             raise UserError(_('Processing  FAILED'))

    def test_purchase_delivery_status_to_receive(self):
        print('test_purchase_delivery_status_receive.........')
        po = Form(self.env['purchase.order'])
        partner = self.env['res.partner'].browse(1)
        product_a = self.env['product.product'].search([('detailed_type', '=', 'product')])[0]
        po.partner_id = partner
        with po.order_line.new() as po_line:
            po_line.product_id = product_a
            po_line.product_qty = 20
            po_line.price_unit = 100
        po = po.save()
        po.button_confirm()
        print('po..........', po)
        po.picking_ids[0].move_ids[0].quantity_done = 10
        if all(o.qty_received == 0 for o in po.order_line):
            po.delivery_status = 'to_receive'
            if po.delivery_status == 'to_receive':
                print('To Receive Success')
            else:
                print('To Receive Failed')
                raise UserError(_('To Receive  FAILED'))
