Introduction
============

quintagroup.formlib.captcha is a package that allows to add captcha to zope.formlib.
As a result such forms are prevented from automatic submit.

Get a Recaptcha key
-------------------

Go to `Google Recaptcha`_ and register a new key.

To to your portal and add 2 new properties with the following names, and enter there
the keys obtained from Google Recaptcha site: RECAPTCHA_SITEKEY and RECAPTCHA_SECRET.


Captchas in a formlib form
--------------------------

Using quintagroup.formlib.captcha in a formlib form is simple. Just add a
Captcha field to your schema, and away you go:

  >>> from zope.interface import Interface
  >>> from quintagroup.formlib.captcha import Captcha
  >>> class CaptchaSchema(Interface):
  ...     captcha = Captcha(
  ...         title=_(u'Type the code'),
  ...         description=_(u'Type the code from the picture shown below.'))

and formlib will take care of the rest. The widget associated with this field 
will render the captcha and verify the use input automatically.

Supported Plone versions
------------------------

quintagroup.formlib.captcha was tested with Plone 3.x and Plone 4.x.



Authors
-------

* Vitaliy Podoba
* Andriy Mylenkyi
* Vitaliy Stepanov
* Mikel Larreategi

Copyright (c) "Quintagroup": http://quintagroup.com, 2004-2017

.. _`Google Recaptcha`_: https://www.google.com/recaptcha/admin
