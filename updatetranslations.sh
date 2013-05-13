#!/bin/sh

## policy
bin/i18ndude rebuild-pot --pot src/policy/policy/locales/policy.pot --create policy src/policy/policy
bin/i18ndude sync --pot src/policy/policy/locales/policy.pot src/policy/policy/locales/*/LC_MESSAGES/policy.po
