from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


    
class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    
    interval_count = fields.Integer('Cycle Count', default=0)
    interval_number = fields.Integer('Interval Number', default=0)
    interval_type = fields.Selection(selection='_get_interval_types', string='Interval Unit', default='none')
    next_interval_date = fields.Datetime('Next Create Date')
    pre_interval_number = fields.Integer('Pre-Interval Number', default=0)
    pre_interval_type = fields.Selection(selection=[('hours','Hours'),('days','Days'),('weeks','Weeks'),('months','Months')], string='Pre-Interval Unit', default='hours')

    def write(self, vals):
        if vals.get('stage_id'):
            #this request is now closed, check scheduler if we open a new request
            if self.env['maintenance.stage'].browse(vals.get('stage_id')).done:
                self._onchange_interval_type()
                
        #         #OK! lets make a new request copied from self
        #         new_request = self.copy_data()[0]
        #         new_request['request_date'] = fields.Date.today()
        #         nextcall = datetime.now()
        #         nextcall = self.compute_interval(nextcall, self.interval_type, self.interval_number)
                
        #         new_request['schedule_date'] = nextcall
        #         new_request['source_request_id'] = self.id
        #         new_request['stage_id'] = self._default_stage().id
        #         if self.interval_count > 0:
        #             new_request['interval_count'] = self.interval_count - 1
        #         self.next_request_id = self.create(new_request)
                    
        return super(MaintenanceRequest, self).write(vals)
        
    def compute_interval(self, base_date, interval_type, interval_number):
        intervalTypes = {
            
            'work_days': lambda interval: relativedelta(days=interval),
            'days': lambda interval: relativedelta(days=interval),
            'hours': lambda interval: relativedelta(hours=interval),
            'weeks': lambda interval: relativedelta(days=7*interval),
            'months': lambda interval: relativedelta(months=interval),
            'minutes': lambda interval: relativedelta(minutes=interval),
            'years' : lambda interval: relativedelta(years=interval),
            }
            
        return base_date + intervalTypes[interval_type](interval_number)
        
    def _get_interval_types(self):
        types = []
        types.append(('none', 'None'))
        types.append(('minutes', 'Minutes'))
        types.append(('hours', 'Hours'))
        types.append(('days', 'Days'))
         #types.append(('work_days', 'Work Days'))
        types.append(('weeks', 'Weeks'))
        types.append(('months', 'Months'))
        types.append(('years', 'Years'))
        return types
    
    @api.onchange('interval_type','interval_number','interval_count','pre_interval_type','pre_interval_number')
    def _onchange_interval_type(self, from_date=datetime.now()):
        
        if self.interval_type != 'none':
            base_interval_date = self.compute_interval(from_date, self.interval_type, self.interval_number)
            pre_interval = self.compute_interval(base_interval_date, self.pre_interval_type, self.pre_interval_number * -1)
            self.next_interval_date = pre_interval
        
        #if interval count is zero the schedule is dead, -1 to continue forever
        if self.interval_count == 0 or self.interval_type == 'none':
            self.next_interval_date=False
        
    @api.model
    def _cron_generate_requests(self):
        #find requests that are ready to generate
        requests = self.search([('next_interval_date',"<=", datetime.now())])
        
        for request in requests:
            #grab the data from this request, to build the new request
            new_data = request.copy_data()[0]
            new_data['request_date'] = request.compute_interval(datetime.now(), request.interval_type, request.interval_number)
            new_data['schedule_date'] = new_data['request_date']
            new_data['close_date'] = False
            new_data['next_interval_date'] = False
            new_data['stage_id'] = request._default_stage().id
            if request.interval_count > 0:
                new_data['interval_count'] = request.interval_count - 1
            
            #create the new request
            new_request = self.create(new_data)
            
            #if the new request is created, blank out this requests next interval
            if len(new_request) > 0:
                request.next_interval_date = False
            
            
        return True