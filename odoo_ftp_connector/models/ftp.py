# -*- coding: utf-8 -*-
from io import StringIO
import time
from odoo import models, fields, os, _
try:
    import pysftp
except ModuleNotFoundError:
    os.system("pip3 install pysftp")
    time.sleep(20)
    import pysftp
from pysftp import CnOpts

class OdooFtpServers(models.Model):
    """
    Custom model for handling FTP servers
    """
    _name = 'odoo_ftp_connector.ftp_servers'
    _description = "FTP servers."

    name = fields.Char()
    company_id = fields.Many2one('res.company')
    ftp_server = fields.Char('FTP Server')
    ftp_login = fields.Char('FTP Login')
    ftp_password = fields.Char('FTP Password')
    ftp_port = fields.Integer('FTP Port')
    ftp_path = fields.Char('FTP Path')

    def message(self,title,message,type="success"):
        """
        Display message
        """
        return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': title,
                    'message': message,
                    'type': type,
                    'sticky': False,
                }
            }
    
    def test_connection(self):
        """
        Send string to FTP
        """
        cnopts = CnOpts()
        cnopts.hostkeys = None
        server = self.env.context.get('server')
        ftp = self.env['odoo_ftp_connector.ftp_servers'].search([('id','=',server)],limit=1)
        for rec in ftp:
            try:
                sftp = pysftp.Connection(host=rec.ftp_server,
                            username=rec.ftp_login,
                            password=rec.ftp_password,
                            port=rec.ftp_port,
                            cnopts=cnopts)
                title = _("Success")
                message = _("SFTP Connection valid.")
                return self.message(title,message)
                
            except Exception as e:
                title = _("Failed")
                message = _(str(e))
                return self.message(title,message,'danger')
                
        title = _("Failed")
        message = _("No FTP information found.")
        return self.message(title,message,'warning')
                
       

    def ftp_send_string(self,server,filename,string):
        """
        Send string to FTP
        """
        cnopts = CnOpts()
        cnopts.hostkeys = None
        ftp = self.env['odoo_ftp_connector.ftp_servers'].search([('id','=',server)],limit=1)
        for rec in ftp:
            with pysftp.Connection(host=rec.ftp_server,
                            username=rec.ftp_login,
                            password=rec.ftp_password,
                            port=rec.ftp_port,
                            cnopts=cnopts) as sftp:
                sftp.putfo(StringIO(string),
                    rec.ftp_path + '/' + filename)
                
        return True
    
    def ftp_download_file(self, server, filename, local_path):
        """
        Download file from FTP server
        """
        cnopts = CnOpts()
        cnopts.hostkeys = None
        ftp = self.env['odoo_ftp_connector.ftp_servers'].search([('id','=',server)],limit=1)
        for rec in ftp:
            with pysftp.Connection(host=rec.ftp_server,
                            username=rec.ftp_login,
                            password=rec.ftp_password,
                            port=rec.ftp_port,
                            cnopts=cnopts) as sftp:
                sftp.get(rec.ftp_path + '/' + filename, local_path + filename)
                
        return True