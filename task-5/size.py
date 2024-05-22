import re


def extract_size(size_string):
    try:
        # Regular expression pattern to match size and quantity like "90g×1本"
        size_quantity_pattern = r'(\d+(\.\d+)?(?:g|kg|ml|l|oz|lb))\s*×\s*(\d+個|袋|本)'
        size_quantity_match = re.search(size_quantity_pattern, size_string)

        if size_quantity_match:
            # Extract size and quantity from the match
            size = size_quantity_match.group(1)
            quantity = size_quantity_match.group(3)
            # Combine size and quantity in the format "size (quantity)"
            Product_Size = f"{size}×{quantity}"
        else:
            # Regular expression pattern to match sizes only (e.g., 90g, 200ml)
            size_pattern = r'\b\d+(\.\d+)?\s*(ml|mL|l|g|kg|oz|lb)\b'
            size_match = re.search(size_pattern, size_string)

            # Regular expression pattern to match quantities only (e.g., 24本入り)
            # quantity_pattern = r'\(\d+\s*本入り\)'
            quantity_pattern = r'\(\d+\s*本入り\)|(\d+\s*個)'
            quantity_match = re.search(quantity_pattern, size_string)

            # Extract the size and quantity separately
            if size_match:
                size = size_match.group()
            else:
                size = ""

            if quantity_match:
                quantity = quantity_match.group()
            else:
                quantity = ""

            # Combine size and quantity if both are present
            if size and quantity:
                Product_Size = f"{size} {quantity}"
            else:
                Product_Size = size or quantity



    except:
        Product_Size = ""

    return Product_Size


if __name__ == '__main__':
    print("Before :","27g×20袋")
    Product_Size = extract_size("令和５年産　お米 10kg　白米 新潟県産 コシヒカリ 5kg×2袋　送料無料（一部地域を除く）")
    print("After  :", Product_Size)