# Release checklist

- [ ] Get `main` to the appropriate code release state.
      [GitHub Actions](https://github.com/prettytable/prettytable/actions) should be
      running cleanly for all merges to `main`.
      [![GitHub Actions status](https://github.com/prettytable/prettytable/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/prettytable/prettytable/actions)

- [ ] Edit release draft, adjust text if needed:
      https://github.com/prettytable/prettytable/releases

- [ ] Check next tag is correct, amend if needed

- [ ] Publish release

- [ ] Check the tagged
      [GitHub Actions build](https://github.com/prettytable/prettytable/actions/workflows/release.yml)
      has deployed to [PyPI](https://pypi.org/project/prettytable/#history)

- [ ] Check installation:

```bash
pip uninstall -y prettytable
pip install -U prettytable
python3 -c "import prettytable; print(prettytable.__version__)"
```
