import streamlit as st
import csv
from io import StringIO

# Define adjacent keys (QWERTY layout)
adjacent_keys = {
    'a': ['q', 'w', 's', 'z'],
    'b': ['v', 'g', 'h', 'n'],
    'c': ['x', 'd', 'f', 'v'],
    'd': ['s', 'e', 'r', 'f', 'c', 'x'],
    'e': ['w', 's', 'd', 'r'],
    'f': ['d', 'r', 't', 'g', 'v', 'c'],
    'g': ['f', 't', 'y', 'h', 'b', 'v'],
    'h': ['g', 'y', 'u', 'j', 'n', 'b'],
    'i': ['u', 'j', 'k', 'o'],
    'j': ['h', 'u', 'i', 'k', 'n', 'm'],
    'k': ['j', 'i', 'o', 'l', 'm'],
    'l': ['k', 'o', 'p'],
    'm': ['n', 'j', 'k'],
    'n': ['b', 'h', 'j', 'm'],
    'o': ['i', 'k', 'l', 'p'],
    'p': ['o', 'l'],
    'q': ['w', 'a'],
    'r': ['e', 'd', 'f', 't'],
    's': ['a', 'w', 'e', 'd', 'x', 'z'],
    't': ['r', 'f', 'g', 'y'],
    'u': ['y', 'h', 'j', 'i'],
    'v': ['c', 'f', 'g', 'b'],
    'w': ['q', 'a', 's', 'e'],
    'x': ['z', 's', 'd', 'c'],
    'y': ['t', 'g', 'h', 'u'],
    'z': ['a', 's', 'x']
}

def typo_variants(word):
    word = word.lower()
    variants = set()

    # Omission
    for i in range(len(word)):
        variants.add(word[:i] + word[i+1:])

    # Duplication
    for i in range(len(word)):
        variants.add(word[:i+1] + word[i] + word[i+1:])

    # Transposition
    for i in range(len(word) - 1):
        swapped = list(word)
        swapped[i], swapped[i+1] = swapped[i+1], swapped[i]
        variants.add(''.join(swapped))

    # Substitution with adjacent keys
    for i, char in enumerate(word):
        if char in adjacent_keys:
            for adj in adjacent_keys[char]:
                variants.add(word[:i] + adj + word[i+1:])

    return sorted(variants)

def generate_typos_for_keywords(keywords):
    all_typos = {}
    for kw in keywords:
        all_typos[kw] = typo_variants(kw)
    return all_typos

def save_to_csv(typo_dict):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Keyword", "Typo Variant"])
    for keyword, typos in typo_dict.items():
        for typo in typos:
            writer.writerow([keyword, typo])
    return output.getvalue()

# Streamlit UI
st.set_page_config(page_title="Typo Generator", page_icon="⌨️")
st.title("⌨️ Typo Generator Tool")

st.markdown("""
This tool generates common typographical errors for given keywords based on QWERTY keyboard layout.
Enter your keywords below to generate typo variants.
""")

# Input keywords
input_text = st.text_area(
    "Enter keywords (separated by commas)",
    placeholder="e.g., hello, world, python",
    height=100
)

if st.button("Generate Typos", type="primary"):
    if input_text.strip():
        keywords = [kw.strip() for kw in input_text.split(",") if kw.strip()]
        
        with st.spinner("Generating typo variants..."):
            typo_data = generate_typos_for_keywords(keywords)
            
        # Display results
        st.success(f"Generated {sum(len(v) for v in typo_data.values())} typo variants for {len(keywords)} keywords!")
        
        # Show preview
        st.subheader("Preview")
        for keyword, typos in list(typo_data.items())[:3]:  # Show first 3 keywords
            with st.expander(f"Keyword: {keyword}"):
                st.write(f"Typos: {', '.join(typos[:20])}{'...' if len(typos) > 20 else ''}")
        
        # Download CSV
        csv_data = save_to_csv(typo_data)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="typo_variants.csv",
            mime="text/csv"
        )
    else:
        st.warning("Please enter at least one keyword.")

# Add some information about the tool
with st.expander("About this tool"):
    st.markdown("""
    This tool generates four types of typographical errors:
    1. **Omission**: Missing a character (e.g., "helo" instead of "hello")
    2. **Duplication**: Duplicating a character (e.g., "helllo" instead of "hello")
    3. **Transposition**: Swapping adjacent characters (e.g., "hlelo" instead of "hello")
    4. **Adjacent key substitution**: Replacing with nearby keyboard keys (e.g., "jello" instead of "hello")
    
    The tool uses a standard QWERTY keyboard layout to determine adjacent keys.
    """)
