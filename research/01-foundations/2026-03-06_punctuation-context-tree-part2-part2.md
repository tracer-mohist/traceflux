            # Extract segment before this punctuation
            seg_text = text[prev_pos:pos]
            if seg_text.strip():  # Skip empty segments
                child = _build(
                    seg_text,
