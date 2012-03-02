SignupSheet
===========

SignupSheet is an add-on product that allows site managers to create **custom
registration forms for events, workshops, fundraisers** and other events that
require **online registration**.  Each SignupSheet defines the fields that are used
for each *Registrant* object they contain, through the ATSchemaEditorNG product.
The Registrant object is what the end user fills out and submits.  The workflow
places each submitted Registrant in a private state once it is submitted so
that it can be reviewed and approved.

The SignupSheet has these additional features:
 
- Registrant fields can be exported to CSV
- A waiting list and event size can be set, end users are emailed a message
  stating whether they are pending approval or on the waiting list.  
- The signup sheet view indicates whether the SignupSheet is 'full', 'open' or
  whether user will be put on a  waiting list. This is calculated using the
  event size and waiting list settings.
- End user is directed to a customizable thank you page.
  
The key motivation behind this product is to provides a way for site managers
to setup registration forms that do more than email the fields to an address.
Having the fields be configurable is essential, since many groups have specific
requirements for the data they are collecting for their events.

Authenticated user
------------------

If you plan to give to authenticated users a way to subscribe to events,
SignupSheet try to fill automatically some registration data from the user's
data.

Know that if you keep all default fields ("*First name*", "*Last name*" and
"*E-mail*"), they are filled automatically taking the same fields from the
user.

As Plone commonly use a single "*Fullname*" info, while SignupSheet split it
to first and last name, the procedure try to split your fullname in two.

If your fullname policy is to keep last, then first name in that order, you
can change the same order modifiying the ``first_last_name_order`` property
in the product's ZMI properties sheet.

License
=======
    
SignupSheet is released under the GNU General Public Licence, version 2.
Please see http://gnu.org for more details.

Installation
============
  
- Install in the usual way, using the QuickInstaller
- Requires ATSchemaEditorNG 0.6 or greater
- Requires TemplateFields and TALESField
- Tested with Plone 3.3.5 and Archetypes 1.6.15 and ATSchemaEditorNG 0.6
        
Acknowlegements
===============

- This product would not be possible without the Poi and RichDocument
  products by Martin Aspeli.  They provided useful example code, specifically
  around the workflow trigger pattern.  
- In addition Upfront Contacts by Roche Compaan for the CSV export code.  
- In addition thanks to Simon Pamies for assisting me with ATSchemaEditorNG, and
  Andreas Jung for providing useful code improvements.  
- Naro for the Plone 3 compatibility work
- Andres Jung for eggifying SignupSheet

PloneGov
--------

Those sponsored the product inside the `PloneGov`__ initiative.

__ http://www.plonegov.it/

- `Camera di Commercio di Ferrara`__ sponsored some i18n fixes
- `S. Anna Hospital, Ferrara`__ sponsored the workflows and roles update

__ http://www.fe.camcom.it/
__ http://www.ospfe.it/

Known Issues and Potential Improvements
=======================================
    
- Signupsheet needs more explanatory text.  Schema editor has been simplified
  but needs better explanatory text.
- It is possible to prematurely fill up registration by malicious user.
  Subscriptions are no more saved (and a portal status message is displayed),
  but confirmation e-mail are sent.
- At release time, the last ATSchemaEditorNG available version was the `0.6.0`__.
  Using this version you will have some problems with signup sheet validation
  (see ticket `#26`__ for the fix)
- If you are using this behind `Varnish`__ or other reverse-proxy, you can experience
  privacy problems. Please configure you environment to not cache URL with
  ``thank_you_message``, or enable the ``traverse_to_thankyou`` flag in the
  ``signupsheet_properties`` sheet.

__ http://pypi.python.org/pypi/Products.ATSchemaEditorNG/0.6
__ http://plone.org/products/atseng/issues/26/
__ http://www.varnish-cache.org/

Authors
=======

Aaron VanDerlip (avanderlip AT gmail dot com) and others
