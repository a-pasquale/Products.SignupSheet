#!/bin/sh

i18ndude rebuild-pot --pot signupsheet.pot --create signupsheet --merge manual.pot ..
i18ndude sync --pot signupsheet.pot signupsheet-??.po
