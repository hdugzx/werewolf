import easyocr
from pathlib import Path

def extract_all_rules(output_file="rule/rule.txt"):
    rule_dir = Path("rule")
    images = sorted(rule_dir.glob("rule_*.jpg"))
    if not images:
        raise FileNotFoundError("No rule_*.jpg files found in rule/")

    reader = easyocr.Reader(["en"], gpu=False)

    all_text = []
    for image_path in images:
        print(f"Processing {image_path.name} ...")
        results = reader.readtext(str(image_path), detail=0, paragraph=True)
        text = "\n".join(results).strip()
        header = f"{'='*40}\n{image_path.name}\n{'='*40}\n{text}\n"
        all_text.append(header)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(all_text), encoding="utf-8")
    print(f"\n✓ Combined text saved to {output_path}")

if __name__ == "__main__":
    extract_all_rules()