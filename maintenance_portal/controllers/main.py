import odoo, logging
from odoo import http, models, fields, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
logger = logging.getLogger(__name__)


class CustomerPortal(CustomerPortal):
    
    def _prepare_portal_layout_values(self):
        values = super(CustomerPortal, self)._prepare_portal_layout_values()
        values['equipment_count'] = 0#request.env['project.project'].search_count([])
        values['request_count'] = 0#request.env['project.task'].search_count([])
        return values
        
    @http.route(['/my/maintenance', '/my/maintenance/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_projects(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Requests = request.env['maintenance.request']
        
        domain = [('user_id', '=', request.env.user.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'due_date': {'label': _('Due Date'), 'order': 'schedule_date'},
        }
        if not sortby:
            sortby = 'due_date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        
        # request count
        request_count = Requests.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/maintenance",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=request_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        requests = Requests.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'requests': requests,
            'page_name': 'requests',
            
            'default_url': '/my/maintenance',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("maintenance_portal.my_requests", values)
        
    # @http.route(['/my/project/<int:project_id>'], type='http', auth="public", website=True)
    # def portal_my_project(self, project_id=None, access_token=None, **kw):
    #     try:
    #         project_sudo = self._document_check_access('project.project', project_id, access_token)
    #     except (AccessError, MissingError):
    #         return request.redirect('/my')

    #     values = self._project_get_page_view_values(project_sudo, access_token, **kw)
    #     return request.render("project.portal_my_project", values)
    
    @http.route(['/maintenance/loc/','/maintenance/loc/<model("stock.location"):stock_location>'], type='http', auth="public", website=True)
    def portal_my_projects(self, page=1, date_begin=None, date_end=None, sortby=None, stock_location=None, **kw):
        values = self._prepare_portal_layout_values()
        Requests = request.env['maintenance.request']
        
        domain = [('user_id', '=', request.env.user.id)]

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'due_date': {'label': _('Due Date'), 'order': 'schedule_date'},
        }
        if not sortby:
            sortby = 'due_date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
        
        # request count
        request_count = Requests.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/maintenance",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=request_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        requests = Requests.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'requests': requests,
            'page_name': 'requests',
            'stock_location': stock_location,
            'default_url': '/my/maintenance',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("maintenance_portal.maintenance_location", values)