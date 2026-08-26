import pandas as pd

# Original Open Food Facts CSV
input_file = "openfoodfacts-products.csv"

# Output file
output_file = "openfoodfacts_products.csv"

# Fields required for your project
fields = [
    "code",
    "product_name",
    "brands",
    "categories",
    "countries",
    "quantity",
    "packaging",
    "manufacturing_places",
    "image_url",
    "image_front_url",
    "image_back_url"
]

print("Reading Open Food Facts dataset...")

df = pd.read_csv(
    input_file,
    encoding="utf-8",
    encoding_errors="replace",
    usecols=lambda column: column in fields,
    low_memory=False
)

print("Dataset loaded successfully!")
print("Total products:", len(df))

# Save selected fields
df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig"
)

print("Dataset saved successfully!")
print("File:", output_file)