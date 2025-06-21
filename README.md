# XYZ ↔ PNG Converter for RPG Maker 2000/2003

A set of tools to convert between the XYZ image format (used in RPG Maker 2000 and 2003) and modern PNG format, enabling easy image editing with modern software.

## 📦 Included Tools

- `xyz2png.py` - Converts XYZ → PNG (with preserved color palette)
- `png2xyz.py` - Converts PNG → XYZ (with 256-color verification)
- `256colors.py` - Reduces PNG images to 8-bit (256 colors) for compatibility

## ⚙️ Requirements

- Python 3.6+
- Pillow (installable via requirements.txt)

```bash
pip install -r requirements.txt
```

## 🚀 How to Use

1. Extract RPG Maker Images
```bash
python xyz2png.py
```
• Select XYZ files or folders to convert

2. Edit the Images\
• Use any graphics editor (Photoshop, GIMP, etc.)\
• Keep colors within 256-color limit

3. Prepare for RPG Maker
```bash
python 256colors.py
```
• Select your edited PNG to reduce it to 256 colors

4. Convert Back to XYZ
```bash
python png2xyz.py
```
• Import the resulting XYZ file back into your project

## ✨ Key Features
✔ Batch conversion (single files or entire folders)\
✔ Directory structure preservation\
✔ Progress bar with time estimation\
✔ Automatic 256-color limit verification\
✔ Organized output in Downloads folder

## ⚠️ Limitations
• XYZ format supports maximum 256 colors per image\
• Images with transparency may require special handling\
• Always backup original files before conversion

## 📂 Output Structure
Converted files are saved to:

• ~/Downloads/XYZ2PNG_Output/ (for XYZ→PNG conversions)\
• ~/Downloads/PNG2XYZ_Output/ (for PNG→XYZ conversions)

Created by Rafaelmorai - For the RPG Maker development community
