# PDF Exercises

## Very Basic

### Setup

```bash
echo "This is a secret message hidden in a PDF." | base64 > secret.txt
convert -size 300x100 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,50 'Nothing to see here'" pdf:- | pdftk - update_info secret.txt output exercise1.pdf
```

### Instructions

You're given a PDF file. Extract the hidden message encoded in the PDF metadata.

Hint: Use a PDF metadata extraction tool.

### Solution

```bash
exiftool exercise1.pdf | grep -i base64 | cut -d: -f2 | base64 -d
```

## Basic

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'The flag is: h1dd3n_t3xt'" pdf:exercise2.pdf
qpdf --encrypt "" "secret" 256 -- exercise2.pdf exercise2_encrypted.pdf
```

### Instructions

You're given an encrypted PDF. The password is "secret". Find the flag inside the PDF.

Hint: You need to decrypt the PDF first, then extract the text.

### Solution

```bash
qpdf --password=secret --decrypt exercise2_encrypted.pdf decrypted.pdf
pdftotext decrypted.pdf -
grep "flag is:" decrypted.txt
```

## Intermediate

### Setup

```bash
echo "Flag: 1nv1s1bl3_1nk" | convert -size 300x300 xc:white -font Arial -pointsize 20 -fill rgba(0,0,0,0.01) -draw "text 10,150 '@'" pdf:exercise3.pdf
```

### Instructions

There's an invisible message in this PDF. Find it.

Hint: The text is present but nearly transparent.

### Solution

```bash
convert -density 300 exercise3.pdf -fill black -opaque white output.png
tesseract output.png stdout
```

## Advanced

### Setup

```bash
echo "Flag: PDF_str3am_h4ck1ng" > flag.txt
qpdf --empty --pages . -- blank.pdf
qpdf blank.pdf --replace-object 1 0 "<<\n/Type /Catalog\n/Pages 2 0 R\n/Names << /EmbeddedFiles << /Names [(flag.txt) 4 0 R] >> >>\n>>"
qpdf --empty --pages blank.pdf -- --add-attachment flag.txt -- exercise4.pdf
```

### Instructions

There's a flag hidden in the PDF structure. Find it without extracting embedded files.

Hint: Investigate the PDF object structure.

### Solution

```bash
qpdf --show-object=4 exercise4.pdf | strings | grep Flag
```

# JPEG Exercises

## Very Basic

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Nothing here'" jpeg:exercise1.jpg
exiftool -Comment="The flag is: EXIF_d4ta" exercise1.jpg
```

### Instructions

Extract the hidden flag from the JPEG metadata.

Hint: Look at the image's EXIF data.

### Solution

```bash
exiftool exercise1.jpg | grep Comment
```

## Basic

### Setup

```bash
echo "Flag: st3g0_h1dd3n" | steghide embed -cf cover.jpg -ef - -p "" -q
```

### Instructions

There's a flag hidden in this image using steganography. Extract it.

Hint: Use a steganography tool. No password is required.

### Solution

```bash
steghide extract -sf cover.jpg -p ""
```

## Intermediate

### Setup

```bash
jpegtran -outfile exercise3.jpg input.jpg
echo "Flag: JFIF_chunk_d4ta" | dd conv=notrunc oflag=append of=exercise3.jpg
```

### Instructions

There's a flag appended to the end of this JPEG file. Find it.

Hint: The flag is after the JPEG end marker.

### Solution

```bash
strings exercise3.jpg | tail -n 1
```

## Advanced

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Look deeper'" jpeg:base.jpg
echo "Flag: DCT_coefficient_hack" > secret.txt
outguess -k "secret_key" -d secret.txt base.jpg exercise4.jpg
```

### Instructions

A message is hidden in the DCT coefficients of this JPEG. The key is "secret_key". Extract the flag.

Hint: Use a tool that can extract data hidden in DCT coefficients.

### Solution

```bash
outguess -k "secret_key" -r exercise4.jpg output.txt
cat output.txt
```

# BMP Exercises

## Very Basic

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Plain sight'" bmp:exercise1.bmp
echo "Flag: BMP_metadata" | sed 's/./&\x00/g' | dd conv=notrunc of=exercise1.bmp bs=1 seek=54
```

### Instructions

There's a flag hidden in the bitmap data. Extract it.

Hint: Look at the raw data just after the BMP header.

### Solution

```bash
xxd -s 54 -l 30 exercise1.bmp | cut -d' ' -f2- | xxd -r -p | tr -d '\0'
```

## Basic

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Color matters'" bmp:exercise2.bmp
steghide embed -cf exercise2.bmp -ef <(echo "Flag: LSB_steganography") -p "" -q
```

### Instructions

A flag is hidden using LSB steganography. Extract it.

Hint: Use a steganography tool that works with BMP files. No password is needed.

### Solution

```bash
steghide extract -sf exercise2.bmp -p ""
```

## Intermediate

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Palette tricks'" bmp8:exercise3.bmp
echo "Flag: palette_hack" | xxd -p | sed 's/\(..\)/\1 /g' > colors.txt
convert exercise3.bmp -colors 256 -unique-colors txt:- | tail -n +2 | cut -d' ' -f4 | paste - colors.txt | sed 's/^/#/' | convert exercise3.bmp -colorspace RGB +dither -remap inline:- exercise3_modified.bmp
```

### Instructions

The flag is encoded in the color palette of this 8-bit BMP. Decode it.

Hint: Each color in the palette represents a character of the flag.

### Solution

```bash
convert exercise3_modified.bmp -unique-colors txt:- | tail -n +2 | cut -d'#' -f2 | xxd -r -p
```

## Advanced

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Hidden structure'" bmp:exercise4.bmp
echo "Flag: BMP_structure_manipulation" | dd conv=notrunc of=exercise4.bmp bs=1 seek=2
```

### Instructions

The flag is hidden within the BMP file structure. Find it without using typical forensic tools.

Hint: The flag is placed in an unusual location within the file structure.

### Solution

```bash
dd if=exercise4.bmp bs=1 skip=2 count=30 2>/dev/null
```

# MP4 Exercises

## Very Basic

### Setup

```bash
ffmpeg -f lavfi -i color=c=white:s=320x240:d=5 -vf "drawtext=fontfile=/path/to/font.ttf:fontsize=20:fontcolor=black:x=10:y=100:text='Sample Video'" exercise1.mp4
exiftool -Comment="Flag: MP4_metadata" exercise1.mp4
```

### Instructions

Extract the flag from the MP4 file's metadata.

Hint: Look at the file's metadata, particularly the comments.

### Solution

```bash
exiftool exercise1.mp4 | grep Comment
```

## Basic

### Setup

```bash
ffmpeg -f lavfi -i color=c=white:s=320x240:d=5 -vf "drawtext=fontfile=/path/to/font.ttf:fontsize=20:fontcolor=black:x=10:y=100:text='Hidden Frame'" exercise2.mp4
ffmpeg -i exercise2.mp4 -vf "select='eq(n,50)',scale=320:240" -frames:v 1 flag_frame.png
convert flag_frame.png -pointsize 20 -draw "text 10,200 'Flag: hidden_frame'" flag_frame_modified.png
ffmpeg -i exercise2.mp4 -i flag_frame_modified.png -filter_complex "[0:v][1:v]overlay=0:0:enable='between(t,2,2.04)'" exercise2_final.mp4
```

### Instructions

There's a hidden frame in this video containing the flag. Find it.

Hint: The flag appears briefly around the 2-second mark.

### Solution

```bash
ffmpeg -i exercise2_final.mp4 -vf "select='between(t,1.9,2.1)'" -vsync 0 frame%d.png
# Manually inspect the extracted frames
```

## Intermediate

### Setup

```bash
ffmpeg -f lavfi -i color=c=white:s=320x240:d=5 -vf "drawtext=fontfile=/path/to/font.ttf:fontsize=20:fontcolor=black:x=10:y=100:text='Audio Secrets'" exercise3.mp4
ffmpeg -i exercise3.mp4 -f wav -acodec pcm_s16le silence.wav
echo "Flag: audio_steganography" | steghide embed -cf silence.wav -ef - -p "" -q
ffmpeg -i exercise3.mp4 -i silence.wav -c:v copy -map 0:v:0 -map 1:a:0 exercise3_final.mp4
```

### Instructions

The flag is hidden in the audio stream of this MP4 file using steganography. Extract it.

Hint: Extract the audio, then use a steganography tool. No password is needed.

### Solution

```bash
ffmpeg -i exercise3_final.mp4 -vn -acodec copy audio.wav
steghide extract -sf audio.wav -p ""
```

## Advanced

### Setup

```bash
ffmpeg -f lavfi -i color=c=white:s=320x240:d=5 -vf "drawtext=fontfile=/path/to/font.ttf:fontsize=20:fontcolor=black:x=10:y=100:text='Corrupt MP4'" exercise4.mp4
# Manually corrupt the MP4 file structure to hide the flag
```

### Instructions

The flag is hidden by corrupting the MP4 file structure. Extract the flag without using standard MP4 parsing tools.

Hint: Investigate the low-level structure of the MP4 container.

### Solution

```bash
# Manually inspect the hex dump of the file to find the hidden flag
hexdump -C exercise4.mp4 | grep -i "flag"
```

# DOCX Exercises

## Very Basic

### Setup

```bash
echo "This is a sample document. The flag is: DOCX_metadata" > exercise1.txt
libreoffice --convert-to docx exercise1.txt
```

### Instructions

Extract the flag from the DOCX file's metadata.

Hint: Look at the file's properties or metadata.

### Solution

```bash
unzip -p exercise1.docx docProps/core.xml | grep -i flag
```

## Basic

### Setup

```bash
echo "This is a sample document." > exercise2.txt
libreoffice --convert-to docx exercise2.txt
# Manually add the following to the end of the DOCX file:
# [Content_Types].xml
# <?xml version="1.0" encoding="UTF-8"?>
# <Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
#   <Default Extension="txt" ContentType="text/plain"/>
#   <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
#   <Override PartName="/customXml/item1.xml" ContentType="application/xml"/>
#   <Override PartName="/customXml/itemProps1.xml" ContentType="application/xml"/>
# </Types>
# 
# word/_rels/document.xml.rels
# <?xml version="1.0" encoding="UTF-8"?>
# <Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
#   <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/customXml" Target="/customXml/item1.xml"/>
# </Relationships>
# 
# customXml/item1.xml
# <?xml version="1.0" encoding="UTF-8"?>
# <b:Flag xmlns:b="http://customschema/">Flag: hidden_in_docx</b:Flag>
# 
# customXml/itemProps1.xml
# <?xml version="1.0" encoding="UTF-8"?>
# <ds:datastoreItem ds:itemID="{B4166C8B-C6D2-4022-AEB5-D1F4C8BBDFDA}" xmlns:ds="http://schemas.openxmlformats.org/officeDocument/2006/customXml">
#   <ds:schemaRefs>
#     <ds:schemaRef ds:uri="http://customschema/"/>
#   </ds:schemaRefs>
# </ds:datastoreItem>
```

### Instructions

The flag is hidden in the custom XML parts of this DOCX file. Extract it.

Hint: Look for additional parts and XML structures beyond the main document.

### Solution

```bash
unzip -l exercise2.docx
unzip -p exercise2.docx customXml/item1.xml | grep -i flag
```

## Intermediate

### Setup

```bash
echo "This is a sample document." > exercise3.txt
libreoffice --convert-to docx exercise3.txt
# Manually add the following to the end of the DOCX file:
# word/media/image1.png
# (A PNG image containing the text "Flag: embedded_image")
# 
# [Content_Types].xml
# (Add an override for the new image file)
#
# word/_rels/document.xml.rels
# (Add a relationship for the new image file)
```

### Instructions

The flag is hidden as an embedded image in this DOCX file. Extract it.

Hint: Look for additional media files and their relationships within the DOCX structure.

### Solution

```bash
unzip -l exercise3.docx
unzip -p exercise3.docx word/media/image1.png > flag_image.png
# Inspect the flag_image.png file
```

## Advanced

### Setup

```bash
echo "This is a sample document." > exercise4.txt
libreoffice --convert-to docx exercise4.txt
# Manually add the following to the end of the DOCX file:
# word/document.xml
# (Modify the XML to include the flag as a hidden comment)
# 
# [Content_Types].xml
# (Add an override for the modified document.xml file)
# 
# word/_rels/document.xml.rels
# (Add a relationship for the modified document.xml file)
```

### Instructions

The flag is hidden as a comment in the document.xml file of this DOCX. Extract it.

Hint: Look for hidden comments or other modifications within the core document.xml file.

### Solution

```bash
unzip -p exercise4.docx word/document.xml | grep -i flag
```

# PDF Exercises

## Very Basic

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Plain Sight'" exercise1.pdf
echo "Flag: PDF_metadata" | pdftk exercise1.pdf update_info - output exercise1_updated.pdf
```

### Instructions

The flag is hidden in the PDF file's metadata. Extract it.

Hint: Use a tool that can inspect PDF metadata.

### Solution

```bash
pdfinfo exercise1_updated.pdf | grep -i "flag"
```

## Basic

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Hidden Content'" exercise2.pdf
qpdf --password='' --decrypt exercise2.pdf exercise2_decrypted.pdf
# Manually add the following to the end of the PDF file:
# %%EOF
# %PDF-1.7
# 1 0 obj
# <<
#   /Type /Catalog
#   /Pages 2 0 R
# >>
# endobj
# 
# 2 0 obj
# <<
#   /Type /Pages
#   /Kids [3 0 R]
#   /Count 1
# >>
# endobj
# 
# 3 0 obj
# <<
#   /Type /Page
#   /Parent 2 0 R
#   /Resources <<>>
#   /Contents 4 0 R
#   /MediaBox [0 0 300 300]
# >>
# endobj
# 
# 4 0 obj
# <</Length 52>>
# stream
# BT
#   /F1 20 Tf
#   10 150 Td
#   (Flag: hidden_in_pdf) Tj
# ET
# endstream
# endobj
# 
# 5 0 obj
# <<
#   /F1 <<
#     /Type /Font
#     /Subtype /Type1
#     /BaseFont /Helvetica
#   >>
# >>
# endobj
# 
# trailer
# <<
#   /
```

### Instructions

The flag is hidden in the corrupted structure of this PDF file. Extract it.

Hint: Manually inspect the modified PDF structure and contents.

### Solution

```bash
# Manually inspect the hex dump of the file to find the hidden flag
hexdump -C exercise2_decrypted.pdf | grep -i "flag"
```

## Intermediate

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Embedded Content'" exercise3.pdf
# Manually add the following to the end of the PDF file:
# %%EOF
# %PDF-1.7
# 1 0 obj
# <<
#   /Type /Catalog
#   /Pages 2 0 R
# >>
# endobj
# 
# 2 0 obj
# <<
#   /Type /Pages
#   /Kids [3 0 R]
#   /Count 1
# >>
# endobj
# 
# 3 0 obj
# <<
#   /Type /Page
#   /Parent 2 0 R
#   /Resources <<
#     /XObject <<
#       /Img 4 0 R
#     >>
#   >>
#   /Contents 5 0 R
#   /MediaBox [0 0 300 300]
# >>
# endobj
# 
# 4 0 obj
# <<
#   /Type /XObject
#   /Subtype /Image
#   /Width 300
#   /Height 300
#   /ColorSpace /DeviceGray
#   /BitsPerComponent 8
#   /Filter /FlateDecode
#   /Length 90
# >>
# stream
# H??cr`d``????????H3?@?I??d???????Ź?F	
# endstream
# endobj
# 
# 5 0 obj
# <</Length 52>>
# stream
# BT
#   /F1 20 Tf
#   10 150 Td
#   (Flag: embedded_pdf) Tj
# ET
# endstream
# endobj
#
# 6 0 obj
# <<
#   /F1 <<
#     /Type /Font
#     /Subtype /Type1
#     /BaseFont /Helvetica
#   >>
# >>
#
```

### Instructions

The flag is hidden as an embedded image in this PDF file. Extract it.

Hint: Look for additional image or media objects embedded within the PDF structure.

### Solution

```bash
# Extract the embedded image object from the PDF
pdfimages -j exercise3.pdf embedded_image

# Inspect the extracted image for the flag
strings embedded_image.jpg | grep -i "flag"
```

## Advanced

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Hidden Content'" exercise4.pdf
# Manually add the following to the end of the PDF file:
# %%EOF
# %PDF-1.7
# 1 0 obj
# <<
#   /Type /Catalog
#   /Pages 2 0 R
#   /AcroForm 3 0 R
# >>
# endobj
# 
# 2 0 obj
# <<
#   /Type /Pages
#   /Kids [4 0 R]
#   /Count 1
# >>
# endobj
# 
# 3 0 obj
# <<
#   /Fields [5 0 R]
# >>
# endobj
# 
# 4 0 obj
# <<
#   /Type /Page
#   /Parent 2 0 R
#   /Resources <<>>
#   /Contents 6 0 R
#   /MediaBox [0 0 300 300]
# >>
# endobj
# 
# 5 0 obj
# <<
#   /Type /Annot
#   /Subtype /Widget
#   /FT /Tx
#   /T (Flag)
#   /V (flag_in_pdf_form)
# >>
# endobj
# 
# 6 0 obj
# <</Length 52>>
# stream
# BT
#   /F1 
```

### Instructions

The flag is hidden in a PDF form field in this file. Extract it.

Hint: Look for any PDF form fields or annotations that may contain the flag.

### Solution

```bash
# Extract the PDF form field containing the flag
pdfparser exercise4.pdf | grep -i "flag"
```

# JPG Exercises

## Very Basic

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Plain Sight'" exercise1.jpg
exiftool -comment="Flag: jpg_metadata" exercise1.jpg
```

### Instructions

The flag is hidden in the EXIF metadata of this JPG file. Extract it.

Hint: Use a tool that can inspect EXIF metadata.

### Solution

```bash
exiftool exercise1.jpg | grep -i "flag"
```

## Basic

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Hidden Content'" exercise2.jpg
# Manually add the following to the end of the JPG file:
# Flag: hidden_in_jpg
```

### Instructions

The flag is hidden in the file structure of this JPG. Extract it.

Hint: Inspect the hex dump of the file to find the hidden flag.

### Solution

```bash
hexdump -C exercise2.jpg | grep -i "flag"
```

## Intermediate

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Steganography'" exercise3.jpg
# Embed a hidden image containing the flag in the JPG file
```

### Instructions

The flag is hidden using steganography in this JPG file. Extract it.

Hint: Look for any hidden or embedded images within the JPG file.

### Solution

```bash
# Extract any embedded images from the JPG
steghide extract -sf exercise3.jpg

# Inspect the extracted image for the flag
strings hidden_image.png | grep -i "flag"
```

## Advanced

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Encrypted Content'" exercise4.jpg
# Encrypt the JPG file with a password
openssl aes-256-cbc -salt -in exercise4.jpg -out exercise4_encrypted.jpg -pass pass:supersecretpassword
```

### Instructions

The flag is hidden in this encrypted JPG file. Extract it.

Hint: You'll need to decrypt the file first to access the hidden content.

### Solution

```bash
# Decrypt the JPG file
openssl aes-256-cbc -d -in exercise4_encrypted.jpg -out exercise4_decrypted.jpg -pass pass:supersecretpassword

# Inspect the decrypted file for the flag
hexdump -C exercise4_decrypted.jpg | grep -i "flag"
```

# ZIP Exercises

## Very Basic

### Setup

```bash
# Create a ZIP file with a single file containing the flag
zip exercise1.zip flag.txt
echo "Flag: zip_basic" > flag.txt
```

### Instructions

The flag is hidden in this basic ZIP file. Extract it.

Hint: Simply extract the contents of the ZIP file.

### Solution

```bash
unzip exercise1.zip
cat flag.txt
```

## Basic

### Setup

```bash
# Create a ZIP file with multiple files and directories
mkdir exercise2_dir
echo "Flag: zip_basic_2" > exercise2_dir/flag.txt
zip -r exercise2.zip exercise2_dir
```

### Instructions

The flag is hidden in this basic ZIP file with multiple files and directories. Extract it.

Hint: Extract the contents of the ZIP file and look through the directory structure.

### Solution

```bash
unzip exercise2.zip
cat exercise2_dir/flag.txt
```

## Intermediate

### Setup

```bash
# Create a password-protected ZIP file
zip -P supersecretpassword -r exercise3.zip exercise2_dir
```

### Instructions

The flag is hidden in this password-protected ZIP file. Extract it.

Hint: You'll need to provide the correct password to extract the contents.

### Solution

```bash
unzip -P supersecretpassword exercise3.zip
cat exercise2_dir/flag.txt
```

## Advanced

### Setup

```bash
# Create a ZIP file with a corrupted structure
zip -FF exercise4.zip --out exercise4_fixed.zip
```

### Instructions

The flag is hidden in this corrupted ZIP file. Extract it.

Hint: Inspect the structure of the ZIP file and try to fix any issues.

### Solution

```bash
unzip exercise4_fixed.zip
cat exercise2_dir/flag.txt
```

# ELF Exercises

## Very Basic

### Setup

```c
// Write a simple C program that prints the flag
#include <stdio.h>

int main() {
    printf("Flag: elf_very_basic\n");
    return 0;
}
```

### Instructions

The flag is hidden in this basic ELF file. Extract it.

Hint: Run the ELF file to get the flag.

### Solution

```bash
gcc -o exercise1 exercise1.c
./exercise1
```

## Basic

### Setup

```c
// Write a C program that hides the flag in the ELF structure
#include <stdio.h>

int main() {
    printf("This is a basic ELF file.\n");
    return 0;
}
```

### Instructions

The flag is hidden in the structure of this basic ELF file. Extract it.

Hint: Inspect the hex dump of the ELF file to find the hidden flag.

### Solution

```bash
gcc -o exercise2 exercise2.c
hexdump -C exercise2 | grep -i "flag"
```

## Intermediate

### Setup

```c
// Write a C program that hides the flag using simple obfuscation
#include <stdio.h>

int main() {
    int flag = 0x464c4147; // 'FLAG' in hex
    int obfuscated = flag ^ 0xdeadbeef;
    printf("Obfuscated flag: %x\n", obfuscated);
    return 0;
}
```

### Instructions

The flag is hidden using obfuscation in this ELF file. Extract it.

Hint: Reverse the obfuscation to get the original flag.

### Solution

```bash
gcc -o exercise3 exercise3.c
./exercise3
# Obfuscated flag: beefdead
# Deobfuscate the flag: 0x464c4147 ^ 0xdeadbeef = 0x464c4147 (or 'FLAG')
```

## Advanced

### Setup

```c
// Write a C program that hides the flag using advanced techniques
#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <password>\n", argv[0]);
        return 1;
    }

    char password[] = "supersecretpassword";
    if (strcmp(argv[1], password) != 0) {
        printf("Incorrect password.\n");
        return 1;
    }

    printf("Flag: elf_advanced\n");
    return 0;
}
```

### Instructions

The flag is hidden behind a password in this advanced ELF file. Extract it.

Hint: You'll need to provide the correct password to get the flag.

### Solution

```bash
gcc -o exercise4 exercise4.c
./exercise4 supersecretpassword
```

# GIF Exercises

## Very Basic

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Plain Sight'" exercise1.gif
echo "Flag: gif_basic" > flag.txt
convert flag.txt -resize 50x50 exercise1_flag.gif
convert exercise1.gif exercise1_flag.gif -layers composite exercise1.gif
```

### Instructions

The flag is hidden in this basic GIF file. Extract it.

Hint: Look for any embedded images or text within the GIF file.

### Solution

```bash
convert exercise1.gif gif:-
# Inspect the GIF output for the flag
```

## Basic

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Hidden Content'" exercise2.gif
# Manually add the following to the end of the GIF file:
# Flag: gif_basic_2
```

### Instructions

The flag is hidden in the file structure of this basic GIF file. Extract it.

Hint: Inspect the hex dump of the GIF file to find the hidden flag.

### Solution

```bash
hexdump -C exercise2.gif | grep -i "flag"
```

## Intermediate

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Steganography'" exercise3.gif
# Embed a hidden image containing the flag in the GIF file
```

### Instructions

The flag is hidden using steganography in this GIF file. Extract it.

Hint: Look for any hidden or embedded images within the GIF file.

### Solution

```bash
# Extract any embedded images from the GIF
steghide extract -sf exercise3.gif

# Inspect the extracted image for the flag
strings hidden_image.png | grep -i "flag"
```

## Advanced

### Setup

```bash
convert -size 300x300 xc:white -font Arial -pointsize 20 -fill black -draw "text 10,150 'Encrypted Content'" exercise4.gif
# Encrypt the GIF file with a password
openssl aes-256-cbc -salt -in exercise4.gif -out exercise4_encrypted.gif -pass pass:supersecretpassword
```

### Instructions

The flag is hidden in this encrypted GIF file. Extract it.

Hint: You'll need to decrypt the file first to access the hidden content.

### Solution

```bash
# Decrypt the GIF file
openssl aes-256-cbc -d -in exercise4_encrypted.gif -out exercise4_decrypted.gif -pass pass:supersecretpassword

# Inspect the decrypted file for the flag
hexdump -C exercise4_decrypted.gif | grep -i "flag"
```

# DOCX Exercises

## Very Basic

### Setup

```bash
# Create a basic DOCX file with the flag in the text
echo "Flag: docx_basic" > flag.txt
pandoc -o exercise1.docx flag.txt
```

### Instructions

The flag is hidden in this basic DOCX file. Extract it.

Hint: Extract the contents of the DOCX file and look for the flag.

### Solution

```bash
unzip exercise1.docx
cat word/document.xml
```

## Basic

### Setup

```bash
# Create a DOCX file with the flag hidden in the metadata
echo "Flag: docx_basic_2" > flag.txt
pandoc -o exercise2.docx flag.txt
# Manually add the following XML to the [Content_Types].xml file in the DOCX:
# <Override PartName="/docProps/custom.xml" ContentType="application/vnd.openxmlformats-officedocument.custom-properties+xml"/>
# Create the docProps/custom.xml file with the following content:
# <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# <Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/custom-properties">
#   <property fmtid="{D5CDD505-2E9C-101B-9397-08002B2CF9AE}" pid="2" name="Flag">docx_basic_2</property>
# </Properties>
```

### Instructions

The flag is hidden in the metadata of this basic DOCX file. Extract it.

Hint: Look for any custom properties or metadata in the DOCX file.

### Solution

```bash
unzip exercise2.docx
cat docProps/custom.xml
```

## Intermediate

### Setup

```bash
# Create a DOCX file with the flag hidden using steganography
echo "Flag: docx_steganography" > flag.txt
pandoc -o exercise3.docx flag.txt
# Manually add an image to the word/media directory of the DOCX file that contains the flag hidden using steganography
```

### Instructions

The flag is hidden using steganography in this DOCX file. Extract it.

Hint: Look for any hidden or embedded images within the DOCX file.

### Solution

```bash
unzip exercise3.docx
# Extract any embedded images from the DOCX
# Inspect the extracted image for the flag using steganography tools
```

## Advanced

### Setup

```bash
# Create a password-protected DOCX file with the flag
echo "Flag: docx_advanced" > flag.txt
pandoc -o exercise4.docx flag.txt
# Manually add password protection to the DOCX file
```

### Instructions

The flag is hidden in this password-protected DOCX file. Extract it.

Hint: You'll need to provide the correct password to access the contents.

### Solution

```bash
unzip -P supersecretpassword exercise4.docx
cat word/document.xml
```
