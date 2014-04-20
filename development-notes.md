### Contributing ###

I'm happy to receive patches to Pysolar. Please make sure that your patch does not break the test suite before you send a pull request. If that's confusing, please feel free to send me an email.

### Release procedure ###

(These notes are just to remind Brandon how releases worked the last time he released a new version of Pysolar.)

1. Patch, test, patch, test, until it works right. Commit and push to Github.
2. Update the version number in setup.py.
3. Update contributors.markdown if needed.
4. Add a release on Github that matches the new version number: https://github.com/pingswept/pysolar/releases
5. Test PyPI credentials with `python setup.py register`
6. Run `python setup.py sdist upload`
