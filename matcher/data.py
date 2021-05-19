# =====================
# Package imports
# =====================
# =====================
# Module imports
# =====================
# =====================
# Script
# =====================

class Data:
    profiles = {}
    output = None
    input_csv = None
    filter_csv = None
    use_tsv_inputs = None
    use_tsv_filtered = None
    use_filtered_list = None
    only_include_filtered = None
    output_option = None
    conversions = None
    inputs = None
    filtered = None
    save_output_as = None
    status = 0
    config = None
    grade_quantities = {
        12: 0,
        11: 0,
        10: 0,
        9: 0
    }
