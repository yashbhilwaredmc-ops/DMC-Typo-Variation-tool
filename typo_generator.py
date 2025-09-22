import streamlit as st
import csv
from io import StringIO

# Set page configuration with your DMC branding
st.set_page_config(
    page_title="DMC Typo Variation Tool",
    page_icon="⌨️",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
st.title("⌨️ DMC Typo Variation Tool")

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
            
        # Calculate total variants
        total_variants = sum(len(v) for v in typo_data.values())
        
        # Display results
        st.success(f"Generated {total_variants} typo variants for {len(keywords)} keywords!")
        
        # Show preview - FIXED: Now shows all variants
        st.subheader("All Generated Typo Variants")
        
        # Create a container for each keyword with all its variants
        for keyword, typos in typo_data.items():
            with st.expander(f"Keyword: '{keyword}' - {len(typos)} variants"):
                # Display all variants in a scrollable text area
                st.text_area(
                    f"All typo variants for '{keyword}':",
                    value="\n".join([f"{i+1}. {typo}" for i, typo in enumerate(typos)]),
                    height=min(300, 50 + (len(typos) * 20)),  # Dynamic height based on number of variants
                    key=f"variants_{keyword}"
                )
        
        # Download CSV
        csv_data = save_to_csv(typo_data)
        st.download_button(
            label="Download All as CSV",
            data=csv_data,
            file_name="dmc_typo_variants.csv",
            mime="text/csv",
            help="Download all generated typo variants as a CSV file"
        )
        
        # Show statistics
        st.subheader("Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Keywords Processed", len(keywords))
        with col2:
            st.metric("Total Typo Variants", total_variants)
        with col3:
            avg_variants = total_variants / len(keywords) if keywords else 0
            st.metric("Average Variants per Keyword", f"{avg_variants:.1f}")
            
    else:
        st.warning("Please enter at least one keyword.")

# Add some information about the tool
with st.expander("About DMC Typo Variation Tool"):
    st.markdown("""
    ## DMC Typo Variation Tool
    
    This tool generates four types of typographical errors:
    1. **Omission**: Missing a character (e.g., "helo" instead of "hello")
    2. **Duplication**: Duplicating a character (e.g., "helllo" instead of "hello")
    3. **Transposition**: Swapping adjacent characters (e.g., "hlelo" instead of "hello")
    4. **Adjacent key substitution**: Replacing with nearby keyboard keys (e.g., "jello" instead of "hello")
    
    The tool uses a standard QWERTY keyboard layout to determine adjacent keys.
    
    ### Why showing all variants is important
    Unlike the previous version that only showed the first 20 variants, this tool now displays
    ALL generated variants for each keyword. This ensures you don't miss any potential typos
    that might be relevant for your use case.
    """)
