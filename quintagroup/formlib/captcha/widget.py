from Products.statusmessages.interfaces import IStatusMessage

import urllib2
import urllib
import simplejson as json
try:
    from zope.site.hooks import getSite
    getSite()
except ImportError:
    from zope.app.component.hooks import getSite
from zope.app.form.browser import ASCIIWidget
from zope.app.form.interfaces import ConversionError

from zope.i18n import MessageFactory

from Acquisition import aq_parent


from Products.CMFCore.interfaces import ISiteRoot

from quintagroup.captcha.core.utils import detectInlineValidation

try:
    from plone.app.form import inline_validation
except ImportError:
    # BBB Plone < 4.3 compatibility.
    # The implementation of inline validation was switched
    # to a non-KSS-based in plone.app.form-2.2.0
    try:
        from plone.app.form.kss import validation as inline_validation
    # BBB: Plone 3.0 compatibility.
    # The KSS validation was added in plone.app.form-1.1.0.
    except:
        inline_validation = None

_ = MessageFactory('quintagroup.formlib.captcha')

import logging

logger = logging.getLogger('quintagroup.formlib.captcha')


class CaptchaWidget(ASCIIWidget):

    def get_site(self):
        # get from plone.app.form.widgets.wysiwygwdget
        site = getSite()
        while site is not None and not ISiteRoot.providedBy(site):
            site = aq_parent(site)
        return site

    def __call__(self):
        sitekey = self.get_site().getProperty('RECAPTCHA_SITEKEY')
        lang = self.request.LANGUAGE
        form = """<script src="https://www.google.com/recaptcha/api.js?hl=%s"></script>
        <div class="g-recaptcha" data-sitekey="%s"></div>""" % (lang, sitekey)
        return form

    def hasInput(self):
        # The validator looks for the captcha only if the captcha field
        # is present. If the captcha field is omitted from the request,
        # then the captcha validation never happens. That's why 'required'
        # option is useless. So, we have to simulate 'required': set up 'True'
        # for the captcha input.
        return True

    def _getFormInput(self):
        """ It returns current form input. """
        # The original method isn't suitable when the captcha field
        # is omitted from the request.
        return self.request.get(self.name, u'')

    def _toFieldValue(self, input):
        # Captcha validation is one-time process to prevent hacking
        # This is the reason for in-line validation to be disabled.
        if inline_validation and detectInlineValidation(inline_validation):
            return super(CaptchaWidget, self)._toFieldValue(input)

        # Verify the user input against the captcha.
        # Get captcha type (static or dynamic)
        google_dict = {'secret': self.get_site().getProperty('RECAPTCHA_SECRET')}
        google_dict['response'] = self.request.form['g-recaptcha-response']
        #  google_dict['remoteip'] = self.request.environ["HTTP_X_FORWARDED_FOR"]
        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = urllib.urlencode(google_dict)
        req = urllib2.Request(url, data)
        recaptcha_value = urllib2.urlopen(req)
        json_result = json.loads(recaptcha_value.read())

        if not json_result['success']:
            message = _('Invalid captcha value')
            return ConversionError(message)

        return 'ok'
