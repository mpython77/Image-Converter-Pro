# Image Converter Pro

Professional-grade image converter and editor with a modular architecture, batch processing, and powerful effects.

## Features

- **Format Conversion**: JPEG, PNG, BMP, GIF, TIFF, WEBP, ICO
- **Batch Processing**: Parallel processing with ThreadPoolExecutor
- **Image Effects**: Brightness, contrast, saturation, 9 artistic filters
- **Crop Tool**: Free-form, center, and aspect ratio (16:9, 4:3, etc.)
- **Watermark**: Text watermark with opacity, positioning, and shadow
- **Undo/Redo**: History management (up to 20 steps)
- **EXIF Metadata**: Camera info, GPS, and image details viewer
- **Presets**: Save and load processing presets (JSON)
- **DPI Management**: Web (72 DPI) and Print (300 DPI) quality
- **Themes**: Dark and Light theme switching
- **File Renaming**: Pattern-based batch renaming ({num}, {date}, {orig})
- **Statistics**: Compression ratio, speed, timing reports

## Architecture

```
Image-Converter-Pro/
├── main.py                  # Entry point
├── requirements.txt         # Dependencies
├── LICENSE                  # MIT License
├── config/
│   ├── constants.py         # Application constants
│   └── themes.py            # Theme management
├── core/
│   ├── converter.py         # Format conversion, resize, rotate
│   ├── effects.py           # Effects and filters engine
│   ├── watermark.py         # Text watermark engine
│   ├── cropper.py           # Image cropping
│   ├── batch_processor.py   # Parallel batch processing
│   ├── preset_manager.py    # Preset management (JSON)
│   ├── history.py           # Undo/Redo system
│   ├── metadata.py          # EXIF metadata reader
│   ├── dpi_manager.py       # DPI management
│   └── stats.py             # Processing statistics
├── ui/
│   ├── app.py               # Main application window
│   ├── tabs/                # Tab panels
│   ├── widgets/             # Reusable UI components
│   └── dialogs/             # Dialog windows
├── utils/
│   ├── validators.py        # Input validation
│   ├── file_utils.py        # File utilities
│   └── logger.py            # Logging system
└── tests/                   # Unit tests (119 tests)
```

## Installation

```bash
git clone https://github.com/mpython77/Image-Converter-Pro.git
cd Image-Converter-Pro
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Testing

```bash
python -m pytest tests/ -v
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open images |
| `Ctrl+S` | Process & save |
| `Ctrl+Z` | Undo |
| `Ctrl+Y` | Redo |
| `Ctrl+T` | Toggle theme |
| `Ctrl+Q` | Exit |
| `Ctrl+Enter` | Process |

## License

MIT License — free for everyone, no restrictions. See [LICENSE](LICENSE) for details.
