# PyPI Deployment Guide for env-banner

This guide walks you through the steps to publish the `env-banner` package to PyPI, making it installable via `pip install env-banner`.

## Prerequisites

Before deploying to PyPI, ensure you have:

1. A PyPI account at https://pypi.org/account/register/
2. A PyPI API token (recommended) or username/password
3. The required build tools installed

## Step 1: Install Build Tools

Install the required Python packages for building and uploading:

```bash
pip install --upgrade build twine
```

**What these tools do:**
- `build`: Creates distribution packages (wheel and source distribution)
- `twine`: Securely uploads packages to PyPI

## Step 2: Clean Previous Builds (if any)

Remove any previous build artifacts to ensure a clean build:

```bash
rm -rf dist/ build/ *.egg-info
```

## Step 3: Build the Distribution Packages

From the project root directory, run:

```bash
python -m build
```

This will create two files in the `dist/` directory:
- `env-banner-0.1.0.tar.gz` (source distribution)
- `env_banner-0.1.0-py3-none-any.whl` (wheel distribution)

**Verify the build:**
```bash
ls -lh dist/
```

You should see both files listed.

## Step 4: Verify the Package Contents

Check what files will be included in the package:

```bash
tar -tzf dist/env-banner-0.1.0.tar.gz
```

**Important:** Verify that:
- ✅ The `envbanner/` directory is included
- ✅ `README.md` and `LICENSE` are included
- ❌ The `test/` directory is **NOT** included (should be excluded by pyproject.toml)

## Step 5: Test Upload to TestPyPI (RECOMMENDED)

Before uploading to the real PyPI, test with TestPyPI first:

### 5a. Create a TestPyPI Account

If you don't have one, register at https://test.pypi.org/account/register/

### 5b. Upload to TestPyPI

```bash
python -m twine upload --repository testpypi dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your TestPyPI API token (starts with `pypi-`)

### 5c. Test Installation from TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ env-banner
```

### 5d. Verify the Installation

```bash
python -c "import envbanner; print(envbanner.__file__)"
```

If this works, you're ready for the real PyPI!

## Step 6: Upload to PyPI

### 6a. Get Your PyPI API Token

1. Log in to https://pypi.org
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Name: `env-banner-upload` (or any name you prefer)
5. Scope: "Entire account" (or specific to this project after first upload)
6. Copy the token (starts with `pypi-`) - **you won't see it again!**

### 6b. Upload to PyPI

```bash
python -m twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token

**Example:**
```
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: __token__
Enter your password: pypi-AgEIcHlwaS5vcmcC...
Uploading env_banner-0.1.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 15.2/15.2 kB • 00:00
Uploading env-banner-0.1.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.4/12.4 kB • 00:00

View at:
https://pypi.org/project/env-banner/0.1.0/
```

## Step 7: Verify the Package on PyPI

1. Visit https://pypi.org/project/env-banner/
2. Check that:
   - The README renders correctly
   - The version number is correct
   - All links work (GitHub, Issues)
   - The classifiers are appropriate

## Step 8: Test Installation from PyPI

```bash
# In a new virtual environment
pip install env-banner

# Verify import
python -c "import envbanner; print('Success!')"
```

## Step 9: Update Your GitHub Repository

After successful deployment:

1. **Tag the release:**
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

2. **Create a GitHub Release:**
   - Go to your GitHub repo → Releases → "Create a new release"
   - Tag: `v0.1.0`
   - Title: `env-banner v0.1.0`
   - Description: Copy the main features from README.md

## Troubleshooting

### Error: "File already exists"

You've already uploaded this version. You need to:
1. Increment the version in `pyproject.toml`
2. Rebuild: `python -m build`
3. Upload again

### Error: "Invalid credentials"

- Make sure you're using `__token__` as the username (not your PyPI username)
- Make sure your API token is correct and has the right scope
- For TestPyPI, use a TestPyPI token, not a PyPI token

### Error: "Package name already taken"

The package name `env-banner` is already in use. You'll need to choose a different name in `pyproject.toml`.

## Future Releases

For version 0.2.0 and beyond:

1. **Update the version** in `pyproject.toml`:
   ```toml
   version = "0.2.0"
   ```

2. **Document changes** in CHANGELOG.md (create if it doesn't exist)

3. **Rebuild and upload:**
   ```bash
   rm -rf dist/ build/ *.egg-info
   python -m build
   python -m twine upload dist/*
   ```

4. **Tag the release:**
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

## Automation (Optional)

Consider setting up GitHub Actions to automatically publish to PyPI when you create a new release tag. See the official PyPI publishing guide for details:
https://packaging.python.org/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/

## Security Best Practices

1. **Use API tokens** instead of username/password
2. **Use project-scoped tokens** after the first upload
3. **Never commit tokens** to your repository
4. **Store tokens securely** (use a password manager)
5. **Revoke tokens** if compromised

## Summary of Commands

```bash
# Install tools
pip install --upgrade build twine

# Clean and build
rm -rf dist/ build/ *.egg-info
python -m build

# Test on TestPyPI (recommended)
python -m twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ env-banner

# Upload to PyPI
python -m twine upload dist/*

# Verify
pip install env-banner
python -c "import envbanner; print('Success!')"

# Tag release
git tag v0.1.0
git push origin v0.1.0
```

## Questions?

If you encounter issues not covered here:
1. Check the official Python Packaging Guide: https://packaging.python.org/
2. Review PyPI's help docs: https://pypi.org/help/
3. Check the twine documentation: https://twine.readthedocs.io/
