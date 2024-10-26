# Release checklist

- [ ] Get `main` to the appropriate code release state.
      [GitHub Actions](https://github.com/hugovk/tinytext/actions) should be running
      cleanly for all merges to `main`.
      [![GitHub Actions status](https://github.com/hugovk/tinytext/workflows/Test/badge.svg)](https://github.com/hugovk/tinytext/actions)

- [ ] Edit release draft, adjust text if needed:
      https://github.com/hugovk/tinytext/releases

- [ ] Check next tag is correct, amend if needed

- [ ] Publish release

- [ ] Check the tagged
      [GitHub Actions build](https://github.com/hugovk/tinytext/actions/workflows/deploy.yml)
      has deployed to [PyPI](https://pypi.org/project/tinytext/#history)

- [ ] Check installation:

```bash
pip uninstall -y prettytable
pip install -U prettytable
python3 -c "import prettytable; print(prettytable.__version__)"
```
