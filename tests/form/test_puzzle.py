import sys
sys.path.append("packages/form/puzzle")
import puzzle

def test_chess():
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    assert puzzle.extract_fen(fen) == fen

    out = f"hello {fen} world"
    assert puzzle.extract_fen(out) == fen
    
    fen = "8/6k1/8/7p/8/5K2/5PPP/7Q"
    out = f"""
Here you go:    
    
Check this FEN:   "{fen}"
 
Bye!
""" 
    assert puzzle.extract_fen(out) == fen  
    assert not puzzle.extract_fen("no fen\nhere\nsorry")
