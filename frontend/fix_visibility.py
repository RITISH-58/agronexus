import os
import re

def fix_visibility():
    base_dir = r"c:\Users\RITISH REDDY\OneDrive\Desktop\agriculture\frontend\src"
    
    replacements = [
        # Text Grays (Darken)
        (r'\btext-gray-600\b', 'text-gray-800'),
        (r'\btext-gray-500\b', 'text-gray-700'),
        (r'\btext-gray-400\b', 'text-gray-600'),
        
        # Text white fades
        (r'\btext-white/40\b', 'text-white/80'),
        (r'\btext-white/50\b', 'text-white/90'),
        (r'\btext-white/60\b', 'text-white/90'),
        (r'\btext-white/70\b', 'text-white'),
        (r'\btext-white/80\b', 'text-white'),
        
        # Opacity tags
        (r'\bopacity-40\b', 'opacity-80'),
        (r'\bopacity-50\b', 'opacity-90'),
        (r'\bopacity-60\b', 'opacity-100'),
        (r'\bopacity-70\b', 'opacity-100'),
        
        # Placeholders
        (r'\bplaceholder-white/40\b', 'placeholder-gray-200'),
        (r'\bplaceholder-white/50\b', 'placeholder-gray-200'),
        (r'\bplaceholder-gray-400\b', 'placeholder-gray-600'),
        (r'\bplaceholder-gray-500\b', 'placeholder-gray-600'),
        
        # Glassmorphism backgrounds (make more opaque & add contrast border)
        (r'\bbg-white/50\b', 'bg-white/85 border border-black/5'),
        (r'\bbg-white/60\b', 'bg-white/90 border border-black/5'),
        (r'\bbg-white/70\b', 'bg-white/95 border border-black/5'),
    ]

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(('.jsx', '.js')):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content
                
                # Apply regex replacements
                for pattern, replacement in replacements:
                    content = re.sub(pattern, replacement, content)
                
                # Special Hero Text Fix
                content = content.replace(
                    "<><Zap size={22} /> Get Smart Business Recommendations</>",
                    "<span className=\"text-gray-900 font-semibold drop-shadow-sm flex items-center gap-2\"><Zap size={22} /> Get Smart Business Recommendations</span>"
                )

                if content != original_content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Updated: {file}")

if __name__ == "__main__":
    fix_visibility()
