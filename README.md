# QR Generator App

This is a separate macOS QR app project.

- Paste a URL
- Choose width and height
- Generate a QR code preview
- Download the result as a PNG
- Build a standalone macOS `.app`

## Project Folder

```text
Mac-QR-Code-App
```

## Run with Python

```bash
python3 -m pip install -r requirements.txt
python3 qr_generator_app.py
```

## Build a macOS app

Build this on a Mac:

```bash
chmod +x build_mac.sh
./build_mac.sh
```

The standalone app will be created here:

```text
release/QRGenerator.app
```

## Build a macOS app without owning a Mac

If you do not have a Mac, use the included GitHub Actions workflow in:

```text
.github/workflows/build-macos.yml
```

Steps:

1. Create a new GitHub repository.
2. Upload everything from `Mac-QR-Code-App` into that repository.
3. Open the repository on GitHub.
4. Click the `Actions` tab.
5. Run the `Build macOS App` workflow.
6. When it finishes, download the artifact named `QRGenerator-macOS`.
7. Send that zip file to the Mac user.

The Mac user only needs to:

1. Unzip the file.
2. Open `QRGenerator.app`.
3. If macOS warns them, right-click the app, choose `Open`, then confirm.
