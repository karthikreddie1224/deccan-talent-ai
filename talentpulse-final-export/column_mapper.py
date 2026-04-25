import pandas as pd
import re
import difflib

class FlexibleCSVParser:
    def __init__(self, required_columns=None, aliases=None, fuzzy_threshold=0.8):
        self.required_columns = required_columns or ["Name", "Role", "Skills", "Experience"]
        self.aliases = aliases or {
            "name": ["name", "full_name", "candidate_name", "first_name", "applicant_name"],
            "role": ["role", "job_role", "position", "preferred_role", "title", "job_title"],
            "skills": ["skills", "skillset", "primary_skill", "technologies", "tech_stack", "core_skills"],
            "experience": ["experience", "exp", "experience_years", "years", "total_experience", "yoe", "work_experience"],
            "location": ["location", "city", "region", "based_in", "candidate_location"],
            "current company": ["current_company", "company", "employer", "organization"]
        }
        self.fuzzy_threshold = fuzzy_threshold
        
    def _normalize_string(self, s):
        s = str(s).lower().strip()
        s = re.sub(r'[^a-z0-9]+', '_', s)
        return s.strip('_')

    def parse_and_map(self, df):
        mapped_columns = {}
        unmapped_cols = list(df.columns)
        
        for req_col in self.required_columns:
            req_norm = self._normalize_string(req_col)
            alias_list = self.aliases.get(req_norm, [req_norm])
            
            for actual_col in unmapped_cols:
                actual_norm = self._normalize_string(actual_col)
                if actual_norm in alias_list:
                    mapped_columns[actual_col] = req_col
                    unmapped_cols.remove(actual_col)
                    break
                    
        remaining_required = [c for c in self.required_columns if c not in mapped_columns.values()]
        
        for req_col in remaining_required:
            req_norm = self._normalize_string(req_col)
            alias_list = self.aliases.get(req_norm, [req_norm])
            actual_norm_map = {self._normalize_string(c): c for c in unmapped_cols}
            
            best_match = None
            for target in alias_list:
                matches = difflib.get_close_matches(target, actual_norm_map.keys(), n=1, cutoff=self.fuzzy_threshold)
                if matches:
                    best_match = actual_norm_map[matches[0]]
                    break
                    
            if best_match:
                mapped_columns[best_match] = req_col
                unmapped_cols.remove(best_match)
                
        # Optional columns
        optional_targets = ["Location", "Current Company", "Notice Period", "Availability", "Risk Flag", "Recommended Action"]
        for opt_col in optional_targets:
            if opt_col in mapped_columns.values(): continue
            opt_norm = self._normalize_string(opt_col)
            alias_list = self.aliases.get(opt_norm, [opt_norm])
            
            for actual_col in unmapped_cols:
                actual_norm = self._normalize_string(actual_col)
                if actual_norm in alias_list:
                    mapped_columns[actual_col] = opt_col
                    unmapped_cols.remove(actual_col)
                    break
                
        df_mapped = df.rename(columns=mapped_columns)
        
        missing = [c for c in self.required_columns if c not in df_mapped.columns]
        
        if missing:
            suggestions = {}
            all_actual_norm = {self._normalize_string(c): c for c in df.columns}
            
            for m in missing:
                m_norm = self._normalize_string(m)
                m_aliases = self.aliases.get(m_norm, [m_norm])
                for alias in m_aliases:
                    matches = difflib.get_close_matches(alias, all_actual_norm.keys(), n=3, cutoff=0.5)
                    if matches:
                        suggestions[m] = [all_actual_norm[match] for match in matches]
                        break
                        
            error_msg = f"Missing required columns: {', '.join(missing)}."
            if suggestions:
                sugg_text = " | ".join([f"For '{k}' did you mean: {', '.join(v)}?" for k, v in suggestions.items()])
                error_msg += f"\nSuggestions: {sugg_text}"
                
            raise ValueError(error_msg)
            
        return df_mapped
