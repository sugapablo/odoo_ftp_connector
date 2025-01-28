# -*- coding: utf-8 -*-
from io import StringIO
from odoo import models, fields, os
try:
    import pysftp
except ModuleNotFoundError:
    os.system("pip3 install pysftp")
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
    