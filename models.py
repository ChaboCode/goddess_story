from odoo import fields, models, api

class GoddessStory(models.Model):
    _name = "goddess_story"
    _description = 'Goddess Story Products Management'


    code = fields.Text(string='Code', compute='_compute_code', store=False)
    tier = fields.Selection([('1', '1 Yuan'),
                             ('2', '2 Yuan'),
                             ('5', '5 Yuan'),
                             ('10', '10 Yuan')], string='Yuan Tier',
                            required=True)
    set_num = fields.Integer(string='Set #')
    is_online = fields.Boolean(string='Is online?')

    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    price_per_box = fields.Monetary(string='Price per Box', required=True)
    price_per_pack = fields.Monetary(string='Price per Pack', required=True)

    @api.depends('tier', 'set_num')
    def _compute_code(self):
        for record in self:
            m_code = ""
            if not record.tier == '1':
                m_code = f'{record.tier}M-'
            record.code = f'NS-{m_code}{record.set_num:02}'
    
    @api.model
    def create(self, vals):
        record = super(GoddessStory, self).create(vals)
        record.create_product(vals)
        return record
    
    @api.model
    def create_product(self, pack):
        print(pack)
        packs_per_box = {'1':30, '2':30, '5':20, '10':18}[self.tier]
        box_product = self.env['product.template'].create({
            'name': f'{self.code} Box',
            'type': 'consu',
            'list_price': self.price_per_box,
            'uom_id': self.env.ref(f'goddess_story.uom_box_{packs_per_box}').id,
            'uom_po_id': self.env.ref(f'goddess_story.uom_box_{packs_per_box}').id,
            'sale_ok': True,
            'purchase_ok': True,
            'is_storable': True,
            'available_in_pos': True,
            'public_categ_ids': [fields.Command.set([self.env.ref('goddess_story.category_display').id])]
        })

        pack_product = self.env['product.template'].create({
            'name': f'{self.code} Pack',
            'type': 'consu',
            'list_price': self.price_per_pack,
            'uom_id': self.env.ref(f'goddess_story.uom_reference_pack').id,
            'uom_po_id': self.env.ref(f'goddess_story.uom_reference_pack').id,
            'sale_ok': True,
            'purchase_ok': True,
            'available_in_pos': True,
            'is_storable': True,

            # refer to :50
            'public_categ_ids': [fields.Command.set([self.env.ref('goddess_story.category_pack').id])]
        })

        self.env['mrp.bom'].create({
            'product_tmpl_id': box_product.id,
            'product_uom_id': box_product.uom_id.id,
            'type': 'phantom',
            'product_qty': 1,
            'bom_line_ids': [(0, 0, {
                'product_id': pack_product.product_variant_id.id,
                'product_qty': packs_per_box
            })]
        })


