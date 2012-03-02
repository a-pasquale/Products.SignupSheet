# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Aaron VanDerlip <avanderlip@gmail.com>"""
__docformat__ = 'plaintext'


# Workflow Scripts for: signupsheet_registrant_workflow

def sendInitialEmail(self, state_change, **kw):
    obj = state_change.object
    if not obj.getEventsize() or obj.getSeatsLeft()>0:
        state_change.object.sendNotificationMail()
